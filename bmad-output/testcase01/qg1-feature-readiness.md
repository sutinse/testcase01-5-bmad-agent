# QG1: testcase01

Paikallinen arviointi, ei GitHub-portin hyväksyntä. Arvioitu vain [Rovo-snapshotin](input/rovo-feature.md) ja [QG1-rubriikin](../../docs/qg1/feature-readiness.md) perusteella sekä käyttäjän tässä arvioinnissa antamilla tarkennuksilla. Snapshotin lähde-URL:n ja poiminta-ajan oikeellisuutta ei ole varmennettu ulkoisesta järjestelmästä.

## Alkuperäisen kuvauksen kartoitus

| Artefakti | Tila ja näyttö snapshotista |
| --- | --- |
| Featuren kuvaus | Kuvattu: "Yli 10.000 euron vakuutusmaksupalautusten hyväksyjä ja palautuksen käsittelijän tulee olla eri henkilö". |
| Liiketoiminta-arvo | Osittainen: useat palautukset herättävät "huoli rahanpesusta"; konkreettinen vaikutus ei ole kuvattu. |
| Odotettu tulos | Osittainen: eri henkilö hyväksyy rajan ylittävän palautuksen; mittaria ei ole annettu. |
| Hyväksymiskriteerit | Osittaiset: eri henkilö ja luonnollinen henkilö mainitaan; kumulointi, valuutta, asiakasrajat ja osapalautukset kysytään auki. |
| Sidosryhmät | Ei löydy snapshotista; käyttäjän mukaan ei tiedossa. |
| Rajaus | Osittainen: palautuksen hyväksyntä; muut rajat avoimia snapshotissa. |
| Riippuvuudet | Osittaiset: kumulointi, valuutta ja asiakasrajat edellyttävät päätöksiä; teknisiä lähteitä tai tiloja ei luetella. |
| Liitedokumentit | Ei löydy snapshotista. |
| Prioriteetti ja ajoitus | Ei löydy snapshotista; käyttäjän mukaan ei tiedossa. Ei mukana pisteissä. |
| Estävät kysymykset | Avoimet säännöt kumuloinnista, valuutasta ja osapalautuksista mainitaan suoraan. |
| Tiimin saatavuus | Ei löydy snapshotista; ei mukana pisteissä. |
| Rajoitteet ja hallinto | Hyväksyjän on oltava luonnollinen henkilö, ei botti eikä ryhmä; muuta sääntely- tai hyväksyntäprosessia ei kuvata. |

Kartoitus vahvistettiin käyttäjän kanssa ennen pisteytystä. "Voidaan vaikka keksiä että ei sallita" ei ollut alkuperäisessä aineistossa päätös osapalautusten kiellosta.

## Lähtöaineiston rubriikki

Pisteet kuvaavat raakaa snapshotia **ennen** tarkennusvastauksia. Arvio ja riskihuomio vahvistettiin käyttäjän kanssa ennen kysymyksiä.

| Kriteeri | Arvio | Raakapisteet | Paino | Osuus | Lyhyt näyttö |
| --- | --- | ---: | ---: | ---: | --- |
| A1 Odotettu tulos | Partial | 1/2 | 15 % | 7,5 | Eri hyväksyjä mainitaan, mutta todennettava liiketoimintatulos jää ohueksi. |
| A2 Ongelma | Partial | 1/2 | 10 % | 5 | Kaksi 6 000 euron palautusta ja rahanpesuhuoli ovat esimerkki, vaikutus jää avoimeksi. |
| A3 Hyväksymiskriteerit | Partial | 1/2 | 20 % | 10 | Eri henkilö ja luonnollinen henkilö ovat testattavia aihioita, mutta laskenta ja rajatapaukset puuttuvat. |
| A4 Esiehdot | Partial | 1/2 | 5 % | 2,5 | "kun palautus on päätetty muodostaa" on esiehdon alku; datan saatavuutta ei kuvata. |
| B1 Rajaus | Partial | 1/2 | 15 % | 7,5 | Hyväksyntä kuvataan, mutta asiakas-, valuutta- ja osapalautusrajat ovat auki. |
| B2 Riippuvuudet | Partial | 1/2 | 20 % | 10 | Päätösriippuvuuksia kysytään, mutta omistajia ja tiloja ei luetella. |
| B3 Liitedokumentit | No | 0/2 | 5 % | 0 | Ei viittauksia tukidokumentteihin. |
| C2 Ei estäviä kysymyksiä | No | 0/2 | 15 % | 0 | Kumuloinnin ja valuutan päätökset voivat muuttaa perussääntöä. |

