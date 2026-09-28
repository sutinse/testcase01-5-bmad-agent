# Decision Log - testcase01

Paikallinen suunnitteluloki. Nämä päätökset eivät ole GitHub-portin hyväksyntöjä. Uusi päätös lisätään ylimmäksi; aiempia ei poisteta.

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