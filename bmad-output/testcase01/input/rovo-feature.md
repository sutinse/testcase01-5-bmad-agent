**Lähde-URL:** https://lahitapiola.atlassian.net/feature/testcase01
**Poiminta-aika:** 2026-09-28T10:30:00Z

Yli 10.000 euron vakuutusmaksupalautusten hyväksyjä ja palautuksen käsittelijän tulee olla eri henkilö

tuossa oli vielä se aukko että miten palautus määritellään ja huomioidaanko kumulatiiviset palautukset. Eli kun palautus on päätetty muodostaa, hyväksyntäprosessi tulee käyttöön jos summa on yli 10.000 eur. Mutta mitä jos asiakkaalle tulee esim kaksi 6000 eur palautusta, voidaanko ne käsitellä erillisinä. Todennäköisesti mutta jos näitä tulee useampia niin herää huoli rahanpesusta. Lisäksi valuutan huomiointi. 
 
Lisäksi se onko tässä asiakaskohtaisia rajoja eli sovelletaanko tätä sekä henkilö- että yritysasiakkaisiin. 

se vielä mikä tuli mieleen että hyväksyjän on oltava luonnollinen henkilö, sitä ei voi siirtää AI:llet ai botille tai ryhmälle jos heillä on käyttöoikeuksia

tuli vielä mieleen osapalautusten käsittely, jos käsittelijä haluaa palauttaa vain osan ja osan allokoida vaikka regresseihin niin sallitaanko tämä. Voidaan vaikka keksiä että ei sallita.

---

**Katselmointihuomautus (2026-09-29):** Yllä oleva alkuperäinen Rovo-kuvaus on ennallaan. Tämä lähdesnapshot on mukana uudessa PRD-vaiheen katselmoinnissa; validoidun testitokenin ei-tyhjiä `sub`- ja `groups`-väitteitä koskeva NFR-001-tarkennus on myöhempi PRD-vaatimus, ei osa Rovo-lähdetekstiä.