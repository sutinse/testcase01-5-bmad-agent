# Decision Log - testcase01

Paikallinen suunnitteluloki. Lokkimerkinnät eivät itsessään ole GitHub-portin hyväksyntöjä: arkkitehtuuri hyväksyttiin PR #5:ssä ja näyttö kirjattiin PR #6:ssa. Alla olevan 2026-09-28 ADR-luettelon "Proposed" kuvaa sen silloista tilaa, ei nykyistä porttitilaa. Uusi päätös lisätään ylimmäksi; aiempia ei poisteta.

### 2026-09-29 - Suunnittelupaketin ei-tyhjien JWT-väitteiden tarkennus (ehdotus)
- **Decision:** Tarina 3.1 omistaa frameworkin validoiman tokenin yhteisen `sub`/`groups`-sisältötarkistuksen ja testifixturen; tarinat 1.3, 2.1 ja 2.3 kytkevät sen omiin reitteihinsä ja todentavat puuttuvien, tyhjien ja vain tyhjää tilaa sisältävien väitteiden 401 problem+json -vasteet sekä väärän roolin 403-vasteen. Päivitetty tiedosto-omistus näkyy sprintissä ja handoffissa; tarinoiden järjestystä ei muuteta.
- **Source:** Hyväksytyt NFR-001 ja ADR-0021; suunnittelun vanha hyväksyntä mitätöitiin PR #19:n `CHANGES_REQUESTED`-arvion perusteella PR #20:ssä.
- **Gate:** Tämä paketti tarvitsee oman riippumattoman hyväksynnän, yhdistämisen ja porttiin kirjatun suunnitteluhyväksynnän ennen Java-työtä. Tämä lokimerkintä ei myönnä sitä.

### 2026-09-29 - ADR-0021: ei-tyhjät paikalliset JWT-väitteet (ehdotus)
- **Decision:** Täydennetään ADR-0016:ta: validoidun testitokenin `sub` ja `groups` tarkistetaan ennen liiketoimintakäsittelyä kaikilla kolmella reitillä; tyhjä tai puuttuva identiteetti tai ryhmäjoukko hylätään 401-virheenä. `@RolesAllowed` säilyy erillisenä roolirajana.
- **Gate:** PRD:n tarkennus hyväksyttiin PR #13:ssa ja kirjattiin PR #14:ssa; aiempi arkkitehtuurihyväksyntä mitätöitiin PR #16:ssa. Tämä ADR sekä tarinan 3.1 ja suunnittelupaketin muutokset edellyttävät omia riippumattomia hyväksyntöjään ennen Java-toteutusta.

### 2026-09-29 - PRD:n JWT-vaatimuksen uudelleenkatselmointipyyntö (ehdotus)
- **Change requested:** Paikallisen MVP:n NFR-001:een ehdotetaan vaatimusta, jonka mukaan validoidun testitokenin `sub` ei saa olla tyhjä tai pelkkää tyhjää tilaa ja `groups`-joukossa on oltava vähintään yksi ei-tyhjä, ei pelkkää tyhjää tilaa sisältävä ryhmä kaikilla kolmella toiminnolla. Puuttuvat ja tyhjät väitteet on katettava negatiivisilla HTTP-testeillä; roolivaatimus säilyy erillisenä.
- **Rationale:** Pakollisen väitteen läsnäolo ei takaa ei-tyhjää arvoa; tyhjä `sub` läpäisi paikallisen HTTP-varmennuksen. Nykyinen hyväksytty PRD ei kata näitä arvoja.
- **Gate:** Tämä PR pyytää riippumattomalta arvioijalta GitHubin **Request changes** -arviota nykyiselle head-commitille, ei hyväksyntää tai yhdistämistä. Vasta tämän jälkeen `request-changes testcase01 prd --pr <numero>` voi kirjata mitätöinnin. Hyväksyttyä PRD:tä ja muita hyväksyttyjä artefakteja ei muuteta tässä PR:ssä. Korjattu PRD, arkkitehtuuri ja suunnittelupaketti tarvitsevat omat uudet suojatut hyväksymiskierroksensa.

