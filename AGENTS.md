# Feature delivery contract

This repository has a planning pipeline and no Java application yet. Keep each feature's
planning output under `bmad-output/<feature-id>/`. The input must be a saved Rovo
snapshot with source URL and retrieval time. QG1 requires the authentic external rubric;
`.github/skills/qg1-feature-readiness/SKILL.md` does not provide one. Pause when either
source is missing. Do not fabricate the refund `CONTEXT.md`, ADRs or spec. For the
testcase01 local MVP, those legacy files are unavailable: use its approved PRD,
`bmad-output/testcase01/project-context.md` and approved architecture as the
reviewable planning sources. Any later change to the source hierarchy requires a
protected PR and the affected stage approvals; this exception does not authorize
production refund approvals.

Use the BMAD skills in `.github/skills/` for planning only. Product owns QG1, PRD,
stories, sprint and handoff; Architect owns architecture and ADR decisions. Run
`bmad-readiness-check` before proposing the planning package. The final planning
artifact is `handoff-manifest.json`; Java development and review use separate agents.

Every agent runs `python scripts/workflow_gate.py check <feature-id> <stage>` with
`stage` equal to `prd`, `architecture`, `planning`, `development` or `review` before
starting its phase. The command must exit successfully. Stage PR approvals are recorded
with `record-approved` only after a protected, merged GitHub PR has a review from a
different human on its current head. An agent must stop at any `STOP` result. Human
approval in chat or a locally edited YAML file is not approval. See
`.github/skills/workflow-gate/SKILL.md` for the command contract and setup.

Approved story files and handoff manifests are immutable inputs to implementation.
Record story execution separately in `.bmad/features/<feature-id>/execution/`; a
requirement change requires a new planning package and another human approval.
Develop only files within a ready story's `ownedScope` under `app/` and verify its
dependencies. The reviewer reports findings independently and does not change
production code. The final code PR needs a human review and required CI before merge.

For refund implementation, `.github/copilot-instructions.md` remains the authoritative
locked technical decision reference. Read it before Java work. For the testcase01
local MVP, reconcile it with the approved PRD, architecture and stories; the absent
legacy `CONTEXT.md`, `docs/adr/` and spec are not implementation prerequisites or
sources to reconstruct. The approved architecture contains the three-request flow
and local-only ADR-0016/ADR-0020 exceptions; it does not approve production use.