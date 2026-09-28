# Product Requirements Document (PRD) - testcase01

**Project Name:** Refund Approval Check, paikallinen MVP
**Version:** 0.1
**Date:** 2026-09-28
**Author:** Product, luonnos
**Status:** Luonnos; ei GitHubin PRD-vaiheen hyväksyntää
**Track:** BMad Method

Lähteet: [Rovo-snapshot](input/rovo-feature.md), [QG1-uudelleenarviointi](qg1-feature-readiness.md), [projektikonteksti](project-context.md) ja [päätösloki](decision-log.md). Rovo-lähteen URL ja poiminta-aika ovat käyttäjän vahvistamia, eivät ulkoisesti todennettuja. Tässä PRD:ssä kuvataan vain suljettu paikallinen MVP; tuotantokelpoisuutta ei väitetä.

## Executive Summary

**Problem Statement:** Yksittäisen palautuksen 10 000 EUR raja ei yksin huomaa saman asiakkaan useita pienempiä vakuutusmaksupalautuksia. Esimerkiksi kaksi 6 000 EUR palautusta voi ylittää asiakkaan kokonaisrajan, jolloin hyväksynnän erottaminen käsittelystä on tarpeen.

**Proposed Solution:** Paikallinen palvelu laskee saman asiakkaan palautusten liukuvan kertymän, tallentaa rajanylityksen odottavaksi ja erottaa käsittelijän lähetyksen, hyväksyjän päätöksen ja käsittelijän tilakyselyn toisistaan. Hyväksyjä simuloidaan testitokenilla.

**Business Value:** Sääntöjen ja tilojen toiminta voidaan osoittaa paikallisesti ennen erillistä tuotantoratkaisua. Maksatuksen todellista turvallisuutta tai hyväksyjän luonnollista henkilöllisyyttä tämä toimitus ei osoita.

**Target Outcome:** BG-1: paikallisissa testeissä jokainen yli 10 000 EUR kumulatiivisen rajan ylittävä palautus odottaa erillistä päätöstä ja muut sallitut palautukset etenevät ilman sitä. BG-2: vain erillinen testihyväksyjä voi ratkaista odottavan palautuksen, ja valtuutettu käsittelijä saa sen ajantasaisen tilan. BG-3: hyväksyntäsimulaatio ei toimi paikallisen testiprofiilin ulkopuolella.

## Project Overview

### Background

Lähtökuvaus nostaa esiin kumuloinnin, valuutan, asiakasryhmät, osapalautukset ja luonnollisen henkilön vaatimuksen. QG1:n jälkeen käyttäjä täsmensi säännöt ja rajasi tämän toimituksen paikalliseen testiin. Tuotannon ihmisyyden varmentaminen sekä Entra ID -integraatio vaativat erillisen myöhemmän toimituksen.

### Current State -> Desired State

- **Current:** Ei toteutettua palvelua eikä paikallisen MVP:n kolmen toiminnon testinäyttöä.
- **Desired:** Paikallisista testipyynnöistä syntyneet palautukset noudattavat tässä kuvattuja kynnys-, päätös- ja tilasääntöjä, eikä hyväksyntäsimulaatiota voi käyttää muiden profiilien kautta.

### Stakeholders

| Stakeholder | Role | Interest | Influence |
| --- | --- | --- | --- |
| Palautuksen käsittelijä | Lähettäjä ja tilan kysyjä | Näkee oikean tilan ennen maksatusta | Käyttää paikallista toimintoa |
| Testihyväksyjä | Erillinen testikäyttäjä | Ratkaisee odottavan palautuksen paikallisesti | Käyttää paikallista päätöstoimintoa |
| Seppo Sutinen | Käyttäjän nimeämä riskipäätösomistaja ja demon hyväksyjä | Historian poisjätön ja hylätyn kertymävaikutus, demo | Käyttäjän ilmoitus, ei varmennettua muodollista hyväksyntää |
| Muut omistajat | Unknown | Tukidokumentit ja riippuvuudet | Unknown |

## Goals and Objectives

