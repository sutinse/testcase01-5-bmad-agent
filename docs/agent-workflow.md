# Agenttien käyttö ja ihmisportit

Tämä ohje koskee yhtä featurea kerrallaan. Agentit ovat VS Coden `.github/agents/`-rooleja; suunnitteluun käytetään `.github/skills/`-BMAD-skillejä. Gate-komennot ajetaan repojuuresta. `<id>` on featuren tunnus (kirjaimet, numerot, `_` ja `-`); korvaa kulmasulkeiset arvot omilla arvoilla ennen komentojen ajoa.

## Ennen aloitusta

1. Tallenna aito Rovo-feature tiedostoon `bmad-output/<id>/input/rovo-feature.md`, sisältäen lähde-URL:n ja poiminta-ajan. Tuo aito QG1-rubriikki tiedostoon `docs/qg1/feature-readiness.md`. QG1-skill ei sisällä rubriikkia. Jos lähteet puuttuvat, PRD-vaihe pysähtyy.
2. Käytä GitHubiin liitettyä Git-checkoutia; asenna `python -m pip install -r requirements-gate.txt` ja kirjaudu `gh auth login`. Tarkista `gh repo view`. Tässä paikallisessa checkoutissa ei vielä ole `.git`-metadataa, joten tässä kuvattuja GitHub-portteja ei voi harjoitella loppuun täällä.
3. Pyydä repo-ylläpitäjää korvaamaan [CODEOWNERS](../.github/CODEOWNERS)-tiedoston `@REPLACE_WITH_HUMAN_OWNER` oikealla GitHub-käyttäjällä tai tiimillä. Suojaa `main`: vain PR-merge, vähintään yksi muu ihminen hyväksyjänä, vanhojen review-hyväksyntöjen mitätöinti uusilla commiteilla, vaaditut `workflow-gate`- ja test-checkit sekä rajatut bypass-/admin-oikeudet. Varmista, että CLI ja CI voivat lukea branch protection -asetukset. Älä pidä pelkkää CODEOWNERS-tiedostoa riittävänä ilman GitHubin asetuksia.

## Järjestys ja ihmisen review

| Vaihe | Käynnistä VS Codessa | Ihminen tarkistaa ennen PR:n hyväksyntää |
| --- | --- | --- |
| PRD | **Feature Product**, ensin `check <id> prd`; QG1, spec ja PRD | Rovo-lähteen oikeellisuus, QG1:n päätökset ja avoimet kysymykset, PRD:n rajaus, FR/NFR:t ja hyväksymiskriteerit. Hyväksy **PRD-PR** toisena luonnollisena henkilönä. |
| Arkkitehtuuri | **Feature Architect**, `check <id> architecture` | Kattavatko ratkaisu ja ADR:t hyväksytyn PRD:n FR/NFR:t, turvallisuus, data ja rajapinnat. Hyväksy **arkkitehtuuri-PR**. |
| Suunnittelupaketti | **Feature Product**, `check <id> planning`; epics, storyt, sprint, readiness ja handoff | Vastaavatko storyt ja AC:t PRD:tä/arkkitehtuuria, ovatko riippuvuudet, `ownedScope` ja `ready-for-dev`-handoff järkeviä; readiness-verdict on PASS. Hyväksy **suunnittelupaketin PR**. |
| Toteutus | **Feature Java Developer**, `check <id> development`; yksi valmis story kerrallaan | Java-kehittäjä ei muuta hyväksyttyjä storyja tai handoffia. Refund-työ odottaa viitattuja `CONTEXT.md`-, ADR- ja spec-lähteitä. |
| Riippumaton review | **Feature Independent Reviewer**, `check <id> review` | Reviewer vertaa koodidiffiä storyn AC:ihin, ADR:iin, turvallisuusvaatimuksiin ja testituloksiin, kirjaa löydökset ja pyytää korjaukset. **Toteutus-PR:n** hyväksyy lopuksi toinen ihminen GitHubissa vasta vaadittujen checkien jälkeen; CLI ei hyväksy tätä viimeistä PR:ää. |

