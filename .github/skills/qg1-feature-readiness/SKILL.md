---
name: qg1-feature-readiness
description: Run a Quality-Gate-1 (QG1) feature-readiness review — map a raw feature/business
  description to artifacts, score readiness against the document's own rubric, list risks,
  and resolve every open question before the feature goes to a BA/PRD-writing step. Use when
  the user says "run QG1", "quality gate 1", "feature readiness review", "QG1-ajo", "is this
  feature ready for refinement", or asks to validate a raw business/feature description before
  writing a PRD, tech-spec, or user stories.
---

# QG1 feature readiness review

QG1 is not this skill's content — it is a persona/rubric document that already exists
somewhere in the target workspace (or is pasted directly by the user). This skill's job is to
find that document and the raw input it should review, then execute the document's own
Execution Order literally, using `vscode_askQuestions` at every point a human decision is
needed.

## 1. Locate the QG1 document and the input

Search the workspace for a quality-gate / feature-readiness persona file (common names:
`feature-qualitygate-one.md`, `quality-gate-1.md`, `qg1.md`) and for the raw feature/business
description it should review (e.g. `testcase01-kuvaus.md`, a Jira export, meeting notes).

Ask via `vscode_askQuestions`:
- Which file is the QG1 persona/rubric? Offer any single unambiguous match found in the
  workspace as the **recommended** option; allow freeform path or "paste the rubric directly"
  as fallback.
- Which file or pasted text is the input to review? Same pattern: recommend an unambiguous
  match, allow freeform/paste.

Read the QG1 document in full — its Execution Order, Output Limits, and rubric/reference
sections — before starting. Do not work from a summary or from memory of a similar document.

## 2. Execute the QG1 document's Execution Order literally

Follow the steps exactly as the QG1 document defines them, in order, including whatever
domain adaptation, extraction, and mapping steps it specifies. Do not skip, reorder, or
paraphrase its rubric.

At every point the QG1 document says to pause for user confirmation (mapping confirmed,
verdict confirmed, etc.), use `vscode_askQuestions` rather than a plain chat question — offer
the confirmation as a yes/proceed vs. revise choice so the answer is unambiguous.

When the QG1 document reaches its clarifying-questions step, run it as **rounds**, one round
per `vscode_askQuestions` call: number each question, give a recommended answer as the
recommended option, and only ask the next round once the current one is answered — a
question whose answer depends on one still open belongs to a later round. This is the
`grilling` skill's frontier mechanic (`<USERPROFILE>/.agents/skills/grilling/SKILL.md`); reuse
its round discipline here without adopting any of its own content. The round must close every
gap the input text itself raises — explicit open questions, hedges ("probably", "should
consider"), and unresolved options — plus every Unknown/Partial item the rubric step flagged.

## 3. Save the result

The QG1 document's own "Output Limits" (or equivalent) section defines the required shape of
the final artifact — treat it as authoritative, not a plain question-and-answer transcript.

Ask via `vscode_askQuestions` where to save the result (recommend `clarified-feature-notes.md`
at the workspace root as the default), then write the full result there in the shape the QG1
document specifies — mapping, rubric, risks, resolved clarifying questions, verdict, and
next actions, each in the format that document's Output Limits section requires.
