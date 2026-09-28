# QG1: testcase01

Paikallinen arviointi, ei GitHub-portin hyväksyntä. Arvioitu vain [Rovo-snapshotin](input/rovo-feature.md) ja [QG1-rubriikin](../../docs/qg1/feature-readiness.md) perusteella sekä käyttäjän tässä arvioinnissa antamilla tarkennuksilla. Käyttäjä vahvisti snapshotin lähde-URL:n ja poiminta-ajan oikeiksi; niitä ei ole varmennettu ulkoisesta järjestelmästä.

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

## Tarkennetun paikallisen MVP:n QG1-uudelleenarviointi (2026-09-28)

Tämä arvio perustuu yllä olevaan [Rovo-snapshotiin](input/rovo-feature.md), tämän muistion käyttäjän vahvistamiin tarkennuksiin ja [projektikontekstiin](project-context.md). Käyttäjä vahvisti uuden kartoituksen, pistetulkinnan ja riskihuomion erikseen. Alkuperäinen 42,5/100 arvio koskee vain muuttamatonta lähtöaineistoa; tätä arviota ei tule käyttää tuotantovalmiuden tai GitHub-vaiheportin hyväksyntänä.

| Artefakti | Tarkennettu kartoitus ja lähde |
| --- | --- |
| Toiminto ja odotettu tulos | Käsittelijän lähetys, erillinen päätös ja tilakysely; vain paikallisen MVP:n sääntöjen ja rajauksen osoittaminen [käyttäjän vahvistamat tarkennukset, projektikonteksti]. Tuotannon todellinen henkilötodennus ei sisälly toimitukseen. |
| Ongelma ja hyöty | Kaksi erillistä 6 000 euron palautusta voi ohittaa yksittäisen palautuksen rajan ja herättää rahanpesuhuolen [Rovo-snapshot]. Vaikutusta todelliseen maksatukseen ei mitata tässä paikallisessa toimituksessa. |
| Hyväksymiskriteerit ja rajaus | Yli 10 000 EUR saman asiakkaan 365 vuorokauden kertymässä johtaa `PENDING`-tilaan; kolme erillistä toimintoa, päättävät tilat, uusinnat, roolit, EUR-raja ja paikallinen testiympäristö ovat kirjattuja [käyttäjän tarkennukset, projektikonteksti]. Luonnollisen henkilön todennus on myöhemmän toimituksen asia. |
| Esiehdot ja riippuvuudet | SQLite tallentaa vain tämän palvelun kautta syntyvät palautukset; vanhaa historiaa ei tuoda [käyttäjän tarkennukset]. Paikallisen tokenin roolikartoituksen, testiavainparin hallinnan ja atomisen tallennuksen ratkaisut odottavat suunnittelua [projektikonteksti]. Muita lähteitä tai omistajia ei tunneta. |
| Tukidokumentit ja esteet | Rovo-snapshot, paikallinen QG1-muistio, päätösloki ja projektikonteksti löytyvät tästä työtilasta; riippumattomat politiikka- ja datalähteet ovat Unknown. Lukittujen käyttöoikeuspäätösten ristiriita vaatii hyväksytyn suunnitteluratkaisun ennen kehitystä, ei ennen paikallisen MVP:n jatkojalostusta [projektikonteksti]. |

| Kriteeri | Arvio | Pisteet | Paino | Osuus | Perustelu |
| --- | --- | ---: | ---: | ---: | --- |
| A1 Odotettu tulos | Partial | 1/2 | 15 % | 7,5 | Paikalliset testit ja demo ovat todennettavia, mutta liiketoimintavaikutus jää erilleen simulaatiosta. |
| A2 Ongelma | Partial | 1/2 | 10 % | 5 | Kahden 6 000 EUR palautuksen ohitusriski tunnetaan, mutta vaikutus ja vaikutuksen kohteet jäävät ohuiksi. |
| A3 Hyväksymiskriteerit | Yes | 2/2 | 20 % | 20 | Raja, UTC-ikkuna, tilat, uusinnat ja oikeudet kattavat olennaiset paikalliset virta- ja rajatapaukset. |
| A4 Esiehdot | Partial | 1/2 | 5 % | 2,5 | Oma SQLite ja historian poisjättö tunnetaan; paikallisen testidatan ja käyttörajauksen tarkennus saatiin vasta pisteytyksen jälkeen. |
| B1 Rajaus | Yes | 2/2 | 15 % | 15 | Paikallinen simulaatio ja tuotantohyväksynnän poisrajaus ovat eksplisiittisiä. |
| B2 Riippuvuudet | Partial | 1/2 | 20 % | 10 | Testitoken, tallennus ja päätösristiriidat on nimetty, mutta toteutustapa ja usean riippuvuuden omistajuus ovat avoinna. |
| B3 Liitedokumentit | Partial | 1/2 | 5 % | 2,5 | Paikalliset päätös- ja lähtödokumentit ovat löydettävissä; riippumattomia tukilähteitä ei tunneta. |
| C2 Ei estäviä kysymyksiä | Yes | 2/2 | 15 % | 15 | Tuotannon identiteettikontrollit on siirretty myöhemmäksi; avoimet tekniset ratkaisut kuuluvat paikallisen MVP:n suunnitteluun ennen kehitystä. |