- **BG-1:** Estää yksittäisen palautuksen rajaan perustuva ohitus paikallisesti laskettavissa 365 päivän palautuksissa.
- **BG-2:** Erottaa odottavan palautuksen päätös lähetyksestä ja näyttää sen tila kaikille oikeutetuille käsittelijöille.
- **BG-3:** Pitää synteettinen hyväksyntä vain eksplisiittisessä paikallisessa testiprofiilissa.
- **User goals:** Käsittelijä voi lähettää ja seurata palautusta; testihyväksyjä voi hyväksyä tai hylätä käsittelijästä erillisellä identiteetillä.

## Functional Requirements

### FR-001: Palautuksen lähetys — MUST
**Description:** Oikeutettu käsittelijä lähettää kokonaisen palautuksen ilman hyväksyjää ja saa nykyisen päätöstilan.
**Acceptance Criteria:**
- Kun asiakkaan uusi kertymä on enintään 10 000 EUR, lähetys antaa `ALLOWED` ja `allowed=true` HTTP 200 -vastauksessa; tasan 10 000 EUR on sallittu.
- Kun uusi kertymä ylittää 10 000 EUR, palautus tallentuu `PENDING`-tilaan, `allowed=false`, eikä lähetyksessä ole hyväksyjää.
- Lähetyksessä annettu `processorId` täsmää lähettäjän validoidun JWT:n `sub`-arvoon; ristiriitainen tunniste ei luo palautusta.
**Related Epic:** EPIC-001

### FR-002: Asiakaskohtainen kertymä — MUST
**Description:** Lähetyksen päätös käyttää saman asiakkaan palveluun tallennettujen palautusten 365 vuorokauden liukuvaa summaa.
**Acceptance Criteria:**
- Kahdesta saman asiakkaan 6 000 EUR palautuksesta ensimmäinen antaa `ALLOWED` ja toinen `PENDING`, kun muita ikkunaan kuuluvia palautuksia ei ole.
- UTC-lähetyshetkestä täsmälleen 365 vuorokautta aiemmin tallennettu palautus kuuluu ikkunaan; vanhempi ei kuulu.
- `PENDING`- ja `BLOCKED`-tilaiset palautukset lasketaan myöhempään kertymään, eikä aiemman palautuksen tilaa arvioida takautuvasti uudelleen.
- Eri asiakkaiden kertymät eivät vaikuta toisiinsa; ennen palvelun paikallista käyttöä tehtyjä palautuksia ei tuoda laskentaan.
**Related Epic:** EPIC-001

### FR-003: Odottavan palautuksen päätös — MUST
**Description:** Erillinen testihyväksyjä hyväksyy tai hylkää `PENDING`-palautuksen paikallisessa simulaatiossa.
**Acceptance Criteria:**
- Testihyväksyjän identiteetti poikkeaa juuri tämän palautuksen tallennetun alkuperäisen käsittelijän identiteetistä; sama identiteetti ei voi päättää palautusta.
- Hyväksyntä muuttaa `PENDING`-tilan `ALLOWED`-tilaksi ja `allowed=true`; hylkäys muuttaa sen lopulliseen `BLOCKED`-tilaan ja `allowed=false`.
- Päätös on erillinen lähetyksestä, ja onnistunut liiketoimintatila palautuu HTTP 200 -vastauksessa.
- Muu kuin `PENDING`-palautus ei saa uutta päätöstä lukuun ottamatta FR-006:n identtistä uusintaa.
**Related Epic:** EPIC-002

### FR-004: Palautuksen tilakysely — MUST
**Description:** Jokainen oikeutettu käsittelijä voi kysyä minkä tahansa palveluun tallennetun palautuksen nykyisen tilan.
**Acceptance Criteria:**
- Kysely palauttaa `PENDING`, `ALLOWED` tai `BLOCKED` ja vastaavan `allowed`-arvon HTTP 200 -vastauksessa.
- Myös muu oikeutettu käsittelijä kuin palautuksen alkuperäinen lähettäjä saa tilan ilman että tallennettu käsittelijä vaihtuu.
- Ilman käsittelijän oikeutta kysely hylätään eikä palauta palautuksen tilaa.
**Related Epic:** EPIC-002