**Feature Orchestrator** kertoo seuraavan omistajan ja estävän portin; se ei korvaa vaiheagentteja eikä ihmisen review'ta. QG1:n keskustelussa annetut vastaukset ja BMAD-readiness PASS ovat suunnittelun syötteitä, eivät GitHub-PR:n hyväksyntöjä. Jokainen kolmesta suunnitteluvaiheesta vaatii oman hyväksytyn ja mergetyn PR:n. PR:n tekijä ei voi olla sen gate-hyväksyjä.

## Portin komennot

Jokainen vaiheagentti ajaa ennen työn aloitusta saman esivalidoinnin (esimerkki):

```powershell
python scripts/workflow_gate.py check <id> architecture
```

`STOP` ja ei-nolla-paluukoodi tarkoittavat, ettei vaihetta saa aloittaa. PRD-vaihe vaatii Rovo-snapshotin ja QG1-rubriikin; arkkitehtuuri vaatii PRD:n hyväksynnän; suunnittelu molemmat; development ja review kaikki kolme. Tarkastele tilaa komennolla `python scripts/workflow_gate.py status <id>` ja tarkista kirjattu historia komennolla `python scripts/workflow_gate.py validate-history <id>`.

**Hyväksyminen tehdään kahdessa eri järjestelmässä:** toinen ihminen tarkistaa ja hyväksyy stage-PR:n GitHubissa, vaaditut checkit läpäisevät, PR mergetään suojattuun haaraan; vasta tämän jälkeen kirjataan gate-tapahtuma `record-approved`-komennolla samassa repossa, jossa ovat mergetyt, muuttumattomat artefaktit. Pelkkä chat-viesti, paikallinen YAML-muutos tai hyväksymätön PR ei riitä.

```powershell
python scripts/workflow_gate.py record-approved <id> prd --pr <prd-pr-numero> --artifacts bmad-output/<id>/input/rovo-feature.md bmad-output/<id>/prd.md
python scripts/workflow_gate.py record-approved <id> architecture --pr <arkkitehtuuri-pr-numero> --artifacts bmad-output/<id>/architecture.md
python scripts/workflow_gate.py record-approved <id> planning --pr <suunnittelu-pr-numero> --artifacts bmad-output/<id>/epics.md bmad-output/<id>/sprint-status.yaml bmad-output/<id>/handoff-manifest.json bmad-output/<id>/stories/1.1.example.story.md
```

Viimeisen komennon story-polku on vain esimerkki: luettele **kaikki** `bmad-output/<id>/`-hakemiston `*.story.md`-tiedostot, ei vain handoffiin valitut. Portti vaatii täsmällisen tiedostojoukon ja tarkistaa sisällön SHA-256-hashit, PR:n muuttuneet tiedostot, merge-commitin sisällön, suojatun haaran asetukset ja eri ihmisen nykyiseen PR-head-commitiin antaman hyväksynnän. Kirjauksen jälkeen vie uusi `.bmad/features/<id>/events/*.yaml` ja johdettu `workflow.yaml` suojatun haaran kautta GitHubiin. Älä muokkaa tai poista vanhoja eventtejä. Sama `record-approved` samalla PR-numerolla ei lisää duplikaattia.

Jos hyväksyttyyn vaiheeseen tarvitaan muutos, toinen ihminen antaa GitHubissa uuden PR:n nykyiselle head-commitille **Request changes** -review'n. Kirjaa mitätöinti `python scripts/workflow_gate.py request-changes <id> <vaihe> --pr <muutos-pr-numero>`, vie uusi event ja snapshot versionhallintaan ja pyydä korjatuille artefakteille uusi hyväksytty stage-PR. Vanha hyväksyntä jää auditoitavaan historiaan. Ylävaiheen muutos edellyttää myös alavaiheiden suunnitelmien uudelleenarviointia ennen työn jatkamista.

Paikallinen `workflow.yaml` on vain event-hashien tilannekuva. Luottamuksen juuri on suojattu GitHub-haara, ihmisreview ja vaadittu [CI-portti](../.github/workflows/workflow-gate.yml); ylläpitäjän bypass tai varastetut tunnukset eivät kuulu CLI:n suojaan. Tarkempi komentojen sopimus on [workflow-gate-skillissä](../.github/skills/workflow-gate/SKILL.md) ja refundin lukitut tekniset päätökset [projektiohjeessa](../.github/copilot-instructions.md).