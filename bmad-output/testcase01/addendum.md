# PRD Addendum - testcase01

**Companion to:** [PRD](prd.md)
**Version:** 0.1
**Date:** 2026-09-28
**Status:** PRD:n tukimuistio; ei itsessään arkkitehtuurin hyväksyntäasiakirja (arkkitehtuuri hyväksytty PR #5:ssä)

Tämä muistio ei laajenna PRD:n paikallista MVP-laajuutta. Avoimet toteutus- ja hallintakysymykset eivät ole ratkaistuja vaatimuksia tai tuotantokäytön hyväksyntää.

## Open Questions

| # | Question | Owner | Needed By | Status |
| --- | --- | --- | --- | --- |
| Q1 | Miten testiavaimen hallinta, roolikartoitus, hyväksytty `iss` ja `aud` sekä eksplisiittinen paikallinen testiprofiili toteutetaan siten, ettei testiavaimella hyväksytä muissa profiileissa? | Unknown | Arkkitehtuuri ja hyväksytty ADR ennen kehitystä | Ratkaistu suunnittelussa: ADR-0016 ja PR #7; `exp`-pakko ja roolikartoitus varmennetaan toteutuksen integraatiotesteissä. |
| Q2 | Miten saman asiakkaan lähetykset ja saman palautuksen päätökset järjestetään atomisesti tallennusjärjestykseen paikallisessa tietokannassa? | Unknown | Arkkitehtuuri ennen kehitystä | Ratkaistu suunnittelussa: ADR-0015:n yksi kirjoittaja ja varhainen kirjoituslukko. |
| Q3 | Mikä hyväksytty ADR korvaa vanhan alkuperäiseen käsittelijään rajatun tilakyselyn ja valmiiksi validoidun JWT:n oletuksen? | Unknown | Arkkitehtuurin hyväksyntä ennen kehitystä | ADR-0016/0020 hyväksyttiin PR #5:ssä, ja repo-ohjeet sovitettiin niihin hyväksytyssä PR #7:ssä. |
| Q4 | Mitkä muut liiketoiminta- tai tietoomistajat ja tukidokumentit tulee huomioida? | Käyttäjä | Ennen suunnittelupaketin hyväksyntää | Käyttäjän vastaus 2026-09-28: ei muita. Puuttuvien lähteiden paikallinen korvaus hyväksyttiin PR #7:ssä; suunnittelupaketti odottaa omaa hyväksyntäänsä. |
| Q5 | Missä ja milloin Seppo Sutisen paikallisen demon arviointi kirjataan? | Seppo Sutinen (käyttäjän ilmoitus) | MVP:n valmistumisen yhteydessä | Ei arvioitu |

Käyttäjän 2026-09-28 tarkennuksen mukaan `.github/copilot-instructions.md` oli ainoa saatavilla oleva lukittuja ratkaisuja kuvaava tiedosto. Sen aiemmin viittaamat `CONTEXT.md`, ADR:t ja refund-spec eivät ole saatavilla. PR #7 hyväksyi PRD:n, projektikontekstin, arkkitehtuurin ja sovitetut repo-ohjeet paikallisen MVP:n lähteiksi; se ei hyväksynyt suunnittelupakettia eikä tuotantokäyttöä.

Paikallisen demon jälkeen kehittäjä poistaa SQLite-tietokannan. Poiston ajankohta, vastuullinen suorittaja ja todennus tulee määrittää demon hyväksymisen yhteydessä. PostgreSQL:n käyttö kuuluu erilliseen myöhempään toimitukseen, eikä muuta tämän MVP:n SQLite-ratkaisua.

## Deferred Requirements

- **Tuotannon luonnollinen hyväksyjä:** Luotettavasti todennettu käsittelijästä eri luonnollinen henkilö hyväksyy rajanylityksen. Erillinen toimitus; paikallinen testitoken ei osoita ihmisyyttä.
- **Tuotannon Entra- ja IAM-varmennus:** Myöntäjän, yleisön, avainlähteen, käyttäjätokenin ja myöntöoikeuden kontrollien todentaminen. Erillinen toimitus; käyttäjän ilmoittamia lähteitä ei ole varmennettu.
- **Aiemman historian huomiointi:** Paikallinen MVP ei tuo käyttöönottoa edeltäviä palautuksia. Tuotannon historiallisen kertymän tarve ja lähde vaativat uuden päätöksen.
- **Konfiguroitava kynnys:** Kiinteä 10 000 EUR riittää tähän toimitukseen; mahdollinen myöhempi muutos vaatii uuden vaatimuksen.

## Supporting References

- [Projektikonteksti](project-context.md): käyttäjän vahvistamat paikallisen testin rajat ja avoimet omistajat.
- [QG1-uudelleenarviointi](qg1-feature-readiness.md): alkuperäinen lähtöarvio 42,5/100 ja erillinen paikallisen MVP:n arvio 77,5/100 (`NEEDS_MINOR_CLARIFICATION`, HIGH risk). Pisteet eivät ole vaihehyväksyntä.
- [Päätösloki](decision-log.md): PR #5:n arkkitehtuuripäätökset sovitettiin repo-ohjeisiin hyväksytyssä PR #7:ssä; suunnittelupaketin hyväksyntä on erillinen.
- [Rovo-snapshot](input/rovo-feature.md): käyttäjän vahvistama lähde-URL ja poiminta-aika; ulkoista varmennusta ei ole tehty.