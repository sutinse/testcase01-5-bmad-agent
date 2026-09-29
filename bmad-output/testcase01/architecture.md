# System Architecture: testcase01 / Refund Approval Check

**Versio:** 0.2 (NFR-001-muutosehdotus)  \
**Päiväys:** 2026-09-29  \
**Vastuu:** Architect  \
**Raide:** BMad Method  \
**Tila:** aiempi arkkitehtuurihyväksyntä mitätöity PR #16:ssa; ADR-0021 odottaa uutta vaihehyväksyntää  \
**Lähde:** [hyväksytty PRD](prd.md), [projektikonteksti](project-context.md), [päätösloki](decision-log.md), [PRD:n addendum](addendum.md)

PRD:n uusi NFR-001 on hyväksytty PR #13:ssa ja kirjattu porttiin PR #14:ssa. Arkkitehtuurin aiempi hyväksyntä mitätöitiin PR #15:n muutospyynnön perusteella PR #16:ssa. ADR-0021 ja muutettu kattavuus tulevat voimaan vasta uuden arkkitehtuuri-PR:n riippumattoman katselmoinnin, yhdistämisen ja porttiin kirjaamisen jälkeen.

## 1. System Overview

Yksi suljettu, paikallinen REST-palvelu tallentaa testipyynnöistä syntyneitä kokonaisia EUR-palautuksia, laskee asiakaskohtaisen 365 UTC-vuorokauden kertymän ja sallii kynnyksen ylittävän palautuksen ratkaisun vain erillisellä testihyväksyjällä. Käsittelijä voi erikseen lukea minkä tahansa tallennetun palautuksen nykytilan. Maksatusta, todellista henkilötodennusta, Entra-tuotantointegraatiota, historian tuontia ja muita valuuttoja ei toteuteta.

**Arkkitehtuuriajurit:** NFR-001 (testitokenin allekirjoitus, issuer, audience, voimassaolo sekä ei-tyhjät `sub` ja `groups`), NFR-002 (päätösreitin ehdoton testiprofiiliraja), NFR-003 (järjestys ja yksi päätös kilpailutilanteissa) sekä NFR-004 (erotellut virheet ja jäljitettävyys). FR-002:n alarajan sisällyttäminen ja FR-004:n laajempi tilan luku ovat sopimuksen kriittiset rajatapaukset. Tiimin koko, suorituskykytavoite, tietojen säilytysaika ja tuotantovaatimukset eivät ole tiedossa; niitä ei oleteta.

## 2. Architecture Pattern

**Pattern:** layered modular monolith, yksi prosessi. REST-resurssit sovittavat JSON-pyynnöt palveluille; `RefundProcessorService` omistaa kertymän ja kynnyksen, `RefundApprovalService` käsittelijästä erillisen päätöksen, ja `RefundApprovalCheckRepository` SQL:n sekä transaktiot. SmallRye JWT ja Quarkus-hoitama roolivalvonta ovat HTTP-reunan turvaraja. **State management:** palvelin omistaa kaiken tilan; ei käyttöliittymää, välimuistia eikä tapahtumajonoa. Yksi SQLite-tiedosto ja yksi Quarkus-instanssi sopivat suljettuun paikalliseen testiin; mikropalvelut, hajautettu lukitus ja tuotannon HA eivät ole perusteltuja.

## 3. Architecture Decision Records

ADR-0014–0020 ovat aiemman hyväksytyn arkkitehtuurin päätöksiä; ADR-0021 on **Proposed**, kunnes uusi arkkitehtuuri-PR hyväksytään ja kirjataan porttiin. Vanhoja lähteitä `CONTEXT.md`, `docs/adr/` ja `.scratch/refund-approval-check/spec.md` ei ole tässä repossa; niiden sisältöä ei rekonstruoida. Paikallisen MVP:n lähdekorvaus ja repo-ohjeet hyväksyttiin PR #7:ssa. Tämä muutos ei tee tuotantohyväksynnästä sallittua.

### ADR-0014: Pidä rajapinta kolmessa REST-pyynnössä