**Yhteensä 77,5/100: NEEDS_MINOR_CLARIFICATION.** Pisteytys koskee käyttäjän vahvistamaa kartoitusta ennen alla olevia viimeisiä täsmennyksiä; niitä ei laskettu takautuvasti uuteen numeroon. Jatkojalostus on mahdollinen, mutta tämä ei ole tuotanto- eikä vaihehyväksyntä.

**Kokonaisriskihuomio: HIGH.** Historiatiedon poisjättö voi aliarvioida todellisen 365 päivän kertymän (A4, B2); hylättyjen palautusten mukaanlaskenta voi nostaa kertymää ilman maksua (A3, B2); testitokenin hyväksyntä paikallisen testiprofiilin ulkopuolella rikkoisi tuotantorajauksen (A3, B1, B2). Käyttäjä ilmoitti Seppo Sutisen hyväksyneen kaksi laskentariskiä paikallisesti; tämä ei ole varmennettu muodollinen hyväksyntä. Pidä simulaatio estettynä muiden profiilien käytössä.

Pisteytyksen jälkeiset käyttäjän vahvistamat vastaukset: testin asiakas- ja palautustiedot syntyvät vain tämän palvelun testipyynnöistä; simulaatio voidaan käynnistää vain eksplisiittisessä paikallisessa testiprofiilissa ja hyväksyntä estetään muissa profiileissa; paikallisen MVP:n onnistuminen osoitetaan sääntöjen ja rajauksen automaattisilla testeillä sekä Seppo Sutisen manuaalisesti hyväksymällä demolla. Demon hyväksyntää ei ole vielä saatu. Näiden ratkaisujen tekninen toteutus täsmentyy arkkitehtuurissa.

**Välittömät toimet:** Kuvaa PRD:ssä paikallisen testiprofiilin fail-closed-raja ja kolmen toiminnon testi- ja demokriteerit (A3, B1, B2). Päätä arkkitehtuurissa roolikartoitus, avainhallinta ja transaktioraja; korjaa ristiriitaiset lukitut käyttöoikeusohjeet hyväksytyllä päätöksellä ennen kehitystä (A4, B2). Pidä muut tukidokumentit ja päätösomistajat Unknown-tilassa, kunnes näyttöä on saatavilla (B3). Tuotannon ihmisyystodennus ja Entra-varmennus pysyvät myöhemmän toimituksen kysymyksinä (B1, C2).

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
- Käyttäjän uuden tarkennuksen mukaan tuotanto- ja testiympäristöjen `TENANT_ID` ja `APP_ID` tulevat ympäristöparametreista; ehdotettu julkisten avainten osoite rakennetaan muodossa `https://login.microsoftonline.com/{TENANT_ID}/discovery/keys?appid={APP_ID}`. Käyttäjä ilmoitti myös, että `iss` ja `aud` annetaan ympäristöparametreissa, mutta niiden arvoja tai varmennettavaa konfiguraatiota ei toimitettu. Osoitteen vastaavuutta käytettyyn tokeniin ei ole tarkistettu; paikallisen MVP:n testiavaimen rajaus säilyy.
- Käyttäjän vahvistaman toimintatavan mukaan asiakkaan IAM liittää hyväksymiseen oikeuttavan ryhmäoikeuden vain oikealle henkilölle. Tämä on hyväksytty suunnittelun liiketoimintaoletukseksi, ei todennetuksi tokenin ihmisyysväitteeksi: ryhmäoikeuden välittyminen hyväksyttyyn käyttäjätokeniin, sovellustokenien poissulku ja tuotantokonfiguraation varmennus on määriteltävä ennen tuotantohyväksyntää.
- Käyttäjä nimesi nyt Azure Entra ID:n tuotantotokenin myöntäjäksi ja ilmoitti, ettei sen käyttöä tarvitse hänen mielestään varmistaa erikseen. Tämä täsmentää myöntäjän suunnitteluoletusta mutta ei todenna juuri tämän palvelun hyväksymän tokenin `iss`- ja `aud`-arvoja, allekirjoitusavainta tai käyttäjä- ja sovellustokenien erottelua; palvelun tuotantovarmennus pysyy avoimena.
- Käyttäjä toisti, että IAM lisää hyväksynnän oikeuttavan ryhmäoikeuden vain luonnolliselle henkilölle. Kontrollin dokumenttia, omistajaa, valvontaa tai tokenin väitteiden ja roolin kartoitusta ei toimitettu; ilmoitusta ei tulkita tuotannon ihmisyysvaatimuksen tekniseksi näytöksi.
- Käyttäjä muutti toimituksen rajausta ja vahvisti vaikutuksen: tämä toimitus on vain paikallinen suljettu MVP, jossa hyväksyntä simuloidaan testitokenilla. Tuotantohyväksyntä, Entra ID -tokenin varmennus ja luonnollisen henkilön todennettava hyväksyntä siirtyvät erilliseen myöhempään toimitukseen. Paikallista simulaatiota ei saa käyttää tuotannossa eikä esittää alkuperäisen ihmisyysvaatimuksen tuotantokelpoisena toteutuksena. Aiempi tämän toimituksen tuotantotavoite ei enää ole voimassa; muita QG1:n liiketoimintasääntöjä ei muuteta.
- Käyttäjä valitsi paikallisen MVP:n hyväksymistavaksi automaattiset testit ja niiden lisäksi manuaalisen demon hyväksynnän. Hän nimesi demon hyväksyjäksi Seppo Sutisen. Demon hyväksyntää tai hyväksyjän henkilöllisyyttä ei ole vielä todennettu. Muita tämän MVP:n lähdedokumentteja tai päätösomistajia ei käyttäjän mukaan ole tiedossa; niiden tila on Unknown.