### 2026-09-29 - Suunnittelupaketin sarjallinen jonotus
- **Decision:** Suunnittelu-PR:n luonnoksessa 12 tarinaa järjestetään aaltoihin 3.1 -> 1.1 -> 1.2 -> 1.3 -> 1.4 -> 2.1 -> 2.3 -> 1.5 -> 2.2 -> 3.2 -> 3.3 -> 3.4. Kukin aalto sisältää yhden tarinan, koska jaettuja tiedostoja ja yleismerkkipolkuja ei ole sertifioitu rinnakkaiseen ajoon. Vain 3.1 merkitään `ready-for-dev`-jonoon ja handoff-manifestiin.
- **Gate:** Jonotus ja manifesti ovat katselmoitavia luonnoksia, eivät valtuutus Java-työhön. Toteutus vaatii erikseen hyväksytyn ja yhdistetyn suunnittelu-PR:n sekä kirjatun suunnitteluportin hyväksynnän.
- **Source:** [sprint-status](sprint-status.yaml), [handoff](handoff-manifest.json), [valmiusarvio](readiness-report-testcase01-2026-09-28.md).

### 2026-09-29 - Paikallisen MVP:n lähdekorvaus hyväksytty PR #7:ssä
- **Decision:** PR #7 hyväksyttiin riippumattomasti (`sutinse1`), sen `workflow-gate` onnistui ja PR yhdistettiin suojattuun `main`-haaraan. Paikallisen MVP:n katselmoitavat lähteet ovat hyväksytty PRD, projektikonteksti, hyväksytty arkkitehtuuri ja päivitetyt repo-ohjeet. Puuttuvia `CONTEXT.md`-, `docs/adr/`- ja refund-spec-tiedostoja ei rekonstruoida tai vaadita paikallisen MVP:n kehityksen lähtötiedoiksi.
- **Scope:** Repo-ohjeet noudattavat ADR-0016/0020:n paikallista testitokenin varmennusta, simuloitua päätöstä ja kaikkien oikeutettujen käsittelijöiden tilakyselyä. Tämä ei muuta hyväksytyn arkkitehtuuritiedoston sisältöä eikä oikeuta tuotantohyväksyntää.
- **Gate:** PRD ja arkkitehtuuri ovat hyväksyttyjä, mutta suunnittelupaketti on vielä `pending`; tarinoita ei ole hyväksytty kehitykseen.
- **Source:** [PR #7](https://github.com/sutinse/testcase01-5-bmad-agent/pull/7), [arkkitehtuuri](architecture.md).

### 2026-09-29 - Ehdotus lukittujen lähteiden korvaamiseksi ja repo-ohjeiden sovittamiseksi
- **Status:** Myöhempi lähdekorvaus ja ohjemuutokset ovat ehdotuksia; PR #5:ssä hyväksyttyä arkkitehtuuria tai repo-ohjeita ei ole muutettu.
- **Source hierarchy proposal:** Käyttäjän mukaan vain `.github/copilot-instructions.md` on saatavilla; sen viittaamia `CONTEXT.md`-, `docs/adr/`- ja refund-spec-lähteitä ei ole. Ehdotetaan, että suojattu PR nimeää tämän puutteen nimenomaisesti ja hyväksyy PRD:n, projektikontekstin, uuden arkkitehtuuripäätöksen ja repo-ohjeiden päivitetyt kohdat paikallisen MVP:n lähteiksi. Puuttuvien asiakirjojen sisältöä ei rekonstruoida.
- **ADR-0016 alignment:** PR #5:ssä hyväksytty paikallisen `local-mvp`-profiilin päätös varmentaa testitokenin, sallii simuloidun eri identiteetin ja estää päätösreitin muissa profiileissa. Tuotantohyväksyntä ei sisälly toimitukseen. Vanha valmiiksi validoidun JWT:n ja luonnollisen henkilön oletus on vielä päivitettävä repo-ohjeessa.
- **ADR-0020 alignment:** PR #5:ssä hyväksytyssä paikallisessa MVP:ssä jokainen validoitu `refund-system`-käsittelijä voi lukea testipalautuksen tilan; lähetys vaatii edelleen `processorId == sub`. Repo-ohjeen vanha ADR-0013-yhteenveto on vielä päivitettävä.
- **Approval path:** Hyväksyttyä `architecture.md`-tiedostoa ei saa muuttaa paikallisesti tämän ehdotuksen perusteella. `AGENTS.md`:n lähdevaatimus, `.github/copilot-instructions.md`:n ristiriidat ja myöhempi lähdekorvaus on ratkaistava suojatussa, riippumattomasti katselmoidussa PR:ssä. Jos hyväksytty arkkitehtuurisisältö tai sen hyväksytyt riippuvuudet muuttuvat, tarvitaan uusi vaiheen PR ja hyväksyntä portin ohjeen mukaan. Chat-vastaus ei ole hyväksyntä.
- **Made by:** käyttäjän 2026-09-29 vahvistamat ehdotusvalinnat
- **Source:** [arkkitehtuuri](architecture.md), [addendum](addendum.md)

### 2026-09-28 - Puuttuvat lähteet ja paikallisen testidatan elinkaari
- **Decision:** Käyttäjä vahvisti, että `.github/copilot-instructions.md` on ainoa saatavilla oleva lukittuja ratkaisuja kuvaava tiedosto; sen viittaamia `CONTEXT.md`-, ADR- ja refund-spec-lähteitä ei ole saatavilla. Muita liiketoiminta- tai tietoomistajia tai tukidokumentteja ei käyttäjän mukaan ole. Kehittäjä poistaa paikallisen SQLite-tietokannan demon jälkeen; PostgreSQL:n käyttö määritellään erillisessä myöhemmässä toimituksessa.
- **Rationale:** Puuttuvaa alkuperäistä lähdeaineistoa ei voi rekonstruoida ohjeen perusteella. Testidatan poisto rajaa paikallisen demon elinkaarta muuttamatta MVP:n tallennusteknologiaa.
- **Impact:** Addendumin Q4 ja testidatan elinkaari tarkentuvat. Poiston toteutus ja todennus sekä lukitut päätökset korvaava hyväksytty lähde- ja ADR-paketti ovat vielä avoinna. Tämä ei ole GitHub-vaihehyväksyntä eikä poista valmiusarvion FAIL-tilaa.
- **Made by:** käyttäjä, paikallinen tarkennus
- **Source:** [addendum](addendum.md)

### 2026-09-28 - Arkkitehtuurin ADR-ehdotukset (ei hyväksytty)
- **ADR-0014 (Proposed):** Kolme erillistä REST-pyyntöä: lähetys, myöhempi päätös ja tilakysely.
- **ADR-0015 (Proposed):** Yksi SQLite-kirjoittaja, varhainen kirjoituslukko, täsmälliset senttimäärät ja atominen 365 vuorokauden kertymä.
- **ADR-0016 (Proposed):** Paikallisen testitokenin varmennus, framework-roolit ja vain testiprofiilissa sallittu päätösreitti.
- **ADR-0017 (Proposed):** Palvelimen omistama palautuksen tila, identtinen uusinta ja ensimmäinen päätöksentekijä jäävät voimaan.
- **ADR-0018 (Proposed):** 200 liiketoimintatiloille ja RFC 7807 -virherunko epäkelvoille pyynnöille.
- **ADR-0019 (Proposed):** Yhtenäinen nimeäminen ja JSON-lokien pyyntökorrelaatio.
- **ADR-0020 (Proposed):** Kaikki oikeutetut käsittelijät voivat kysyä tilan; vanhan, vain alkuperäiselle käsittelijälle sallitun tilakyselyn korvaaminen edellyttää erillistä hyväksyntää.
- **Source:** [arkkitehtuuriluonnos](architecture.md). Ehdotukset eivät muuta lukittua ohjetta tai anna toteutuslupaa ennen riippumatonta GitHub-katselmointia, puuttuvien lähteiden käsittelyä ja ristiriitojen ratkaisemista.

### 2026-09-28 - PRD-luonnoksen laajuus ja priorisointi
- **Decision:** PRD 0.1 kuvaa vain käyttäjän vahvistaman suljetun paikallisen MVP:n. Kaikki kahdeksan toiminnallista ja neljä laatua koskevaa vaatimusta ovat Must, koska kukin osallistuu välttämättömään kolmen toiminnon, kertymän eheyden tai testin eristämisen kokonaisuuteen; uusia Should/Could-toimintoja ei oleteta. Tuotantohyväksyntä, todellinen ihmisyyden todennus, Entra-tuotantointegraatio ja vanha historia pysyvät tämän toimituksen ulkopuolella.
- **Rationale:** Prioriteetit ilmaisevat tämän toimituksen vähimmäisrajan, eivät arvioita tulevista ominaisuuksista. PRD:n avoimet tekniset ja hallinnolliset päätökset kirjataan addendumiin arkkitehtuuria varten.
- **Impact:** Luotu `prd.md` ja `addendum.md` luonnoksina. PRD-aloitusportin läpäisy ei ole PRD:n hyväksyntä; erillinen suojattu, riippumattomasti arvioitu ja yhdistetty PR vaaditaan ennen arkkitehtuurivaihetta. Lukitun tilakysely- ja JWT-oletuksen poikkeamat vaativat hyväksytyn ADR:n ennen kehitystä.
- **Made by:** Product, käyttäjän vahvistaman QG1-rajauspäätöksen pohjalta
- **Source:** [PRD](prd.md), [addendum](addendum.md), [QG1-muistio](qg1-feature-readiness.md)

### 2026-09-28 - QG1-tarkennus: paikallinen testidata ja profiiliraja
- **Decision:** Käyttäjä vahvisti, että asiakas- ja palautustiedot syntyvät vain palvelun paikallisista testipyynnöistä. Hyväksyntäsimulaatio toimii vain eksplisiittisessä paikallisessa testiprofiilissa ja on estetty muissa profiileissa. Onnistuminen osoitetaan sääntöjen ja rajauksen automaattisilla testeillä sekä Seppo Sutisen manuaalisesti hyväksymällä demolla.
- **Rationale:** Rajaa paikallisen testin datan ja identiteettisimulaation erilleen todellisista palautuksista; tarkka tekninen toteutus päätetään arkkitehtuurissa.
- **Impact:** Täsmennetään paikallisen MVP:n esiehdot ja hyväksymiskriteerit. Ei tuotantokäyttöä eikä muutosta GitHubin vaiheportteihin; demoarviota ei ole vielä annettu.
- **Made by:** käyttäjä, QG1-uudelleenarvioinnin jälkeinen vahvistus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)

