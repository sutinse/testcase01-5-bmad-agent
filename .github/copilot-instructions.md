# Copilot instructions — testcase01 (Refund Approval Check service)

**Local MVP (approved architecture, ADR-0014/0016/0020):** Three separate
requests are required: processor submission (persist `PENDING` above the
threshold), later decision by a distinct simulated test identity, and status
query by any authorized `refund-system` processor. `PENDING` is a valid 200 OK
business state; there is no approver on submission. Decisions require the
`refund-approver` role; submission and status require `refund-system`.
Submission must match `processorId` to the validated JWT `sub`; status does
not require the original processor's subject. The decision route works only
in the explicit `local-mvp` profile, never as a production approval.

This repo implements a Quarkus REST API that enforces segregation-of-duties on
insurance premium refund approvals (approver must differ from processor for
the refund that pushes a customer's rolling 365-day cumulative refund total
over €10,000). For the local MVP, the approved PRD and architecture under
`bmad-output/testcase01/` and the project context there are the reviewable
planning sources. The older `CONTEXT.md`, `docs/adr/` and
`.scratch/refund-approval-check/spec.md` are unavailable; do not reconstruct
or cite their contents. This file remains the quick locked-decision reference
for generating code; **when in doubt, prefer these locked decisions over a
more "idiomatic" default.**

Planning sources (read for depth, don't restate them here):
- `bmad-output/testcase01/prd.md` — approved local MVP requirements
- `bmad-output/testcase01/architecture.md` — approved architecture and
  ADR-0014 through ADR-0020, including local-only identity and status rules
- `bmad-output/testcase01/project-context.md` — project boundaries; reconcile
  any later local clarification through the review and approval gates

## Locked technical decisions (do not deviate without an approved decision)

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
- **AuthN/AuthZ:** JWT bearer via `quarkus-smallrye-jwt`. The local MVP
  validates the test JWT signature, configured local issuer and audience, and
  required expiration; missing or invalid claims are rejected. No real Entra
  issuer/JWKS/tenant integration is provided. The private test signing key
  stays outside the application and repository. Role checks use `@RolesAllowed`:
  `refund-system` submits and reads status, `refund-approver` decides.
  Submission requires `processorId == sub`; the decision actor comes from the
  validated `sub` and must differ from that refund's processor. Status requires
  a validated `sub` but does not compare it with the original processor.
  The decision route is disabled outside `local-mvp`, and test keys are not
  configured there (fail closed). The test identity is not proof of a natural
  person; no production approval or history endpoint is in this MVP. Do not
  hand-roll JWT verification or add unsupported claim checks.
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
