
Olen luomassa konseptia jossa asiakkaan Rovo AI agentilla luotu feature muunnetaan ensin BMAD yhteensopivaksi.

Sitten se bmad skills käyttäen tuotetaan prd,,epics, stories,sprint ja aina lopulta implementaatio.

Hyödynkö mitään agent:ien käytöstä

Kyllä — mutta käyttäisin agenteja roolien ja vaiheiden eristämiseen, en jokaisen BMAD-stepin muuttamiseen omaksi agentiksi.

Konseptissasi erottaisin kaksi asiaa:

AGENT = kuka tekee / missä kontekstissa / millä oikeuksilla
SKILL = miten tietty työ tehdään

Sinulla BMAD sopii mielestäni ennen kaikkea skills-kerrokseksi. Agentit toisivat sen päälle kontrolloidun orchestration-kerroksen.

Esimerkiksi:

Rovo AI
  │
  │ feature / business requirement
  ▼
┌───────────────────────────────┐
│ BMAD Orchestrator Agent       │
└──────────────┬────────────────┘
               │
       normalize-to-bmad skill
               │
               ▼
        BMAD Feature Spec
               │
      ┌────────┴─────────┐
      ▼                  ▼
 Product Agent      Architecture Agent
      │                  │
 PRD skills         architecture skills
      │                  │
      └────────┬─────────┘
               ▼
        Planning Agent
               │
        epic/story skills
               │
               ▼
        Implementation Agent
               │
        coding skills
               │
               ▼
          Review Agent
               │
               ▼
              PR
Missä agentit toisivat sinulle oikeasti hyötyä?

1. Context isolation. Tämä olisi ehkä suurin hyöty. PRD:n tuottamiseen tarvitaan asiakkaan feature, business context ja BMAD-metodiikka. Implementointiin taas tarvitaan story + repo + arkkitehtuuri + coding rules. Implementointiagentin ei tarvitse kantaa mukanaan kaikkea PRD:n tuottamisen reasoning-historiaa.

Sen sijaan se saa artifactit:

PRD
 ↓
Epic
 ↓
Story
 ↓
Implementation

Tämä tekee prosessista huomattavasti deterministisemmän kuin yksi pitkä agenttikeskustelu.

2. Eri agenteille eri oikeudet. Tämä on enterprise-käytössä erittäin hyödyllinen ominaisuus.

Esimerkiksi:

Product Agent
  read repo
  read Rovo/Jira
  write BMAD artifacts
  ✗ cannot modify source

Planning Agent
  read PRD
  read architecture
  write stories
  ✗ cannot modify source

Developer Agent
  read story
  modify source
  terminal/tests
  ✗ cannot modify PRD

Reviewer Agent
  read everything
  run tests
  review diff
  ✗ cannot modify source

Silloin esimerkiksi PRD-agentti ei vahingossa ala "olla avulias" ja implementoida featurea.

3. Agent-to-agent handoff. Tästä voisi tulla konseptisi ehkä kiinnostavin osa.

Sen sijaan että workflow olisi pelkkä:

skill
 → skill
 → skill
 → skill

se olisi:

Agent A
  ↓
validated artifact
  ↓
Agent B
  ↓
validated artifact
  ↓
Agent C

Artifactista tulee agenttien välinen contract.

Esimerkiksi Developer Agent ei saa aloittaa ennen kuin sillä on:

story:
  id: PAY-123
  status: ready-for-development

acceptance_criteria:
  - ...
  - ...

architecture:
  references:
    - ADR-017

dependencies:
  - PAY-119

Tämä sopii mielestäni erittäin hyvin BMAD-ajatteluun.

Mutta en tekisi tästä 10 agentin järjestelmää

Jos nykyinen workflow on:

feature
→ convert-to-bmad
→ create-prd
→ create-epics
→ create-stories
→ create-sprint
→ implement
→ test
→ review

en tekisi:

FeatureAgent
PRDAgent
EpicAgent
StoryAgent
SprintAgent
CodingAgent
TestAgent
ReviewAgent
...

Siitä tulee helposti agent theateria: samat LLM:t vain siirtelevät tekstiä toisilleen, kontekstia katoaa ja järjestelmästä tulee vaikeampi debugata.

