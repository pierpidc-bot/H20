# Formato `.lpk` per un agente — LogicPaint TP 320

Obiettivo: produrre o modificare un file `.lpk` che **si apre** in LogicPaint 2.0.5.3, **compila** e si può **inviare** al TP 320.

Presupposto: il `.lpk` si scrive come testo. I limiti si **verificano** in editor, non si assumono.

Round-trip:

1. L’agente scrive/modifica `Proj/Tino_H20.lpk`
2. Preview 320×240: [`tools/tp320_preview`](../../tools/tp320_preview/README.md) (`preview.py`) — l’agente vede i PNG e si corregge
3. Tu apri/ricarichi in LogicPaint (se era aperto, non risalvare sopra), **Compila**, screenshot se serve

**Specifica impianto:** [`doc/Tino_H20.md`](../Tino_H20.md)  
**Manuale oggetti UI:** [`09_guida_grafica_hmi.md`](09_guida_grafica_hmi.md)  
**Stile pagine:** [`10_stile_pagine.md`](10_stile_pagine.md)  
**File di lavoro:** `Proj/Tino_H20.lpk`

---

## Indice

1. [Stato delle prove](#1-stato-delle-prove)
2. [Struttura del file](#2-struttura-del-file)
3. [Sezioni di intestazione](#3-sezioni-di-intestazione)
4. [Immagini `ImgGrafica`](#4-immagini-imggrafica)
5. [Pagine e oggetti](#5-pagine-e-oggetti)
6. [Tipi oggetto (verificati)](#6-tipi-oggetto-verificati)
7. [Variabili PLC ↔ HMI](#7-variabili-plc--hmi)
8. [Testi e lingue](#8-testi-e-lingue)
9. [Come aggiungere una pagina](#9-come-aggiungere-una-pagina)
10. [Pulsanti (tasto K)](#10-pulsanti-tasto-k)
11. [Compilazione e invio](#11-compilazione-e-invio)
12. [Checklist pre-invio](#12-checklist-pre-invio)
13. [Aperti / da verificare](#13-aperti--da-verificare)

---

## 1. Stato delle prove

Prova 2026-08-18 su `Tino_H20.lpk` + LogicPaint 2.0.5.3:

| Fatto | Esito |
|---|---|
| Aggiungere `[Pagina_5]` scritta a testo | **OK** — albero `Pag.5 : TRAVASO` |
| Aggiungere `[Variabile_44]` `H_ISTO` | **OK** — *Impostazioni Variabile* |
| **Compila** | **OK** |
| Tipo 2, 11 WORD, 14 H_ISTO, 17 KEY | Si vedono |
| Tipo 3 come fascia piena | **NO** — linea `(X,Y)`→`(Width,Height)` (può uscire diagonale) |
| `Keytext` nel tasto K da solo | In editor **non si legge** |
| Testo Tipo 2 + KEY `Trasparente=True` sopra | **OK** — nav HOME/FILL/TRAVASO/SETUP e AVVIA/STOP visibili |
| Tipo 12 IMAGE (`Modo=DEL`) + KEY trasparente sopra | **OK** — luna/sole TRAVASO visibili in editor |
| KEY `KeyTouch_-1_Immagine_P` su hex scritta a mano | **NO** — l’icona non si vede; usare Tipo 12 |
| `MAC_NULL` sul tasto OUT | **OK** — compile; in editor è un quadrato verde |
| WORD in editor | Mostra `DATA.xxxx` + placeholder cifre (`vvvv`), es. LT TRAVASO = `DATA.2006` |
| Screenshot senza barra nav | [`img_hmi/pag5_travaso_senza_nav.png`](img_hmi/pag5_travaso_senza_nav.png) |
| Screenshot con nav + OUT=K | [`img_hmi/pag5_travaso_con_nav.png`](img_hmi/pag5_travaso_con_nav.png) |

In editor i KEY trasparenti possono mostrare un **retino** sopra il testo: è la hit-area, non necessariamente l’aspetto sul pannello.

Conseguenza pratica: per una barra titolo o un tasto con etichetta usare **Testo (Tipo 2)** con `BackColor` che riempie il box `Width×Height`. Il tasto K va **sopra**, `Trasparente=True`, per la macro touch.

---

## 2. Struttura del file

Prima riga: `LogicPaint` (senza sezione). Poi blocchi INI. **Non esistono** sezioni chiamate `[Immagini]`, `[Pagine]`, `[OggettoGrafico]`.

Nomi reali:

| Ci si aspetta | Nel file |
|---|---|
| immagini | `[Lista Immagini]` → `ImgGrafica_0` … |
| pagine | `[Pagina_0]` `[Pagina_1]` … numerazione **0-based contigua** |
| oggetti | chiavi `Pag_N_Obj_M_*` **dentro** `[Pagina_N]` |

Ordine nel progetto Tino (non invertire a caso):

```
LogicPaint
[Info]
[Slots TCP Client]     ; anche GPRS/FTP/HTML sotto questo header
[Term_Settings]
[Filtri] [Timer] [Counter] [SetFonts]
[Lingue]
… PID, encoder, log …
[Pagina_0] … [Pagina_N]
[Allarme_0] … [Allarme_9]
[Variabile_0] … [Variabile_M]
[Lista Immagini]
[Ladder]                 ; solo progetto ladder
[Network_0000] …
[FunctionBlock]
[Simbolici]
[Commenti]
```

Progetto **AWL** (Lista istruzioni): niente `[Ladder]` / reti / FB. Al loro posto `[Lista Istruzioni]` … `[End Lista Istruzioni]` con `END` + `SBR INITIALIZE`. Come prepararlo: [11_awl_logicpaint.md](11_awl_logicpaint.md).

Vincoli visti nel file (da tenere, da confermare se si rompe la compile):

- oggetti pagina **prima** di `[Allarme_0]`
- anagrafiche `[Variabile_N]` **prima** di `[Ladder]` / `[Lista Istruzioni]` e di `[Lista Immagini]`
- niente carattere `°` in testi/simbolici
- su una WORD: `Minimo ≠ Massimo`

Non c’è `NUM_PAGINE`: LogicPaint conta i blocchi `[Pagina_N]` da 0.

---

## 3. Sezioni di intestazione

### `[Info]`

Metadati (`InfoAzienda`, `InfoProgetto`, …) e opzioni SPW Wi‑Fi / TCP Client. Per H20 si possono lasciare vuoti/`False`.

### `[Slots TCP Client]`

`NUM_SLOTS_TCP_CLIENT=0` Nel file di riferimento. Sotto lo stesso header ci sono template mail/FTP/HTML. Non servono per un TP 320 solo mini-USB.

### `[Term_Settings]` — quelli che fanno aprire/compilare/inviare

Dal file di riferimento:

```
Term_Nome=TP_320
Term_MainCom=INTERNAL
Term_SerSet_Protocollo_0=SLAVE
Term_SerSet_Baud_0=115200
Term_SerSet_Parita_0=NO_PARITY
Term_SerSet_Bits_0=8
Term_SerSet_Stops_0=1
Term_SerSet_PlcAddr_0=1
Term_Ini_Page=0
Term_TCiclo=16
Term_Ip_Addr_0=192
Term_Ip_Addr_1=168
Term_Ip_Addr_2=1
Term_Ip_Addr_3=120
Term_Ip_Port=80
Term_ProtoETH=KER_SLAVE
Term_Ena_ANA=False
```

- `Term_Nome` sbagliato → *Tipo di terminale errato! Caricamento interrotto!*
- Mini-USB sul PC = una **COM** in *Opzioni → Porta COM*. Baud debugger: 115200 (ARM + mini-USB anche 230400/460800).
- `Term_Ena_ANA=False` nel backup di campo mentre il ladder usa `DATA.417` — **normale** su TP 320 /SCT. Non mettere `True` nel file; non serve toggle in *Opzioni progetto* LogicPaint.
- Ethernet è opzionale (`/ETH`). Non è il canale di programmazione di questo pannello.

---

## 4. Immagini `ImgGrafica`

Sezione: `[Lista Immagini]`. nel file di riferimento: `ImgGrafica_0` … `ImgGrafica_27`. Nel file di lavoro arrivano almeno fino a `ImgGrafica_38` (luna/sole + 2 mani MAN).

Formato di **ogni** riga:

```
ImgGrafica_N=<5 cifre larghezza><5 cifre altezza><pixel RGB24 hex>
```

6 caratteri hex = 1 pixel (`FFFFFF` = bianco). Ordine row-major, origine in alto a sinistra. Lunghezza body = `W × H × 6`.

Esempio reale:

```
ImgGrafica_3=0004200024FFFFFFFF...
```

`00042` + `00024` → **42 × 24** px, poi i pixel.

Indici **contigui** da 0. Una riga nuova si appende in fondo alla sezione, prima di `[Ladder]`. Non c’è un campo `NumImmagini`.

### Tabella conversione (file di riferimento)

| Indice | Size | Hex iniziale | Ruolo tipico |
|---|---|---|---|
| 0 | 60×32 | `0000FF` pieno | slot / chroma blu |
| 1 | 84×40 | icona 3D | nav |
| 2 | 84×40 | `0000FF` | vuoto |
| 3, 5 | 42×24 | tasto 3D | MANUALI |
| 4, 7, 10, 24 | 42×24 / 84×40 / 78×40 | `000000` | maschera nera |
| 6, 8 | 84×40 | icone | SCALATURA |
| 9 | 78×40 | icona | Pag.2 |
| 11–16 | 42×24 | tasti (alcuni P/R) | Pag.2 |
| 17–19 | 78×48 | icone (18 blu) | Pag.0 |
| 20 / 21 | 78×48 | coppia P/R | Pag.0 |
| 22 / 23 | 84×48 | coppia P/R | Pag.0 |
| 25 | 60×56 | `808080` | sfondo |
| 26, 27 | 60×56 | tasto 3D | KEY Pag.0 |

Relazione con gli oggetti: il tasto (Tipo 17) **non** incorpora i pixel. Punta agli indici:

```
KeyTouch_-1_Immagine_P=20    ; premuto
KeyTouch_-1_Immagine_R=21    ; rilasciato
```

`0000FF` Nel file di riferimento è blu pieno: in editor il tasto che usa `Immagine_P=0` non mostra un’icona utile (chroma / vuoto).

**Come si vede un’immagine a video** (verificato 2026-08-19):

| Metodo | Esito |
|---|---|
| Palette **Immagine** in LogicPaint (bmp/png) | **OK** — diventa `ImgGrafica_N` + oggetto Tipo 12 |
| Oggetto Tipo 12 `IdVar=N` verso `ImgGrafica_N` | **OK** — W×H oggetto = W×H bitmap |
| Hex RGB24 scritta nel `.lpk` e mostrata da Tipo 12 | **OK** (luna ridotta 24×24, sole 24×24) |
| Stesso hex attaccato solo al KEY (`KeyTouch_-1_Immagine_P`) | **non si vede** |

L’indice `N` di `ImgGrafica_N` **non** è `[Variabile_N]`: sono due liste diverse. Su TRAVASO `IdVar=35` sull’oggetto luna punta a `ImgGrafica_35`, mentre `[Variabile_35]` resta `MAN MODE`.

JPG “grandi” in compile: larghezza multipla di 32 (`Italiano.txt`). Icone piccole (24×24) in RGB24 nel `.lpk` hanno compilato. Conversione RGB24 → 65536 colori (RGB565) la fa LogicPaint in compilazione.

---

## 5. Pagine e oggetti

Indici **v1.00** in `Tino_H20.lpk` (0–10). Contratto: [12_h20.md](12_h20.md).

| N | Nome | Note |
|---|------|------|
| 0 | HOME | KEY MAN; box OSMOSI/RETE/TRAVASO |
| 1 | FILL | AVVIA `FLAG.200`; MAN osmosi/rete |
| 2 | TRAVASO | AVVIA `FLAG.203`; pompa `FLAG.207` |
| 3 | TANK | SETUP; nav SETUP atterra qui |
| 4 | MIX | tab SETUP |
| 5 | TRASD | IDX SENS `DATA.4116` |
| 6 | CONTAT | totalizzatori (tab TOT) |
| 7–10 | REFILL / WARN | avvisi e rabbocco |

Nav basso: HOME \| FILL \| TRAVASO \| SETUP. `MAC_PAGE` è **0-based**.

Intestazione pagina (esempio storico Pag.5; oggi TRASD):

```
[Pagina_5]
Pag_5_NomePagina=TRASD
Pag_5_Attributi=2
Pag_5_ColoreSfondo=-4144960
Pag_5_ColoreEditorVar=-1
Pag_5_ColoreGriglia=-1
```

`NomePagina` è quello in albero (`Pag.5 : TRASD`).

Ogni oggetto: stesso scheletro di chiavi (`IdObj`, `Tipo`, `Modo`, `X Y Width Height`, colori ARGB signed .NET, `IdVar`, font). Quasi tutti hanno `Modo=DRAW`. **Eccezione:** Tipo 12 IMAGE usa `Modo=DEL` (così lo serializza LogicPaint; non cancellare l’oggetto).

Poi campi specifici:

- Tipo 2: `ObjText.Testo=0:` / `=1:` e `X_Lang` / `Y_Lang` / `Dim_Lang` **per lingua**
- Tipo 11 / 14 / 15 / 16: `IdVar` = indice `[Variabile_N]`
- Tipo 12: `IdVar` = indice `ImgGrafica_N` (niente `ObjText`, niente `KeyTouch`)
- Tipo 17: `KeyTouch_0_*` (forma + testi / hit-area trasparente) oppure `KeyTouch_-1_*` (icone libreria Pag.0)

Display **320×240**, origine **(0,0) in alto a sinistra**, griglia editor **6×8** (X multiplo di 6, Y di 8).

Colori ARGB signed (.NET):

| Valore | Colore |
|---|---|
| `-1` | bianco |
| `-16777216` | nero |
| `-16776961` | blu |
| `-16744448` | verde |
| `-16711936` | lime (isto) |
| `-65536` | rosso |
| `-256` | giallo |
| `-4144960` | grigio canvas |
| `-8355712` | grigio scuro |

Font: `D11` piccolo, `D22` medio (altezza testo ~16 px), `D33` grande.

In *Finestra Proprietà* l’oggetto si chiama `n : TEXT` / `n : H ISTO` / `n : KEY` — `n` è `IdObj` sulla pagina. `Larghezza` / `Altezza` per WORD e H_ISTO sono **W×H veri**, non l’angolo opposto.

---

## 6. Tipi oggetto (verificati)

Palette UI (ordine in `Italiano.txt`): Testo, Linea, Cerchio, Rettangolo, Rett. arrotondato, Cornice, Cerchio pieno, Rettangolo pieno, H Istogramma, V Istogramma, Grafico, Pulsante, Variabile, Immagine, Tachimetro, …

Numeri nel `.lpk` **non** seguono l’ordine palette. Mappa da file + screenshot Pag.5:

| Tipo | Nome in Proprietà | Geometria nel `.lpk` | Note |
|---|---|---|---|
| 2 | TEXT | X Y **W×H** | `BackColor` riempie il box (titolo blu TRAVASO) |
| 3 | (linea) | `(X,Y)` → **`(Width,Height)` estremità** | `ImgGrafica` no. Usato in Pag.2 come riga orizzontale (`Y = Height`). Su Pag.5 `(0,0)→(320,24)` è uscito **diagonale blu** |
| 11 | (variabile WORD) | W×H | `IdVar` → anagrafica `WORD` |
| 14 | H ISTO | W×H | barra orizzontale; in Proprietà `17 : H ISTO` esempio oggetto 17 |
| 15 | (V ISTO) | W×H | tino Pag.0, `IdVar=0` |
| 16 | (GRAPH) | W×H | Pag.3 |
| 12 | IMAGE | W×H = bitmap | `Modo=DEL`, `IdVar` → `ImgGrafica_N`. Luna/sole TRAVASO |
| 17 | KEY | W×H | macro `MAC_PAGE` / `MAC_SETFLG` / `MAC_RESFLG` |
| 0 | **non verificato** | Pag.0 Obj.10 | non usare finché non si clicca in Proprietà |

`FILL RECTA` (rettangolo pieno in UI) **non** è Tipo 3. Numero `.lpk` **ancora sconosciuto**. Workaround verificato: Tipo 2 con `Width×Height` e `BackColor`.

La tabella in [`06_hmi_tp320.md`](06_hmi_tp320.md) che metteva 11=bargraph e 14=WORD era **invertita** rispetto a `IdVar` e allo screenshot.

---

## 7. Variabili PLC ↔ HMI

Due strati:

1. **`[Variabile_N]`** — nome, `TipoVar` (`WORD`, `H_ISTO`, `V_ISTO`, `GRAPH`, `MENU`, …), `IndirizzoVar=DATA.xxxx`, min/max, ENA/RFS/REMOTE.
2. **Oggetto** sulla pagina — `IdVar=N`.

Stesso DATA può avere due anagrafiche (es. `DATA.1000`: `V_ISTO` Id 0 e `WORD` Id 5). Pag.5: `DATA.2026` è sia `PROGRESS` WORD (Id 41) sia `BAR TRAVASO` H_ISTO (Id 44).

Esempio anagrafica (file di lavoro):

```
[Variabile_21]
Var_21_Nome=LT TRAVASO
Var_21_TipoVar=WORD
Var_21_IndirizzoVar=DATA.2006
Var_21_Minimo=0
Var_21_Massimo=5000
Var_21_CifreIntere=4
Var_21_ENA=True
```

Default di progetto **330 L**. `DATA.2006` è in RAM volatile (`< 4096`): all’accensione è 0 finché SETUP/TRAVASO o INITIALIZE (`MOV 330` se ancora 0) non lo caricano. Per tenerlo spento il PLC: copia in EEPROM (`DATA.4096+`) o NVDATA, poi FB Save EEPROM. Vedi documentazione CPU ARM su [kernelsistemi.it](https://www.kernelsistemi.it/).

In editor il campo WORD mostra `DATA_xxxx` e cuoricini al posto delle cifre (placeholder). Non è un errore di indirizzo.

H_ISTO barra TRAVASO (`BAR TRAVASO`, `IdVar=44`):

- `DATA.2026` = calo di livello (lo scrive il ladder quando la pompa è on)
- **REM** on: min = `DATA.2030` (ZERO, resta 0), max = `DATA.2006` (LT TRAVASO impostato in SETUP)
- **NORM** (`NormInv=False`) = riempie **da sinistra a destra**
- **RFS** on = la barra segue il valore restando sulla pagina; senza RFS si ridisegna solo all’ingresso pagina
- ENA off (non si scrive dal touch)

Lo strumento palette **filtra** il tipo: un oggetto WORD non elenca le `H_ISTO`.

Per una **lampada ON/OFF** non creare una seconda anagrafica. Stesso `IdVar` su ogni pagina: `LED_POMPA` è `[Variabile_1]` → `DATA.5000` (min 0 max 1), già usato su Pag.2 / HOME / TRAVASO. L’oggetto grafico **non** si condivide tra pagine: si copia quello di Pag.2 (24×24, `ForeColor=-65536` rosso, `BackColor=-16711936` lime) e si cambia solo X/Y. Un tasto K con `MAC_NULL` è solo un rettangolo fisso.

---

## 8. Testi e lingue

```
[Lingue]
NUM_LINGUE=2
Lingua_0=Italiano
Lingua_1=INGLESE
```

Ogni Tipo 2 ha **due** stringhe. `X_Lang` / `Y_Lang` possono differire (nel file di riferimento `EV` e `CARICO` non stanno nello stesso punto). Per H20 copiare la stessa stringa e le stesse coordinate su 0 e 1, finché non si fa la lingua inglese.

---

## 9. Come aggiungere una pagina

Fatto su Pag.5 (compile OK):

1. Copiare lo scheletro `[Pagina_N]` con `NomePagina`, attributi, sfondo.
2. Inserire il blocco **subito prima** di `[Allarme_0]` (dopo l’ultima pagina).
3. `N` = ultimo indice + 1, niente buchi.
4. Oggetti `IdObj` 0…k contigui, prefisso `Pag_N_Obj_M_`.
5. Se serve un tipo nuovo (`H_ISTO` per la barra): aggiungere `[Variabile_M]` **prima** di `[Lista Immagini]`, poi `IdVar=M`.
6. Aprire in LogicPaint, selezionare la pagina in albero, **Compila**.

TRAVASO è Pag.2; TRASD è Pag.5; CONTAT Pag.6.

Non copiare Tipo 3 sperando in una fascia piena.

Macro nav: `MAC_PAGE` e `PaginaDATA_P` **0-based** (HOME=0, FILL=1, TRAVASO=2, TANK/SETUP=3, MIX=4, TRASD=5, TOT/CONTAT=6).

---

## 10. Pulsanti (tasto K)

Due serializzazioni Nel file di riferimento Kernel:

| Stile | Chiavi | Dove |
|---|---|---|
| Icona libreria | `KeyTouch_-1_Immagine_P/R=` | Pag.0, Pag.2 |
| Forma + testo | `KeyTouch_0_` + `TextTouch_0_Keytext` | Pag.4 `MENU` |

Esempio senza nav: `KeyTouch_0` + `Keytext` da solo → rettangoli senza scritte; nav grigia invisibile. Vedi [`img_hmi/pag5_travaso_senza_nav.png`](img_hmi/pag5_travaso_senza_nav.png).

Schema **verificato** (compile OK, [`img_hmi/pag5_travaso_con_nav.png`](img_hmi/pag5_travaso_con_nav.png)):

1. Tipo 2: box `80×24` (nav) o `72×24` (AVVIA/STOP) con `BackColor` forte e `Testo`.
2. Tipo 17 sopra, **stesso** X Y W H, `Trasparente=True`, macro.
3. Z-order: prima il testo, poi il tasto.
4. Lampada POMPA: copia del H_ISTO Pag.2 (`IdVar=1`, 24×24, rosso/lime), solo X/Y diversi. Non una variabile nuova e non un tasto K.

Stesso schema per un’**icona cliccabile** (luna/sole, 24×24 in `(296,0)`):

1. Tipo 12 IMAGE (`Modo=DEL`, `IdVar` = indice bitmap, W×H = size `ImgGrafica`).
2. Tipo 17 sopra, stesso X Y W H, `KeyTouch_0_Trasparente=True`, `MAC_PAGE`.
3. Z-order: prima l’immagine (`IdObj` più basso), poi il tasto (ultimo oggetto della pagina va bene).

Non mettere i pixel sul KEY: `KeyTouch_-1_Immagine_P` mostra le icone **già in libreria** (Pag.0/Pag.2), non un `ImgGrafica` nuovo scritto a hex.

Esempio nav HOME (Pag.5, 80×24 in basso):

```
Pag_5_Obj_19_Tipo=2
Pag_5_Obj_19_X=0
Pag_5_Obj_19_Y=216
Pag_5_Obj_19_Width=80
Pag_5_Obj_19_Height=24
Pag_5_Obj_19_ObjText.Testo=0:HOME
Pag_5_Obj_19_ObjText.ForeColor=0:-1
Pag_5_Obj_19_ObjText.BackColor=0:-16776961
…
Pag_5_Obj_20_Tipo=17
Pag_5_Obj_20_X=0
Pag_5_Obj_20_Y=216
Pag_5_Obj_20_Width=80
Pag_5_Obj_20_Height=24
Pag_5_Obj_20_KeyTouch_0_Trasparente=True
Pag_5_Obj_20_KeyTouch_0_Macro_P=MAC_PAGE
Pag_5_Obj_20_KeyTouch_0_PaginaDATA_P=0
```

Macro già usate nel progetto:

| Macro | `PaginaDATA_P` significa |
|---|---|
| `MAC_PAGE` | indice pagina |
| `MAC_SETFLG` / `MAC_RESFLG` | numero FLAG (AVVIA/STOP → `203`) |
| `MAC_LANG` | Pag.1 |
| `MAC_NULL` | nessuna azione (OUT / lampada) — **compile OK** |

`PortaCOM_P=INTERNAL`, `IndPLC_P=1`.

---

## 11. Compilazione e invio

Menu italiano (`Italiano.txt`):

- **Compila**
- **Compila + Invia Applicazione**
- **Invia Applicazione**
- **Trasmetti Pagine** / **Trasmetti Setup + PLC**

Flusso help (*Getting Started*): Salva → Compila → Trasmetti. Cavo **mini-USB** = stessa COM del download.

Opzioni PC: *Opzioni → Porta COM*. Non è `COM1` RS232 del PLC: è la COM virtuale del mini-USB.

Dopo compile: *Controlla dimensione* (chiede se ricompilare). Sul file di lavoro il programma era ~7 % (17152 / 262143 byte).

Se i font sul pannello non coincidono: *Font Management → Compile and Send Font [F1]*.

Full Erase Flash (solo display 65536 colori): *File → Full Erase*, poi al download il pannello conta fino a 300 e carica. Non serve a ogni invio.

PLC in STOP/RUN: il download sostituisce applicazione in flash; i DATA volatili si perdono, EEPROM/NVDATA no se non si fa set default. Dettaglio da confermare sul TP 320 fisico.

Verifica a video: pagina iniziale `Term_Ini_Page=0`; tap su WORD con ENA → tastiera 7-8-9 … ENT. SETUP EEPROM è su `DATA.4100+` (ENT salva da Kernel). Livello da `DATA.417` (Filter INP 1, TP 320 /SCT).

---

## 12. Checklist pre-invio

- [ ] `Term_Nome=TP_320`
- [ ] File aperto è `Tino_H20.lpk`
- [ ] `[Pagina_N]` contigui da 0, oggetti `IdObj` contigui
- [ ] ogni `IdVar` su WORD/ISTO/GRAPH esiste come `[Variabile_N]` e il `TipoVar` coincide (WORD↔11, H_ISTO↔14, …)
- [ ] Tipo 12: `IdVar` = indice `ImgGrafica_N`, W×H oggetto = W×H bitmap
- [ ] nessun Tipo 3 usato come fascia / fondo (è una linea)
- [ ] tasti testo: etichetta Tipo 2 visibile + KEY per la macro
- [ ] tasti icona: Tipo 12 visibile + KEY trasparente sopra (non solo `Immagine_P` sul KEY)
- [ ] `MAC_PAGE` verso pagine che esistono
- [ ] **Compila** senza *Errore in Compilazione*
- [ ] *Controlla dimensione* pagine+programma sotto tetto
- [ ] COM mini-USB selezionata prima di Invia
- [ ] `Term_Ena_ANA=False` nel file; livello su `DATA.417` (TP 320 /SCT)

---

## 13. Aperti / da verificare

1. Retino sui KEY trasparenti: solo editor o anche sul TP 320?
2. Numero Tipo di **FILL RECTA** / rettangolo pieno: disegnarne uno in UI e leggere `Tipo=` nel `.lpk`.
3. Tipo 0 in Proprietà (Pag.0 Obj.10).
4. Indice Menu 0-based vs 1-based sul pannello.
5. Upload mini-USB: STOP/RUN, cosa resta in EEPROM.
6. ENA off su LIV/FLOW/ETA (oggi on: un tap apre la tastiera).
7. Nav 0–12 allineata (HOME/FILL/TRAVASO/SETUP + tab TANK/MIX/TRASD). Pag.6 VUOTA resta fuori nav.

Quando un punto si chiude con screenshot, aggiornare la tabella del §1 e toglierlo da qui.