Nämä ovat käyttäjän vahvistamia uusia rajauksia; ne eivät muuta alkuperäisen Rovo-tekstin 42,5/100-lähtöpisteytystä.

## Seuraavat toimet

- Suunnittele UTC-aikaleimaan perustuvan 365 vuorokauden ikkunan atominen tallennusjärjestys ja kilpailutilanteiden suojaus rinnakkaisissa lähetyksissä; säilytä käyttäjän ilmoittama riskikanta ja sen vaikutukset näkyvissä myöhemmässä suunnittelussa (B2, C2).
- Täsmennä paikallisen MVP:n ympäristömuuttujien nimet ja arvonhankinta, testiavainparin hallinta ja roolikartoitus. Rajaa testiavaimen käyttö suljettuun paikalliseen ympäristöön. Myöhemmän tuotantotoimituksen lähtötiedoiksi tarvitaan IAM:n ja ilmoitetun Entra ID -myöntäjän roolien hallintaketju, henkilökohtaisen hyväksyjäoikeuden myöntökontrollin dokumentti ja omistaja, tuotantotokenin varmennetut `iss`- ja `aud`-arvot sekä allekirjoitusavainten lähde ja hyväksytyt väitteet. `sub` ja rooli eivät yksin riitä ihmisyyden todentamiseen; pidä hyväksyntä estettynä paikallisen simulaation ulkopuolella (A3, B2).
- Päivitä alkuperäisen käsittelijän tilakyselyyn rajaava suunnittelupäätös sekä sitä koskevat toteutusohjeet vastaamaan kaikkien oikeutettujen käsittelijöiden näkyvyyttä. Varmista, että idempotentin lähetyksen uusi käsittelijä ei korvaa tallennettua käsittelijää ja että ensimmäinen päätöksentekijä säilyy samanaikaisissa yrityksissä (A3, B2).
- Merkitse muut tukidokumentit, sidosryhmät ja riippuvuuksien päätösomistajat Unknown-tilaan, kunnes ne voidaan yksilöidä; käyttäjän mukaan muita ei nyt ole tiedossa. Rovo-URL ja poiminta-aika ovat käyttäjän vahvistamia, mutta niitä ei ole tarkistettu ulkoisesta lähteestä. Älä esitä puuttuvia lähteitä varmennettuina PRD:ssä (B2, B3).
- Kirjoita kolme toimintoa ja tilasiirtymät testattaviksi hyväksymiskriteereiksi: tasan 10 000 euroa, kaksi peräkkäistä palautusta, `PENDING`-tilan kysely, hyväksyntä/hylkäys, uudelleen lähetetty `refundId` ja hylätyn vaikutus myöhempään summaan (A3, C2).
- Näytä automaattisissa testeissä myös roolirajat ja hyväksynnän esto paikallisen testin ulkopuolella. Esitä paikallisen MVP:n kolme toimintoa manuaalisessa demossa Seppo Sutiselle ja tallenna erillinen hyväksyntänäyttö ennen kuin demo merkitään hyväksytyksi; tämä ei korvaa GitHubin vaiheportin riippumatonta hyväksyntää (A1, A3, B2).