Tekisin ehkä vain 3–4 agenttia:

               Rovo
                 │
                 ▼
       ┌───────────────────┐
       │ 1. Product Agent  │
       │                   │
       │ BMAD normalization│
       │ PRD               │
       │ Epics             │
       │ Stories           │
       │ Sprint planning   │
       └─────────┬─────────┘
                 │
            artifacts
                 │
                 ▼
       ┌───────────────────┐
       │ 2. Dev Agent      │
       │                   │
       │ Story → code      │
       │ Tests             │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │ 3. Review Agent   │
       │                   │
       │ AC validation     │
       │ architecture      │
       │ code review       │
       │ tests             │
       └─────────┬─────────┘
                 │
                 ▼
                 PR

Ja BMAD olisi pääosin skills-kirjasto näiden agenttien sisällä.

Yksi agentti voisi olla erityisen arvokas

Tekisin lisäksi mahdollisesti Orchestrator Agentin, joka ei itse kirjoita tuotantokoodia.

Sen tehtävä olisi:

Rovo feature
     ↓
validate input
     ↓
delegate Product Agent
     ↓
validate BMAD artifacts
     ↓
delegate Dev Agent
     ↓
validate implementation
     ↓
delegate Review Agent
     ↓
PR ready

Silloin saat hyvin selkeän separation of concernsin:

Orchestrator = process

Agents = roles

Skills = methods

Artifacts = contracts

Tools/MCP = capabilities

AGENTS.md = repository rules

Minusta tämä on paljon vahvempi konsepti kuin "Rovo feature → kasa BMAD-prompteja → koodi". Siitä tulee oikeastaan agentic software-delivery pipeline, jossa BMAD määrittelee delivery-prosessin ja artifactit.

Ja siinä olisi vielä yksi todella kiinnostava ominaisuus: human gates. Esimerkiksi PRD:n tai storyjen jälkeen orchestrator pysähtyy asiakkaan hyväksyntään ennen kuin koodiin kosketaan:

Rovo Feature
     ↓
Product Agent + BMAD skills
     ↓
PRD / Epics / Stories
     ↓
  HUMAN APPROVAL
     ↓
Dev Agent
     ↓
Review Agent
     ↓
  HUMAN APPROVAL
     ↓
PR

Jos tämä on asiakaskonsepti, pitäisin juuri agents + skills + artifact contracts + human gates -rakennetta sen teknisen arkkitehtuurin ytimenä.

Kyllä — asiakasympäristöön tarkoitetussa konseptissasi tekisin lähtökohtaisesti human gaten jokaisen sellaisen agenttivaiheen jälkeen, joka muuttaa seuraavan vaiheen lähtötietoa merkittävästi.

Eli en niinkään "gate jokaisen agenttikutsun jälkeen", vaan gate jokaisen merkittävän artifactin jälkeen.

Rovo Feature
     │
     ▼
┌──────────────────┐
│ Product Agent    │
│ Normalize + PRD  │
└────────┬─────────┘
         ▼
    PRD ARTIFACT
         │
    👤 HUMAN GATE 1
         │ approve
         ▼
┌──────────────────┐
│ Architect Agent  │
│ Solution Design  │
└────────┬─────────┘
         ▼
 ARCHITECTURE ARTIFACT
         │
    👤 HUMAN GATE 2
         │ approve
         ▼
┌──────────────────┐
│ Product Agent    │
│ Epics + Stories  │
│ Sprint           │
└────────┬─────────┘
         ▼
 PLANNING ARTIFACTS
         │
    👤 HUMAN GATE 3
         │ approve
         ▼
┌──────────────────┐
│ Dev Agent        │
│ Code + Tests     │
└────────┬─────────┘
         ▼
 IMPLEMENTATION
         │
    👤 HUMAN GATE 4
         │ approve
         ▼
┌──────────────────┐
│ Review Agent     │
│ Independent      │
│ validation       │
└────────┬─────────┘
         ▼
 REVIEW RESULT
         │
    👤 HUMAN GATE 5
         │ approve
         ▼
        PR

Tässä on yksi erittäin tärkeä ominaisuus: seuraava agentti saa vain hyväksytyn upstream-artifactin lähtökohdakseen.

Esimerkiksi Architect Agent ei saa suunnitella ratkaisua draft-PRD:n pohjalta:

PRD
status: DRAFT
      ↓
   STOP ⛔

Human approval
      ↓

PRD
status: APPROVED
      ↓
Architect Agent ✓

Sama jatkuu koko ketjun läpi.

Mutta tekisin gateista eritasoisia

Kaikkea ei kannata pakottaa samanlaiseksi manuaaliseksi hyväksynnäksi. Konseptiin sopisi esimerkiksi kolme gate-tyyppiä:

Approval gate — ihminen hyväksyy varsinaisen päätöksen. PRD, architecture ja esimerkiksi epic/story scope.

