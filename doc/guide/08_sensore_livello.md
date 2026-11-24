# Sensore di livello (pressione) e problema portata

Acqua a 20 °C: **1 bar ≈ 10,2 m** di colonna (≈ 1020 cm). Geometria confermata dal costruttore (Ø interno 1270 mm): `CIRC 399 cm`, area ≈ 12 668 cm² → **12,667 L/cm**, cono inferiore 77 L. `OFFSET` **85 L**, confermato: 77 L di cono più ~8 L in rubinetti e raccordi a valle. Tabella di taratura costruttore del serbatoio e derivati: [`Tino_H20.md`](../Tino_H20.md).

Pressione sopra il sensore a tino pieno 2500 L:

- altezza ≈ 191 cm → **≈ 0,187 bar**
- OFFSET 85 L ≈ 6,7 cm → ≈ 0,007 bar

Il tino vive tutta la vita sotto **0,2 bar**.

## Posizione del sensore: quota 0

Il trasduttore è montato **alla quota 0 dell'asta, dove finisce il cono**, cioè sulla base del cilindro. Posizione confermata in campo.

Coincide con l'origine della tabella di taratura costruttore del serbatoio, quindi il sensore misura esattamente la `h` del modello del costruttore su un tratto tutto cilindrico: **`LIV = OFFSET + A × h` è esatto**, non un'approssimazione, e non serve alcuna linearizzazione a tratti.

Il cono resta sotto il sensore e non produce pressione misurata. Se il trasduttore fosse stato sul punto più basso avrebbe visto i suoi 18,2 cm (`3V/A = 3 × 77 000 / 12 668`), che il modello avrebbe contato come ≈ 231 L invece di 77: fino a ~154 L di sovrastima a tino quasi vuoto. Rischio escluso.

Due conseguenze operative:

- Sotto la quota 0 la pressione è nulla e il programma mostra `OFFSET` fisso. Gli ultimi 85 L non sono misurabili per costruzione: da qui la coda TRAVASO a `OFFSET` (`FLAG.234`) e il dead-point FLOW a `OFFSET + BANDA MORTA`.
- Svuotando fino alla quota 0 si ha un punto di taratura netto per `ZERO 4mA`: `DATA.417` deve leggere il valore di zero (default 816 count).

## Sensore attuale (in campo)