### FR-005: Lähetyksen uusinta — MUST
**Description:** Sama `refundId` ei lisää palautusta tai kertymää uudelleen.
**Acceptance Criteria:**
- Kun `refundId`, `customerId` ja `amount` vastaavat tallennettua palautusta, lähetyksen uusinta palauttaa nykyisen tilan ilman uutta päätöstä tai summaa.
- Toinenkin oikeutettu käsittelijä voi tehdä identtisen uusinnan, kun pyynnön `processorId` vastaa hänen validoitua `sub`-arvoaan; alkuperäinen käsittelijä ei vaihdu.
- Saman `refundId`-tunnisteen eri `customerId` tai `amount` antaa 409 `application/problem+json` eikä muuta tallennetta tai kertymää.
**Related Epic:** EPIC-001

### FR-006: Päätöksen uusinta — MUST
**Description:** Yksi tallennettu päätös ja sen tekijä pysyvät voimassa myös toistetuissa ja kilpailevissa pyynnöissä.
**Acceptance Criteria:**
- Alkuperäisen hyväksyjän identtinen päätöspyyntö palauttaa nykyisen lopputilan muuttamatta päätöstä.
- Alkuperäisen hyväksyjän vastakkainen päätös antaa 409 `application/problem+json` muuttamatta päätöstä.
- Eri hyväksyjän myöhempi päätösyritys antaa 409 `application/problem+json`, myös jos päätös on sisällöltään sama.
- Samanaikaisista päätöksistä vain ensimmäinen tallennettu päätös ja sen hyväksyjä jäävät voimaan.
**Related Epic:** EPIC-002

### FR-007: Palautuksen syötteen rajoitukset — MUST
**Description:** Palvelu käsittelee vain kokonaisia, jakamattomia EUR-määräisiä palautuksia molemmille asiakasryhmille.
**Acceptance Criteria:**
- Muu kuin EUR-valuutta hylätään ennen tallennusta ilman muunnosta.
- Osapalautus tai loppuosan erillinen allokointi ei muodosta sallittua palautusta.
- Sama sääntö ja raja koskevat henkilö- ja yritysasiakasta.
**Related Epic:** EPIC-001

### FR-008: Oikeutettu paikallinen käyttö — MUST
**Description:** Lähetys ja tilakysely kuuluvat käsittelijäroolille, päätös hyväksyjäroolille, ja hyväksyntä on käytettävissä vain paikallisessa testiprofiilissa.
**Acceptance Criteria:**
- Ilman voimassa olevaa oikeaa roolia lähetys, kysely tai päätös hylätään asianomaisen toiminnon osalta.
- Paikallisen testiprofiilin ulkopuolella hyväksyntä ja hylkäys ovat estettyjä myös testihyväksyjän tokenilla.
- Paikallisessa testissä eri `sub` ja hyväksyjärooli simuloivat erillistä hyväksyjää, mutta vastausta tai lokia ei esitetä luonnollisen henkilön tuotantovarmennuksena.
**Related Epic:** EPIC-003

## Non-Functional Requirements

### NFR-001: Testitokenin varmennus — MUST (Security)
**Description:** Paikallinen palvelu hyväksyy testipyynnön vasta allekirjoituksen, sallitun myöntäjän ja yleisön sekä voimassaolon tarkistuksen jälkeen.
**Acceptance / Threshold:** Kaikki neljä ehtoa täyttyvät; yhdenkin ehdon puuttuessa tai epäonnistuessa yksikään pyyntö ei saa onnistunutta liiketoimintavastausta.
**Measurement Method:** Automaattiset positiiviset ja kunkin ehdon rikkomista osoittavat negatiiviset testit.

### NFR-002: Simulaation eristäminen — MUST (Security)
**Description:** Testitokenilla tehtävä hyväksyntä toimii vain eksplisiittisesti valitussa paikallisessa testiprofiilissa.
**Acceptance / Threshold:** Muissa profiileissa onnistuneita testihyväksyntä- tai hylkäyspäätöksiä on nolla, myös jos testitoken on kelvollinen.
**Measurement Method:** Testit paikallisessa ja vähintään yhdessä muussa profiilissa sekä manuaalinen demo paikallisessa profiilissa.

### NFR-003: Rinnakkaisten tapahtumien eheys — MUST (Reliability)
**Description:** Saman asiakkaan rinnakkaiset lähetykset ja saman palautuksen rinnakkaiset päätökset säilyttävät yhden tallennusjärjestyksen.
**Acceptance / Threshold:** Rinnakkaisissa testitapauksissa yksikään `refundId` ei tuota kahta kertymäkirjausta tai kahta päätöstä; ensin tallennettu palautus vaikuttaa seuraavan kynnykseen ja ensimmäinen päätös jää pysyväksi.
**Measurement Method:** Samanaikaiset lähetys- ja päätöstestit, joissa tarkistetaan tallennettu kertymä, tilat ja päätöksen tekijä.

