# lpk-tp320

Round-trip **HMI con un code agent**: l’agente scrive il `.lpk` come testo, questo tool mostra le pagine a 320×240, tu apri il file in [LogicPaint](https://www.kernelsistemi.it/) e fai **Compila / Invia** sul **TP 320**.

LogicPaint resta l’unico compilatore. Qui si vede in fretta se layout, colori e nav tornano, così l’agente si autocorregge prima che tu ricarichi l’editor.

English: design Kernel LogicPaint HMI with a code agent (`.lpk` is text). Preview TP 320 pages, then compile in LogicPaint. Not a firmware toolchain.

## Flusso

```
agente  →  .lpk (testo)  →  lpk-tp320 (PNG / HTML)  →  LogicPaint Compila  →  TP 320
                ↑                    │
                └──── screenshot / preview ─────────┘
```

1. L’agente modifica `[Pagina_N]`, variabili, `ImgGrafica`.
2. `preview.py` genera `pag_N.png` e `index.html` (click sui `MAC_PAGE`).
3. Tu ricarichi il `.lpk` in LogicPaint (se era aperto: non risalvare sopra), **Compila**, invii al pannello.

Il `.lpk` è già un formato testuale (INI). LogicPaint non ha un viewer headless: questo lo copre.

Oggi la cartella sta in `tools/tp320_preview/` nel repo **[tp320-osmosi-tino-mix](https://github.com/pierpidc-bot/tp320-osmosi-tino-mix)**. È fatta per **staccarsi** in un pacchetto suo (niente dipendenze dal ladder del tino).

## Requisiti

- Python 3.10+
- [Pillow](https://pypi.org/project/Pillow/)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\pip install -r requirements.txt
# Unix:
.venv/bin/pip install -r requirements.txt
```

Oppure: `pip install -e .` (espone il comando `lpk-tp320`).

## Uso

```bash
# Windows, da questa cartella:
.venv\Scripts\python preview.py percorso\progetto.lpk
.venv\Scripts\python preview.py percorso\progetto.lpk --open
.venv\Scripts\python preview.py percorso\progetto.lpk -o out --scale 2

# Nel repo Tino H20, senza argomenti usa Proj/Tino_H20.lpk
.venv\Scripts\python preview.py
```

Output in `out/` (o `-o`):

- `pag_0.png` … `pag_N.png` — pagine a 320×240 × scala
- `index.html` — elenco pagine; click sui KEY `MAC_PAGE` per cambiare pagina

## Cosa disegna (v0.1)

| Tipo `.lpk` | Oggetto LogicPaint |
|---|---|
| 2 | TEXT |
| 3 | linea |
| 11 | WORD (etichetta DATA + placeholder cifre) |
| 12 | IMAGE (`ImgGrafica_N`) |
| 14 | H ISTO (barre e LED 24×24) |
| 15 | V ISTO |
| 16 | GRAPH (box vuoto) |
| 17 | KEY (retino editor; nav/AVVIA/STOP riempiono il BackColor) |

Colori ARGB signed .NET come nel file (`-1` bianco, `-16777216` nero, …). Font D11/D22/D33 approssimati (bitmap 5×7 scalato), non i glifi originali Kernel.

## Cosa non è (e non sarà il passo 1)

- Compilatore / invio al pannello — quello è LogicPaint
- Runtime del TP 320 (DATA live, tastiera numerica)
- Font Kernel pixel-perfect
- Emulatore di **allarmi** o **ladder** — eventuale passo 2; il ladder Kernel potrebbe convenire via **AWL** piuttosto che dal dump `.lpk`

## Formato `.lpk`

Il file inizia con `LogicPaint`. Pagine `[Pagina_N]`, variabili `[Variabile_N]`, bitmap in `[Lista Immagini]`:

```
ImgGrafica_N=<5 cifre W><5 cifre H><pixel RGB24 hex>
```

Note di formato nate sul campo (TP 320, LogicPaint 2.0.5.x) restano documentate nel repo Tino H20, `doc/guide/03_formato_lpk_agente.md`, finché questo tool non ha una guida propria.

## Licenza

MIT — vedi [LICENSE](LICENSE). LogicPaint, TP 320 e Kernel Sistemi sono marchi dei rispettivi titolari; questo progetto non è affiliato.

## Dopo (quando il viewer HMI è solido)

- Font più fedeli (glifi da screenshot)
- Menu / tipi ancora non mappati
- Pacchetto PyPI, test su `.lpk` di esempio (senza impianti)
- Semmai: preview allarmi; ladder solo se ha senso (valutare AWL)