**Yhteensä 42,5/100: NOT_READY_MAJOR_GAPS.** C2:n avoimet peruspäätökset estävät vihreän arvion. Tämä on lähtöaineiston pistemäärä, ei uudelleenlaskettu tulos tarkennusten jälkeen.

## Riskit ja päätökset

| Riskihuomio | Näyttö lähtöaineistosta | Toimi |
| --- | --- | --- |
| HIGH: pienemmät erilliset palautukset voivat ohittaa yksittäisen rajan | "kaksi 6000 eur palautusta" | Vahvistettu 365 kalenteripäivän liukuva kumulointi; päätettävä historialähde ja laskennan tarkka ajankohta. |
| HIGH: soveltamisala ja summa voivat tulkintautua eri tavoin | "Lisäksi valuutan huomiointi" ja kysymys henkilö-/yritysasiakkaista | Vahvistettu vain EUR ja sama sääntö molemmille asiakasryhmille. |
| MEDIUM: osapalautukset ja hyväksyjän ihmisyys voivat jäädä valvomatta | Kysymys osapalautuksesta sekä kielto botille/ryhmälle | Vahvistettu osapalautusten kielto ja vaatimus luonnollisesta henkilöstä; varmistettava, miten token osoittaa ihmisyyden. |

**Kokonaisriskihuomio: HIGH.** Riskihuomio ei ole lakisääteinen tai numeerinen riskiluokitus.

Käyttäjän vahvistamat tarkennukset (eivät alkuperäisen Rovo-tekstin päätöksiä):

1. Yksi palautus on yksi jakamaton, kokonainen maksu; hyväksyntä tarkistetaan ennen maksatusta. Laskentaikkuna koskee saman asiakkaan palautuksia.
2. Saman asiakkaan palautukset lasketaan liukuvalla 365 kalenteripäivän ikkunalla. Hyväksyntäraja on **yli** 10 000 euroa, ei tasan 10 000 euroa.
3. Vain EUR hyväksytään; muut valuutat hylätään ilman muunnosta.
4. Sama sääntö koskee henkilö- ja yritysasiakkaita.
5. Rajan ylittävän palautuksen hyväksyjän on oltava eri luonnollinen henkilö kuin juuri sen palautuksen käsittelijä; botti tai ryhmä ei kelpaa.
6. Osapalautusta ja loppusumman muuta allokointia ei sallita tämän toiminnon piirissä.
7. Todennettava tavoite: jokainen rajan ylittävä palautus vaatii toisen luonnollisen henkilön hyväksynnän.
8. Käyttäjätunnus ja käyttäjäryhmä tulevat saapuvasta JWT:stä. Asiakas- ja palautustietojen lähde, historiallisen ikkunan saatavuus, hyväksyjän ihmisyyden todennus, päätösomistajat ja tukidokumentit ovat **Unknown**.
9. Valuuttamuunnos, osapalautukset ja muiden kuin EUR-palautusten hyväksyntä ovat tämän ominaisuuden ulkopuolella.

Vastausten kooste vahvistettiin käyttäjän kanssa. Raakatekstiä ei muokattu vastaamaan jälkikäteen tehtyjä päätöksiä.

## Uusi tarkennus: erilliset toiminnot ja tilat

Käyttäjän myöhemmin vahvistamat lisäpäätökset (eivät alkuperäisen Rovo-snapshotin sisältöä):

