# Project Context - testcase01

- **Track:** bmad-method
- **Created:** 2026-09-28
- **Status:** paikallinen luonnos; käyttäjä ilmoitti riskien paikallisesta hyväksynnästä, ei muodollisesta vaihehyväksynnästä

## Project Goal

Paikallisessa suljetussa MVP:ssä vakuutusmaksupalautuksen hyväksyntäsäännöt ja tilat voidaan testata simuloiduilla tokeneilla. Tuotannossa rajan ylittävä palautus saa edetä maksatukseen vasta käsittelijästä erillisen luonnollisen henkilön päätöksellä; tämän vaatimuksen todennettava toteutus kuuluu erilliseen myöhempään toimitukseen. Käsittelijä voi tarkistaa palautuksen tilan erikseen.

## Primary Users

- Palautuksen käsittelijä lähettää palautuksen ja kysyy tilan.
- Paikallisessa MVP:ssä erillisellä testikäyttäjän tunnisteella ja hyväksyjäroolilla simuloitu hyväksyjä hyväksyy tai hylkää odottavan palautuksen. Tuotannossa hyväksyjän on oltava käsittelijästä eri luonnollinen henkilö.

## Scope

- Kolme erillistä toimintoa: lähetys ilman hyväksyjää, odottavan palautuksen päätös ja tilakysely.
- Tämän toimituksen hyväksyntä on suljetun paikallisen ympäristön testitokenilla tehtävä simulaatio; tuotantohyväksyntää tai luonnollisen henkilön todennusta ei toimiteta tässä vaiheessa.
- Saman asiakkaan UTC-aikaleimoihin perustuva liukuva 365 vuorokauden kertymä (alaraja mukana): yli 10 000 EUR johtaa `PENDING`-tilaan; enintään 10 000 EUR johtaa heti `ALLOWED`-tilaan. Päätös muuttaa `PENDING`-tilan `ALLOWED`- tai lopulliseen `BLOCKED`-tilaan.
- Odottavat ja hylätyt palautukset ovat mukana myöhemmässä kertymässä. Vain tämän uuden palvelun kautta tallentunut historia lasketaan; aiempia palautuksia ei tuoda.
- Paikallisen MVP:n asiakas- ja palautustiedot syntyvät vain tämän palvelun testipyynnöistä; ulkoista datalähdettä ei ole tässä toimituksessa.
- Saman asiakkaan rinnakkaiset lähetykset käsitellään atomisesti yksi kerrallaan tallennusjärjestyksessä: aiemmin tallennettu kuuluu seuraavan kertymään. Saapumishetki ei anna etusijaa; vain järjestyksessä kynnyksen ylittävä palautus odottaa hyväksyntää.
- Kaikki oikeutetut käsittelijät saavat kysyä minkä tahansa palautuksen tilan. Saman `refundId`-tunnisteen uusinnassa vain `customerId` ja `amount` määrittävät alkuperäiseen verrattavan sisällön (vain EUR sallitaan): samat arvot palauttavat nykytilan ilman uutta laskentaa, eri arvot antavat 409 muuttamatta palautusta. Uuden pyynnön `processorId` täsmää JWT:n `sub`-arvoon; toinenkin oikeutettu käsittelijä saa uusia pyynnön, mutta tallennettu alkuperäinen käsittelijä ei vaihdu. Ensimmäinen tallennettu päätös ja hyväksyjä pysyvät voimassa. Identtinen saman hyväksyjän päätösuusinta palauttaa nykyisen lopputilan; eri hyväksyjän yritys, myös samansisältöinen, tai vastakkainen päätös antaa 409.

## Core Constraints