### 2026-09-28 - Paikallisen MVP:n hyväksyntänäyttö
- **Decision:** Käyttäjä valitsi automaattiset testit ja niiden lisäksi Seppo Sutisen hyväksymän manuaalisen demon paikallisen MVP:n hyväksymistavaksi. Muita lähdedokumentteja tai päätösomistajia ei käyttäjän mukaan tunneta.
- **Rationale:** Paikallisen simulaation toiminta ja rajaus pitää osoittaa ennen valmistumisen toteamista; demoarviota ei ole vielä annettu. Automaattisten testien ja demon tarkempi sisältö täsmennetään hyväksymiskriteereissä.
- **Impact:** Täsmennetään PRD:n paikalliset hyväksymiskriteerit; ei tuotantohyväksyntää eikä muutosta GitHubin vaiheportteihin.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)

### 2026-09-28 - Course Correction: paikallinen MVP ilman tuotantohyväksyntää
- **Decision:** Käyttäjä rajasi tämän toimituksen suljettuun paikalliseen MVP:hen, jossa hyväksyntä simuloidaan testitokenilla. Tuotantohyväksyntä, Entra ID -tokenin varmennus ja luonnollisen henkilön hyväksynnän todennus kuuluvat erilliseen myöhempään toimitukseen. Paikallista simulaatiota ei saa käyttää tuotannossa.
- **Rationale:** Aiempi tuotantotavoite ei ole tämän toimituksen käytettävissä olevilla lähtötiedoilla osoitettavissa. Käyttäjä valitsi paikallisen MVP:n ja vahvisti laajuusmuutoksen vaikutusarvion erikseen.
- **Impact:** PRD:tä, epicejä, tarinoita tai sprint-status.yaml-tiedostoa ei vielä ole; niitä ei muuteta. Päivitetään QG1:n ja projektikontekstin toimitusrajaus ennen PRD:tä. Muut liiketoimintasäännöt säilyvät.
- **In-progress stories affected:** ei yhtään
- **Made by:** käyttäjä; bmad-correct-course, paikallinen suunnittelupäätös
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan tuotannon henkilötodennuksen tähän toimitukseen sijoittavan päätöksen ja muiden tuotannon tämän toimituksen tavoitteena pitävien kirjausten soveltamisen; niiden historia säilyy

