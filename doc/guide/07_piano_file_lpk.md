# Piano per il file `.lpk` caricabile

Obiettivo: un `.lpk` che si apre in LogicPaint 2.0.5.3, compila, e si trasmette al TP 320 via mini-USB.

File di lavoro: `Proj/Tino_H20.lpk` (Net.0) e gemello AWL `Proj/Tino_H20_AWL.lpk`. Contratto v1.00: [12_h20.md](12_h20.md). ADC INP 1 → `DATA.417`, codice **/SCT**.

## Principio

Non fidarsi della portata stimata da `dL/dt`: in campo oscillava (RIB100 0–2 bar). Le portate in SETUP sono le **misure documentate** ([Tino_H20.md](../Tino_H20.md) §3). FLOW a video e ETA usano quei LTH, senza apprendimento. Misura litri e ricette per il sensore **0–0,3 bar**, interi, LONG solo su scratch `1200+`. Nucleo tenuto: latch emergenza, **solo** `INP.01` → `DATA.08` bit 1 (pagina Alr), beep `DATA.01`. Vedi [08_sensore_livello.md](08_sensore_livello.md) e [04_mappa_progetto.md](04_mappa_progetto.md).

## Mappa

**EEPROM** `4100`–`4125`: SETUP (CIRC, LT TOT, OFFSET, ALLARME, mix, SMORZ SEC, FS bar, LTH, T STAB, LT TRAVASO, ZERO 4 mA, banda, campionamento, TIMEOUT MIN) + LONG totali. Default se `SYS.02` e `4100=0`. Specchio RAM ogni ciclo verso `2010`–`2022`, `2006`, `2029`, `2044`, …

**RAM** `2004`–`2037`: target FILL, Vo/Vn, livello filtrato, FLOW/ETA, barre, lampada MAN. `2040`–`2043` LED. `1000` = copia di `2007`.

Filtro: `2007 = (2007 * (T−1) + 2028) / T` ogni `SYS.10` (1 s). `T` = `2016` = `SMORZAMENTO SEC` (default 3, range 1–15). `T=1` passa il grezzo. EEPROM `4106` fuori 1–15 (vecchio %) → 3.

FS: `4107` specchiato in `2017` (3 → 0,3 bar, 20 → 2,0). `4116` = TIMEOUT minuti (0 = watchdog off).

## Mix

```
Vn = Lt * Ht / Hn
Vo = Lt - Vn
```

Clamp: `Ht > Hn` → 100% rete; `Hn=0` o `Ht=0` → 100% osmosi.

FLOW a video = LTH di SETUP dello step in corso. ETA = residuo×60/LTH. Coda TRAVASO sotto OFFSET: sempre `LTH TRAVASO` (`2021`). `CAMP SEC` non è usato.

## Sequenza FILL (`FLAG.200`)

1. Mix Vo/Vn in `2008`/`2009`
2. Se `FLAG.210` o non `FLAG.01` o MAN → abort
3. STEP1 OSMOSI (`OUT.02`) fino a Vo − TOLL (se Vo=0 o Vo < TOLL → salta OSM)
4. Pausa T STAB (`SYS.10` + `DATA.2037`)
5. STEP2 RETE (`OUT.01`) fino a LT TARGET
6. `FLAG.220` → salva EEPROM `4100`–`4125` (`SYS.20`)

## Sequenza TRAVASO (`FLAG.203`)

Se `2007 < 2006` → `FLAG.212`, non parte: fronte AVVIA apre Pag.16/17 (`WARN VUOTO`), OK (`FLAG.181`) ripristina `DATA.2062`. Altrimenti snapshot `2027`, `OUT.00`, `2026 = 2027 − 2007` fino a `2026 >= 2006`. Sotto OFFSET, se ancora corto: coda a tempo `FLAG.234` (LTH TRAVASO). Vedi [12_h20.md](12_h20.md).

Pieno: se `2007 > ALLARME` → RES `OUT.01` e `OUT.02`, lascia `OUT.00`, `FLAG.211`.

## MAN MODE

Tasto HOME `MAC_SETFLG`/`MAC_RESFLG` impulso `FLAG.254` → ladder inverte `FLAG.204` sul fronte 0→1 (dito tenuto non ritoggla). OSM/RETE/TRAV: impulsi `185`/`186`/`187` → `205`/`206`/`207` solo se `204=1`. Non usare FLAG 255+ sull’HMI (`0xFF` / wrap). Lampada `DATA.2020`.

- Se `204=0`: ogni scan `RES` 205/206/207 (i tap HMI non devono accodare un comando che parte quando si riaccende MAN). Fronte 1→0: RES OUT 00–03 e FLAG 200–203, 205–207.
- Se `204=1`: OSM/RETE seguono 205/206 **solo se** `FLAG.211=0`; pompa (`207` / `OUT.00`) non è bloccata dal pieno.
- Se `FLAG.211`: RES 205 e 206 (LED OSM/RETE spenti, niente coda). `207` resta.

## HOME — RFS e litri

Litri `IdVar=5` (`DATA.1000`), `%` `IdVar=38` (`DATA.2023`), barra `IdVar=46` (REM max `2012`), lampada MAN `IdVar=47`: **RFS=True**, ENA off. `LIVELLO REAL` è **WORD_WIDE** 16 bit (non LONG: eviterebbe di leggere `DATA.1001`). Lampade uscite 1–3: RFS on, ON=lime / OFF=nero.

## Verifica in LogicPaint

- Compila (`Pag.0 : HOME` nell’albero). Lasciare analogica **OFF** nel file; *Controlla dimensione*.
- Emergenza spegne ricette e OUT 00–03; `OUT.04` segue `FLAG.01`.
- AVVIA FILL bloccato se target > allarme; pieno chiude OSM/RETE non pompa; travaso vuoto non parte.
