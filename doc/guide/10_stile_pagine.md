# Stile pagine H20 — TRAVASO come riferimento

Display **320 × 240**. Griglia editor **6 × 8**. Origine **(0,0)** in alto a sinistra.

**Palette scura unica (H20 v1.00).** Pagine **0–10**, senza gemelle chiaro/scuro.

Questa guida è il **come si fa una pagina nuova**. Oggetti: [`09_guida_grafica_hmi.md`](09_guida_grafica_hmi.md).

---

## 1. Un tema per pagina

LogicPaint non ha fogli di stile. `Pag_N_ColoreSfondo` è fisso per ogni pagina.

---

## 2. Chrome comune (ogni pagina ricetta)

Area utile contenuto: **Y = 24 … 215**. Nav fissa in basso.

| Elemento | Geometria | Note |
|---|---|---|
| Titolo | `(12, 4)` **84 × 16**, font `D22`, testo bianco | Solo il nome pagina, allineato a sinistra. Non barra a tutta larghezza. |
| MAN (HOME/FILL/TRAV) | `(210, 0)` **40 × 24** | `BIT_STR` ON/OFF + testo `MAN`. KEY `FLAG.254`. |
| Nav | Y = **216**, quattro tasti **80 × 24** a X = `0 / 80 / 160 / 240` | Etichette `HOME` `FILL` `TRAV` `SETUP`. Testo Tipo 2 + KEY `Trasparente=True`. |
| Tab attiva | testo nero, fondo **`-256`** (`#FFFF00`) | Giallo elettrico `#FFFF00`. |
| AVVIA / STOP | hit-area **72 × 24**; etichetta ~60 × 16 | AVVIA verde, STOP rosso. KEY sopra il testo. |

Non rimettere `TANK A->B` né altre scritte decorative in alto a destra.

---

## 3. Palette (valori `.lpk`)

| Ruolo | ARGB signed | Hex |
|---|---|---|
| Sfondo pagina | `-16777216` | `#000000` |
| Titolo | `-1` su `-16750904` | bianco su `#0066C8` |
| Etichette | `-1` su nero | bianco |
| Unità / accento | `-4064769` | ciano `#C1F5FF` |
| WORD | `-1` su nero, BOX `-16750904` | bianco, bordo blu elettrico |
| Barra H_ISTO | fill `-14900267`, fondo `-16771033` | `#1CA4D5` su `#001827` |
| AVVIA | lime su `-13619152` | su grigio `#303030` |
| STOP | rosso su `-13619152` | non rettangolo pieno rosso |
| Nav inattiva | `-1` su `-16767912` | bianco su navy `#002458` |
| Tab attiva | nero su `-256` | `#FFFF00` |
| Griglia editor | `-16767912` | navy (solo editor) |

LED pompa: **non ricolorare** (rosso/lime restano leggibili sullo sfondo).

---

## 4. Ricette oggetto

| Bisogno | Cosa mettere | Z-order |
|---|---|---|
| Etichetta | Tipo 2, `D22`, `BOX=False` | — |
| Numero | Tipo 11 WORD, ~**72 × 24**, `D11`, `BOX=True` | — |
| Tasto con scritta | Tipo 2 visibile + Tipo 17 `KeyTouch_0_Trasparente=True` stesso X Y W H | prima testo, poi KEY |
| Icona cliccabile | Tipo 12 `Modo=DEL` + KEY trasparente | prima IMAGE, poi KEY |
| Progresso | Tipo 14 H_ISTO, `RFS` on se deve muoversi restando sulla pagina | — |
| Lampada ON/OFF | H_ISTO 24×24, stesso `IdVar` delle altre pagine | non un KEY |

Non usare Tipo 3 come fascia. Non attaccare un `ImgGrafica` nuovo al KEY (`Immagine_P`): non si vede.

Lingue: copiare **stesso** testo e coordinate su `=0:` e `=1:`.

---

## 5. Come nasce una pagina nuova

1. Disegnare la pagina con chrome §2 e palette §3, stessi `IdVar` già in anagrafica (o nuova `[Variabile_N]` prima di `[Lista Immagini]`).
2. **Compila** in LogicPaint. Se il `.lpk` è aperto, ricaricare dopo edit a testo; non risalvare da editor sopra le modifiche.
3. Controllare indici `MAC_PAGE` coerenti con [12_h20.md](12_h20.md) (0–10).
4. Nav: tab attiva gialla; SETUP con linguette `TANK | MIX | TRASD | TOT` (pagine 3–6).
5. Compila di nuovo.

`NomePagina`: es. `HOME`, `FILL`, `TRAVASO`, `TANK`, senza suffissi gemella.

---

## 6. Indici pagina (v1.00)

Nav: HOME 0, FILL 1, TRAV 2, SETUP 3. Tab SETUP: TANK 3, MIX 4, TRASD 5, TOT 6. REFILL 7, WARN VUOTO 8, WARN LT 9, WARN DUR 10.

Linguette SETUP: TANK X=80 W=48, MIX 132/44, TRASD 180/52, TOT 236/48.

**CONTAT** — tre righe OSMOSI / RETE / TRAVASO, LONG litri, tasto AZZERA. Chrome SETUP. Dettaglio: [12_h20.md](12_h20.md).

---

## 7. Checklist

- Titolo `(12,4) 84×16`, non barra piena larghezza.
- Nav Y=216; tab attiva gialla.
- MAN solo dove previsto (HOME/FILL/TRAV).
- Nessun secondo rung illegale in ladder (vedi [12_h20.md](12_h20.md)).