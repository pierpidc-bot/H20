# Mappa del progetto `Tino_H20.lpk` (v1.00)

`InfoVersione=H20-v1.00`. Contratto: [12_h20.md](12_h20.md). Generatore: `python tools/h20_apply_plan.py`. Nel `.lpk` lasciare `Term_Ena_ANA=False`.

## Pagine HMI (0–10, palette scura)

Niente luna/sole. Nav: HOME | FILL | TRAV | SETUP.

| Pagina | Nome | Ruolo |
|--------|------|--------|
| 0 | HOME | Litri, %, lampade, MAN OFF/ON, OSM/RETE/TRAV |
| 1 | FILL | RESET 268, mix↔cm, AVVIA 238 / STOP. OSM/RETE in MAN |
| 2 | TRAVASO | LT, AVVIA 196. Pompa MAN |
| 3 | TANK | SETUP tino + CARICA DEFAULT |
| 4 | MIX | H/DUR, TOLLERANZA LT |
| 5 | TRASD | ZERO, banda, TIMEOUT |
| 6 | CONTAT | Totali LONG |
| 7 | REFILL | Durezza litri presenti, SI/NO |
| 8 | WARN VUOTO | START TRAVASO con LIV < LT |
| 9 | WARN LT | Target litri non maggiore del livello |
| 10 | WARN DUR | Mix durezza/litri impossibile |

## I/O di quadro

Confermata da `Schema elettrico gestione reintegro.pdf` (fogli 51–52, lista cavi) e dalle etichette della pagina MANUALI di *(programma di campo precedente, non pubblicato)* (= `programma di campo consegnato` del cliente). Il revamping **non tocca il cablaggio**.

| Punto | Organo di quadro | Funzione | Codice attuale |
|---|---|---|---|
| `OUT.00` / Q0 | KM1 → pompa travaso P2 | Travaso | Travaso |
| `OUT.01` / Q1 | KA1, contatto pulito 5220/5221 | **Spare** | Spento ogni scan |
| `OUT.02` / Q2 | KA2, contatto pulito 5240/5241 | **Osmosi** | Osmosi |
| `OUT.03` / Q3 | YV1 elettrovalvola riempimento | **Rete** | Rete (niente OR) |
| `OUT.04` / Q4 | SH1, lampada pulsante | Spia `FLAG.01` | Spia |
| `INP.00` / E0 | QM1 magnetotermico pompa | TERMICO POMPE (Alr.0) | idem |
| `INP.01` | fungo emergenza | EMERGENZA (Alr.1) | idem |
| `INP.02` / E2 | *probabile* J18 S-RO; in campo morsetto vuoto | ALLARME OSMOSI (Alr.2) | idem — cavo non sbarcato |
| `INP.03` / E3 | SH1 pulsante blu | RESET BLU `SET FLAG.00` | idem |
| `DATA.417` | LV1 trasduttore, ADC1 | Livello 4–20 mA | idem |

Simbolici: `INP.00=TERMICO POMPE`, `INP.01=EMERGENZA`, `INP.02=ALLARME OSMOSI`, `INP.03=RESET BLU`. Contratto: [`../Tino_H20.md`](../Tino_H20.md) §3.3.

Consenso verso il programmatore S-RO: RUN J7 **29–30** (contatto KA2 / `5240–5241`). Non ponticellare J4 (MAX LEV) chiuso: l'S-RO resterebbe in standby (tino pieno).

## Allarmi (`DATA.08`)

Pagina rossa Kernel (blocca il touch): **solo Alr.1 emergenza**. Tutto il resto è warning + sicurezze in ladder; le pagine restano usabili. Beep: `DATA.08 ≠ 0` → `DATA.01` (quindi solo fungo).