**Context (FR-001, FR-003, FR-004, FR-005):** Lähetys ei sisällä hyväksyjää, päätös tehdään myöhemmin ja tila kysytään erikseen. **Decision:** `POST /api/v1/refund-approval-checks` luo tai uusii palautuksen; `POST /api/v1/refund-approval-checks/{refundId}/decisions` päättää odottavan; `GET /api/v1/refund-approval-checks/{refundId}` palauttaa nykytilan. JSON-kentät ovat camelCase, versio kuuluu polkuun. **Consequences / lukittu hyväksynnän jälkeen:** resurssit eivät laske kertymää tai erottele hyväksyjää itse; päätösreitti ei luo palautusta. Kolme kutsua helpottaa eri roolien erottamista mutta vaatii asiakkaalta tilan kyselyn. **Alternative:** välitön hyväksyntä lähetyksen yhteydessä hylätään, koska se rikkoo PRD:n. **Revisit:** vain uusi hyväksytty PRD, joka muuttaa työnkulkua.

### ADR-0015: Säilytä vahva järjestys yhdessä SQLite-tiedostossa

**Context (FR-002, FR-005, FR-006, NFR-003):** Myös `PENDING` ja `BLOCKED` vaikuttavat kertymään; yhtäaikaiset kirjoitukset eivät saa ohittaa rajaa. **Decision:** yksi SQLite-tiedosto ja yksi palveluinstanssi, vain JDBC/Agroal sekä Flyway-migraatiot. Yhteysaltaan kirjoituspolku käyttää yhtä yhteyttä kerrallaan; transaktio hankkii SQLite-kirjoituslukon (`BEGIN IMMEDIATE`) ennen idempotenssitarkistusta tai kertymän lukua, kirjoittaa ja commitoi ennen vastausta. Toteutus käyttää yhtä JDBC-transaktion aloitusmekanismia (SQLite IMMEDIATE -tila tai eksplisiittinen `BEGIN IMMEDIATE` automaattisen commitin ollessa käytössä), ei kahta peräkkäistä `BEGIN`-komentoa. Virhepolku tekee rollbackin samalla yhteydellä. Lukon epäonnistuminen aikakatkaisun jälkeen palauttaa palveluvirheen, ei `ALLOWED`-oletusta. Palvelin ottaa kellon UTC-ajasta lukon jälkeen; myöhemmin tallennettu näkee aiemman commitin. `refundId` on yksikäsitteinen avain. Päätös tehdään samalla kirjoituslukolla ja verrataan tallennettuun päätökseen ennen päivitystä. Rahat tallennetaan positiivisina kokonaisina sentteinä; syöte muunnetaan täsmällisesti `BigDecimal`-arvosta enintään kahdella desimaalilla, summa lasketaan ilman liukulukua ja ylivuoto on virhe. Kiinteä kynnys määritellään kerran 10 000 EUR `BigDecimal`-vakiona. Ikkuna on `submitted_at >= now - 365 * 24h` ja `submitted_at <= now`, alaraja mukana; kaikki tilat lasketaan, eikä aiempia tiloja muuteta. **Consequences / lukittu hyväksynnän jälkeen:** kaikki saman asiakkaan lähetykset ja päätökset järjestyvät tallennusjärjestykseen; myös eri asiakkaiden kirjoitukset serialisoituvat, mikä hyväksytään paikallisessa MVP:ssä. Välimuistia ei käytetä. **Alternative:** pelkkä luku ja myöhempi kirjoitus ilman varhaista lukkoa voi päästää kaksi palautusta saman kertymän läpi. **Revisit:** useampi instanssi tai mitattu kirjoituskuorma vaatii eri tietokannan ja uuden ADR:n.

### ADR-0016: Varmenna testitoken ja rajaa päätös testiprofiiliin

