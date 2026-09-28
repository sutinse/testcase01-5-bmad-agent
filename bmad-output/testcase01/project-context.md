# Project Context - testcase01

- **Track:** bmad-method
- **Created:** 2026-09-28
- **Status:** paikallinen luonnos; käyttäjä ilmoitti riskien paikallisesta hyväksynnästä, ei muodollisesta vaihehyväksynnästä

## Project Goal

Vakuutusmaksupalautus saa edetä maksatukseen vain hyväksyntäsääntöjen täyttyessä; rajan ylittävä palautus odottaa käsittelijästä erillisen luonnollisen henkilön päätöstä. Käsittelijä voi tarkistaa palautuksen tilan erikseen.

## Primary Users

- Palautuksen käsittelijä lähettää palautuksen ja kysyy tilan.
- Hyväksyjä, joka on eri luonnollinen henkilö kuin kyseisen palautuksen käsittelijä, hyväksyy tai hylkää odottavan palautuksen.

## Scope

- Kolme erillistä toimintoa: lähetys ilman hyväksyjää, odottavan palautuksen päätös ja tilakysely.
- Saman asiakkaan UTC-aikaleimoihin perustuva liukuva 365 vuorokauden kertymä (alaraja mukana): yli 10 000 EUR johtaa `PENDING`-tilaan; enintään 10 000 EUR johtaa heti `ALLOWED`-tilaan. Päätös muuttaa `PENDING`-tilan `ALLOWED`- tai lopulliseen `BLOCKED`-tilaan.
- Odottavat ja hylätyt palautukset ovat mukana myöhemmässä kertymässä. Vain tämän uuden palvelun kautta tallentunut historia lasketaan; aiempia palautuksia ei tuoda.
- Saman asiakkaan rinnakkaiset lähetykset käsitellään atomisesti yksi kerrallaan tallennusjärjestyksessä: aiemmin tallennettu kuuluu seuraavan kertymään. Saapumishetki ei anna etusijaa; vain järjestyksessä kynnyksen ylittävä palautus odottaa hyväksyntää.
- Kaikki oikeutetut käsittelijät saavat kysyä minkä tahansa palautuksen tilan. Saman `refundId`-tunnisteen uusinnassa vain `customerId` ja `amount` määrittävät alkuperäiseen verrattavan sisällön (vain EUR sallitaan): samat arvot palauttavat nykytilan ilman uutta laskentaa, eri arvot antavat 409 muuttamatta palautusta. Uuden pyynnön `processorId` täsmää JWT:n `sub`-arvoon; toinenkin oikeutettu käsittelijä saa uusia pyynnön, mutta tallennettu alkuperäinen käsittelijä ei vaihdu. Ensimmäinen tallennettu päätös ja hyväksyjä pysyvät voimassa. Identtinen saman hyväksyjän päätösuusinta palauttaa nykyisen lopputilan; eri hyväksyjän yritys, myös samansisältöinen, tai vastakkainen päätös antaa 409.

## Core Constraints