### NFR-004: Jäljitettävät virhe- ja tapahtumatiedot — MUST (Operability)
**Description:** Virheet erotetaan sallituista liiketoimintatiloista ja pyyntöjen tapahtumat ovat yhdistettävissä palautukseen.
**Acceptance / Threshold:** Virhevastaukset ovat `application/problem+json`; `PENDING` ja `BLOCKED` eivät yksin ole virheitä. Jokaisen pyynnön rakenteisessa lokitapahtumassa on korrelaatiotunniste ja palautukseen liittyvissä tapahtumissa tunnisteen avulla haettavissa oleva viite.
**Measurement Method:** Vasteiden mediatyypin sekä JSON-lokien kenttien tarkistus kaikille kolmelle toiminnolle ja virhetapauksille.

## Epics and User Stories (Outline)

### EPIC-001: Lähetys ja kertymä
**Business Value:** BG-1, myös peräkkäiset pienemmät palautukset havaitaan paikallisesti.
**User Segments:** Käsittelijä.
**Related Requirements:** FR-001, FR-002, FR-005, FR-007, NFR-003.

**User Stories (sketch):**
- **STORY-001:** As a käsittelijä, I want lähettää kokonaisen EUR-palautuksen, so that saan sen sallitun tai odottavan tilan. Given 6 000 EUR kertymä, when lähetän toisen 6 000 EUR palautuksen, then uusi tila on `PENDING`.
- **STORY-002:** As a käsittelijä, I want uusia saman palautuksen lähetyksen, so that saan sen nykytilan kasvattamatta kertymää. Given sama `refundId` ja muuttunut summa, when uusin pyynnön, then saan 409 ilman muutosta.

### EPIC-002: Erillinen päätös ja tilan näkyvyys
**Business Value:** BG-2, päätös ja tilan seuranta eivät sekoitu lähetykseen.
**User Segments:** Testihyväksyjä ja käsittelijä.
**Related Requirements:** FR-003, FR-004, FR-006, NFR-003.

**User Stories (sketch):**
- **STORY-003:** As a testihyväksyjä, I want päättää odottavan palautuksen, so that sen lopullinen tila on tiedossa. Given alkuperäisestä käsittelijästä eri tunniste, when hyväksyn tai hylkään, then tila on `ALLOWED` tai `BLOCKED`.
- **STORY-004:** As a käsittelijä, I want kysyä palautuksen tilan, so that näen odottavan ja lopullisen päätöksen. Given oikeutettu eri käsittelijä, when kysyn tilan, then näen nykytilan muuttamatta alkuperäistä käsittelijää.

### EPIC-003: Paikallisen simulaation turvaraja
**Business Value:** BG-3, testikäytön tulos ei siirry vahingossa tuotantohyväksynnäksi.
**User Segments:** Paikallisen demon osallistujat.
**Related Requirements:** FR-008, NFR-001, NFR-002, NFR-004.

**User Stories (sketch):**
- **STORY-005:** As a demon arvioija, I want nähdä että hyväksyntä toimii vain paikallisella testiprofiililla, so that sitä ei tulkita tuotantokäyttöiseksi. Given muu profiili, when yritän tehdä päätöksen testitokenilla, then se ei onnistu.

## Prioritization Summary (MoSCoW)

| Priority | Requirements | Rationale |
| --- | --- | --- |
| Must | FR-001–FR-008, NFR-001–NFR-004 | Nämä ovat käyttäjän vaatiman kolmen toiminnon, eheän kertymän ja suljetun testin jakamaton vähimmäiskokonaisuus; yksittäisen Must-kohdan pudotus rikkoo tavoitteen. |
| Should | Ei vahvistettuja ehdokkaita | Toimitukseen ei lisätä valinnaista käyttäytymistä ilman lähdepäätöstä. |
| Could | Ei vahvistettuja ehdokkaita | Ei spekulatiivisia ominaisuuksia. |
| Won't (this release) | Tuotantohyväksyntä, todellinen luonnollisen henkilön todennus, Entra-tuotantointegraatio, vanhan historian tuonti, valuuttamuunnos ja osapalautus | Paikallinen MVP tai käyttäjän erikseen pois rajaama käyttäytyminen. |