| Slot | Testo | Bit `DATA.08` | Trigger | Sicurezza (senza bloccare l’HMI) |
|------|-------|---------------|---------|----------------------------------|
| Alr.0 | *(non usato)* | — | `INP.00` termico | Pompa e ricette OFF |
| Alr.1 | EMERGENZA PREMUTA | **1** | `INP.01` NC | Unica pagina allarme. OUT 00–03 OFF, `FLAG.00` RES |
| Alr.2 | *(non usato)* | — | `INP.02` allarme osmosi | Niente OSM (`OUT.02`); FILL esce da STEP1 |
| Alr.3 | *(non usato)* | — | `FLAG.210` target > allarme | FILL/REFILL non partono |
| Alr.4 | *(non usato)* | — | `FLAG.211` troppo pieno | RES OSM/RETE, no FILL/REFILL |
| Alr.5 | *(non usato)* | — | `FLAG.212` travaso vuoto | TRAVASO non parte; Pag.16/17 + OK |
| Alr.6 | *(non usato)* | — | `FLAG.228` stallo FILL | OUT 00–03 OFF |
| Alr.7 | *(non usato)* | — | `FLAG.229` stallo TRAVASO | OUT 00–03 OFF |

Avviso HMI (lampade HOME) da aggiungere al generate.

## Variabili HMI (punti toccati)

| Id | Nome | Tipo | DATA |
|----|------|------|------|
| 1–4 | LED pompa/rete/osmosi/EV | H_ISTO | **2040–2043** (RAM, specchio OUT; non EEPROM `5000`) |
| 5 | LIVELLO REAL | WORD **16 bit** | 1000 |
| 6 | AREA TANK | WORD **16 bit** | 2000 (niente overlap con `2001`) |
| 21 | LT TRAVASO | WORD | **4112** (EEPROM; specchio runtime `2006`) |
| 25–37 | SETUP | WORD | **4100+** (CIRC, LT TOT, OFFSET, ALLARME, DUR, TOLL, SMORZ SEC, FS BAR, LTH, T STAB) |
| 44 | barre TRAVASO | H_ISTO | REM max **2006** (RAM; non `4112`) |
| 45 | ZERO barre | WORD | 2030, max=1 |
| 46 | TANK HOME | V_ISTO | 1000, REM max **2012**, **INV** (dal basso) |
| 50–52 | ZERO 4 mA / BANDA / CAMP | WORD | **4113–4115** |
| 53 | barre FILL | V_ISTO | REM max **2012** |
| 54 | TIMEOUT MIN | WORD | **4116** (0–60) |
| 55–57 | TOT OSM / RETE / TRAV | WORD **LONG_WIDE** | **4120 / 4122 / 4124** |

Anagrafiche vecchie (`2105`, `3100`, `6000`/`6001`, `8000`–`8004`) non sono più usate dal ladder.

## Ladder

| Rete | Titolo | Stato |
|------|--------|--------|
| Net.0 | Area Programma Principale | emergenza, FILL, TRAVASO (un solo main) |
| Net.1 | Fine del programma principale | **END + SBR INITIALIZE** |
| Net.2 | Area Subroutine | Vuota |

Niente CAMME `888`–`951`, niente `LMOV` su `417`, niente write EEPROM ogni ciclo. LONG solo su coppie scratch `1200`–`1223`.

Istruzioni nel Net.0: `MOV`, `CMP`, `ESUB`, `LESUB`, `LEMUL`, `LEDIV`, `DIV`, `MUL`, `SET`, `RES`. Niente `EADD`/`LEADD` (KeyNotFound). Somma = `ESUB`/`LESUB` con zero in `DATA.2030`. `DIV`/`MUL` sovrascrivono il secondo operando.

## FLAG

Non toccare `00`/`01`, fascia `100`–`104` (logica vecchia ritirata), `300`, `1998`–`2047` (FB).