Review gate — agentti saa jatkaa, ellei ihminen löydä ongelmaa. Soveltuu pienempiin muutoksiin.

Automated quality gate — testit, lint, security scan, schema validation jne. Ei tarvitse ihmistä, jos kyseessä ei ole päätös.

Silloin prosessi voisi olla:

Rovo
 ↓
Product Agent
 ↓
PRD
 ↓
👤 Product Owner approval
 ↓
Architect Agent
 ↓
Solution Design
 ↓
👤 Architect approval
 ↓
Product Agent
 ↓
Epics + Stories
 ↓
👤 PO / Tech Lead approval
 ↓
Dev Agent
 ↓
Implementation
 ↓
⚙ tests / lint / security
 ↓
👤 Developer review
 ↓
Review Agent
 ↓
Review findings
 ↓
👤 PR approval
 ↓
Merge

Tämä on minusta paljon vahvempi asiakaskonsepti kuin täysin autonominen Rovo → code -putki.

Ja tästä syntyy hyvä orchestration-malli

Orchestrator ei siis vain kutsu agentteja järjestyksessä. Se ylläpitää state machinea:

FEATURE_RECEIVED
      ↓
PRD_DRAFT
      ↓
AWAITING_PRD_APPROVAL
      ↓
PRD_APPROVED
      ↓
ARCHITECTURE_DRAFT
      ↓
AWAITING_ARCH_APPROVAL
      ↓
ARCHITECTURE_APPROVED
      ↓
PLANNING_DRAFT
      ↓
AWAITING_PLANNING_APPROVAL
      ↓
READY_FOR_DEVELOPMENT
      ↓
IMPLEMENTATION_COMPLETE
      ↓
AWAITING_REVIEW
      ↓
READY_FOR_PR

Ja tämä sopii erityisen hyvin siihen, että Rovo/Jira voisi olla control plane. Gate ei välttämättä tarkoita VS Codessa kysymystä "Continue? Y/N". Agentti voi esimerkiksi tuottaa artifactin → Jira-status muuttuu Architecture Review → oikea henkilö hyväksyy → workflow jatkuu.

Silloin kokonaisuuden arkkitehtuuri alkaa mielestäni olla:

Rovo/Jira = intent + workflow + human governance
Agents = päätöksenteko/orkestrointi omassa roolissaan
BMAD Skills = standardoitu tapa tehdä työ
Artifacts = agenttien väliset sopimukset
Human Gates = päätöksenteko ja accountability
Automated Gates = tekninen laadunvarmistus

Tämä olisi myös hyvä kohta erottaa konseptissa "AI autonomous execution" ja "human-controlled progression": agentti voi tehdä oman vaiheensa hyvinkin autonomisesti, mutta se ei itse päätä, että sen tuotoksen perusteella saa siirtyä seuraavaan merkittävään SDLC-vaiheeseen.

Saturday 11:13 PM
Kuinka nuo gatet kuitataan?

Jos rakennat tämän aluksi VS Code + custom agents + BMAD skills -konseptina, gate ei ole mikään automaattisesti olemassa oleva erityinen "Human Gate" -objekti. Sinun pitää määritellä, mikä toimii hyväksynnän source of truthina.

Yksinkertaisimmassa PoC:ssa tekisin gaten artifactin tilaksi.

Esimerkiksi Product Agent tuottaa PRD:n:

---
artifact: prd
feature: ROVO-142
status: pending-approval
---

Agentti pysähtyy:

Product Agent
    │
    ├─ PRD generated
    ├─ validation passed
    │
    ▼
⏸ PENDING_APPROVAL

Ihminen tarkastaa PRD:n ja kuittaa esimerkiksi VS Code Agent Windowissa:

Approve PRD for ROVO-142

Orchestrator/Product Agent käsittelee tämän approval-toimintona ja muuttaa:

status: approved
approved_by: ...
approved_at: ...

Sen jälkeen seuraava vaihe saa jatkaa.

Mutta oikeassa asiakasratkaisussa en käyttäisi chattia approval-tietokantana

Koska sinulla on jo Rovo/Jira lähtöpisteenä, Jira olisi minusta luonteva source of truth.

Esimerkiksi:

Product Agent
     │
     ▼
PRD generated
     │
     ▼
Jira:
Status = PRD Review
     │
     ▼
👤 Product Owner
   [Approve]
     │
     ▼
Jira:
PRD Approval = Approved
     │
     ▼
Orchestrator
     │
     ▼
Architect Agent