### 2026-09-28 - Ilmoitettu Entra ID -myöntäjä ja Rovo-lähteen vahvistus
- **Decision:** Käyttäjä nimesi Azure Entra ID:n tuotantotokenin myöntäjäksi, toisti IAM:n liittävän hyväksymisen ryhmäoikeuden vain luonnolliselle henkilölle ja vahvisti Rovo-snapshotin lähde-URL:n sekä poiminta-ajan oikeiksi. Käyttäjän mukaan Entra ID:n käyttöä ei tarvitse erikseen varmistaa. Nämä ovat paikallisia lähtötietoja, eivät tuotantokontrollien tai vaiheportin hyväksyntä.
- **Rationale:** JWT:n hyväksyttävää `iss`- ja `aud`-arvoa, allekirjoitusavainten soveltuvuutta, delegoidun käyttäjätokenin ja sovellustokenin erottelua tai IAM-oikeuden myöntö- ja valvontakontrollia ei toimitettu tarkistettavaksi. Rovo-metatietoja ei ole tarkistettu ulkoisesta lähteestä. Tuotantohyväksynnän esto säilyy.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevien tuotantotokenin myöntäjää ja Rovo-metatietojen käyttäjävahvistusta koskevien avoimien kysymysten tila; varmennusvaatimukset säilyvät