1. Käsittelijä lähettää palautuksen hyväksyttävyyskyselyn ilman hyväksyjää lähetyspyynnössä. Päätös perustuu saman asiakkaan palautusten 365 kalenteripäivän kumulatiiviseen summaan, ei pelkän uuden palautuksen summaan.
2. Jos summa on enintään 10 000 EUR, lähetys antaa heti `ALLOWED`. Jos summa ylittää 10 000 EUR, palautus tallentuu `PENDING`-tilaan odottamaan erillistä hyväksyjän päätöstä. Odottavat palautukset lasketaan mukaan seuraavan palautuksen kumulatiiviseen summaan.
3. Eri luonnollinen henkilö kuin kyseisen palautuksen käsittelijä voi hyväksyä odottavan palautuksen (`ALLOWED`) tai hylätä sen (`BLOCKED`). `BLOCKED` on lopullinen tila; päätöksen on erotuttava lähetyksestä.
4. Käsittelijöille tarvitaan erillinen palautuksen tilakysely, joka näyttää myös odottavan ja hylätyn tilan. Käyttäjän uusi valinta sallii kyselyn kenelle tahansa oikeutetulle käsittelijälle; tämä poikkeaa työtilan aiemmasta alkuperäiseen käsittelijään rajatusta linjauksesta ja edellyttää päätöksen päivittämistä ennen toteutusta.
5. `BLOCKED`-tilaan hylätty palautus jää mukaan myöhempien palautusten 365 päivän kumulatiiviseen summaan. Tämä voi vaatia hyväksynnän myös silloin, kun aiempi palautus ei johtanut maksatukseen; käyttäjän mukaan päätösomistaja hyväksyi vaikutuksen paikallisesti.
6. Sama `refundId` ei muodosta uutta palautusta eikä toista päätöstä uusintapyynnöllä, eikä summa kasva kahteen kertaan. Saman sisältöisen lähetyksen uusinnan vastaus on nykyinen tila.
7. Ikkuna rajataan UTC-aikaleimalla: lähetyshetkestä tasan 365 vuorokautta taaksepäin oleva alaraja kuuluu mukaan (`checkedAt >= lähetyshetki - 365 vuorokautta`).
8. Jos jo tallennetun `refundId`-tunnisteen `customerId` tai `amount` poikkeaa alkuperäisestä, vastaus on 409 `application/problem+json` eikä tallennettua palautusta tai kertymää muuteta. EUR on ainoa sallittu valuutta.
9. Identtinen saman hyväksyjän päätöspyynnön uusinta palauttaa nykyisen lopullisen tilan muuttamatta päätöstä. Ensimmäinen tallennettu päätös ja sen hyväksyjä pysyvät voimassa; eri hyväksyjän päätösyritys, myös samansisältöinen, sekä vastakkainen päätös antavat 409 `application/problem+json`.

Vielä täsmennettävä: miten rinnakkaiset lähetykset ja päätökset suojataan teknisesti ja mitä JWT-väitteitä sekä roolikartoitusta käytetään. Lähtöaineiston 42,5/100-pisteitä ei ole laskettu uudelleen tämän lisäyksen perusteella.

### Paikallisen jatkovaiheen päätökset

