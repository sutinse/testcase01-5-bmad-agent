# Epics - testcase01 / Refund Approval Check

> BMad Method; paikallisen MVP:n suunnitteluluonnos. Tarinoita ei ole vielä hyväksytty
> toteutukseen. Lähteet: [hyväksytty PRD](prd.md), [arkkitehtuuri](architecture.md)
> ja [päätösloki](decision-log.md). EPIC-tunnukset seuraavat PRD:n hahmotelmaa.

## Epic 1: Lähetys ja kertymä (EPIC-001)

**Goal:** Käsittelijä tallentaa kokonaisen EUR-palautuksen ja saa järjestyksessä
lasketun 365 vuorokauden kertymän mukaisen tilan ilman kaksoiskirjausta.

**In scope (cited):** FR-001, FR-002, FR-005 ja FR-007
[Source: prd.md#functional-requirements]; NFR-003:n lähetyspuoli
[Source: prd.md#non-functional-requirements].

**Architecture touchpoints:** `RefundProcessorService`,
`RefundApprovalCheckRepository`, Flyway, SQLite ja lähetyksen REST-reitti
[Source: architecture.md#component-design]; varhainen kirjoituslukko ja UTC-ikkuna
[Source: architecture.md#adr-0015-säilytä-vahva-järjestys-yhdessä-sqlite-tiedostossa].

**Out of scope:** Päätöksen tekeminen, tilakysely, tuotannon identiteetti ja
aiemman historian tuonti.

**Stories (ordered):**

| ID | Slug | Intent | Status |
| --- | --- | --- | --- |
| 1.1 | sqlite-schema | Flyway-skeema ja kertymäkyselyn indeksi | backlog |
| 1.2 | jdbc-write-boundary | JDBC-repositoryn varhainen kirjoituslukko ja UTC-kertymäkysely | backlog |
| 1.3 | submit-and-total | Lähetys, UTC-365-päivän kertymä ja täsmällinen 10 000 EUR raja | backlog |
| 1.4 | submission-retry | `refundId`-uusinnan idempotenssi ja ristiriitaisen sisällön 409 | backlog |
| 1.5 | eur-input | EUR:n, jakamattomuuden ja määrän tarkkuuden syöterajat | backlog |

**Cross-epic dependencies:** 3.1:n Quarkus-runko mahdollistaa 1.1:n migraatiotestin;
1.3 tarvitsee 1.1:n, 1.2:n ja 3.1:n validoidun käsittelijäidentiteetin.
Epic 2:n päätös ja tilakysely tarvitsevat tallennetun
palautuksen. NFR-003:n rinnakkaislähetykset osoitetaan tämän epicin tarinoissa,
ei lykätä päätöstarinaan.

## Epic 2: Erillinen päätös ja tilan näkyvyys (EPIC-002)

**Goal:** Erillinen testihyväksyjä ratkaisee odottavan palautuksen kerran, ja
jokainen oikeutettu käsittelijä näkee tallennetun nykytilan.

**In scope (cited):** FR-003, FR-004 ja FR-006
[Source: prd.md#functional-requirements]; NFR-003:n päätöspuoli
[Source: prd.md#non-functional-requirements].

**Architecture touchpoints:** `RefundApprovalService`, päätöksen ja tilan
REST-reitit, sama transaktion kirjoituslukko ja pysyvä alkuperäinen käsittelijä
[Source: architecture.md#component-design] [Source: architecture.md#api-specifications].

**Out of scope:** Uusien palautusten kertymä, audit-historia ja tuotannon
luonnollisen henkilön todennus.

**Stories (ordered):**

| ID | Slug | Intent | Status |
| --- | --- | --- | --- |
| 2.1 | decide-pending | Hyväksy tai hylkää vain `PENDING` eri testitunnisteella | backlog |
| 2.2 | decision-retry | Ensimmäinen päätös säilyy uusinnassa ja kilpailutilanteessa | backlog |
| 2.3 | read-status | Nykytilan luku myös muulle oikeutetulle käsittelijälle | backlog |

**Cross-epic dependencies:** 2.1 tarvitsee 1.3:n ja 3.1:n;
2.2 tarvitsee 2.1:n; 2.3 tarvitsee tallennetun palautuksen ja 3.1:n.
3.2 rajaa päätösreitin profiiliin ennen kokonaisuuden luovutusta.

## Epic 3: Paikallisen simulaation turvaraja (EPIC-003)

**Goal:** Kolmen toiminnon paikallinen testikäyttö on varmennettu, rooleilla
rajattu ja jäljitettävä, eikä päätössimulaatio toimi muissa profiileissa.

**In scope (cited):** FR-008 [Source: prd.md#functional-requirements];
NFR-001, NFR-002 ja NFR-004 [Source: prd.md#non-functional-requirements].

**Architecture touchpoints:** SmallRye JWT, `@RolesAllowed`, `local-mvp`-raja,
problem+json ja korreloitavat JSON-lokit [Source: architecture.md#technology-stack]
[Source: architecture.md#api-specifications].

**Out of scope:** Entra-tuotantointegraatio, luonnollisen henkilön todistus ja
testiavaimen yksityisen osan tallentaminen sovellukseen.

**Stories (ordered):**

| ID | Slug | Intent | Status |
| --- | --- | --- | --- |
| 3.1 | validate-test-jwt | Paikallinen allekirjoitus-, issuer-, audience-, expiry- ja roolivarmennus | ready-for-dev |
| 3.2 | guard-decisions | Testiprofiiliin sidottu päätösreitti ja muiden profiilien estot | backlog |
| 3.3 | problem-responses | Yhteinen problem+json-virhesovitus kaikille reiteille | backlog |
| 3.4 | correlated-json-logs | JSON-lokien korrelaatio onnistumisissa ja virheissä | backlog |

**Cross-epic dependencies:** 3.1 edeltää suojattujen lähetys-, päätös- ja
tilareittien viimeistelyä. 3.2 tarvitsee 2.1:n päätösreitin; 3.3 tarvitsee
kaikkien kolmen toiminnon reitit virhetarkistukseen; 3.4 tarvitsee samat reitit
ja 3.3:n virhelokitusta varten. Riippuvuudet
ovat tarinatasoisia, eivät koko Epic 3:n valmistumista odottava sykli.

## Delivery Tracking (count-based)

- Total stories: 12
- Done: 0
- Remaining: 12
- Completion rate: 0/12

## Notes

Käyttäjän hyväksymän epic-kartan 12 tarinaa on laadittu `backlog`-luonnoksiksi,
mutta tämä ei ole valmis handoff. Tarkistuksen tulos on
[valmiusraportissa](readiness-report-testcase01-2026-09-28.md): FAIL.
Arkkitehtuurin puuttuvat lukitut lähteet ja vanhan
ohjeen JWT-/statusristiriidat sekä PRD-addendumin Q4 pysyvät avoimina; niitä ei
merkitä ratkaistuiksi eikä Java-kehitystä käynnistetä tämän kartan perusteella
[Source: architecture.md#future-considerations-and-approval-blockers]
[Source: addendum.md#open-questions].