### 2026-09-28 - Tuotannon avainlähteen ja IAM-ryhmäoikeuden tarkennus
- **Decision:** Käyttäjän mukaan `TENANT_ID`, `APP_ID`, `iss` ja `aud` annetaan ympäristökohtaisina parametreina. Tuotannon julkisten avainten osoite ehdotetaan muodostettavaksi muodossa `https://login.microsoftonline.com/{TENANT_ID}/discovery/keys?appid={APP_ID}`. Asiakkaan IAM liittää hyväksymiseen oikeuttavan ryhmäoikeuden vain oikealle henkilölle. Tämä on suunnittelun liiketoimintaoletus, ei muodollinen vaihehyväksyntä.
- **Rationale:** Käyttäjä on täsmentänyt aiemmin avoimen avainlähteen muodostustavan ja roolihallinnan toimintatavan. `iss`- ja `aud`-arvoja, tokeniin soveltuvaa avainlähdettä, ryhmäoikeuden välittymistä käyttäjätokeniin tai sovellustokenien poissulkua ei ole vielä varmennettu; tuotantohyväksynnän esto säilyy siihen asti.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan IAM-roolihallintamerkinnän avainlähteen muodostustapaa koskevan avoimuuden; muut varmennusvaatimukset säilyvät

### 2026-09-28 - Ehdotus erilliseksi paikalliseksi toimituspäätökseksi
- **Status:** Ehdotus, ei voimassa oleva porttihyväksyntä.
- **Decision:** Käyttäjä haluaa jatkaa ilman GitHub-repoa erillisellä päätöksellä. Ehdotettu muutos on määritellä paikallinen suunnittelun tarkistus- ja hyväksyntämenettely ennen PRD:n aloittamista sekä erottaa luonnokset hyväksytyistä artefakteista. Nykyinen GitHub-portti on edelleen voimassa; epäonnistunutta `check testcase01 prd` -tarkistusta ei korvata tällä kirjauksella.
- **Rationale:** Repossa ei käyttäjän mukaan ole GitHub-repoa, ja porttitarkistus pysähtyi `gh`-kirjautumisen puuttumiseen. Paikallisen menettelyn hyväksyjä, riippumattoman tarkastuksen näyttö, muutoshistoria ja voimaantulo on määriteltävä ennen kuin toimitussopimusta voidaan muuttaa; tuotantotokenin varmennuksen avoimet kysymykset pysyvät erillisinä.
- **Impact:** Ei PRD:tä, arkkitehtuuria, epicejä tai tarinoita muutettu. Tuotantohyväksynnän esto ja nykyiset vaiheportit säilyvät.
- **Made by:** käyttäjän pyytämä paikallinen suunnitteluehdotus
- **Supersedes:** ei mitään ennen voimassa olevaa toimitussopimuksen muutosta

### 2026-09-28 - IAM roolihallintana, tuotantotokenin myöntäjä avoin
- **Decision:** Käyttäjä täsmensi, että IAM on asiakkaan Identity Management, jossa käyttäjien roolit määritellään. Hänen mukaansa hyväksyjärooli myönnetään Entra ID:ssä vain luonnolliselle henkilölle, ei palvelulle. Tokenin myöntäjää, `iss`-arvoa, julkisten avainten lähdettä, roolirajoituksen dokumenttia tai kontrollin omistajaa ei yksilöity. Aiempi IAM:n nimeäminen tokenin myöntäjäksi ei ole enää vahvistettu lähtötieto. Tuotantohyväksynnän esto säilyy.
- **Rationale:** Roolien hallintapaikka ei todista, mikä palvelu allekirjoittaa tokenin tai miten henkilökohtainen rooli valvotaan. Käyttäjän antama tarkennus ei ole tekninen varmennus eikä muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan IAM:n myöntäjävalinnan ja sitä koskevan paikallisen hyväksynnän tulkinnan; aiemmat merkinnät säilyvät historiana

