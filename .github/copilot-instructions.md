# Copilot instructions — testcase01 (Refund Approval Check service)

**2026-09-25 correction:** ADR-0013 supersedes the immediate approval flow below.
Three separate requests are required: processor submission (persist `PENDING`
above the threshold), approval by another natural person, and the original
processor's status query. `PENDING` is a valid 200 OK business state; there is
no approver on submission. Approval requires the `refund-approver` role;
submission/status require `refund-system` and a matching JWT subject. See
`docs/adr/0013-three-request-approval-workflow.md` for the full contract.

This repo implements a Quarkus REST API that enforces segregation-of-duties on
insurance premium refund approvals (approver must differ from processor for
the refund that pushes a customer's rolling 365-day cumulative refund total
over €10,000). Full requirements/design live in `CONTEXT.md`, `docs/adr/`, and
`.scratch/refund-approval-check/spec.md` — this file is the quick,
locked-decision reference for generating code; **when in doubt, prefer these
locked decisions over a more "idiomatic" default.**

Planning sources (read for depth, don't restate them here):
- `CONTEXT.md` — domain glossary (Refund, Processor, Approver, Cumulative
  Refund Total, Partial Refund, Refund Currency)
- `docs/adr/` — architectural decision records
- `.scratch/refund-approval-check/spec.md` — problem statement, user stories,
  implementation/testing decisions (LOCKED planning artifact — see
  `docs/agents/issue-tracker.md`)

## Locked technical decisions (ADRs — do not deviate without a new ADR)

- **Persistence: plain JDBC only. NO JPA, NO Hibernate ORM, NO Panache.**
  Use `quarkus-agroal` + `org.xerial:sqlite-jdbc`. Data rows are plain Java
  `record`s, never `@Entity` classes. All SQL is hand-written
  `PreparedStatement`/`ResultSet` in one `RefundApprovalCheckRepository` class
  per table; always use try-with-resources for `Connection`/`Statement`/`ResultSet`.
- **Schema:** Flyway migrations only (`quarkus-flyway`). Never hand-write DDL
  outside a versioned migration.
- **Store:** SQLite file, single Quarkus instance — **SQLite only for MVP**, not
  a long-term choice. Do not scale to multiple instances without first moving
  off SQLite — it has no built-in HA.
- **AuthN/AuthZ:** JWT bearer via `quarkus-smallrye-jwt`. **MVP does not stand up
  real Entra ID issuer/JWKS/tenant integration** — assume a valid JWT is
  already present on every request. Role checks via `@RolesAllowed` only.
  Roles: `refund-system` (submits and polls), `refund-approver` (approves),
  `compliance-auditor` (calls the history endpoint). One narrow, explicitly-justified exception to
  "never hand-rolled claim inspection": verifying the approver is a natural
  person (not a bot/service principal/group) requires inspecting the token's
  claims directly, per `docs/adr/0001-explicit-human-approver-claim-check.md`
  — processor-subject matching for submission/status is separately authorized
  by ADR-0013; don't add other claim inspection.
- **API style:** REST + JSON (`quarkus-rest`, `quarkus-rest-jackson`).
  **Business outcomes are always `200 OK`** with an `allowed: boolean` field and
  an `outcome` wire enum (`"PENDING" | "ALLOWED" | "BLOCKED"`) — a segregation-of-duties
  block or pending approval is a valid state, not an HTTP error. HTTP 4xx/5xx are reserved for
  malformed requests / auth failures / server faults, always
  `application/problem+json` (RFC 7807).
- **Enforcement:** `RefundProcessorService` alone owns the threshold and rolling
  365-day cumulative refund total per `customerId`; `RefundApprovalService`
  alone owns the processor≠approver decision for a pending refund. REST resources
  are thin adapters and never re-implement these rules. Only the refund that
  pushes the rolling total over the threshold requires approval; earlier
  compliant refunds are never
  retroactively re-evaluated, and the approver must differ only from that
  refund's own processor (not every processor in the window).
- **Threshold:** fixed constant, €10,000, defined once (`BigDecimal`, strictly
  "greater than"). Configurable threshold (FR-006) is deferred — don't build it
  speculatively. Applies uniformly to natural-person and corporate customers.
- **Currency:** EUR only. Reject non-EUR requests outright — no currency
  conversion is attempted or supported.
- **Partial refunds:** disallowed. Every refund request is one complete,
  indivisible amount — never a partial payout with the remainder allocated
  elsewhere.
- **Logging:** JSON-structured logging only (`quarkus-logging-json`) — never
  plain-text log lines. Log messages must be clear and meaningful on their own
  (state what happened and to which refund/customer, not generic phrases), and
  every log line for a request must carry a correlation identifier (e.g.
  `refundId`, trace/span id) as a structured field so entries can be tied back
  to the request in application monitoring/APM, not just grepped from text.

## Naming conventions

- REST paths: plural, kebab-case, versioned — `/api/v1/refund-approval-checks`.
- JSON fields: camelCase (`refundId`, `customerId`, `processorId`, `approverId`,
  `amount`, `currency`, `outcome`, `checkedAt`).
- DB tables/columns: snake_case (`refund_approval_check`, `customer_id`,
  `processor_id`, `approver_id`, `checked_at`).
- Java packages: `com.example.refundapproval.<layer>` (`resource`, `service`,
  `persistence`, `exception`) — replace `com.example` with the real group ID.
- Wire enums: upper-snake strings (`"outcome": "BLOCKED"`), never ordinals.

## Stack

Java 25, Quarkus (pin the exact latest stable version in `pom.xml` at
implementation time — verify Java 25 support first), Maven. Application code
lives under `/app` once scaffolded.