- Saman asiakkaan yhtä aikaa saapuvat palautukset käsitellään atomisesti yksi kerrallaan tallennusjärjestyksessä. Ensin tallennettu vaikuttaa seuraavan kertymään; saapumisaika ei anna etusijaa. Näin vain järjestyksessä kynnyksen ylittävä palautus siirtyy `PENDING`-tilaan. Tekninen transaktio- ja kilpailutilanteiden suojaus jää suunniteltavaksi.
- Samanaikaisissa päätöspyynnöissä ensimmäinen tallennettu päätös ja sen hyväksyjä jäävät voimaan. Toisen hyväksyjän yritys antaa 409 `application/problem+json`, vaikka päätös olisi sama; vain alkuperäisen hyväksyjän identtinen uusinta palauttaa nykytilan. Tekninen suojaus jää suunniteltavaksi.
- Kuka tahansa oikeutettu käsittelijä saa kysyä minkä tahansa palautuksen tilaa. Tämä korvaa aiemman vain alkuperäiseen käsittelijään rajatun suunnittelupäätöksen; ristiriitaiset toteutusohjeet on päivitettävä ennen toteutusta.
- Uusi palvelu luo oman SQLite-tietokantansa. Kertymään otetaan vain tämän palvelun kautta syntyneet palautukset; ennen käyttöönottoa tehtyä historiaa ei tuoda. Käyttöönoton alussa 365 päivän todellinen kertymä voi siksi alittua laskennassa; käyttäjä ilmoitti päätösomistajan hyväksyneen tämän riskin paikallisesti.
- Paikallisessa MVP:ssä testiluokka tuottaa Entra ID -mallisen JWT:n myös ajonaikaisiin pyyntöihin. Palvelu validoi sen allekirjoituksen konfiguroidulla julkisella testiavaimella sekä myöntäjän, yleisön ja voimassaolon; arvot annetaan ympäristömuuttujina. Paikallinen validointi ei käytä Entra JWKS:ää eikä testiavainta saa käyttää tuotantoympäristön luottamuslähteenä. Asiakkaan IAM määrittää käyttäjien rooleja, mutta tuotantotokenin myöntäjä ja luotettu varmennuslähde ovat vielä avoimia. Hyväksyminen ja hylkääminen edellyttävät delegoitua käyttäjätokenia ja hyväksyjäroolia; sovellustunnuksen token, ryhmä ja puuttuva käyttäjätieto eivät kelpaa luonnolliseksi henkilöksi. Väitteiden nimet ja roolikartoitus ovat vielä avoimia.
- Kun sama `refundId` lähetetään uudelleen samalla `customerId`- ja `amount`-arvolla, nykyinen tila palautetaan ilman uutta laskentaa tai päätöstä. Eri käsittelijä saa uusia pyynnön, kun hänen `processorId`-arvonsa täsmää oman validoidun JWT:n `sub`-arvoon; tallennettu alkuperäinen käsittelijä ei vaihdu. Eri asiakas tai summa samalla tunnisteella antaa 409 ilman muutosta. Identtinen saman hyväksyjän päätösuusinta palauttaa nykytilan; vastakkainen päätös antaa 409.
- Paikallisen suljetun MVP:n testitokenissa hyväksyjän `sub` ja hyväksyjärooli sallivat hyväksynnän vain simulaationa. Ne eivät todista hyväksyjää luonnolliseksi henkilöksi, joten alkuperäinen ihmisyysvaatimus ei vielä täyty tuotantokelpoisesti; hyväksyntä on estettävä paikallisen testiympäristön ulkopuolella, kunnes luotettava näyttö ja tuotantovarmennus on päätetty.
- Käyttäjä rajasi tuotantohyväksynnän tähän toimitukseen. Aiempi kirjaus IAM-käyttäjähallinnasta tuotantotokenin myöntäjänä täsmentyi: IAM on asiakkaan Identity Management, jossa määritellään käyttäjien roolit, eikä käyttäjä yksilöinyt tuotantotokenin myöntäjää. Aiempi paikallinen hyväksyntä koski näin epäselvää lähdevalintaa eikä osoita teknistä tai muodollista tuotantohyväksyntää. Tokenin identiteetti ja rooli eivät yksin todista luonnollista henkilöä. Hyväksynnän käyttö tuotannossa pysyy estettynä, kunnes varmennus ja ihmisyyskontrolli on ratkaistu; aiempi Entra JWKS:n siirto myöhempään vaiheeseen on sovitettava tämän toimituksen tuotantotavoitteeseen.
- Käyttäjän ilmoituksen mukaan hyväksyjärooli myönnetään Entra ID:ssä vain luonnolliselle henkilölle, ei palvelulle. Roolin myöntökontrollin dokumenttia, valvontaa ja vastuullista omistajaa ei nimetty eikä väitettä ole voitu todentaa; myöskään tuotantotokenin `iss`-arvoa tai julkisten allekirjoitusavainten lähdettä ei toimitettu. Roolin hallinta ei yksin vahvista tokenin myöntäjää. Tuotantohyväksynnän esto säilyy, kunnes tokenin alkuperä ja roolin myöntökontrolli on tarkistettu ennen käyttöönottoa.
- Käyttäjä valitsi paikallisen jatkosuunnittelun poluksi BMad Methodin (PRD ja arkkitehtuuri). Käyttäjä nimesi Seppo Sutisen käyttöönottoa edeltävän historian poisjätön ja hylättyjen palautusten mukaanlaskennan riskien päätösomistajaksi.
- Käyttäjän ilmoituksen mukaan Seppo Sutinen hyväksyy paikallisena liiketoimintapäätöksenä molemmat nimetyt laskentariskit: laskenta alkaa ilman vanhaa historiaa, ja lopullisesti hylätyt palautukset kasvattavat kertymää. Tämä ei todenna päätösomistajan henkilöllisyyttä eikä ole muodollinen vaihehyväksyntä.
- Käyttäjä valitsi JWT:n allekirjoituksen, myöntäjän, yleisön ja voimassaolon validoinnin palvelun vastuulle. Hän tarkensi, että paikallisen MVP:n ajossa käytetään testiluokan luomaa tokenia, ympäristömuuttujilla määriteltyjä hyväksyttyjä arvoja ja konfiguroitua testiavaimen julkista vastinetta. Aiempi valinta käyttää Entra JWKS -rajapintaa ei koske paikallista MVP:tä; tuotannon varmennustapa on päätettävä tämän toimituksen aikana. Palvelun oma validointi poikkeaa työtilan oletuksesta valmiiksi validoidusta JWT:stä; lukittu päätös on päivitettävä ennen toteutusta.