### 2026-09-28 - IAM tuotantotokenin myöntäjäksi ja lähdevalinnan hyväksyntä
- **Decision:** Käyttäjä vahvisti IAM-käyttäjähallinnan tuotantotokenin myöntäjäksi ja hyväksyi tämän valinnan tuotantohyväksynnän osalta. Tämä on paikallinen lähdevalinnan hyväksyntä, ei vahvistus teknisestä varmennuksesta eikä muodollinen vaihehyväksyntä. Hyväksynnän käyttö tuotannossa pysyy estettynä, kunnes myöntäjätunniste, allekirjoitusavainten luottamuslähde, roolin ihmisyyskontrolli ja vastuullinen päätösomistaja on todennettu ja hyväksytty.
- **Rationale:** Lähteen nimeäminen ratkaisee avoimen myöntäjävalinnan käyttäjän ilmoituksena, mutta ei yksin osoita, että palvelu hyväksyy vain luotetun myöntäjän henkilökohtaiset käyttäjätokenit.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan merkinnän avoimen tuotantotokenin myöntäjävalinnan; todentamattomuus ja tuotantoesto säilyvät

### 2026-09-28 - IAM-käyttäjähallinta ilmoitetun takuun lähteenä
- **Decision:** Käyttäjä nimesi IAM-käyttäjähallinnan ilmoitetun henkilökohtaisen hyväksyjäroolin takuun lähteeksi. Takuun dokumenttia, valvontakontrollia ja omistajaa ei nimetty eikä IAM-käyttäjähallintaa ole vahvistettu tuotantotokenin myöntäjäksi. Tuotantohyväksynnän esto säilyy, kunnes näyttö ja varmennus on hyväksytty.
- **Rationale:** Takuun lähde ja tokenin myöntäjä ovat eri tietoja; pelkkä lähteen nimi ei todenna luonnollista henkilöä tai tokenin alkuperää. Tämä on käyttäjän ilmoittama paikallinen tarkennus, ei muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan merkinnän avoimen takuun lähteen; todentamattomuus ja tuotantoesto säilyvät

### 2026-09-28 - Ilmoitettu henkilökohtaisen hyväksyjäroolin takuu
- **Decision:** Käyttäjän mukaan tokenin myöntäjällä on dokumentoitu ja valvottu takuu siitä, että hyväksyjärooli myönnetään vain luonnollisen henkilön henkilökohtaiselle tunnukselle, ei palvelu-, jaetulle tai ryhmätunnukselle. Dokumenttia, valvontakontrollia, myöntäjää eikä omistajaa nimetty; takuuta ei ole todennettu. Tuotantohyväksyntä pysyy estettynä, kunnes näyttö ja tuotantotokenin varmennus on hyväksytty.
- **Rationale:** Tokenin identiteetti- ja roolitieto voivat tukea ihmisyyden todentamista vain, jos niiden myöntö- ja käyttöehdot ovat luotettavat ja tarkistettavissa. Tämä on käyttäjän ilmoittama QG1-lähtötieto, ei tuotantoturvallisuuden tai vaiheportin hyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** ei muuta alla olevaa tuotantohyväksynnän estoa; ilmoittaa mahdollisesta todistusaineistosta

### 2026-09-28 - Tuotannon henkilötodennus kuuluu toimitukseen
- **Decision:** Käyttäjä rajasi tuotantohyväksynnän tähän toimitukseen ja ehdotti hyväksyjän identiteetin sekä ryhmä/rooli-oikeuden lukemista tokenista. Tokenin väitteet eivät yksin todista, että tunnus kuuluu luonnolliselle henkilölle. Hyväksyntä pysyy estettynä paikallisen testin ulkopuolella, kunnes luotettu myöntäjä, henkilötiedon lähde, varmennusmenetelmä ja päätösomistaja on määritelty ja hyväksytty.
- **Rationale:** Käyttäjä ei nimennyt todistuslähdettä eikä päätösomistajaa. Aiempi Entra JWKS:n siirto myöhempään vaiheeseen on ristiriidassa tämän toimituksen tuotantotavoitteen kanssa; tuotannon varmennuslähde ja lukitut suunnittelupäätökset on sovitettava yhteen ennen toteutusta. Tämä ei ole muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus; ihmisyyden näytön puute on QG1-havainto
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan merkinnän oletuksen tuotantohyväksynnän myöhemmästä vaiheesta; paikallisen testiavaimen rajaus säilyy

