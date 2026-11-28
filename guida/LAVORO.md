# Come lavoriamo — Sound System Diaries

Documento di passaggio per continuare il lavoro in una nuova chat. Aggiornato al 28 novembre 2026.

## 1. Il progetto
- **Sound System Diaries (SSD)**: pagina Instagram + sito https://soundsystemdiaries.it, il diario dei sound system italiani (roots, reggae, dub, culture).
- Gestito da **Shaka**. Contatti: Instagram SSD, email soundsystemdiaries@gmail.com.
- Il sito raccoglie le **schede dei sound** (foto, città, anno, storia, link social) e gli **eventi** (flyer, data, città, line-up).
- Dati utili dagli Insights: i reel portano la crescita; circa il 63% delle visualizzazioni arriva da chi non segue ancora la pagina.

## 2. Regole fisse
Vedi `CLAUDE.md` nella cartella principale. Le più importanti:
1. Mai pubblicare senza "pubblica".
2. "Diario", mai "archivio". Niente "VS".
3. Fatti veri, citazioni identiche, nomi completi.
4. I testi di Shaka non si riscrivono: solo refusi e punteggiatura.
5. Ogni contenuto con un concetto suo.

## 3. Il sito, tecnicamente
- `data/sounds.json` — `items`: `id, name, photo, city, region, founded, story, story_en, instagram, facebook, lat, lon` (+ facoltativi `photo_credit`, `photo_credit_url`, es. Nobada → Mina Maya).
- `data/events.json` — eventi con `title, date, time, city, venue, lineup, entry, flyer, lat, lon`.
- `data/home.json` — `recent` = tutti i sound con storia, ordinati dal più vecchio (anno di fondazione).
- `build/build.py` costruisce `dist/`; `build/template.html` è la pagina; `static/img` foto (WEBP), `static/og` anteprime social.
- Pannello: https://soundsystemdiaries.it/admin/ (Decap CMS). Moduli "Aggiungi sound/evento" → Netlify Forms.
- **Netlify** (site id d5f074bd-d1be-4862-b752-fc9d3906b986) pubblica da `main` del repo `siakashakasamake/soundsystemdiaries`.
- Commit con `git -c user.name=Claude -c user.email=noreply@anthropic.com commit ...`.

### Aggiungere una foto a un sound
PIL → WEBP qualità 82–88, larghezza max 1080, nome = primi 12 caratteri dello sha1 del file, in `static/img/`; campo `photo` = `/img/<nome>.webp`.
Poi rigenerare l'anteprima social con `guida/strumenti/og_gen5.js` (lista in `og_list5.json`: id, name, place, img) e copiare `dist/og/<id>.jpg` in `static/og/`.

### Aggiungere una storia
Solo con il testo mandato dal sound. Correggere solo refusi/punteggiatura, tradurre in `story_en`, aggiungere il sound in `home.json` → `recent` rispettando l'ordine per anno.

### Pubblicare
Ramo dedicato → build e controllo locale (`python3 -m http.server -d dist`) → al "pubblica": merge fast-forward su `main`, push, verifica con curl che il sito online abbia la modifica.

## 4. Come si fanno i video (metodo tecnico)
- Ogni video è una pagina HTML 1080×1920 con `window.DUR` (durata) e una funzione `render(t)` che disegna il fotogramma al tempo `t`.
- `guida/strumenti/rng2.js <cartella> <pagina.html> <cartella-frame> <da> <a>`: renderizza i frame a 30 fps (con 75 frame di "riscaldamento"). Fare blocchi di ~30–36 frame alla volta: Chromium si blocca sui render lunghi.
- `guida/strumenti/pvt.js <cartella> <pagina.html> <cartella-out> 0.5,3,7.2`: anteprime a tempi scelti.
- Prima di codificare controllare che non manchi nessun frame (sennò il video si blocca o si accorcia).
- Codifica: ffmpeg libx264 crf 19–23, audio aac 192k, `loudnorm I=-14`, `-movflags +faststart`. Restare sotto i 30 MB. Cancellare i frame dopo.
- Musica: il montaggio va sul battito. Per `stasera/a.wav` il battito è B = 0,894 s (offset 1,574 + k·B). Lo script `esempio-prep-audio-e-dati.py` mostra come si taglia la tune, si aggiungono effetti e si calcola il livello (LV) per far "pompare" gli elementi.
- Mappa satellite: tile Sentinel-2 di EOX (`satellite-tiles.py`), credito "Satellite: Sentinel-2 cloudless 2016 by EOX · Copernicus" (nel video weekend Shaka ha chiesto di togliere la scritta a schermo).
- Esempi completi: `esempio-video-mappa-weekend.html` (mappa con flyer a tempo), `esempio-video-schermo-sito.html` (registrazione schermo del sito), `esempio-showreel.html` (showreel 15 s "Un diario vivo").
- I percorsi negli script sono quelli della vecchia sessione: vanno adattati.