| Voce | Valore |
|---|---|
| Lettura etichetta | **Riels RIB100-C8C** (da verificare sul corpo: il codice ordine standard Riels è `RIB100` + range + uscita + connettore) |
| Range confermato dall’utente | **0 … 2 bar** relativo |
| Uscita | **4 … 20 mA**, 2 fili, 10…30 Vdc |
| Famiglia | Riels RIB100, ceramica, precisione tipica **±0,5 % FS** (max ±1,0 % FS) |
| Scheda | documentazione PDF Kernel ([kernelsistemi.it](https://www.kernelsistemi.it/)) (Riels, range catalogo ceramico **da 2 bar a 100 bar**, codice range `06` = 0…2 bar) |
| PLC | ingresso analogico **0–20 mA** (codice TP 320 **/SCT**). Nel ladder iniziale lo zero 4 mA è sottratto come costante **816** count (`816/4096 ≈ 4 mA / 20 mA`) su `DATA.417` |

Il suffisso `C8C` non compare nella tabella d’ordine del PDF OEM (lì l’ordine è tipo `RIB100 / 06 / G / S1 / E1`). Resta valido ciò che hai letto sul campo: **0–2 bar, 4–20 mA**.

## Sensore nuovo (acquistato)

| Voce | Valore |
|---|---|
| Range | **0 … 0,3 bar** (300 mbar) |
| Motivo | coprire ~1,5–2 m d’acqua con buona frazione di fondo scala |
| 20 mA = 0,3 bar | ≈ 3,06 m H2O ≈ **3870 L** sopra il sensore (CIRC 399) |
| Overrange tino | un tino da 2500 L **non può** arrivare a 0,3 bar: il nuovo FS è largo ma usabile |

`0…0,3 bar` **non** è nel PDF ceramico OEM (quel PDF parte da 2 bar). È un range basso, coerente con le varianti 300 mbar elencate sulla pagina prodotto Riels. Dopo il montaggio annotare modello esatto, FS, 4–20 mA, attacco e connettore.

## Perché 0–2 bar rendeva il programma inutilizzabile

Il tino usa **0,187 / 2 ≈ 9,4 %** del fondo scala. Il resto è “aria” di misura. Valori con la geometria confermata (12,667 L/cm):

| | RIB100 0–2 bar | Nuovo 0–0,3 bar | Rapporto |
|---|---|---|---|
| Uso del FS a 2500 L | 9,4 % | 62 % | ×6,7 |
| Errore tipico ±0,5 % FS | **0,01 bar ≈ 129 L** | **0,0015 bar ≈ 19 L** | ×6,7 |
| 1 count ADC 12 bit (span 4–20 mA ≈ 3280 count) | **≈ 7,9 L** | **≈ 1,2 L** | ×6,7 |
| Rumore 1 count in 1 s → “portata” | **±28 000 L/h** | **±4 300 L/h** | stesso rapporto |

L’auto-apprendimento `FLOW = dL/dt × 3600` su un LSB da 8 L a ogni secondo **non è una portata**: è il rumore del convertitore. Da qui l’**enorme fluttuazione** vista in campo. `SMORZAMENTO SEC` (IIR 1 Hz) e campionamento più lento (2–5 s, non 1 s) servono **anche** col 0–0,3 bar.

Attenzione a come si legge questa tabella: la riga "errore tipico" viene dal ±0,5 % FS di catalogo applicato alla geometria confermata, **non da una misura**. La riga "1 count ADC" invece è geometria pura e non dipende dal sensore. **L'errore reale è da rilevare con un test in campo** su più punti della scala, dopo aver ritarato `ZERO 4mA` alla quota 0. Il confronto 0–2 bar / 0–0,3 bar regge comunque, perché è un rapporto di fondo scala: qualunque sia l'errore misurato, il nuovo sensore lo riduce di ×6,7.

## Cosa non funzionava nel ladder di partenza

Net.0 **non è vuoto**: scalatura analogico → litri (`DATA.417` − 816, poi area/divisore → `DATA.1000`), emergenza, LED uscite, pagina MANUALI.

Non c’è (o non tiene) la sequenza **FILL osmosi→rete**, **travaso a litri noti**, mix durezza, ETA, auto-apprendimento portate. Sospetto allineato ai fatti:

1. **Portata instabile** → stop/start e apprendimento `LT/H` inservibili.
2. **Automatismi FILL/TRAVASO assenti o non chiusi** — le pagine sono stato/manuale/scalatura, non ricette.
3. `Term_Ena_ANA=False` nel `.lpk` mentre il ladder legge `DATA.417` è **corretto** (come in campo). Non serve alcuna voce analogica in *Opzioni progetto* LogicPaint su TP 320 /SCT.

Il file di riferimento si tiene come **base I/O + scalatura**, non come automazione di processo funzionante.

## Scalatura da usare col 0–0,3 bar

Non impostare 20 mA = 3000 L a caso. Il 20 mA è **0,3 bar**.

```
bar      = (count - 816) / 3280 * 0.3
h_cm     = bar * 1020
V_sopra  = h_cm * AREA_cm2 / 1000
LIV      = OFFSET + V_sopra
SMORZ    = (OLD*(T-1) + NEW) / T   → DATA.2007  (T = SMORZAMENTO SEC, default 3, ogni 1 s)
```

La barra HOME ha max = **LT TOT** (`DATA.2012`), non il 20 mA del trasduttore e non `F.SCALA 3000`. HOME mostra il filtrato in continuo (RFS). Dettaglio: [`Tino_H20.md`](../Tino_H20.md) § HOME.

In HMI la scelta 0–2 / 0–0,3 bar si fa con l’oggetto **Menu** (elenco), 2 righe, indice in un DATA dedicato — mai `DATA.1000`. Dettaglio UI: [09_guida_grafica_hmi.md](09_guida_grafica_hmi.md) §10.

Portata: **non** da `dL/dt`. I LTH sono le misure in [`Tino_H20.md`](../Tino_H20.md), battute in SETUP MIX. FLOW a video e ETA copiano quei valori. Vedi [`Tino_H20.md`](../Tino_H20.md) §5.5.

## Cablaggio 4–20 mA (2 fili, DIN43650 tipico)

- Pin 1 `+Vcc` (24 Vdc dal quadro)
- Pin 2 `OUT` verso ingresso analogico TP320 **0–20 mA**
- Massa comune quadro / PLC

Verificare polarità: Riels indica *reverse polarity: no damage – no function*.