### 2026-09-28 - Kilpailevien hyväksyjien päätökset
- **Decision:** Ensimmäinen tallennettu päätös ja sen hyväksyjä jäävät voimaan. Eri hyväksyjän myöhempi päätösyritys antaa 409 `application/problem+json` myös silloin, kun päätös on sama; vain alkuperäisen hyväksyjän identtinen uusinta palauttaa nykyisen lopputilan. Vastakkainen päätös antaa 409.
- **Rationale:** Samanaikainen pyyntö ei saa korvata päätöstä tai sen tekijää; yhden hyväksyjän identtinen uusinta voidaan erottaa toisen hyväksyjän uudesta päätösyrityksestä. Tekninen atomisuus jää suunniteltavaksi. Tämä on paikallinen QG1-tarkennus, ei muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan merkinnän avoimeksi jättämä eri hyväksyjien samansisältöinen päätösyritys

### 2026-09-28 - Rinnakkaisten palautusten järjestys
- **Decision:** Saman asiakkaan yhtä aikaa saapuvat palautukset käsitellään atomisesti yksi kerrallaan tallennusjärjestyksessä. Ensin tallennettu vaikuttaa seuraavan kertymään; saapumisaika ei määritä etusijaa. Vain järjestyksessä kynnyksen ylittävä palautus siirtyy `PENDING`-tilaan.
- **Rationale:** Yhtäaikaiset pyynnöt eivät saa ohittaa kertymärajaa tai siirtää jo tallennettua palautusta jälkikäteen hyväksyttäväksi. Transaktioiden ja päätösten kilpailutilanteiden tekninen suojaus jää suunniteltavaksi. Tämä on paikallinen QG1-tarkennus, ei muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** aiemmin avoimeksi merkitty rinnakkaisten lähetysten liiketoimintajärjestys

### 2026-09-28 - Lähetyksen identtisyys ja paikallisen hyväksynnän raja
- **Decision:** Samalla `refundId`-tunnisteella vertailtavat lähetyskentät ovat `customerId` ja `amount`; EUR on ainoa sallittu valuutta. Uuden lähetyksen `processorId` on aina täsmättävä validoidun JWT:n `sub`-arvoon. Toinen oikeutettu käsittelijä saa tehdä identtisen uusinnan, mutta tallennettu alkuperäinen käsittelijä ei vaihdu. Paikallisen suljetun MVP:n hyväksyntäsimulaatiossa testitokenin `sub` ja hyväksyjärooli riittävät; ne eivät todista hyväksyjää luonnolliseksi henkilöksi.
- **Rationale:** Eri käsittelijä voi tarkistaa saman palautuksen nykytilan muuttamatta auditointia. Luonnollisen henkilön vaatimus jää paikallisessa simulaatiossa todentamatta: hyväksyntää ei sallita testiympäristön ulkopuolella, ennen kuin luotettava ihmisyyden näyttö ja tuotantovarmennus on päätetty. Päätös ei ole muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan merkinnän avoimen lähetyssisällön vertailun; tuotannon hyväksyjätodennus jää avoimeksi

### 2026-09-28 - Kertymän raja ja pyyntöjen uusinnat
- **Decision:** Liukuva 365 vuorokauden kertymä lasketaan UTC-aikaleimoista lähetyshetkeen; tasan 365 vuorokautta vanha tallenne kuuluu mukaan. Eri lähetyssisältö samalla `refundId`-tunnisteella antaa 409 `application/problem+json` ilman muutoksia. Identtinen saman hyväksyjän päätösuusinta palauttaa nykyisen lopputilan, vastakkainen päätös antaa 409 `application/problem+json`.
- **Rationale:** UTC-aikaleiman alaraja poistaa rajapäivän tulkinnan; ristiriitainen lähetys tai päätös ei saa muuttaa jo tallennettua palautusta. Lähetyssisällön vertailukentät ja samanaikaisten pyyntöjen atominen käsittely määritellään myöhemmin. Tämä on paikallinen tarkennus, ei muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** aiemmin avoimiksi merkityt UTC-rajapäivän ja uusintavasteiden säännöt