**Context (FR-001, FR-003, FR-008, NFR-001, NFR-002):** PRD edellyttää palvelun omaa validointia, vaikka vanha lukittu ohje olettaa jo validoidun JWT:n ja luonnollisen henkilön tarkistuksen. **Decision:** `quarkus-smallrye-jwt` validoi testitokenin allekirjoituksen konfiguroidulla julkisella testiavaimella, issuerin ja audiencen paikallisesti asetetuilla arvoilla sekä pakollisen voimassaoloajan; puuttuva tai virheellinen väite hylätään. Paikallisen testiavaimen yksityinen osa kuuluu vain testiluokan hallintaan, ei sovellukseen eikä repoon; julkinen avain ja `iss`/`aud` luetaan paikallisesta ympäristökonfiguraatiosta, eikä palvelu myönnä tokeneita. Roolit tulevat validoidun tokenin framework-kartoituksesta: `refund-system` lähetykseen ja lukuun, `refund-approver` päätökseen, `@RolesAllowed` reiteillä. Lähetyksen `processorId` verrataan validoituun `sub`-arvoon; päätöksen tekijä saadaan validoidusta `sub`-arvosta. Päätösreitti on käytössä vain eksplisiittisessä `local-mvp`-profiilissa; muissa profiileissa se estetään myös muuten kelvollisella testitokenilla. Testiprofiilin ulkopuolella testiavainta ei konfiguroida; virheellinen tai puuttuva turvakonfiguraatio estää käynnistyksen tai kaiken päätöksenteon (fail closed). Ei Entra-avaimia eikä ihmisyyttä koskevaa väitettä tähän MVP:hen. **Consequences / lukittu hyväksynnän jälkeen:** tokenin `sub` ja rooli osoittavat vain testissä eri identiteetit, eivät luonnollista henkilöä; tulosta ei nimetä tuotantohyväksynnäksi. Ennen kehitystä on varmennettava SmallRye JWT:n vaatimus pakolliselle `exp`-kentälle ja rooliväitteiden kartoitus integraatiotestillä. **Alternative:** luottamus valmiiksi validoituun tokeniin tai käsin kirjoitettu allekirjoituksen tarkistus ei täytä hyväksyttyä NFR-001:tä. **Revisit:** tuotannon identiteettitodennus vaatii oman toimituksensa ja hyväksytyt kontrollit.

### ADR-0017: Omista päätöstila palvelimella ja säilytä ensimmäinen tekijä

**Context (FR-001, FR-002, FR-003, FR-005, FR-006):** Tila ei saa muuttua rinnakkaisen yrityksen tai uusinnan vuoksi. **Decision:** alkuperäinen tallennettu palautus on `ALLOWED` tai `PENDING`. Vain `PENDING` muuttuu kerran `ALLOWED`- tai `BLOCKED`-tilaan. `allowed` vastaa aina ehtoa `outcome == ALLOWED`; `PENDING` ja `BLOCKED` ovat `false`. Päätöksen tekijä ja päätösaika tallennetaan lopullisen tilan kanssa atomisesti. Identtinen uusintalähetys vertaa vain `customerId` ja `amount` (EUR on pakollinen), palauttaa nykytilan eikä vaihda alkuperäistä käsittelijää. Päätöksen identtinen uusinta on sallittu vain samalle hyväksyjälle; eri hyväksyjä tai vastakkainen päätös on ristiriita. Samalle käsittelijälle tehty päätösyritys estetään jättämällä `PENDING` muuttumatta. **Consequences / lukittu hyväksynnän jälkeen:** ei takautuvaa uudelleenarviointia eikä erillistä client-side tilaa. Hylätyn laskeminen myöhempään kertymään voi yliarvioida maksatuksen, kuten PRD:n rajauksessa on todettu. **Alternative:** summan johtaminen vain sallituista palautuksista rikkoisi FR-002:n. **Revisit:** maksatusintegraation tai kertymäsäännön muutos edellyttää uutta liiketoimintapäätöstä.

### ADR-0018: Erota liiketoimintatila HTTP-virheestä

**Context (FR-001, FR-003, FR-004, FR-005, FR-006, NFR-004):** `PENDING` ja `BLOCKED` ovat valideja tiloja, ristiriitainen yritys ei ole. **Decision:** onnistunut lähetys, päätös, identtinen uusinta ja tilaluku vastaavat 200 JSON-tilalla (`outcome`, `allowed`). Virheissä käytetään `application/problem+json` (RFC 7807): 400 virheelliselle syötteelle, 401 puuttuvalle/virheelliselle tokenille, 403 rooli-, profiili- tai saman käsittelijän päätöskiellolle, 404 tuntemattomalle `refundId`:lle, 409 ristiriitaiselle `refundId`-sisällölle ja päätösyritykselle, 5xx tallennusvirheelle. Epäonnistunut päätös ei palauta valheellista `BLOCKED`-tilaa vaan jättää tallennetun tilan ennalleen. **Consequences / lukittu hyväksynnän jälkeen:** kaikki resurssit käyttävät samaa virhesovitinta ja JSON-skeemaa; asiakkaan on erotettava virhe liiketoimintatilasta. **Alternative:** 409 odottavasta palautuksesta rikkoisi PRD:n HTTP 200 -sopimuksen. **Revisit:** vain versionoidun API:n uusi sopimus.

