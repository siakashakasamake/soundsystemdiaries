# Sound System Diaries — istruzioni per Claude

Sito: https://soundsystemdiaries.it — "il diario dei sound system italiani".
Chi lo gestisce: Shaka. Si parla in italiano, frasi semplici.

**Prima di lavorare leggi `guida/LAVORO.md`**: c'è tutto su come lavoriamo, lo stato dei contatti e le cose in sospeso.
Lo stile grafico è in `guida/stile-ssd.html`, i modelli in `guida/modelli/`.

## Regole fisse (sempre)
- **Mai pubblicare il sito senza un "pubblica" esplicito di Shaka.** Pubblicare = push su `main` (Netlify ricostruisce da solo).
- SSD **non è un archivio ma un diario**: scrivere sempre "diario", mai "archivio".
- SSD non fa distinzioni: niente "VS", classifiche o confronti tra sound.
- Solo fatti veri da una fonte; citazioni parola per parola. Nomi dei sound completi, scritti come li scrivono loro.
- Quando Shaka dà un testo e chiede di sistemarlo: **non cambiare le sue parole**, correggere solo refusi e punteggiatura.
- Ogni contenuto ha un concetto e uno stile unici, diversi dai precedenti.
- Caption corte con 5 hashtag. CTA "Tutti gli eventi su soundsystemdiaries.it", mai "Ci vediamo lì".
- Negli Spotlight niente date di eventi; nelle scritte a schermo nessun numero di sound.
- Video sotto i 30 MB, senza blocchi, a tempo con la tune. Solo tune di Shaka (stasera/a.wav o quelle che manda in chat).
- Storie sul sito solo se le scrivono i sound. Sound con foto prima di quelli senza.
- Minori (Green Mountain Hi-Fi): solo soprannomi, nessun dato personale, consenso di ragazzi e genitori prima di contenuti social.
- Messaggi ai sound: iniziano con "Greetings and love family", "sono Shaka, il ragazzo dietro la pagina", link diretto alla scheda, email soundsystemdiaries@gmail.com, chiusura "Big up e bless".

## Sito in breve
- Dati: `data/sounds.json`, `data/events.json`, `data/home.json`. Build: `python3 build/build.py` → `dist/`. Template: `build/template.html`.
- Remote corretto: `https://github.com/siakashakasamake/soundsystemdiaries` (il vecchio `siakashakasamake00/...` dà 403). Prima di ogni push: `git remote set-url origin https://github.com/siakashakasamake/soundsystemdiaries`.
- Lavorare su un ramo; al "pubblica": `git checkout main && git merge --ff-only <ramo> && git push origin main`, poi verificare online.