### 2026-09-28 - Paikallisen MVP:n JWT-varmennus
- **Decision:** Käyttäjä täsmensi, että testiluokka generoi tokenin myös paikallisen MVP:n ajonaikaisiin pyyntöihin. Palvelu validoi sen konfiguroidulla julkisella testiavaimella sekä ympäristömuuttujista luetuilla hyväksytyillä issuer- ja audience-arvoilla ja tokenin voimassaololla. Entra JWKS -rajapintaa ei käytetä paikallisen MVP:n varmennukseen; se on myöhempi tavoite. Testiavaimia ei saa käyttää tuotantovarmennukseen.
- **Rationale:** Paikallinen testiluokka ei voi allekirjoittaa tokenia Entran yksityisellä avaimella, joten aiemmin valittu Entra JWKS ei voi validoida paikallista testitokenia. Väitteiden nimet, roolikartoitus, testiavaimen hallinta ja tuotantovarmennus tarvitsevat vielä päätöksen. Tämä ei ole muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** aiemman JWKS-valinnan soveltamisen paikalliseen MVP:hen; alla oleva palvelun validointivastuu säilyy

### 2026-09-28 - Paikallinen riskikanta ja JWT-validoinnin muutos
- **Decision:** Käyttäjän ilmoituksen mukaan Seppo Sutinen hyväksyy paikallisesti vanhan historian poisjätön ja hylättyjen palautusten mukaanlaskennan riskit. Käyttäjä valitsi JWT:n allekirjoituksen, myöntäjän, yleisön ja voimassaolon validoinnin palvelun vastuulle.
- **Rationale:** Laskentariskit on tuotu päätösomistajan tietoon käyttäjän ilmoituksen mukaan. Palvelun oma validointi poikkeaa aiemmasta valmiiksi validoidun JWT:n oletuksesta; avainlähde, hyväksytyt arvot ja roolikartoitus on päätettävä ennen toteutusta. Ilmoitus ei todenna päätösomistajan henkilöllisyyttä eikä ole muodollinen vaihehyväksyntä.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** alla olevan merkinnän avoimen riskikannan; JWT-validoinnin aiempi MVP-oletus on muutosehdotus, kunnes ristiriitaiset linjaukset päivitetään

### 2026-09-28 - Kolme toimintoa ja avoimet riskit
- **Decision:** Käsittelijä lähettää palautuksen, eri luonnollinen henkilö hyväksyy tai hylkää odottavan palautuksen, ja kuka tahansa oikeutettu käsittelijä saa kysyä minkä tahansa palautuksen tilan. Saman asiakkaan 365 päivän summaan lasketaan myös odottavat ja hylätyt palautukset. Vain uuden SQLite-palvelun kautta syntynyt historia lasketaan; saman sisältöinen `refundId`-uusinta palauttaa nykytilan.
- **Rationale:** Käyttäjän vahvistamat QG1-tarkennukset. Vanhan historian poisjättö voi aliarvioida kertymän; hylätyn mukaanlaskenta voi yliarvioida maksetun kertymän. Näiden riskien päätösomistajaksi nimettiin Seppo Sutinen, mutta riskien hyväksyntää ei ole kirjattu. Tilakyselyn muutos poikkeaa aiemmasta, vain alkuperäistä käsittelijää koskevasta linjauksesta ja tarvitsee uuden suunnittelupäätöksen ennen toteutusta.
- **Made by:** käyttäjä, paikallinen QG1-tarkennus
- **Source:** [QG1-muistio](qg1-feature-readiness.md)
- **Supersedes:** aiempi tilakyselyn rajaus alustavasti; ei vielä hyväksyttyä ADR-muutosta

### 2026-09-28 - Track selected: bmad-method
- **Decision:** Alustetaan testcase01 paikallisesti BMad Method -polulle.
- **Rationale:** Käyttäjän valinta; kolme erillistä toimintoa sekä tietojen laskentaan ja käyttöoikeuksiin liittyvät päätökset tarvitsevat erillisen PRD:n ja arkkitehtuurin.
- **Made by:** käyttäjä, bmad-init
- **Supersedes:** none