# Guida grafica HMI — LogicPaint TP 320

Fonte: editor LogicPaint 2.0.5.3 sul progetto `Tino_H20.lpk` (screenshot agosto 2026) + help CHM Kernel.  
Display: **320 × 240** px, touch, 65536 colori. Origine **(0,0) in alto a sinistra**. Griglia **6 × 8**.

Questo file è il manuale oggetti per HOME / FILL / TRAVASO / SETUP.

Stile visivo (chrome, palette scura, come clonare una pagina): [`10_stile_pagine.md`](10_stile_pagine.md). TRAVASO (Pag.2) è il riferimento.

Screenshot archiviati in `doc/guide/img_hmi/`:


| File                                                 | Dialogo LogicPaint                      | Oggetto Pag.0 / Pag.4                    |
| ---------------------------------------------------- | --------------------------------------- | ---------------------------------------- |
| [elenco_menu.png](img_hmi/elenco_menu.png)           | *Impostazione Menu*                     | elenco (Pag.4, prova `ciao/come/va?`)    |
| [variabile_word.png](img_hmi/variabile_word.png)     | *Impostazioni Variabile*                | WORD `RILANCIO` in alto a sinistra Pag.0 |
| [istogramma_visto.png](img_hmi/istogramma_visto.png) | *Selezione Variabile* (filtro `V ISTO`) | barra tino Pag.0                         |


**Variabile e istogramma sono lo stesso flusso UI**: stesso picker, stessi flag, stessa gestione colori. Cambia solo il **tipo** (`WORD` vs `V_ISTO` / `H_ISTO`) e quindi lo strumento palette (V gialla vs H/V Istogramma).

---



## Indice