## Success Metrics

| Metric | Baseline | Target | Measurement Method | Frequency |
| --- | --- | --- | --- | --- |
| Kolmen toiminnon, kertymän ja rajatapausten läpäisy | Ei palvelua | Kaikki PRD:n hyväksymiskriteerit läpäisevät automaattiset testit | Suorita kriteereihin kohdistetut testit ja kirjaa tulokset | Ennen demoa |
| Testiprofiilin ulkopuolinen päätös | Ei palvelua | 0 onnistunutta simuloitua päätöstä | Negatiiviset profiili- ja roolitestit | Ennen demoa |
| Paikallisen demon hyväksyntä | Ei hyväksyntää | Seppo Sutisen erikseen kirjattu hyväksyntä kolmesta toiminnosta | Manuaalinen demo ja erillinen hyväksyntänäyttö | MVP:n valmistumisen yhteydessä |

## Assumptions and Dependencies

### Assumptions

- Paikallinen testi käyttää vain tämän palvelun testipyynnöistä syntyneitä palautuksia, eikä tulosta saa tulkita kaikkien todellisten 365 päivän palautusten kertymäksi.
- Käyttäjän ilmoituksen mukaan Seppo Sutinen hyväksyi paikallisesti vanhan historian poisjätön ja `BLOCKED`-palautusten mukaanlaskennan; henkilöllisyyttä tai muodollista hyväksyntää ei ole todennettu.
- Käsittelijän ja hyväksyjän erillisyys tarkoittaa tässä MVP:ssä vain erillisiä testitokenin identiteettejä, ei luonnollisen henkilön todistamista.

### Dependencies

| Dependency | Type | Owner | Status | Risk | Mitigation |
| --- | --- | --- | --- | --- | --- |
| Testiavain, myöntäjä, yleisö ja roolikartoitus | Paikallinen identiteetti | Unknown | Käyttäytyminen päätetty, tekninen määrittely avoin | Virheellinen oikeus tai testitokenin leviäminen | Arkkitehtuuripäätös ja negatiiviset testit |
| Kertymän ja päätösten atomisuus | Tallennus | Unknown | Järjestyssääntö päätetty, toteutus avoin | Rajan ohitus tai kaksi päätöstä | Arkkitehtuuripäätös ja rinnakkaistestit |
| Aiemmista käyttöoikeus- ja JWT-linjauksista poikkeaminen | Hallinto | Unknown | Hyväksyttyä korvaavaa ADR:ää ei ole | Toteutus rikkoo lukitun ohjeen | Hyväksytty päätös ennen kehitystä |
| Paikallisen demon arviointi | Liiketoiminta | Seppo Sutinen (käyttäjän ilmoitus) | Nimetty, ei vielä arvioitu | Virheellinen väite valmiudesta | Kirjaa erillinen demon hyväksyntänäyttö |
| Muut tukidokumentit ja omistajat | Lähdeaineisto | Unknown | Unknown | Mallin rajoitukset jäävät tunnistamatta | Pidä avoimena; älä päättele puuttuvaa näyttöä |

## Constraints

- **Technical:** Yksi paikallinen palvelu ja SQLite; testitokenia ei saa hyväksyä tuotantovarmennuksena. Repo-ohjeen mukainen REST/JSON-sopimus säilyy; tämän PRD:n teknisten yksityiskohtien ratkaisu kuuluu arkkitehtuurille.
- **Business:** EUR, jakamaton palautus, sama sääntö henkilö- ja yritysasiakkaalle, 365 UTC-vuorokauden liukuva kertymä, yli 10 000 EUR. Maksatuksen ulkoinen toteutus ei kuulu paikalliseen demoon.
- **Timeline:** Julkaisupäivä ja tuotannon erillisen toimituksen aikataulu Unknown.

## Out of Scope

