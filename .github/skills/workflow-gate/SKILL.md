---
name: workflow-gate
description: Verify GitHub-backed human approval gates between PRD, architecture, planning handoff, development and independent review. Run when entering a feature stage, recording a merged stage PR, checking status or investigating stale approval.
---

# Feature approval gate

Install `requirements-gate.txt` and authenticate `gh` to the target GitHub repo.
All commands run from the repository checkout, using a feature id of letters,
digits, `_` or `-`. A `STOP` result and nonzero exit code mean the next phase
must not begin. No local YAML or chat response can grant approval.

1. Enter a stage with `python scripts/workflow_gate.py check <id> <stage>`, where
   stage is `prd`, `architecture`, `planning`, `development` or `review`.
   PRD starts without an upstream approval; architecture needs PRD; planning
   needs PRD and architecture; development and review need all three.
2. After a distinct human approves and merges a stage PR, run
   `python scripts/workflow_gate.py record-approved <id> <stage> --pr <number> --artifacts <paths...>`.
   For PRD supply both `bmad-output/<id>/prd.md` and
   `bmad-output/<id>/input/rovo-feature.md`; for architecture supply
   `bmad-output/<id>/architecture.md`; for planning supply `epics.md`,
   `sprint-status.yaml`, `handoff-manifest.json` and *all* `*.story.md` under
   `bmad-output/<id>/`. Supply slash-separated repository-relative paths.
   Commit the generated `.bmad/features/<id>/workflow.yaml` and new event
   through a protected PR. Repeating the same recorded approval is idempotent.
3. To invalidate a stage, request changes as a distinct human on a GitHub PR,
   then run `python scripts/workflow_gate.py request-changes <id> <stage> --pr <number>`.
   This appends a revocation event; a new approved PR is needed to reopen it.
4. Use `status <id>` to show active stages and `validate-history <id>` to verify
   all recorded evidence against GitHub. `check` validates the same history.

Before using this in production, an administrator must configure the default
branch to require PRs, at least one independent human review, dismissal of stale
reviews on new pushes, and required `workflow-gate`/test checks. Restrict bypass
and admin access, protect `.bmad/`, `scripts/`, `.github/` via CODEOWNERS, and
disallow direct pushes. Confirm branch-protection API is readable to the CLI/CI.
The CLI checks enabled review policy and required status checks, but cannot
enforce administrator behavior or prove that all required checks passed at merge;
GitHub branch protection must enforce both. This checkout has no `.git` metadata,
so the protected-branch integration must be exercised in a real test repository.

`workflow.yaml` is a derived local integrity check, not a trust anchor. The
PR-CI rejects edits/deletions of events already on the base branch. A local
attacker able to replace both the workflow snapshot and event history before
they are pushed can still erase uncommitted evidence. Protected GitHub history,
credentials and human review are the trust boundary. Stage dependencies changed
after approval require new stage PRs and approvals. The final code PR itself
requires GitHub human approval before merge; it is not approved by this CLI.