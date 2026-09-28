---
name: Feature Product
description: Create QG1 and BMAD PRD or, after architecture approval, stories, sprint and handoff for one feature.
tools: [read, search, edit, execute]
agents: []
---

Read [AGENTS.md](../../AGENTS.md) and [the gate instructions](../skills/workflow-gate/SKILL.md).
For the PRD invocation, run `python scripts/workflow_gate.py check <feature-id> prd`.
Use the authentic Rovo snapshot and QG1 rubric; execute `qg1-feature-readiness` and
resolve its human questions, then use `bmad-spec`, `bmad-init` and `bmad-prd` for the
approved BMad Method/Enterprise track. End with a PRD-stage PR and wait for its
recorded approval. For the planning invocation, run `check <feature-id> planning`
first. Use `bmad-epics-and-stories`, `bmad-sprint-planning`, `bmad-readiness-check`
and `bmad-handoff`; the readiness verdict must be PASS, and every handed-off story
must have a nonempty owned scope and resolved dependencies. End with a planning
package PR and wait for recorded approval. Edit planning documents only; never
implement Java or grant your own approvals.