### ADR-0019: Naming conventions ja yhtenäinen korrelaatio

**Context (FR-007, NFR-004):** Rinnakkaisten tarinoiden tieto- ja lokikentät eivät saa erota. **Decision:** polut plural/kebab-case, JSON camelCase, tietokanta snake_case, Java-paketit `<groupId>.refundapproval.{resource,service,persistence,exception}`, wire-tilat `PENDING|ALLOWED|BLOCKED`. JSON-rakenteinen lokitus (`quarkus-logging-json`) lisää jokaiseen pyyntöön korrelaatiotunnisteen, myös virheille ennen onnistunutta `refundId`-jäsennystä; palautukseen liittyvissä viesteissä on `refundId` rakenteisena kenttänä. Lokit kertovat tapahtuman ja tuloksen, eivät koskaan JWT:tä, testiavainta tai asiakkaan koko syötettä. **Consequences / lukittu hyväksynnän jälkeen:** yhdenmukainen haku ja dokumentaatio; paikallinen demo ei vaadi keskitettyä logipalvelua. **Alternative:** vapaamuotoiset lokit eivät läpäise NFR-004:n tarkistusta. **Revisit:** vasta uusi havaittavuusvaatimus.

### ADR-0020: Salli tilan luku jokaiselle oikeutetulle käsittelijälle

**Context (FR-004, FR-005):** Hyväksytty PRD sallii myös muun `refund-system`-käsittelijän kyselyn ja identtisen uusinnan, mutta vanhan ohjeen ADR-0013-yhteenveto vaatii tilakyselylle alkuperäisen käsittelijän JWT-subjektin. **Decision:** `GET` vaatii validoidun `refund-system`-roolin ja `sub`-arvon, mutta ei vertaa kysyjän `sub`:ia tallennettuun `processor_id`:hen. `POST` vaatii aina pyynnön `processorId == sub`, vaikka saman palautuksen identtisen uusinnan tekisi toinen käsittelijä; alkuperäinen käsittelijä pysyy tallessa. Ei uusia listaus- tai historianlukureittejä tähän toimitukseen. **Consequences / lukittu hyväksynnän jälkeen:** PRD:n mukainen näkyvyys toteutuu, mutta roolilla saa lukea kaikkien testipalautusten tilan. Tämä poikkeaa vanhasta lukitusta statusoikeudesta; ennen kehitystä on hyväksyttävä uusi ADR, joka nimenomaisesti syrjäyttää kyseisen kohdan ja päivittää ohjeen. **Alternative:** vain alkuperäisen käsittelijän statusoikeus hylätään, koska se rikkoo FR-004:n. **Revisit:** datan näkyvyyttä rajaava uusi vaatimus ja uusi hyväksytty PRD.

### ADR-0021: Hylkää tyhjät paikalliset JWT-identiteetti- ja ryhmäväitteet (Proposed)

**Context (NFR-001, FR-008; täydentää ADR-0016:ta):** Väitteen läsnäolo ei yksin takaa ei-tyhjää arvoa. **Decision:** Frameworkin varmennettua allekirjoituksen, issuerin, audiencen ja pakollisen voimassaoloajan tarkista validoidusta tokenista `sub` ja `groups` ennen liiketoimintakäsittelyä kaikilla kolmella reitillä. Hylkää pyyntö 401 `application/problem+json` -vastauksella, jos `sub` puuttuu, on tyhjä tai vain tyhjää tilaa, tai jos `groups` puuttuu, on tyhjä joukko tai sisältää vain tyhjiä / pelkkää tyhjää tilaa sisältäviä ryhmänimiä. Yksi ei-tyhjä ryhmä riittää väitteen muodon tarkistukseen, mutta käyttöoikeus vaatii edelleen reitin `@RolesAllowed`-roolin; väärä rooli on 403. Älä tarkista allekirjoitusta itse tai luota varmentamattomiin väitteisiin. **Consequences:** tarinan 3.1 hyväksymiskriteerit ja negatiiviset HTTP-testit on päivitettävä sekä suunnittelupaketti hyväksyttävä uudelleen ennen toteutusta; tuotannon identiteettitodennus ei muutu. **Alternative:** pelkät pakolliset väitteet tai rooliraja eivät takaa ei-tyhjiä `sub`- ja `groups`-arvoja. **Revisit:** tuotantotokenien väitesopimus määritetään erikseen.