Samoin architecture:

Architect Agent
      ↓
Solution Design
      ↓
Jira → Architecture Review
      ↓
👤 Architect / Tech Lead
      ↓
Approve
      ↓
Architecture Approved
      ↓
Product Agent → Epics/Stories

Tällöin saat samalla audit trailin: kuka hyväksyi, mitä versiota, milloin ja mahdollisesti millä kommentilla.

GitHub PR voi toimia myöhemmissä vaiheissa gatena

Kaikkia hyväksyntöjä ei tarvitse viedä Jiraan.

Esimerkiksi:

Requirement / planning
────────────────────────
PRD             → Jira approval
Architecture    → Jira approval
Stories         → Jira approval

Implementation
────────────────────────
Code            → automated CI gates
Review Agent    → review result
PR              → GitHub required reviewer
Merge           → branch protection

Tämä olisi mielestäni luonnollinen jako.

Vielä parempi: hyväksy artifactin versio, älä pelkkää vaihetta

Tämä on tärkeä yksityiskohta.

Älä tallenna vain:

prd: approved

vaan jotakin tämän tapaista:

artifact:
  type: prd
  feature: ROVO-142
  version: 3
  hash: 8d73...

approval:
  status: approved
  approved_by: seppo
  approved_at: 2026-09-26T20:10:00Z

Jos agentti muuttaa PRD:tä hyväksynnän jälkeen:

PRD v3
  ↓
APPROVED ✓
  ↓
agent modifies PRD
  ↓
PRD v4
  ↓
approval invalidated
  ↓
PENDING APPROVAL

Muuten syntyy vaarallinen tilanne, jossa ihminen hyväksyi yhden asian mutta downstream-agentti käyttää myöhemmin muutettua artifactia.

Orchestratorin logiikka pysyy silloin hyvin yksinkertaisena
Product Agent
     ↓
PRD v3
     ↓
WAITING_FOR_APPROVAL
     ↓
        👤
     approve
     ↓
PRD v3 APPROVED
     ↓
Architect Agent
     ↓
Architecture v1
     ↓
WAITING_FOR_APPROVAL
     ↓
        👤
     approve
     ↓
Architecture v1 APPROVED
     ↓
Planning Agent

Ja agenttien ohjeisiin laitetaan guardrail, esimerkiksi:

Before starting architecture design:

- Verify that the PRD exists.
- Verify that the exact PRD version is approved.
- Never proceed from a draft or superseded PRD.
- If approval is missing, stop and report
  WAITING_FOR_PRD_APPROVAL.

Näin gate ei perustu siihen, että LLM "muistaa kysyä ihmiseltä", vaan seuraavan vaiheen preconditioniin.

PoC:ssa aloittaisin hyvin yksinkertaisesti: Git-versionoidut BMAD-artifactit + niiden metadataan draft/pending-approval/approved + agentit eivät saa ylittää gatea ilman approved-tilaa. Kun konsepti toimii, approval state voidaan siirtää Jira/Rovoon ja käyttää MCP:tä/API:a sen lukemiseen ja päivittämiseen.

Se tekee myös hyvän demon: Rovo → PRD → STOP → ihminen hyväksyy → Architecture → STOP → ihminen hyväksyy → Stories → STOP → Dev. Siinä human-in-the-loop näkyy asiakkaalle erittäin konkreettisesti.

En käyttäisi jiraa vaan esim yaml. Muutoshistoria pitää muös tallentaa

Kyllä. Tekisin tästä mieluummin repoon tallennetun workflow-state-mallin, jossa YAML on koneellisesti luettava source of truth ja Git antaa jo yhden audit trailin. Sen lisäksi tallentaisin eksplisiittisen event-historian, jotta agentin ei tarvitse rekonstruoida tilaa Git-historiasta.

Esimerkiksi featurelle:

.bmad/
└── features/
    └── ROVO-142/
        ├── workflow.yaml
        ├── history.yaml
        ├── prd.md
        ├── architecture.md
        ├── epics.md
        └── stories/
            ├── story-001.md
            └── story-002.md

workflow.yaml olisi nykyinen tila:

feature: ROVO-142
workflow_version: 1

current_stage: architecture
state: waiting_for_approval

artifacts:
  prd:
    path: prd.md
    version: 3
    hash: "sha256:8d73..."
    status: approved
    approved_version: 3

  architecture:
    path: architecture.md
    version: 2
    hash: "sha256:921a..."
    status: pending_approval

  epics:
    status: not_started

  stories:
    status: not_started