| FLAG | Ruolo |
|------|--------|
| 00 / 01 | reset emerg / EMERGENZA OK |
| 200 / 201 / 202 | FILL run / STEP1 OSM / STEP2 RETE |
| 203 | TRAVASO run |
| 185 / 186 / 187 | impulso HMI OSM / RETE / TRAV (SET al tocco, RES al rilascio) |
| 196 / 197 | impulso AVVIA / STOP TRAVASO |
| 180 / 181 / 178 | pagina WARN VUOTO / impulso OK / prev OK |
| 198 | impulso STOP FILL |
| 268 | impulso RESET FILL (abort job, tiene i target) |
| 238 | impulso AVVIA FILL / REFILL |
| 204 | MAN MODE |
| 254 | impulso HMI MAN |
| 205 / 206 / 207 | toggle MAN osmosi / rete / pompa (ignorati se `204=0`) |
| 208 / 209 | FILL STAB / MAN precedente (fronte 1→0) |
| 210 / 211 / 212 | alr target / pieno / vuoto |
| 220 / 221 | salva EEPROM / default (virgin o CARICA DEFAULT) |
| 214–227 | temporanei di scan (mix, step, TRAV LIV OK, LTH NZ) |
| 228 / 229 | stallo FILL / TRAVASO |
| 230 / 231 / 232 | richiesta OUT pompa / rete (`OUT.03`) / osmosi (`OUT.02`) |
| 253 | CARICA DEFAULT (HMI SETUP TANK) |
| 234 | TRAVASO coda OFFSET |
| 235–237 | AZZERA tot OSM / RETE / TRAV |
| 243, 246–248 | temporanei di scan (OFFSET, coda, stallo) |
| 249 | solo ladder: bobina sink su ogni CMP (senza → `plc_comp` Stack ERROR). Compila: [12_h20.md](12_h20.md) §9 |
| 262–264 / 267 | migrate `DUR RETE` al `SYS.02` (vecchio intero / ×10 / zero / `>500`) |
| 265 | `DATA.08 ≠ 0` → `BOUT` bit 1 di `DATA.01` (beep). Non scrivere la word `DATA.01` |

## DATA: EEPROM SETUP `4100`–`4125`

Salvataggio: fronte `FLAG.220` (fine FILL/TRAVASO, stallo, AZZERA) → `DATA.58`/`59` e `DATA.8142`/`8143` = 4100…**4125**, `SET SYS.20`. ENT da tastiera su WORD EEPROM scrive già il Kernel. Ogni ciclo: copia `4100+` → specchi RAM `2010`–`2022`, `2006`, `2029`, `2044`, … usati da barre e ricette. Vedi [12_h20.md](12_h20.md).

Valori di fabbrica con range HMI e motivazione: [`Tino_H20.md`](../Tino_H20.md). Il generatore scrive gli stessi numeri.

| DATA | Parametro | Fabbrica |
|------|-----------|---------|
| 4100 | CIRC cm | **399** |
| 4101 | LT TOT | 2500 |
| 4102 | OFFSET | **85** |
| 4103 | ALLARME LIV | 2400 |
| 4104 | DUR RETE F | **24** °F (interi; migrazione da EEPROM in decimi al primo avvio) |
| 4105 | TOLL MIX L | 20 |
| 4106 | SMORZAMENTO SEC | 3 |
| 4107 | FS BAR (3=0,3 bar, 20=2,0) | 20 |
| 4108 | LTH RETE | **22** L/m |
| 4109 | LTH OSMOSI | **7** L/m |
| 4110 | LTH TRAVASO | **26** L/m |
| 4111 | T STAB s | **30** |
| 4112 | LT TRAVASO | 330 |
| 4113 | ZERO 4 mA counts | **786** |
| 4114 | BANDA MORTA L | 20 |
| 4115 | CAMP SEC | 3 |
| 4116 | TIMEOUT MIN (0=off) | **20** |
| 4120–4125 | LONG tot OSM / RETE / TRAV | 0 |

Ricetta v1.00 in RAM volatile, ricaricata a ogni `SYS.02`: `2004` LT TARGET **2300**, `2005` DUR TARGET **8** °F. Su pannello già inizializzato: tasto CARICA DEFAULT in SETUP TANK (`FLAG.253`). `DUR RETE` EEPROM `51…500` (vecchi decimi) viene portato in intero al primo scan. FILL: cm colonna `2063`/`2064`; se si editano i cm il PLC ricalcola Lt/Ht.

## DATA runtime (volatile 0–4095)

`1000` display (= `2007`); `2000` AREA; `2001` h cm; `2004`–`2037` processo; `2038–2039` stallo; `2040`–`2043` LED; `2044–2049` TIMEOUT/coda/totali; `1200`–`1223` LONG scratch; `2050`–`2057` appoggi 16 bit; `2063`/`2064` cm osmosi/rete FILL; `2065`–`2069` snapshot ricetta.

Canale ADC: Filter INP 1 = `DATA.417` (codice hardware **/SCT**).

## Function Block

`FB..0` Save EEPROM — Read Only. Net.0 imposta il range e `SYS.20` (stesso meccanismo del FB).