## 4. Component Design

| Komponentti | Vastuu / rajapinta | Omistama tieto |
| --- | --- | --- |
| REST-resurssi ja virhesovitin | Kolme HTTP-reittiä, syötteen muotovarmistus, tilan JSON-vaste ja problem+json; ei liiketoimintasääntöjä | Ei pysyvää tietoa |
| JWT ja paikallinen profiiliraja | JWT:n framework-validointi, roolit, testiprofiilin päätösesto ja `sub`-identiteetin välitys | Ei pysyvää tietoa |
| `RefundProcessorService` | Uusi/identtinen lähetys, EUR ja jakamattomuus, asiakkaan kertymä, kynnys; kutsuu repositoryn kirjoitustransaktiota | Lähetyksen säännöt |
| `RefundApprovalService` | Odottavan päätös, tekijän ero, saman hyväksyjän uusinta; kutsuu repositoryn kirjoitustransaktiota | Päätöksen säännöt |
| `RefundApprovalCheckRepository` | Ainoa SQL-rajapinta; atomiikka, idempotenssi, haku ja tilapäivitys JDBC:llä | `refund_approval_check` |

Riippuvuussuunta on HTTP -> palvelut -> repository -> SQLite. Ajan lähteenä on injektoitava UTC-kello; testit voivat asettaa 365 vuorokauden rajatapauksen ilman oikean ajan odottamista. Tapahtumaloki ei ole tapahtumavarasto eikä korvaa pysyvää päätöksen tekijää.

## 5. Data Model

Flyway luo taulun `refund_approval_check`: `refund_id` (teksti, PK), `customer_id` (ei tyhjä), `processor_id` (ei tyhjä), `amount_cents` (positiivinen INTEGER), `currency` (vain `EUR`), `submitted_at_utc` (UTC-epoch-millis), `outcome` (`PENDING|ALLOWED|BLOCKED`), `approver_id` (nullable), `decided_at_utc` (nullable). Lopullisessa päätöksessä hyväksyjä ja päätösaika tallentuvat yhdessä; alkuperäisellä heti sallitulla rivillä ne ovat tyhjiä. Rinnakkaisuudessa uniikki PK suojaa `refundId`:n; indeksi `(customer_id, submitted_at_utc)` rajaa kertymäluvun. SQLite CHECK-rajoitteet estävät virheellisen valuutan, määrän ja tilan; palvelut omistavat siirtymäsäännöt. Rivit ovat tavallisia Java `record` -olioita; ei JPA:ta tai muuta ORM:ää. Kertymää ei tallenneta erillisenä päivitettävänä summana, vaan lasketaan transaktion sisältä saman asiakkaan ikkunan riveistä täsmällisesti. Ei välimuistia eikä vanhan historian tuontia. Säilytys- ja poistosääntö on avoin paikallisen testidatan elinkaarta varten; tietokantaa ei saa esittää tuotannon järjestelmäksi.

## 6. API Specifications

Kaikki reitit vaativat validoidun bearer JWT:n. `POST /api/v1/refund-approval-checks` (`refund-system`) ottaa `refundId`, `customerId`, `processorId`, `amount`, `currency=EUR`; asiakastyyppiä ei kysytä, sama sääntö koskee kumpaakin. `POST /api/v1/refund-approval-checks/{refundId}/decisions` (`refund-approver`, vain `local-mvp`) ottaa `decision=APPROVE|REJECT` ja käyttää hyväksyjän tunnisteena tokenin `sub`:ia. `GET /api/v1/refund-approval-checks/{refundId}` (`refund-system`) palauttaa minkä tahansa olemassa olevan palautuksen nykytilan. Onnistuneen 200-vastauksen kentät ovat `refundId`, `customerId`, `processorId`, `approverId` (null ennen päätöstä), `amount`, `currency`, `outcome`, `allowed`, `checkedAt` (UTC). Ei erillistä audit-historiareittiä ilman uutta vaatimusta. Rajapinnan täsmällinen OpenAPI-skeema ja tunniste-/määrärajoitukset määritetään tarinoissa tämän sopimuksen rajoissa. Virheiden `type`, `title`, `status`, `detail` ja pyyntökorrelaatio ovat problem+json-rungossa, eikä niissä vuoda JWT-sisältöä.