| Excluded | Reason | Revisit? |
| --- | --- | --- |
| Tuotantohyväksyntä ja luonnollisen henkilön todennus | Suljettu paikallinen testisimulaatio ei osoita ihmisyyttä | Erillinen tuotantotoimitus |
| Entra ID:n tuotantotokenin varmennus ja IAM-kontrollit | Tuotantotokenien ja oikeuksien näyttö puuttuu | Erillinen tuotantotoimitus |
| Vanhan palautushistorian tuonti ja ulkoinen asiakasdatalähde | Testitiedot syntyvät vain palvelun paikallisista pyynnöistä | Tuotantotarpeen mukaan |
| Muut valuutat, osapalautukset ja valuuttamuunnos | Käyttäjän pois rajaamat liiketoimintatoiminnot | Uusi päätös |

## Risks and Mitigations

| Risk | Impact | Probability | Mitigation | Owner |
| --- | --- | --- | --- | --- |
| Ennen käyttöönottoa tehdyt palautukset jäävät kertymästä | Todellinen 365 päivän summa voi alittua | Unknown | Testi ei väitä tuotantovalmiutta; paikallisesti hyväksytyksi ilmoitettu riskirajaus näkyviin | Seppo Sutinen (käyttäjän ilmoitus) |
| Hylätty palautus kasvattaa kertymää ilman maksatusta | Uusi palautus voi vaatia hyväksynnän | Unknown | Eksplisiittinen hyväksymiskriteeri ja demo | Seppo Sutinen (käyttäjän ilmoitus) |
| Paikallinen testitoken hyväksytään muussa profiilissa | Synteettinen hyväksyntä voidaan sekoittaa oikeaan | Unknown | Oletuksena estävä profiiliraja, negatiiviset testit | Unknown |
| Lukittu alkuperäisen käsittelijän statusoikeus tai valmiiksi validoidun JWT:n oletus jää voimaan | Toteutus on ristiriidassa vahvistetun MVP:n kanssa | Unknown | Päivitä ristiriitaiset päätökset hyväksytyssä arkkitehtuurissa ennen kehitystä | Unknown |

## Traceability Matrix

| Requirement | Business Goal | Epic | User Story | Status |
| --- | --- | --- | --- | --- |
| FR-001 | BG-1 | EPIC-001 | STORY-001 | Luonnos |
| FR-002 | BG-1 | EPIC-001 | STORY-001 | Luonnos |
| FR-003 | BG-2 | EPIC-002 | STORY-003 | Luonnos |
| FR-004 | BG-2 | EPIC-002 | STORY-004 | Luonnos |
| FR-005 | BG-1 | EPIC-001 | STORY-002 | Luonnos |
| FR-006 | BG-2 | EPIC-002 | STORY-003 | Luonnos |
| FR-007 | BG-1 | EPIC-001 | STORY-001 | Luonnos |
| FR-008 | BG-3 | EPIC-003 | STORY-005 | Luonnos |
| NFR-001 | BG-3 | EPIC-003 | STORY-005 | Luonnos |
| NFR-002 | BG-3 | EPIC-003 | STORY-005 | Luonnos |
| NFR-003 | BG-1, BG-2 | EPIC-001, EPIC-002 | STORY-001, STORY-003 | Luonnos |
| NFR-004 | BG-2 | EPIC-003 | STORY-005 | Luonnos |

## Handoff

- **To Architecture:** Määritä atominen tallennus, paikallisen profiilin fail-closed-raja, JWT-väitteiden ja roolien kartoitus sekä testiavainhallinta. Ristiriita aiemman alkuperäisen käsittelijän tilakyselyoikeuden ja valmiiksi validoidun JWT:n oletuksen kanssa on ratkaistava hyväksytyllä ADR:llä ennen kehitystä. Älä oleta olemattomia `CONTEXT.md`- tai ADR-lähteitä toimitetuiksi.
- **To Sprint/Story Planning:** Yllä olevat epic- ja story-luonnokset ovat jäljitettävyyden lähtökohta, eivät vielä ready-for-dev-tarinoita.
- **Open questions / overflow:** katso `addendum.md`; niitä ei saa merkitä ratkaistuiksi pelkän tämän luonnoksen perusteella.
- **Approval boundary:** PRD vaatii erillisen suojatun PR:n riippumattoman ihmishyväksynnän ennen arkkitehtuurivaihetta.

## Revision History

| Version | Date | Author | Changes |
| --- | --- | --- | --- |
| 0.1 | 2026-09-28 | Product | Ensimmäinen paikalliseen MVP:hen rajattu PRD-luonnos |