## 5. Le tune
Non sono nel repository (diritti). Shaka le rimanda in chat quando servono. Usate finora:
- `stasera/a.wav` (tune base)
- Natural Mystic Sound System – "Spring Ray"; Natural Mystic – "The Flying Mystic"
- Prince Alla & King Alpha – "In the Ghetto" (dub plate)
- Almighty Dub; Jah Shaka – "Warrior"; Tony Tuff & Jah Shaka – "Messenger"; Ranking Fox & Earth Power – "U.N.I.T.Y Riddim"; Kanka – "Stepper Style"; O.B.F & Pupajim – "Politricks"; altre caricate in chat.

## 6. Grafica
- Guida visiva: `guida/stile-ssd.html` (aprire nel browser). Pubblicata anche come pagina privata di Shaka.
- Modelli: `guida/modelli/grafiche-1.html` e `grafiche-2.html` (32 modelli: apertura/chiusura reel, spotlight, eventi, sito, zona sicura, caroselli, post, citazione, nuovo nel diario, una regione, linea del tempo, domanda, big up, evento, tune, polaroid, CTA, copertine in evidenza), `cover-fissata.html` ("IL DIARIO dei sound system italiani · Da nord a sud"), `logo-kit.html` (9 versioni del logo).
- Per esportarli: aprire con Playwright a 1080 px e fare lo screenshot di ogni `.f` (id = nome file).
- Colori: nero #0c0c0b, crema #f3e2b0, oro chiaro #ffd98a, rosso #ab0a05, oro #dc9605, verde #0a5a0a, rosso acceso #e8291f. Caratteri: Anton (titoli), Archivo 700 (testi), Space Mono 700 (etichette).
- Il logo disponibile è solo 500×500: se Shaka manda l'originale ad alta risoluzione, rifare il kit.