## 7. FR / NFR Coverage Matrix

| ID | Tyyppi | Vaatimus | Komponentti | ADR | Tila |
| --- | --- | --- | --- | --- | --- |
| FR-001 | FR | Lähetys ja kynnys | Processor, REST, JWT | ADR-0014, ADR-0015, ADR-0016 | Addressed (proposed) |
| FR-002 | FR | 365 vrk kertymä | Processor, Repository | ADR-0015, ADR-0017 | Addressed (proposed) |
| FR-003 | FR | Odottavan erillinen päätös | Approval, JWT | ADR-0014, ADR-0016, ADR-0017 | Addressed (proposed) |
| FR-004 | FR | Tila kaikille oikeutetuille käsittelijöille | REST, JWT, Repository | ADR-0014, ADR-0020 | Partial: vanha ohje vaatii supersession |
| FR-005 | FR | Lähetyksen uusinta | Processor, Repository | ADR-0015, ADR-0017, ADR-0020 | Addressed (proposed) |
| FR-006 | FR | Päätöksen uusinta | Approval, Repository | ADR-0015, ADR-0017, ADR-0018 | Addressed (proposed) |
| FR-007 | FR | Vain EUR ja jakamaton palautus | Processor, Repository | ADR-0015, ADR-0019 | Addressed (proposed) |
| FR-008 | FR | Paikalliset roolit ja profiili | JWT, REST | ADR-0016, ADR-0020, ADR-0021 | Addressed (proposed) |
| NFR-001 | NFR | JWT:n varmennus ja ei-tyhjät sub/groups | JWT, väitteiden tarkistus | ADR-0016, ADR-0021 | Partial: pakollisen exp:n ja tyhjien väitteiden esto varmennettava |
| NFR-002 | NFR | Testiprofiilin eristys | JWT, REST | ADR-0016 | Addressed (proposed) |
| NFR-003 | NFR | Rinnakkaisten tapahtumien eheys | Processor, Approval, Repository | ADR-0015, ADR-0017 | Addressed (proposed) |
| NFR-004 | NFR | Virheet ja korreloitavat JSON-lokit | REST, lokitus | ADR-0018, ADR-0019 | Addressed (proposed) |

**Muut NFR-luokat:** Performance/scalability: mitattua tavoitetta ei ole; paikallinen yksi instanssi, yksi kirjoittaja, asiakas/aika-indeksi ja ei välimuistia, koska eheys on nopeutta tärkeämpi. Security: rajattu testiavain, roolivalvonta, ei tuotantotokenin hyväksyntää; paikallisen demopalvelun verkkosidonta rajataan localhostiin ja pääsy ympäristöön rajoitetaan, eikä tuotannon TLS-, salaamis- tai vaatimustenmukaisuuslupausta anneta. Reliability/availability: ei HA:ta, paikallinen tiedosto voidaan varmuuskopioida demoja varten, eikä palautumistavoitetta ole hyväksytty. Maintainability/observability: erotetut palvelut, JSON-lokit ja päätöksen pysyvä tekijä; ei keskitettyä metriikka- tai hälytysalustaa ilman vaatimusta. Ei käyttöliittymää, joten WCAG-/responsiivisuussuunnitelma ei koske tätä palvelua. Testistrategia kattaa rajapäivän, tarkkuuden, roolien ja profiilien negatiiviset tapaukset sekä kilpailevat lähetykset ja päätökset; manuaalinen demo kirjataan erikseen.

## 8. Technology Stack

**Rationale:** valinnat minimoivat paikallisen käyttöönoton osat ja suojaavat NFR-001:n, NFR-003:n ja NFR-004:n ilman tuotantoinfrastruktuuria.