Nämä ovat käyttäjän vahvistamia uusia rajauksia; ne eivät muuta alkuperäisen Rovo-tekstin 42,5/100-lähtöpisteytystä.

## Seuraavat toimet

- Suunnittele UTC-aikaleimaan perustuvan 365 vuorokauden ikkunan atominen tallennusjärjestys ja kilpailutilanteiden suojaus rinnakkaisissa lähetyksissä; säilytä käyttäjän ilmoittama riskikanta ja sen vaikutukset näkyvissä myöhemmässä suunnittelussa (B2, C2).
- Täsmennä ympäristömuuttujien nimet ja arvonhankinta, testiavainparin hallinta ja roolikartoitus. Yksilöi IAM:n ja Entra ID:n välinen roolien hallintaketju, henkilökohtaisen hyväksyjäroolin myöntökontrollin dokumentti ja omistaja. Nimeä erikseen tuotantotokenin todellinen myöntäjä, `iss`-arvo, julkisten allekirjoitusavainten lähde ja hyväksytyt väitteet; varmista, miten palvelu hyväksyy vain henkilökohtaiset käyttäjätokenit. `sub` ja rooli eivät yksin riitä ihmisyyden todentamiseen. Sovita aiemmin myöhemmäksi siirretty Entra-varmennus tämän toimituksen tuotantotavoitteeseen ja pidä hyväksyntä estettynä ratkaisuun asti (A3, B2).
- Päivitä alkuperäisen käsittelijän tilakyselyyn rajaava suunnittelupäätös sekä sitä koskevat toteutusohjeet vastaamaan kaikkien oikeutettujen käsittelijöiden näkyvyyttä. Varmista, että idempotentin lähetyksen uusi käsittelijä ei korvaa tallennettua käsittelijää ja että ensimmäinen päätöksentekijä säilyy samanaikaisissa yrityksissä (A3, B2).
- Nimeä tukidokumentit, sidosryhmät ja riippuvuuksien päätösomistajat; varmista Rovo-URL:n ja poiminta-ajan alkuperä. Päivitä PRD:n lähtötiedot vasta näiden perusteella (B2, B3).
- Kirjoita kolme toimintoa ja tilasiirtymät testattaviksi hyväksymiskriteereiksi: tasan 10 000 euroa, kaksi peräkkäistä palautusta, `PENDING`-tilan kysely, hyväksyntä/hylkäys, uudelleen lähetetty `refundId` ja hylätyn vaikutus myöhempään summaan (A3, C2).