## 7. Contenuti già fatti (per non ripetersi)
- Serie "Una regione": Friuli (Ep01), Toscana (Ep02), Emilia-Romagna (Ep03).
- Muro di casse (da aggiornare con le foto nuove e l'unione Dub Lab / Spiritual Youth).
- "Cerca il tuo sound nel diario" (storia con schermate reali del sito).
- Carosello crew vol. 1.
- Storia "Questo weekend" 27–29 novembre (mappa + flyer a tempo, tune "In the Ghetto").
- Reel eventi "Ogni weekend si accendono tanti sound" (schermo del sito, tune Natural Mystic, include Winston Francis) — pubblicato.
- Showreel 15 s "Un diario vivo".
- Storia "Dal 1996 al 2026" (I&I Project → Green Mountain Hi-Fi): **ferma finché non c'è il consenso** dei ragazzi di Green Mountain e dei genitori.
- Nuova cover fissata "IL DIARIO".
- Contenuti vecchi che dicono ancora "archivio" (reel "L'archivio regione per regione", carosello "L'archivio da nord a sud"): da rifare con "diario".

## 8. Contatti con i sound
Messaggio tipo:
> Greetings and love family, sono Shaka, il ragazzo dietro la pagina Sound System Diaries.
> All'interno del diario è presente una scheda dedicata a voi: <link scheda>
> Manca ancora <la foto / la storia>. Quando avete il materiale potete mandare tutto qui in chat oppure per email a soundsystemdiaries@gmail.com.
> Big up e bless

Link scheda: `https://soundsystemdiaries.it/#sound/<id>` (id da `sounds.json`).

**Già contattati**
- Puglia: Gargano's Militant HiFi, Angel Dub, Rasta Warrior, Francavilla Posse, Elijah, Black Star Line (storia arrivata ✅), I&I Project (storia ✅). Bad Side e Midnight Resistance HiFi: nessuna risposta.
- Lazio: Tikur, All Tribes, Radio Torre, Street Roots Hi Fi (avvisati della scheda), Skankin' Tree (foto arrivata, storia in attesa). Monkey Man non riceve DM → provare con un commento al post, Facebook o tramite Skankin' Tree.
- Altri: Tanit (foto e storia in attesa), GreenWood (scheda con foto, manca la storia: messaggio scritto il 27/11, da confermare se inviato), Infiammati Dub ✅, Thunder of Jah Army (in attesa bio e foto), Black Lion ✅, No Identity ✅, Green Mountain Hi-Fi (avvisati della scheda), Nobada/Mina Maya (credito foto).
- Messaggi preparati, da confermare se inviati: Roots Reality Hi-Fi, Adriatic Sound, Gianpy, Heavy Hammer, Kooloometoo, South Rockers, Murjah Warriors (chiedere anche Altamura o Amsterdam), i 4 di Torino (Natural Mystic, Madò Che Crew, Vanchiglia, USV).

**Lazio ancora da contattare (senza link nella scheda):** Baracca, Lion's Way, Farisan Hi-Fi, Dubble Track, Orange Beat, Tamrat, Villa Ada Sound.

## 9. Cose in sospeso
- Ramo `lazio-anni` (Kawa fondati nel 2009, Yaga Yaga nel 2001): pronto, da pubblicare al "pubblica".
- Rifare i contenuti con "archivio" usando "diario".
- Aggiornare il muro di casse.
- Consenso Green Mountain Hi-Fi per i contenuti social.
- Aspettare materiali: Thunder of Jah Army, Tanit, GreenWood, Earthikal, Skankin' Tree (storia).
- Idea futura: "I veterani del diario" (I&I Project 1996, Black Star Line 1998, Kalyweed 1999, Heavy Hammer 1999, Dubass 2003, …) quando ci saranno le foto che mancano. Senza "VS".

## 10. Stato del diario (calcolato da data/sounds.json del ramo main)

- Sound nel diario: 148
- Con foto: 95
- Con storia: 20

**Con storia:** Rise & Shine, Sgrasay, Spantka, Dubass, Dogana Bass, Delta Hi-Fi, Heavy Rootation, Black Lion Hi Vibes, Roots Militant Hi-Fi, Black Star Line, Infiammati Dub, Trail Foundation, Friend Sunshine HI-FI, Street Roots Hi Fi, Sattamassagana, I&I Project, No Identity, Dubrividi, X Knives, Green Mountain Hi-Fi

**Senza foto, per regione:**
- Puglia (11): NegusaTribe Hi Fi, Francavilla Posse, Rasta Warrior, Roots Reality Hi-Fi, Adriatic Sound, Gianpy, Angel Dub, Gargano's Militant HiFi, Heavy Hammer, Kooloometoo, South Rockers
- Lazio (11): Tikur, All Tribes, Monkey Man, Radio Torre, Baracca, Lion's Way, Farisan Hi-Fi, Dubble Track, Orange Beat, Tamrat, Villa Ada Sound
- Toscana (6): Romola, Buska, Immiroots, Joker Smoker, Wild Step, Tiburzi
- Sicilia (5): Demetra, Southern Light, Romanoise, T.U.F.F., 90 Degree Sound
- Campania (5): I-Sciamina, Cinque Cinque, Sun System Hi-Fi, Santantonio Rockers, Sunweed
- Lombardia (5): Horns and Bricks, Tunguska Hi-Fi, Thunder of Jah Army, Mr. Brown, Anandamide
- Piemonte (3): Druidiscos, Makinda Hi-Fi, Tanit
- Marche (2): Kunta Kinte, Freedom
- Sardegna (1): Rockersclan
- Abruzzo (1): L'Osento
- Veneto (1): Bassi Gradassi
- Trentino-Alto Adige (1): RadioFontani
- Liguria (1): Altavia

**Senza Instagram né Facebook nella scheda (27):** Culture Keeper Hi-Fi (Sicilia), Elefant HiFi (Veneto), Blue Shepherd (Veneto), Jahlead (Abruzzo), NegusaTribe Hi Fi (Puglia), Druidiscos (Piemonte), Bassi Gradassi (Veneto), Baracca (Lazio), Lion's Way (Lazio), Farisan Hi-Fi (Lazio), Dubble Track (Lazio), Orange Beat (Lazio), Sunweed (Campania), Kunta Kinte (Marche), Nameless (Emilia-Romagna), Buska (Toscana), Joker Smoker (Toscana), Makinda Hi-Fi (Piemonte), RadioFontani (Trentino-Alto Adige), Tiburzi (Toscana), Tamrat (Lazio), Villa Ada Sound (Lazio), Freedom (Marche), 90 Degree Sound (Sicilia), Low Frequency Embassy (Piemonte), Froggy (Piemonte), Afreekan Children (Piemonte)