- EUR ainoana valuuttana, ei osapalautuksia; sama sääntö henkilö- ja yritysasiakkaille. Yksi palautus käsitellään jakamattomana kokonaisuutena ennen maksatusta.
- SQLite uuden palvelun paikallisena tietokantana. Tallennusjärjestyksen toteutus, kertymän ajantasaisuus ja rinnakkaisten palautusten atominen käsittely on suunniteltava.
- Paikallisessa MVP:ssä testiluokka generoi JWT:n myös ajonaikaisiin pyyntöihin; palvelu validoi sen konfiguroidulla julkisella testiavaimella sekä ympäristömuuttujista luetuilla myöntäjän ja yleisön arvoilla ja tokenin voimassaololla. Paikallinen validointi ei käytä Entra JWKS:ää, eikä testiavainta saa käyttää tuotantovarmennukseen. Tuotantohyväksyntä kuuluu tähän toimitukseen, mutta tuotantotokenin myöntäjä, `iss`-arvo ja julkisten avainten varmennuslähde ovat avoimia. Suljetussa paikallisessa testissä hyväksyjältä vaaditaan `sub` ja hyväksyjärooli; ne simuloivat hyväksyjää, mutta eivät todista luonnollista henkilöä. Tokenin identiteetti- ja ryhmätiedot eivät yksin riitä ihmisyyden näytöksi. Hyväksyntä on estettävä testiympäristön ulkopuolella, kunnes luotettu tokenin myöntäjä, henkilötiedon lähde, varmennusmenetelmä ja päätösomistaja on määritelty ja hyväksytty; sovellustunnuksen token tai ryhmä ei kelpaa. Roolikartoitus ja konfiguraation yksityiskohdat ovat avoimia. Palvelun oma validointi muuttaa aiempaa valmiiksi validoidun JWT:n MVP-oletusta ja vaatii suunnittelupäätöksen ennen toteutusta.
- Käyttäjän uuden tarkennuksen mukaan IAM on asiakkaan Identity Management, jossa käyttäjien roolit määritellään; hyväksyjärooli myönnetään Entra ID:ssä vain luonnolliselle henkilölle, ei palvelulle. Tämä ei yksilöi tuotantotokenin myöntäjää eikä todista roolin rajausta: kontrollin dokumentti, omistaja ja tekninen varmennus puuttuvat. Aiempi paikallinen merkintä IAM:sta tokenin myöntäjänä ei ole enää vahvistettu lähtötieto. Tuotantohyväksynnän esto säilyy, eikä chatissa annettu lähdevalinnan hyväksyntä ole muodollinen vaihehyväksyntä.
- Tilakyselyn oikeus muuttaa työtilan aiempaa alkuperäiseen käsittelijään rajattua linjausta. Ristiriitaiset suunnittelu- ja toteutusohjeet on päivitettävä hyväksytyllä päätöksellä ennen kehitystä.

## Non-Goals

- Ei valuuttamuunnosta, osapalautuksia tai muiden kuin EUR-palautusten hyväksyntää.
- Ei käyttöönottoa edeltävän palautushistorian tuontia eikä oman Entra ID -tunnisteiden myöntöpalvelun rakentamista MVP:ssä.

## Key Stakeholders / Roles

- Seppo Sutinen: käyttöönottoa edeltävän historian poisjätön ja hylättyjen palautusten mukaanlaskennan nimetty riskipäätösomistaja; käyttäjä ilmoitti hänen hyväksyneen molemmat riskit paikallisesti, henkilöllisyyttä ei ole todennettu.
- Muut liiketoiminta-, tieto- ja integraatio-omistajat: Unknown.

## Glossary

- **Palautus:** yksilöllisellä `refundId`-tunnisteella kirjattu EUR-määräinen jakamaton palautus.
- **Käsittelijä:** palautuksen lähettäjä; tilakyselyyn oikeutetaan myös muut käsittelijät.
- **Hyväksyjä:** eri luonnollinen henkilö, jolla on hyväksyjärooli.
- **Kertymä:** saman asiakkaan palveluun tallentuneiden palautusten 365 päivän summa, mukaan lukien odottavat ja hylätyt.

## Decision Thread

Päätökset ja ristiriidat ovat [päätöslokissa](decision-log.md). Vahvistettujen tietojen erittely ja lähtöarvio ovat [QG1-muistiossa](qg1-feature-readiness.md).

## Planning Status

- **Track:** bmad-method
- **Stories defined:** 0
- **Stories remaining:** Unknown, kunnes tarinat on laadittu.
- **Next:** täsmennä testiavaimen hallinta, roolikartoitus, tämän toimituksen tuotantovarmennus ja ilmoitetun henkilökohtaisen hyväksyjäroolin takuun näyttö sekä rinnakkaisten tapahtumien suojaus; nimeä tuotannon päätösomistaja ja ratkaise aiemmista käyttöoikeus- ja MVP-päätöksistä poikkeavat muutokset ennen toteutusta. PRD-vaiheen portti on erillinen, eikä paikallinen QG1-tarkennus avaa sitä.