gates:
  prd:
    status: approved
    artifact_version: 3
    approved_by: "user@example"
    approved_at: "2026-09-26T20:10:00Z"

  architecture:
    status: pending

Ja erillinen append-only history.yaml:

events:

  - id: evt-001
    timestamp: "2026-09-26T19:30:00Z"
    actor:
      type: agent
      name: product-agent
    action: artifact_created
    artifact: prd
    version: 1

  - id: evt-002
    timestamp: "2026-09-26T19:42:00Z"
    actor:
      type: human
      id: seppo
    action: changes_requested
    artifact: prd
    version: 1
    comment: >
      Clarify authentication requirements.

  - id: evt-003
    timestamp: "2026-09-26T19:55:00Z"
    actor:
      type: agent
      name: product-agent
    action: artifact_updated
    artifact: prd
    from_version: 1
    to_version: 2

  - id: evt-004
    timestamp: "2026-09-26T20:10:00Z"
    actor:
      type: human
      id: seppo
    action: approved
    artifact: prd
    version: 3
    hash: "sha256:8d73..."

Tässä on tärkeä ero:

workflow.yaml = missä olemme nyt

history.yaml = miten tähän päädyttiin

Git = mitä tiedostoissa konkreettisesti muuttui

Nämä täydentävät toisiaan erittäin hyvin.

Approval kannattaa sitoa sisältöön

Tekisin gaten nimenomaan:

artifact + version + hash

ei vain:

architecture: approved

Esimerkiksi:

approval:
  artifact: architecture
  version: 2
  hash: "sha256:921a..."
  approved_by: seppo
  approved_at: ...

Jos Architecture Agent tämän jälkeen muuttaa architecture.md:tä:

architecture v2
hash ABC
     │
     └── APPROVED ✓

agent modifies file

architecture v3
hash XYZ
     │
     └── NOT APPROVED

Workflow-engine/skill tekee automaattisesti:

architecture:
  version: 3
  status: pending_approval

ja historiaan:

- action: approval_invalidated
  artifact: architecture
  previous_version: 2
  reason: artifact_modified

Tämä on jo aika vahva governance-mekanismi.

Tekisin myös approvalista komennon/skillin

Sen sijaan että ihminen itse editoi YAMLia:

/approve architecture

tai:

Approve architecture

Agentti/skill:

laskee nykyisen artifactin hashin
tarkistaa version
lisää approvalin
lisää history-eventin
päivittää workflow-staten
commit voidaan haluttaessa tehdä samalla.

Samoin:

Request changes to architecture: API must use existing customer identity service.

tuottaa eventin:

action: changes_requested
artifact: architecture
version: 2
comment: "API must use existing customer identity service."

ja palauttaa Architect Agentille työn.

Vielä yksi muutos: historia kannattaa ehkä tehdä event-per-file

Yksi history.yaml toimii PoC:ssa, mutta rinnakkaiset agentit alkavat helposti aiheuttaa Git merge conflicteja, koska kaikki kirjoittavat saman tiedoston loppuun.

Tekisin siksi tuotantomaisemmassa versiossa:

.bmad/features/ROVO-142/

├── workflow.yaml
├── events/
│   ├── 20260926T193000Z-001.yaml
│   ├── 20260926T194200Z-002.yaml
│   ├── 20260926T195500Z-003.yaml
│   └── 20260926T201000Z-004.yaml
│
├── prd.md
├── architecture.md
└── stories/

Jokainen tapahtuma on immutable event.

Tästä syntyy käytännössä kevyt event-sourced agent workflow:

                    events/*
                       │
                       ▼
                  workflow.yaml
                 CURRENT STATE
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Product      Architect      Dev
        Agent         Agent        Agent
          │            │            │
          └──────► new events ◄─────┘
                       │
                       ▼
                      Git
                  AUDIT HISTORY

Minusta tämä sopii sinun konseptiisi paremmin kuin Jira-pohjainen state machine. Koko feature delivery -tila kulkee repossa koodin ja BMAD-artifactien mukana, on branchattavissa, diffattavissa, auditoitavissa ja agenttien luettavissa ilman ulkoista workflow-järjestelmää.

Ja tässä vaiheessa tekisin itse asiassa workflow-state/approvalista oman skillin, jota kaikki Product-, Architecture-, Dev- ja Review-agentit käyttävät. Näin jokainen agentti ei implementoi YAML-state machinea omalla tavallaan.

Usage limit reached
You can keep using basic ChatGPT features or request a limit increase from your workspace admin to use more advanced features.
Request Increase