1. [Area di lavoro](#1-area-di-lavoro)
2. [Palette](#2-palette-ordine-a-video)
3. [Testo](#3-testo-text-nel-lpk-tipo-2)
4. [Rettangolo pieno](#4-rettangolo-pieno-fill-recta)
5. [Come si inserisce una variabile](#5-come-si-inserisce-una-variabile)
6. [Variabile numerica WORD](#6-variabile-numerica-word--oggetto--definizione)
7. [Istogramma V / H](#7-istogramma-verticale-e-orizzontale)
8. [Flag ENA / RFS / REM / …](#8-flag-impostazioni-variabile)
9. [Pulsante K](#9-pulsante-k-keyxx-lpk-tipo-17)
10. [Menu / Elenco](#10-menu--elenco)
11. [Allarmi](#11-allarmi-pagine-allarme-non-oggetti-pagina)
12. [Pagine attuali vs target](#12-pagine-attuali-vs-target-h20)
13. [Colori](#13-colori-lpk-argb-signed-net) `.lpk`
14. [Regole operative](#14-regole-operative)
15. [Kit minimo H20](#15-kit-minimo-per-disegnare-h20)

---



## 1. Area di lavoro

- Finestra canvas: `Display : TP_320`
- Status bar: `Pagina: n - Totale: 4` (oggi 5 pagine, indici 0–4), `X Y` cursore, `W: 320 H: 240`, `Dim X / Dim Y` dell’oggetto selezionato
- Albero `Gestione Progetto`: Pagine, Allarmi, Ladder, Blocchi Funzione
- Pagina evidenziata in **blu** + freccia verde = quella in editor
- `Finestra Proprietà`: oggetto selezionato (`n : TEXT`, `n : FILL RECTA`, …), posizione, colori
- `Casella Strumenti : Strumenti`: palette. Colori nuovi oggetti: **principale bianco, sfondo nero**. Lucchetto + *Spostamenti in Griglia*

Memoria (Controlla Dimensione, compile ok): programma ~7 % (17152 / 262143 byte); pagine ~0 % del tetto. C’è spazio.

---



## 2. Palette (ordine a video)


| Strumento                                     | Icona UI          | Uso H20                                              |
| --------------------------------------------- | ----------------- | ---------------------------------------------------- |
| Cursore                                       | freccia           | selezione (giallo = attivo)                          |
| Gomma                                         | —                 | cancella oggetto                                     |
| Testo                                         | T                 | etichette                                            |
| Linea / Cerchio                               | —                 | raro                                                 |
| Cerchio pieno / Rettangolo / Rettangolo pieno | —                 | box, barre statiche, top/bottom bar                  |
| Rett. arrotondato (pieno)                     | —                 | box status ON/OFF                                    |
| Cornice                                       | —                 | cornice                                              |
| **Variabile**                                 | V gialla          | numeri editabili / sola lettura (`WORD`)             |
| Immagine / Lista immagini                     | —                 | bmp jpg gif png → Tipo 12, `IdVar` = indice lista    |
| Grafico                                       | linea             | trend (Pag.3); non per portata in tempo reale        |
| **H Istogramma**                              | barre orizzontali | progress FILL / TRAVASO; lampade Pag.0               |
| **V Istogramma**                              | barre verticali   | tino livello                                         |
| Tachimetro / Quadrante                        | —                 | non usati                                            |
| **Pulsante**                                  | K gialla          | nav, AVVIA/STOP, MAN, toggle                         |
| **Menu**                                      | elenco verticale  | SETUP: **scelta trasduttore** (max **1 per pagina**) |
| Menu a tendina                                | drop-down         | alternativa ARM; stesso limite 1 per pagina          |


---



## 3. Testo (`TEXT`, nel `.lpk` Tipo 2)

Dialogo **Inserisci Testo**:

- Campo `Testo` (es. `VALORE MASSIMO`)
- Dimensione carattere: **D11** piccolo, **D22** medio (default etichette), **D33** grande (litri HOME)
- Nota UI: `D + DimX + DimY` — W/H del box **non si editano**, dipendono da stringa × font. D22 → altezza tipica **16 px**
- Font: Standard. Colore testo / sfondo (es. nero su grigio chiaro)
- Tastiera Standard [F1] o Cirillico [F2]
- Caratteri speciali 0–5: barre e **frecce** (le frecce blu Pag.0)

Proprietà esempio: `10 : TEXT`, Sinistra 12, Alto 120, Larghezza 168, Altezza 16.

Due lingue nel `.lpk`: `ObjText.Testo=0:` italiano, `=1:` inglese.

Niente carattere `°` nei testi se poi finiscono in simbolici/variabili; in HMI etichetta usare `F` per durezza.

---



## 4. Rettangolo pieno (`FILL RECTA`)

- Posizione e W×H tutti editabili in UI
- Esempio visto in editor: X=57 Y=65, **127 × 102**, colore bianco
- Colore = *Colore principale* della toolbox al momento del disegno
- Uso: top bar blu, bottom nav grigia, box giallo pagina attiva, sfondo campi edit

Rettangolo vuoto / arrotondato: stesso sistema, solo bordo o angoli.

Nel `.lpk` **Tipo 3 non è FILL RECTA**: è una linea da `(X,Y)` a `(Width,Height)` (prova Pag.5: diagonale blu). Il numero di tipo del rettangolo pieno è da leggere da un oggetto disegnato in LogicPaint. Workaround verificato: testo Tipo 2 con `BackColor` sul box W×H. Vedi [`03_formato_lpk_agente.md`](03_formato_lpk_agente.md).

---



## 5. Come si inserisce una variabile

Due cose distinte:

1. **Definizione** (anagrafica in Gestione Variabili / *Aggiungi Variabile*): nome, tipo, DATA, min/max, flag.
2. **Oggetto grafico** sulla pagina: rettangolo che *punta* a una definizione (`IdVar`).



### Flusso in editor

1. Scegli lo strumento giusto in palette (Variabile / V Istogramma / H Istogramma / Menu).
2. Clic sul canvas → si apre **Selezione Variabile**.
3. La barra gialla filtra: *Vengono visualizzate solamente le variabili di tipo : …* (`WORD`, `V ISTO`, `H ISTO`, …). Un oggetto WORD **non** elenca le `V_ISTO`.
4. Bottoni in basso: **Aggiungi / Modifica / Cancella Variabile**, poi **OK**.
5. Doppio clic sull’oggetto già piazzato: o cambi variabile [S], o apri *Impostazioni Variabile* [V].

Copia rapida: **Copia le impostazioni dalla variabile** (es. `5: LIVELLO REAL [WORD]`) e cambia solo indirizzo/nome.

CTRL+C / CTRL+V copia l’oggetto grafico su un’altra pagina (poi riallinea `IdVar` se serve).

---



## 6. Variabile numerica WORD — oggetto ≠ definizione

Esempio Pag.0 in alto a sinistra: campo `RILANCIO`. In editor si vede `DATA 2105` e `VVVVV` (5 cifre). Coordinate tipiche ~ X 12 Y 8, box ~60×32. Screenshot: [variabile_word.png](img_hmi/variabile_word.png).

### 6.1 Impostazioni Variabile (dialogo)

Toolbar: Annulla [ESC], Salva [ENTER], Editor Stringhe [F7], Editor Immagini [F8], Variabili Esterne [F9].


| Campo                                     | Valore visto su `RILANCIO`                                              |
| ----------------------------------------- | ----------------------------------------------------------------------- |
| Nome                                      | `RILANCIO`                                                              |
| Tipo                                      | **WORD**                                                                |
| Cifre intere / decimali                   | 5 / 0 → a video `VVVVV`                                                 |
| Dimensione                                | **WORD_WIDE** (16 bit). `LONG_WIDE` = 32 bit = **due DATA consecutivi** |
| Indirizzo                                 | **DATA.2105** (Sfoglia [F6])                                            |
| Min / Max                                 | 0 … 65535, radio **DEC** (oppure HEX)                                   |
| ENA                                       | **on** = scrivibile da touch (tastiera numerica)                        |
| RFS                                       | refresh continuo; in UI a volte **spuntato e grigio** (forzato)         |
| REM                                       | off → min/max **costanti**, non indirizzi DATA                          |
| SCALE / ENG / PWD / INDEX / IMM / OMR_HEX | off                                                                     |


**Sola lettura** (litri HOME, ETA, %): ENA **off**.  
**Edit SETUP/FILL** (LT TARGET, CIRC, …): ENA **on**, min/max stretti (es. SMORZAMENTO SEC 1–15, F.SCALA 1000–5000).

WORD vs WORD_0: stesso intero; WORD riempie con spazi, WORD_0 con zeri. I decimali sono **solo display**: il valore in DATA resta intero. Se le cifre non bastano, il pannello mostra trattini.

### 6.2 Tipi che servono H20


| Tipo variabile | Strumento palette | Note                                        |
| -------------- | ----------------- | ------------------------------------------- |
| WORD / WORD_0  | Variabile (V)     | numeri, edit o sola lettura                 |
| V_ISTO         | V Istogramma      | barra tino; min/max spesso **REM**          |
| H_ISTO         | H Istogramma      | progress; lampade Pag.0 su DATA.5000 / 8000 |
| GRAPH          | Grafico           | trend Pag.3                                 |
| MENU           | Menu              | elenco; **1 per pagina**                    |


---



## 7. Istogramma verticale e orizzontale

Stesso dialogo *Selezione Variabile* della WORD. Screenshot Pag.0: [istogramma_visto.png](img_hmi/istogramma_visto.png).

Il picker dice: *Vengono visualizzate solamente le variabili di tipo : **V ISTO***.

Help Kernel: la barra è proporzionale al valore tra min e max. **RFS** = segue in tempo reale; senza RFS si aggiorna solo all’apertura pagina.

### 7.1 Barra tino attuale (Pag.0, oggetto ~60×112 a X=228 Y=24)

Nel `.lpk` è Tipo 15, `IdVar=0`. Colori oggetto: barra verde (`-16711936`), sfondo ciano (`-16711681`), BOX rosso, BOX spuntato. Lampeggio / colore dinamico **disabilitati** su quell’oggetto.


|                             | Variabile `LIVELLO`                                                           |
| --------------------------- | ----------------------------------------------------------------------------- |
| Tipo                        | `V_ISTO`                                                                      |
| Indirizzo                   | `DATA.1000` (simbolico `LIVELLO REAL`)                                        |
| Min / Max in tabella picker | `6000` / `6001` — **non sono litri**                                          |
| REM                         | **on** → min = contenuto di `DATA.6000`, max = `DATA.6001` (pagina SCALATURA) |
| NORM / INV                  | In campo **INV** (`NormInv=True`) = riempie dal **basso** (`Var_0` INV). NORM = dall’alto. |
| SCALE                       | off (conversione mA→L nel ladder)                                             |
| ENA                         | False (non si scrive dal touch)                                               |
| Colori nel picker           | Colore variabili **verde**, sfondo **ciano**, BOX **rosso**                   |


H Istogramma: stesso meccanismo, tipo `H_ISTO`. NORM = da **sinistra** a destra, INV = da destra. Barra TRAVASO: NORM, REM min=`DATA.2030` (0) max=`DATA.2006` (LT TRAVASO), **RFS** on.

Lampade HOME (OSMOSI / RETE / TRAVASO): H_ISTO 24×24 su `LED_OSMOSI` `DATA.5002` / `LED_RETE` `DATA.5001` / `LED_POMPA` `DATA.5000` (`IdVar` 3 / 2 / 1). Colori come Pag.2: Fore rosso `-65536`, Back lime `-16711936`. In editor a strisce e spesso si legge l’indirizzo `500x`, non il nome; sul pannello 0/1. Non duplicare le anagrafiche.

### 7.2 HOME

Barra tino: `Variabile_46` TANK HOME, **V_ISTO** (Tipo 15) su `DATA.1000`, REM min=`DATA.2030` max=`DATA.2012` (LT TOT), RFS on, **INV** (`NormInv=True`) = dal basso (con `Var_0`; NORM riempie dall’alto). Oggetto `(216, 40) 84 × 152`. Litri: WORD `IdVar=5` `DATA.1000` D33 a sinistra (niente etichetta LIV). %: WORD `IdVar=38` `DATA.2023`. MAN: tasto blu `(176, 0) 108 × 24` con lampada verde `IdVar=47` + testo MAN + `!` + KEY `MAC_SETFLG` `FLAG.254` (ladder inverte `204`; `MAC_TOGGLE` HMI è muto). Ladder: vedi `07_piano_file_lpk.md` § MAN MODE.

---



## 8. Flag Impostazioni Variabile

Etichette italiane (`Italiano.txt`) + help Kernel:


| Flag              | Significato                                                   | H20                          |
| ----------------- | ------------------------------------------------------------- | ---------------------------- |
| **ENA**           | Abilitazione alla scrittura (tap → tastiera)                  | on solo sui campi SETUP/FILL |
| **RFS**           | Refresh continuo; senza, aggiorna solo all’ingresso pagina    | on su litri e barre          |
| **REM**           | Min/Max diventano **indirizzi DATA** (modificabili a runtime) | on sulla barra tino          |
| **IMM**           | Toggle immediato (BIT_STR / BIT_OBJ, solo touch)              | no                           |
| **OMR_HEX**       | BCD Omron 0000…9999                                           | no                           |
| **INDEX**         | variabile indicizzata                                         | no                           |
| **ENG**           | ingegneristica                                                | no                           |
| **SCALE**         | valore messo in scala in HMI                                  | no (scala nel ladder)        |
| **PWD**           | scrittura protetta da password (serve anche ENA)              | opzionale SETUP              |
| **INIBIT**        | lock scrittura se bit 11 di `DATA.01`                         | di solito off                |
| **BOX**           | rettangolo attorno (gestione colori oggetto)                  | on barre, a gusto sui numeri |
| **COL. DINAMICO** | Fore/Back da `DATA+2` a runtime                               | off per ora                  |
| **LAMPEGGIO**     | due colori                                                    | off                          |


Colore dinamico / lampeggio nel picker Pag.0 erano grigi.

---



## 9. Pulsante K (`KEY.xx`, `.lpk` Tipo 17)

Dialogo **Macro Pulsante**. Ogni tasto: Key Code (es. 22) e nome `KEY.02`.

### Macro (premuto / rilasciato)


| Macro                   | Uso H20                           |
| ----------------------- | --------------------------------- |
| `MAC_NULL`              | niente                            |
| `MAC_PAGE`              | cambio pagina; `PaginaDATA` = 0…n |
| `MAC_WRITE`             | scrive Valore in DATA             |
| `MAC_ADD` / `MAC_SUB`   | ± su DATA (tastierino, non nav)   |
| `MAC_BSET` / `MAC_BCLR` | bit                               |
| `MAC_TOGGLE`            | **non usare** sul TP320: bip, FLAG fermi |
| `MAC_PULSE`             | impulso                           |
| `MAC_PRINT`             | stampa                            |
| `MAC_SETFLG`            | RESET, AVVIA; con `MAC_RESFLG` al rilascio = impulso MAN/`185`–`187` |


Porta COM: **INTERNAL**. Ind PLC: **1**.

Pag.0 tipica: tasti in basso già `MAC_PAGE` con `Immagine_P` ≠ `Immagine_R` (icona premuto/rilasciato).

### Forma

1. **Nessuna** — solo hit-area (anche **Trasparente** sopra un rettangolo/testo)
2. **Forma di sfondo** — *Libreria Forme*: **Immagini esistenti** (es. n.005 interruttore 3D due stati) o **Immagini personalizzate** **bmp / jpg / gif / png** (rilasciato + premuto). *Estrai Immagine* F2/F4
3. **Forma predefinita** — WinKey, RoundKey, Recta, Round Recta + interno **Testi** o **Immagini**

Nav H20: **Forma predefinita + Testi** (`HOME`, `FILL`, `AVVIA`). Pagina attiva: rettangolo giallo dietro il tasto (`-256`).

Icona cliccabile (luna/sole TRAVASO): **non** assegnare un `ImgGrafica` nuovo al KEY. Oggetto **Immagine** Tipo 12 sotto + KEY **Trasparente** sopra, stesso X Y W H. Dettaglio: [`03_formato_lpk_agente.md`](03_formato_lpk_agente.md) §4 e §10.

BOX in editor (rosso, 3 px) non è detto che sia visibile sul pannello.

---



## 10. Menu / Elenco

Oggetto **Menu** (dialogo *Impostazione Menu*). Screenshot: [elenco_menu.png](img_hmi/elenco_menu.png).

Help Kernel + messaggio IDE: **al massimo 1 Menu per pagina** (stesso tetto per il Menu a tendina). Metterlo in SETUP, non in HOME.

Esempio Pag.4 (prova): 5 righe `ciao / come / va? / prova / esci`, Dim **60 × 120**, font **D23**, bianco su nero. Radio **Riga 1…8** (max 8 voci nel dialogo visto).


| Campo UI                            | Significato                                                                                                                                                           |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Numero elementi                     | quante righe visibili (es. 5; per i due sensori: **2**)                                                                                                               |
| Dimensione                          | font `D23` (`D + DimX + DimY`)                                                                                                                                        |
| **Indirizzo salvataggio posizione** | DATA che riceve la **posizione cursore** confermata (tap / Enter). Riapri la pagina: il cursore torna lì. Il ladder può leggere lo stesso DATA come **indice scelta** |
| Per riga                            | Testo, Macro (`MAC_NULL` o azione), Ind PLC **1**, Porta COM **INTERNAL**                                                                                             |
| Font / Colore / Sfondo              | Standard, bianco, nero                                                                                                                                                |
| Tastiera                            | Standard [F1] / Cirillico [F2]                                                                                                                                        |
| Caratteri speciali                  | 0–6 (barre, frecce) da inserire nel testo riga                                                                                                                        |


`MAC_NULL` è sufficiente se l’unica cosa che serve è l’indice in DATA: non serve una macro per riga.

**Non usare** `DATA.1000` per l’indice (è il livello). Nel dialogo di prova era proprio `DATA 1000` — va cambiato. Molti oggetti nel `.lpk` hanno `DataSavePos=1000` come default inerte; sul Menu quel campo **è vivo**.

Verificare sul pannello se l’indice è 0-based (prima riga = 0) o 1-based (prima riga = 1). Il ladder deve usare lo stesso convenzione.

### Uso H20: scelta trasduttore (SETUP)

Numero elementi **2**, macro `MAC_NULL`, indirizzo **DATA dedicato** (libero, es. `2029` se confermato in mappa — non 1000/2007/2017):


| Indice  | Testo riga (corto, D23, box stretto) | Sensore               | FS bar | nota                              |
| ------- | ------------------------------------ | --------------------- | ------ | --------------------------------- |
| 0 (o 1) | `0-2 bar`                            | Riels RIB100 in campo | 2,0    | ~10 L/count — FLOW inutilizzabile |
| 1 (o 2) | `0-0.3bar`                           | nuovo                 | 0,3    | ~1,5 L/count — default futuro     |


Il ladder legge l’indice e usa il fondo scala in bar nella formula `bar = (count-816)/3280 × FS`. Dettaglio scalatura: [08_sensore_livello.md](08_sensore_livello.md).

Menu a tendina (ARM, 65536 colori): stesso concetto, più compatto; resta **1 per pagina**.

---



## 11. Allarmi (pagine Allarme, non oggetti pagina)

Slot 0–9. 0–15 = bit di `DATA.08`. Header a video `Alr:***/***`.


| Stile               | Esempio                                  | Aspetto                                                             |
| ------------------- | ---------------------------------------- | ------------------------------------------------------------------- |
| Allarme sicurezza | Alr.0 BLOCCO TERMICO                     | sfondo **blu**, fascia rossa in alto testo giallo, messaggio bianco |
| Processo H20        | Alr.3–5 (TARGET / PIENO / TRAVASO VUOTO) | **pagina rossa**, bordo ciano, testo bianco                         |


Net.1 arancione in albero = *Fine programma* (END), non errore compile.

---



## 12. Pagine H20 v1.00 (0–10)


| Pag | Nome | Contenuto principale |
| --- | --- | --- |
| 0 | HOME | litri `DATA.1000`, % `2023`, barra `Var_46`, LED osmosi/rete/pompa, MAN |
| 1 | FILL | LT/DUR target, mix, AVVIA `FLAG.200`, cm colonna |
| 2 | TRAVASO | AVVIA `FLAG.203`, barra calo livello, pompa `FLAG.207` |
| 3 | TANK | ricetta, CARICA DEFAULT |
| 4 | MIX | tolleranza LT |
| 5 | TRASD | sensori, IDX |
| 6 | CONTAT | totalizzatori |
| 7–10 | avvisi | REFILL, WARN VUOTO, WARN LT/DUR |


Nav unica in basso: `HOME | FILL | TRAVASO | SETUP` (SETUP a destra). Attiva = giallo.

---



## 13. Colori `.lpk` (ARGB signed .NET)


| Valore      | Colore                             |
| ----------- | ---------------------------------- |
| `-1`        | bianco                             |
| `-16777216` | nero                               |
| `-16776961` | blu                                |
| `-16744448` | verde (alcuni oggetti)             |
| `-16711936` | verde lime (barra / lampade Pag.0) |
| `-16711681` | ciano (sfondo barra tino)          |
| `-65536`    | rosso                              |
| `-256`      | giallo                             |
| `-4144960`  | grigio canvas attuale              |


---



## 14. Regole operative

1. Lo strumento palette filtra il **tipo** (V ISTO ↔ istogramma V; WORD ↔ Variabile).
2. Min/Max **REM** = indirizzi DATA, non costanti litri. In tabella picker `6000`/`6001` con REM on = `DATA.6000`/`DATA.6001`.
3. **1 Menu (o 1 tendina) per pagina.**
4. Indice Menu: DATA dedicato, mai `DATA.1000`.
5. Dopo modifiche: **Compila** (non serve Trasmetti per validare).
6. Mockup `doc/*.webp` = layout, non pixel TP 320.
7. Immagini a video: oggetto Tipo 12 (`Modo=DEL`) verso `ImgGrafica_N`. Per il tap, KEY trasparente sopra. Non usare `Immagine_P` sul KEY per bitmap nuove. Icone 24×24 stanno nella barra titolo.

---



## 15. Kit minimo per disegnare H20


| Bisogno                    | Oggetto              | Tipo variabile / macro                     |
| -------------------------- | -------------------- | ------------------------------------------ |
| Etichetta                  | Testo D22/D33        | —                                          |
| Barra titolo / nav         | FILL RECTA           | —                                          |
| Litri, target, ETA         | Variabile WORD       | ENA off o on                               |
| Tino                       | V Istogramma         | V_ISTO su 2007, REM max 2017               |
| Progress step              | H Istogramma         | H_ISTO                                     |
| Lampada ON/OFF             | H Istogramma piccolo | H_ISTO 0 / ≠0                              |
| HOME FILL TRAVASO SETUP    | Testo + Pulsante K   | MAC_PAGE                                   |
| Icona (luna/sole)          | Immagine + K trasparente | MAC_PAGE                               |
| AVVIA STOP MAN             | Pulsante K           | MAC_SETFLG / MAC_RESFLG                    |
| Scelta sensore 0–2 / 0–0,3 | Menu/Elenco (SETUP)  | indice in DATA dedicato, 2 righe, MAC_NULL |