- EUR ainoana valuuttana, ei osapalautuksia; sama sääntö henkilö- ja yritysasiakkaille. Yksi palautus käsitellään jakamattomana kokonaisuutena ennen maksatusta.
- SQLite uuden palvelun paikallisena tietokantana. Tallennusjärjestyksen toteutus, kertymän ajantasaisuus ja rinnakkaisten palautusten atominen käsittely on suunniteltava.
- Paikallisessa MVP:ssä testiluokka generoi JWT:n myös ajonaikaisiin pyyntöihin; palvelu validoi sen konfiguroidulla julkisella testiavaimella sekä ympäristömuuttujista luetuilla myöntäjän ja yleisön arvoilla ja tokenin voimassaololla. Paikallinen validointi ei käytä Entra JWKS:ää, eikä testiavainta saa käyttää tuotantovarmennukseen. Suljetussa paikallisessa testissä hyväksyjältä vaaditaan `sub` ja hyväksyjärooli; ne simuloivat hyväksyjää, mutta eivät todista luonnollista henkilöä. Hyväksyntä on estettävä testiympäristön ulkopuolella. Palvelun oma validointi muuttaa aiempaa valmiiksi validoidun JWT:n MVP-oletusta ja vaatii suunnittelupäätöksen ennen toteutusta.
- Testitokenin hyväksyntäsimulaatio käynnistyy vain eksplisiittisesti valitussa paikallisessa testiprofiilissa; muissa profiileissa hyväksyntä on estetty. Tekninen toteutus ja sen testaus täsmennetään arkkitehtuurissa.
- Myöhemmässä tuotantotoimituksessa tarvitaan luotettu tokenin myöntäjä, henkilötiedon lähde, varmennusmenetelmä, roolikartoitus ja päätösomistaja; sovellustunnuksen token tai ryhmä ei kelpaa luonnolliseksi henkilöksi. Käyttäjä nimesi Azure Entra ID:n tuotantotokenin myöntäjäksi. Hänen ehdotuksessaan tuotannon avainosoite muodostetaan `TENANT_ID`- ja `APP_ID`-ympäristöparametreista muodossa `https://login.microsoftonline.com/{TENANT_ID}/discovery/keys?appid={APP_ID}`; myös `iss` ja `aud` saadaan ympäristöparametreista. Arvoja, myöntäjää tämän palvelun tokeneissa ja avainlähteen soveltuvuutta kyseiseen tokeniin ei ole varmennettu.
- Käyttäjän tarkennuksen mukaan IAM on asiakkaan Identity Management, jossa käyttäjien roolit määritellään; IAM liittää hyväksymiseen oikeuttavan ryhmäoikeuden vain luonnolliselle henkilölle. Tämä ei todista oikeuden rajausta: kontrollin dokumentti, omistaja ja tekninen varmennus puuttuvat. Aiempi paikallinen merkintä IAM:sta tokenin myöntäjänä ei ole enää vahvistettu lähtötieto. Tuotantohyväksynnän esto säilyy, eikä chatissa annettu lähdevalinnan hyväksyntä ole muodollinen vaihehyväksyntä.
- Tilakyselyn oikeus muuttaa työtilan aiempaa alkuperäiseen käsittelijään rajattua linjausta. Ristiriitaiset suunnittelu- ja toteutusohjeet on päivitettävä hyväksytyllä päätöksellä ennen kehitystä.

## Non-Goals

- Ei valuuttamuunnosta, osapalautuksia tai muiden kuin EUR-palautusten hyväksyntää.
- Ei käyttöönottoa edeltävän palautushistorian tuontia eikä oman Entra ID -tunnisteiden myöntöpalvelun rakentamista MVP:ssä.
- Ei tuotantohyväksyntää tai luonnollisen henkilön todennettavaa hyväksyntää tässä toimituksessa; nämä vaativat erillisen myöhemmän suunnittelun ja hyväksynnän.

## Key Stakeholders / Roles

- Seppo Sutinen: käyttöönottoa edeltävän historian poisjätön ja hylättyjen palautusten mukaanlaskennan nimetty riskipäätösomistaja; käyttäjä ilmoitti hänen hyväksyneen molemmat riskit paikallisesti, henkilöllisyyttä ei ole todennettu.
- Seppo Sutinen: käyttäjän nimeämä paikallisen MVP:n manuaalisen demon hyväksyjä; hyväksyntää ei ole vielä saatu eikä henkilöllisyyttä todennettu.
- Muut liiketoiminta-, tieto- ja integraatio-omistajat: Unknown.

## Glossary

- **Palautus:** yksilöllisellä `refundId`-tunnisteella kirjattu EUR-määräinen jakamaton palautus.
- **Käsittelijä:** palautuksen lähettäjä; tilakyselyyn oikeutetaan myös muut käsittelijät.
- **Hyväksyjä:** paikallisessa MVP:ssä eri testikäyttäjän tunniste, jolla on hyväksyjärooli; tuotannossa käsittelijästä eri luonnollinen henkilö.
- **Kertymä:** saman asiakkaan palveluun tallentuneiden palautusten 365 päivän summa, mukaan lukien odottavat ja hylätyt.

## Decision Thread

Päätökset ja ristiriidat ovat [päätöslokissa](decision-log.md). Vahvistettujen tietojen erittely ja lähtöarvio ovat [QG1-muistiossa](qg1-feature-readiness.md).

## Planning Status

- **Track:** bmad-method
- **Stories defined:** 0
- **Stories remaining:** Unknown, kunnes tarinat on laadittu.
- **Paikallisen MVP:n hyväksyntänäyttö:** sääntöjen ja paikallisen käyttörajauksen automaattiset testit kattavat kolme toimintoa, kumuloinnin, roolit ja hyväksynnän eston muissa profiileissa; lisäksi Seppo Sutiselle esitetään kolmen toiminnon manuaalinen demo. Demon hyväksyntä kirjataan erikseen eikä korvaa GitHub-vaiheportteja. Muita lähdedokumentteja tai päätösomistajia ei tunneta.
- **Next:** täsmennä paikallisen testiavaimen hallinta ja roolikartoitus sekä rinnakkaisten tapahtumien suojaus PRD:ssä ja arkkitehtuurissa; pidä tuotannon IAM- ja Entra-varmennuksen avoimet kysymykset erillisen myöhemmän toimituksen lähtötietoina. Ratkaise aiemmista käyttöoikeus- ja MVP-päätöksistä poikkeavat muutokset hyväksytyllä suunnittelulla ennen toteutusta. GitHub-pohjainen PRD-aloitusportti läpäisee tarkistuksen, mutta QG1:n avoimet kysymykset eivät sillä ratkea eikä PRD-vaihetta ole vielä hyväksytty.