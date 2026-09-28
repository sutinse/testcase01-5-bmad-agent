# PRD Addendum - testcase01

**Companion to:** [PRD](prd.md)
**Version:** 0.1
**Date:** 2026-09-28
**Status:** Luonnoksen tukimuistio; ei hyväksytty arkkitehtuuri

Tämä muistio ei laajenna PRD:n paikallista MVP-laajuutta. Avoimet toteutus- ja hallintakysymykset eivät ole ratkaistuja vaatimuksia tai tuotantokäytön hyväksyntää.

## Open Questions

| # | Question | Owner | Needed By | Status |
| --- | --- | --- | --- | --- |
| Q1 | Miten testiavaimen hallinta, roolikartoitus, hyväksytty `iss` ja `aud` sekä eksplisiittinen paikallinen testiprofiili toteutetaan siten, ettei testiavaimella hyväksytä muissa profiileissa? | Unknown | Arkkitehtuuri ja hyväksytty ADR ennen kehitystä | Avoin |
| Q2 | Miten saman asiakkaan lähetykset ja saman palautuksen päätökset järjestetään atomisesti tallennusjärjestykseen paikallisessa tietokannassa? | Unknown | Arkkitehtuuri ennen kehitystä | Avoin |
| Q3 | Mikä hyväksytty ADR korvaa vanhan alkuperäiseen käsittelijään rajatun tilakyselyn ja valmiiksi validoidun JWT:n oletuksen? | Unknown | Arkkitehtuurin hyväksyntä ennen kehitystä | Avoin |
| Q4 | Mitkä muut liiketoiminta- tai tietoomistajat ja tukidokumentit tulee huomioida? | Unknown | Ennen suunnittelupaketin hyväksyntää | Unknown |
| Q5 | Missä ja milloin Seppo Sutisen paikallisen demon arviointi kirjataan? | Seppo Sutinen (käyttäjän ilmoitus) | MVP:n valmistumisen yhteydessä | Ei arvioitu |

## Deferred Requirements

- **Tuotannon luonnollinen hyväksyjä:** Luotettavasti todennettu käsittelijästä eri luonnollinen henkilö hyväksyy rajanylityksen. Erillinen toimitus; paikallinen testitoken ei osoita ihmisyyttä.
- **Tuotannon Entra- ja IAM-varmennus:** Myöntäjän, yleisön, avainlähteen, käyttäjätokenin ja myöntöoikeuden kontrollien todentaminen. Erillinen toimitus; käyttäjän ilmoittamia lähteitä ei ole varmennettu.
- **Aiemman historian huomiointi:** Paikallinen MVP ei tuo käyttöönottoa edeltäviä palautuksia. Tuotannon historiallisen kertymän tarve ja lähde vaativat uuden päätöksen.
- **Konfiguroitava kynnys:** Kiinteä 10 000 EUR riittää tähän toimitukseen; mahdollinen myöhempi muutos vaatii uuden vaatimuksen.

## Supporting References

- [Projektikonteksti](project-context.md): käyttäjän vahvistamat paikallisen testin rajat ja avoimet omistajat.
- [QG1-uudelleenarviointi](qg1-feature-readiness.md): alkuperäinen lähtöarvio 42,5/100 ja erillinen paikallisen MVP:n arvio 77,5/100 (`NEEDS_MINOR_CLARIFICATION`, HIGH risk). Pisteet eivät ole vaihehyväksyntä.
- [Päätösloki](decision-log.md): uusin päätös syrjäyttää ristiriitaisen vanhan tulkinnan, mutta lukitun ohjeen muutos edellyttää hyväksyttyä arkkitehtuuripäätöstä.
- [Rovo-snapshot](input/rovo-feature.md): käyttäjän vahvistama lähde-URL ja poiminta-aika; ulkoista varmennusta ei ole tehty.