| Kerros | Valinta | Peruste |
| --- | --- | --- |
| Ajonaika | Java 25, Maven, Quarkus; tarkka tuettu Quarkus-versio varmennetaan ennen toteutusta | Olemassa oleva lukittu stack, ei spekulatiivista versiota |
| REST | `quarkus-rest`, `quarkus-rest-jackson` | FR-001/003/004:n JSON-rajapinta |
| Turva | `quarkus-smallrye-jwt`, frameworkin `@RolesAllowed` | NFR-001/002 ja roolien erottaminen |
| Tallennus | `quarkus-agroal`, `org.xerial:sqlite-jdbc`, `quarkus-flyway` | NFR-003, paikallinen yksi instanssi, migraatioiden toistettavuus |
| Lokitus | `quarkus-logging-json` | NFR-004 |

## 9. Trade-off Analysis

- **Yksi SQLite-kirjoittaja vs rinnakkainen kapasiteetti:** sarjallistus yksinkertaistaa FR-002/NFR-003:n osoittamista, mutta rajoittaa läpimenoa; monen instanssin käyttö ei ole sallittu ilman uutta tallennuspäätöstä.
- **Kaikkien oikeutettujen käsittelijöiden luku vs pienin näkyvyys:** FR-004 vaatii laajemman näkyvyyden; testidatassa se hyväksytään, mutta statusoikeuden vanha ADR-yhteenveto pitää nimenomaisesti muuttaa ennen kehitystä.
- **Testitokenin paikallinen validointi vs valmis/tuotannon identiteetti:** NFR-001 toteutuu paikallisesti, mutta ihmisyyttä eikä tuotantoon kelpaavaa avainhallintaa todisteta. Fail-closed-profiiliraja on ehdoton.

## 10. Deployment Architecture

Yksi paikallinen Quarkus-prosessi käyttää vain paikallista SQLite-tiedostoa ja eksplisiittistä `local-mvp`-profiilia. Testiluokka tuottaa testitokenit suljetussa ympäristössä; yksityistä testiavainta ei julkaista sovellukselle. Päätösreitti ei toimi muilla profiileilla eikä muita profiileja voi pitää tuotantokelpoisina tällä suunnitelmalla. Ei kuormantasaajaa, automaattista skaalausta tai tuotantoon vientisuunnitelmaa. Testitiedoston varmuuskopiointi ja poistaminen sovitaan ennen todellista käyttöä, ei tämän demopalvelun HA-vaatimuksena.

## 11. Future Considerations and Approval Blockers

1. Toimita puuttuvat lukitut `CONTEXT.md`, `docs/adr/` ja `.scratch/refund-approval-check/spec.md` tarkistettaviksi tai ratkaise niiden poissaolo nimenomaisella hyväksytyllä suunnittelupäätöksellä; älä oleta niiden sisältöä. `ADR-0020`:n statusoikeus ja `ADR-0016`:n JWT-/ihmisyysraja poikkeavat `.github/copilot-instructions.md`:n vanhasta lukitusta yhteenvedosta. Hyväksytyssä arkkitehtuuri-PR:ssä on osoitettava syrjäytyvät kohdat ja päivitettävä lukittu ohje ennen Java-työtä.
2. Varmenna käytetyn Quarkus/SmallRye-version Java 25 -tuki, vaaditun `exp`-väitteen hylkääminen, roolikartoitus sekä SQLite-kirjoitustransaktion `BEGIN IMMEDIATE` -järjestys integraatiotesteillä toteutusvaiheessa. Näitä ei ole vielä ajettu.
3. Selvitä PRD-addendumin Q4 (tuntemattomat omistajat/lähteet) suunnittelupaketin hyväksyntää varten ja sovi testidatan säilytys. Demon erillistä hyväksyntää ei ole vielä annettu.
4. Entra ID:n avainlähde, IAM:n ihmisyyskontrolli, tuotannon tila-/näkyvyysrajat ja vanhan historian siirto ovat erillisen tuotantotoimituksen kysymyksiä; tätä paikallista simulaatiota ei saa käyttää tuotantopäätöksenä.

**Viitteet:** [PRD](prd.md), [päätösloki](decision-log.md), [projektikonteksti](project-context.md), [addendum](addendum.md), repo-ohje `.github/copilot-instructions.md`. Dokumenttihistoria: 2026-09-28, versio 0.1, ensimmäinen arkkitehtuuriluonnos.