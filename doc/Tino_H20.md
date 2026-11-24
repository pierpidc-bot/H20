# Tino H20 — Specifica di progetto

PLC visualizzato Kernel **TP 320** + LogicPaint per l’impianto acqua di un **birrificio artigianale**.  
Obiettivo: un file `.lpk` compilabile e trasmissibile che gestisca riempimento, miscelazione e travaso del tino.

Documentazione di supporto: `doc/guide/` (formato `.lpk`, ladder, HMI, note di compilazione).  
Geometria, portate e **impostazioni di fabbrica** sono in questo file (§3 e §6).

---

## 1. Identificazione

| Voce | Valore |
|---|---|
| Impianto | Tino H20 — acqua di processo (osmosi + rete) verso sala cottura |
| Contesto | Birrificio artigianale (esempio didattico) |
| Autore software | Manuel Piergigli |
| Pannello | Kernel Sistemi **TP 320**, 320×240 px, TFT 65536 colori, touch, mini-USB |
| IDE | LogicPaint **2.0.5.3** ([Kernel Sistemi](https://www.kernelsistemi.it/)) |
| File ladder | **v1.00** `Proj/Tino_H20.lpk` ([12_h20.md](guide/12_h20.md)) |
| File AWL | `Proj/Tino_H20_AWL.lpk` ([11_awl_logicpaint.md](guide/11_awl_logicpaint.md)) |
| Ingresso analogico | **0–20 mA** → **TP 320/SCT** |

---

## 2. Obiettivo funzionale

1. Riempire il tino miscelando **acqua osmosi** e **acqua di rete** fino a un **volume** e una **durezza** target.
2. Travasare un **numero noto di litri** verso la sala cottura.
3. Consentire comando **manuale** delle uscite, con blocco sicurezza a tino pieno.
4. Filtrare la misura di livello, allarmare su integrità e troppo-pieno, apprendere le portate solo se il dato è credibile.

Presupposto di lavoro: il file `.lpk` (HMI e ladder) si può scrivere e modificare come testo, da zero o per copia. LogicPaint resta lo strumento per aprire, compilare e inviare; eventuali limiti del formato si verificano in editor, non si assumono a priori.

### 2.1 Requisiti funzionali

Confronto tra obiettivo dell’impianto e quanto realizzato:

| Richiesta | Stato |
|---|---|
| Comando manuale elettrovalvola rete (24 Vac, 8 W) | Fatto |
| Comando manuale osmosi via contatto pulito | Fatto |
| Comando manuale pompa travaso 1,5 kW su presa trifase | Fatto |
| Visualizzazione livello acqua nel tank | Fatto (HOME: litri, %, barra) |
| Ciclo automatico miscela: litri totali + rapporto osmosi/rete | Fatto **in durezza °F** invece che in percentuale — §5.2 |
| Ciclo automatico riempimento sala cottura: litri da travasare | Fatto — §5.4 |
| Database 10 ricette con nome (meglio 30), richiamabili | **Non implementato** — secondo step |
| Allarmi sui cicli automatici per produrre senza supervisione | Fatto come watchdog di stallo, max 60 min — §7 |
| Schema elettrico di massima e distinta materiali | Fuori ambito del repository |

**Database ricette — rinviato al secondo step.** L’obiettivo iniziale prevedeva 10 ricette salvate con un nome ("Pils" = 1000 litri al 45 %), richiamabili per il ciclo automatico, e apre a 30 se il costo non cambia. Oggi non esiste: l'unico meccanismo è la coppia `LT TARGET` / `DUR TARGET` ricaricata a ogni accensione, che vale come ricetta 0.

La piattaforma le supporta nativamente e non si parte da zero: `SYS.21` / `SYS.22` sono salva e ripristina ricetta, l'istruzione `INDMOV` indicizza un blocco di DATA per numero di ricetta, e le anagrafiche variabili hanno già il campo `RIC`. Il costo vero è EEPROM e pagine HMI, non logica.

**Watchdog invece della soglia a litri.** In alternativa si era valutato "se dopo 2 ore di osmosi non produce almeno X litri, allarme". Qui il criterio è "il livello non si muove per N minuti", con N impostabile 0–60. È più semplice da tarare e non richiede di conoscere la portata attesa, ma è anche più lasco: basta una deriva del sensore per riarmare il conteggio. Scelta accettata.

**Il revamping non tocca il cablaggio.** Il quadro esistente resta com'è; il software si adatta alla morsettiera (§3.3).

---

## 3. Impianto fisico

### 3.1 Tino

**Serbatoio verticale ~2500 L** (inox, 2019). Cilindro verticale Ø interno 1270 mm, altezza 2000 mm, con cono superiore e inferiore.

La tabella di taratura del costruttore (*(documentazione di impianto non inclusa nel repository pubblico)*) dà **12,667 L/cm** su tutto il tratto cilindrico e 77 L di cono inferiore. Il ladder calcola \(A = C^{2}/(4\pi)\) e con `CIRC = 399` ottiene 12,665 L/cm: scarto **0,02 %**, formula confermata.

| Parametro | Fabbrica | Ruolo |
|---|---|---|
| `CIRC` | **399 cm** | Perimetro cilindro → area (≈ 12,67 L/cm) |
| `LT TOT` | **2500 L** | Capacità nominale. HOME: `% = 100 × LIV / LT TOT` (es. 1850 L → 74 %) |
| `OFFSET` | **85 L** | Volume sotto il trasduttore (non visto dal sensore) |
| `ALLARME PIENO` | **2400 L** | Soglia stop OSMOSI/RETE (anche in manuale). TRAVASO resta possibile |
| `FS BAR` | **20** (= 2,0 bar) | Fondo scala **trasduttore**, non la barra HOME. La barra HOME usa `LT TOT`. In campo oggi è montato un 0–2 bar. |

Altezza a 2500 L ≈ **191 cm** → ≈ **0,19 bar**. Il tino opera sempre sotto **0,2 bar**.

Il trasduttore è montato **alla quota 0 dell'asta, dove finisce il cono** (base del cilindro): confermato in campo. È l'origine stessa della tabella di taratura, quindi il modello lineare qui sotto è **esatto per costruzione** e non serve linearizzare il cono. Se il sensore fosse stato sul fondo avrebbe visto i ~18 cm di cono, con fino a ~154 L di sovrastima a tino quasi vuoto: rischio escluso.

`OFFSET` **85 L** confermato, ed è il volume sotto quella quota: 77 L di cono (tabella costruttore) più ~8 L nei rubinetti e nei raccordi a valle. I due numeri non sono in contraddizione, misurano cose diverse: chi legge 77 sul PDF del costruttore non deve correggerlo. Dettaglio: §3 e §6 di questo file §1.

**Livello usato da logica e video:**

\[
LIV = OFFSET + A \times h,\qquad
h \text{ da pressione 4–20 mA}
\]

Misura grezza → `DATA.2028`. Dopo filtro → `DATA.2007` (valore ufficiale).

### 3.2 Trasduttore di livello

Uscita **4–20 mA**, 2 fili, verso analogica PLC 0–20 mA. Nel ladder iniziale lo zero 4 mA è la costante **816** count su `DATA.417` (`816/4096 ≈ 4/20`).

| | In campo oggi | Nuovo (acquistato) |
|---|---|---|
| Identificazione | Riels **RIB100-C8C** (etichetta) | Da annotare a montaggio |
| Posizione | quota 0 asta (fine cono) | invariata |
| Range | **0–2 bar** relativo | **0–0,3 bar** (300 mbar) |
| Scheda | scheda trasduttore RIB100 (produttore) | — |
| Uso del FS a 2500 L | ~9,4 % | ~62 % |
| Errore tipico ±0,5 % FS (stima da catalogo, **da confermare con test**) | ≈ **129 L** | ≈ **19 L** |
| 1 count ADC 12 bit | ≈ **7,9 L** | ≈ **1,2 L** |
| Jitter 1 count in 1 s, espresso come portata | **±28 000 L/h** | ±4 300 L/h (ancora da filtrare) |

Il catalogo ceramico RIB100 parte da **2 bar**: è un sensore da idraulica, non da 1,5 m d’acqua. Il 0–0,3 bar è la scelta corretta (20 mA ≈ 3,06 m H2O ≈ **3870 L** sopra il sensore con CIRC 399).

Scalatura col nuovo sensore (20 mA = **0,3 bar**, non 3000 L):

```
bar     = (count - 816) / 3280 × 0.3
h_cm    = bar × 1020
V_sopra = h_cm × AREA_cm2 / 1000
LIV     = OFFSET + V_sopra
```

Dettaglio: `doc/guide/08_sensore_livello.md`.

### 3.3 Acque e uscite

Il revamping **non tocca il cablaggio**: il software si adatta alla morsettiera esistente.

La mappa I/O è allineata al quadro esistente dell’impianto (cablaggio non modificato dal revamping software).

| Morsetto | Organo | Funzione reale | Codice attuale |
|---|---|---|---|
| `OUT.00` / Q0 | KM1 → pompa travaso P2 (1,5 kW trifase) | **Travaso** | Travaso |
| `OUT.01` / Q1 | KA1, contatto pulito 5220/5221 | **Spare** | Spento ogni scan |
| `OUT.02` / Q2 | KA2, contatto pulito 5240/5241 | **Osmosi** (consenso S-RO, RUN 29–30) | Osmosi |
| `OUT.03` / Q3 | YV1 elettrovalvola riempimento | **Rete** (24 Vac, 8 W) | Rete (niente OR) |
| `OUT.04` / Q4 | SH1, lampada del pulsante | Spia (`FLAG.01`) | Spia |

Lampade HOME: OSMOSI legge `OUT.02` (`DATA.2042`), RETE legge `OUT.03` (`DATA.2041`).

Consenso S-RO: RUN J7 **29–30** (in campo era l’interruttore manuale). Contatto quadro = KA2 `5240/5241`. Non ponticellare MAX LEV (J4) chiuso. Manuale: *(documentazione di impianto non inclusa nel repository pubblico)* §8.

**Ingressi** (Simbolici): `INP.00` TERMICO POMPE ← QM1. `INP.01` EMERGENZA. `INP.03` RESET BLU ← SH1. `INP.02` ALLARME OSMOSI: morsetto `E2` in quadro è vuoto; il candidato resta J18 dell'S-RO, cavo non sbarcato.

---

## 4. Diagnosi del ladder di partenza

Net.0 **non è vuoto**: scalatura analogico→litri, emergenza, LED uscite, pagina manuale.

In campo risultava **inutilizzabile** per due motivi concomitanti:

1. **Portata.** `FLOW = dL/dt × 3600` su un LSB da 10 L (sensore 0–2 bar) non è una portata: è rumore ADC. L’auto-apprendimento `LT/H` e gli stop su soglia diventano casuali.
2. **Automatismi.** Non c’è (o non chiude) la sequenza FILL osmosi→rete, travaso a litri noti, mix durezza, ETA. Le pagine sono stato / scalatura / manuale, non ricette.

Nel file `Term_Ena_ANA=False` mentre il ladder legge `DATA.417` — **normale** (come il backup di campo). **Non** mettere `True` nel `.lpk` (Compila KeyNotFound). Su TP 320 /SCT non serve alcun toggle analogica in *Opzioni progetto* LogicPaint: Compila → Trasmetti. Dettaglio, REFILL, FLAG.00: `doc/guide/12_h20.md`.

**Politica:** si riusa Net.0 per I/O ed emergenza; si **riscrivono** misura livello (dopo 0–0,3 bar) e ricette. Non si “ripara” l’apprendimento portata sul 0–2 bar.

---

## 5. Processi

### 5.1 Smorzamento livello

`SMORZAMENTO SEC` (EEPROM `4106`, specchio `2016`, default **3**, range **1–15**) è la costante di tempo in **secondi**, non un percento.

Ogni secondo (`SYS.10`):

\[
DATA.2007 = \frac{DATA.2007 \times (T-1) + DATA.2028}{T}
\]

`T=1` → niente smorzamento (si segue il grezzo). Un valore EEPROM fuori 1–15 (es. vecchio filtro 90 %) viene riportato a 3. HOME mostra `2007` con RFS. `CAMP SEC` non è usato.

### 5.2 Mix durezza

\(V_n\) rete, \(V_o\) osmosi, \(L_t\) target litri, \(H_t\) durezza target, \(H_n\) durezza rete (in HMI scrivere `F` — niente `°` nel `.lpk`). In v1.00 le °F sono **intere** (tastiera `8` e `24`). In FILL i cm di colonna sono l’altra faccia della stessa ricetta: `cm = L × 1000 / AREA`; se si editano i cm, `L = cm × AREA / 1000` e si ricalcolano \(L_t\) e \(H_t\).

\[
V_n = L_t \times H_t / H_n,\qquad V_o = L_t - V_n
\]

Clamp: se \(H_t > H_n\) → 100 % rete; se \(H_n=0\) o \(H_t=0\) → 100 % osmosi.  
Tolleranza `TOLL MIX` 20 L. Pausa `T STAB` **30 s** tra step (dimensionata sul ciclo di arresto e lavaggio dell'osmosi: §3 e §6 di questo file §4).

Calcolo in **32 bit** (`LMUL` / `LDIV` o `LEMUL` / `LEDIV`): una word 16 bit satura a 65535.

**Perché durezza e non percentuale.** La specifica funzionale iniziale chiedeva due parametri: litri totali e *rapporto osmotizzata/rete in percentuale* ("1000 litri, 40 %" = 400 L osmosi). Qui si imposta invece la **durezza target** in °F, e la percentuale la calcola il PLC a partire da `DUR RETE`.

È uno scostamento voluto, non una svista. Le due formulazioni sono equivalenti (\(V_n/L_t = H_t/H_n\)), ma l'operatore ragiona sulla grandezza che gli interessa davvero — la durezza dell'acqua di birrificazione — invece di doversi calcolare ogni volta a mano la percentuale che la produce. Con i valori di fabbrica v1.00, 2300 L a 8 °F su rete da 24 °F danno circa 767 L di rete e 1533 L di osmosi.

Il prezzo è che `DUR RETE` deve essere tarato sull'acquedotto reale e riverificato se cambia.

### 5.3 FILL

1. Calcolo \(V_o\), \(V_n\).
2. Se `LT TARGET > ALLARME` → allarme integrità, niente AVVIA (`FLAG.210`).
3. STEP1 OSMOSI fino a \(V_o\) (± TOLL MIX).
4. Stabilizzazione `T STAB` (30 s).
5. STEP2 RETE fino a \(L_t\).
6. STOP, salvataggio EEPROM (parametri SETUP, non le portate: i LTH non si riscrivono da `dL/dt`).

Le uscite fisiche di STEP1 e STEP2 sono `OUT.02` (osmosi) e `OUT.03` (rete).

FLOW a video = `LT/H` dello step in corso (SETUP: OSM `2019`, RETE `2018`). ETA = residuo × 60 / LTH.

### 5.4 TRAVASO

Target finale = `LIV − LT TRAVASO`. Se target &lt; `OFFSET` → allarme vuoto (`FLAG.212`). Altrimenti `OUT.00`.

Progresso barra = **calo di livello** `DATA.2026` = `LIV` all’AVVIA − `LIV` corrente, finché la pompa è on. La barra H_ISTO ha min 0 (`DATA.2030`) e max = `LT TRAVASO` (`DATA.2006`), NORM (sinistra → destra). Stop quando il calo ≥ `LT TRAVASO`.

Troppo pieno: se `LIV > ALLARME` → `RES OUT.02` e `OUT.03`, **lasciare** `OUT.00`, `FLAG.211`. Vale anche in manuale.

### 5.5 Portata

I LTH sono in **L/m** in SETUP MIX / EEPROM (`4108` rete 22, `4109` osmosi 7, `4110` travaso 26). Misure di campo in L/h: §3 e §6 di questo file §3.

Durante FILL/TRAVASO, `DATA.2025` (FLOW) copia il LTH dello step in **L/m**. ETA (`2024`) = residuo / LTH minuti (se LTH = 0 → 999). Unità a video: `min` dopo ETA, `l/m` dopo FLOW.

---

## 6. Interfaccia

Navigazione fissa in basso: `HOME | FILL | TRAVASO | SETUP`. Pagina attiva: fondo giallo. SETUP: linguette `TANK | MIX | TRASD | TOT`. Contratto v1.00: `doc/guide/12_h20.md`.

Mockup di layout: `doc/Home.webp`, `Fill.webp`, `Travaso.webp`, `Setup_tank.webp`, `Setup_mix.webp`. Non sono pixel-perfect del TP 320: la grafica si disegna in LogicPaint.

### HOME (Pag.0)

Pagina di stato del tino. Nav basso `HOME | FILL | TRAV | SETUP` cliccabile; tab attiva giallo.

**Litri e %**

- Litri = `LIV` filtrato (`DATA.2007` specchiato in `DATA.1000`), sola lettura, intero.
- `% = 100 × LIV / LT TOT` (`DATA.2023` / `DATA.2012`). `LT TOT` è la capacità impostata in SETUP (default 2500 L), non il fondo scala del trasduttore.
- Se `LT TOT = 0` → `% = 0` (niente divisione).
- `LIV` può superare `LT TOT` (es. troppopieno): i litri restano il valore reale; la `%` a video si satura a 100.

**Aggiornamento (sensore vs video)**

Il trasduttore risponde in millisecondi; il pelo libero dopo un getto si sistema in pochi secondi. `T STAB` (default 30 s) è solo la pausa tra step FILL, non il refresh HOME.

- Il dato a video è sempre il **filtrato** `DATA.2007`, non il grezzo `DATA.2028`.
- Smorzamento IIR una volta al secondo: `2007 = (2007×(T−1) + 2028) / T` con `T` = `SMORZAMENTO SEC` (default 3, range 1–15). `T=1` segue il grezzo.
- HOME deve avere **RFS on** su litri, `%` e barra tino: il valore segue restando sulla pagina. Senza RFS LogicPaint ridisegna solo all’ingresso pagina.
- Non usare `CAMP SEC` sui litri HOME: il campo SETUP non è più usato.
- Se i litri ballano ancora col getto, alzare `SMORZAMENTO SEC` (es. 5–8), non rallentare l’HMI.

**Offset**

`LIV = OFFSET + volume sopra il sensore`. Il trasduttore non vede i litri sotto di sé: a pressione 0 (o ADC ≤ zero 4 mA) si legge comunque **OFFSET** (default 85 L), non 0 e non “vuoto”. La barra e la `%` usano lo stesso `LIV` (tino “vuoto” visibile ≈ OFFSET / LT TOT).

**Barra tino**

Istogramma verticale (V_ISTO) a destra: min 0, max = `LT TOT` runtime (`DATA.2012`). Riempie dal basso. Rappresenta solo il **riempimento**, non lo stato delle uscite.

**Tre uscite**

A fianco di `OSMOSI` / `RETE` / `TRAVASO` un H_ISTO 0/1 (lampada) specchio delle uscite reali (`DATA.2042` / `2041` / `2040`). Colore: **ON = lime**, **OFF = spento/nero** (non invertire: rosso=ON è sbagliato). RFS on.

Lo specchio segue le uscite fisiche: lampada OSMOSI = `OUT.02` (`DATA.2042`), lampada RETE = `OUT.03` (`DATA.2041`).

**Manuale**

1. Tap su `MAN` in alto → impulso HMI `FLAG.254` (SET al tocco, RES al rilascio), il ladder inverte `FLAG.204` **una volta** per pressione. Lampada `DATA.2020` accesa = MAN ON. Non `MAC_TOGGLE`: sul TP320 fa bip e il flag non si muove.
2. Solo con MAN ON il tap sulla **riga** (etichetta o LED) dà impulso `185`/`186`/`187` e il ladder inverte OSMOSI / RETE / TRAVASO (`FLAG.205` / `206` / `207`).
3. Con MAN OFF i tap sulle uscite **non accodano** comandi: i flag 205–207 restano a 0 ogni scan. Uscire da MAN spegne tutte le OUT e le ricette.
4. **Troppo pieno** (`LIV filtrato > ALLARME`, default 2400 L, `FLAG.211`): OSMOSI e RETE non partono e, se erano ON, si spengono; la richiesta MAN 205/206 si azzera (LED spento). FILL/REFILL non partono. **TRAVASO resta azionabile**. **Niente pagina allarme**. Nessuna isteresi: sotto o uguale ad ALLARME OSM/RETE tornano permessi.
5. **Travaso vuoto** (`LIV < LT TRAVASO`, `FLAG.212`): AVVIA TRAVASO non parte. Pagina `WARN VUOTO` (Pag.8) con LIV, LT e tasto **OK** che torna alla pagina TRAVASO. Non è la pagina rossa Kernel.
6. Emergenza (`INP.01`) spegne ricette e OUT 00–03 anche in MAN.

FILL e TRAVASO automatici si abortiscono se si entra in MAN.

### FILL

- Titolo **RESET** (`FLAG.268`): abortisce il FILL in corso, tiene i target.
- Edit `LT TARGET`, `DUR TARGET` (interi: `2300` e `8`). Oppure i cm di osmosi/rete: il PLC ricalcola litri e °F.
- STEP1 OSMOSI e STEP2 RETE: cm, litri, barra, ETA, **LIV** attuale.
- AVVIA / STOP.

### TRAVASO

- `LT TRAVASO` è un parametro **SETUP** (default **330 L**, stesso `DATA.2006` anche sulla pagina TRAVASO).
- `TANK A → B`, barra = calo livello, FLOW, ETA, LED pompa. AVVIA / STOP.

### SETUP (quattro tab)

- **TANK:** CIRC, LT TOT, OFFSET, ALLARME, DUR RETE, FS bar.
- **MIX:** TOLL MIX, T STAB, LTH RETE / OSM / TRAVASO, `LT TRAVASO`.
- **TRASD:** FS bar (`0.3 o 2`), `SMORZAMENTO SEC`, `CAMP SEC`, `TIMEOUT MIN` (0–60, 0=off), zero 4 mA, banda morta.
- **TOT (CONTAT):** totali litri OSMOSI / RETE / TRAVASO, tasto AZZERA per riga (Pag.6).

Valori di fabbrica di ogni parametro, con range e motivazione: §3 e §6 di questo file §4.

---

## 7. Allarmi

Pagina rossa Kernel (blocca il touch): **solo Alr.1 EMERGENZA PREMUTA** (`INP.01` → `DATA.08` bit 1). Gli altri slot restano nel file ma **non** sono cablati su `DATA.08`: si lavora, con le sicurezze in ladder.

| Slot | Testo (file) | `DATA.08` | Sicurezza |
|---|---|---|---|
| Alr.0 | BLOCCO TERMICO | no | `INP.00`: pompa e ricette OFF |
| Alr.1 | EMERGENZA PREMUTA | **bit 1** | Unica pagina allarme. OUT 00–03 OFF |
| Alr.2 | ALLARME OSMOSI | no | `INP.02`: niente OSM, FILL esce da STEP1 |
| Alr.3 | TARGET OLTRE MAX | no | `FLAG.210`: FILL/REFILL non partono |
| Alr.4 | TROPPO PIENO | no | `FLAG.211`: stop OSM/RETE, no FILL |
| Alr.5 | TRAVASO VUOTO | no | `FLAG.212`: TRAVASO non parte se `LIV < LT` |
| Alr.6 | STALLO FILL | no | `FLAG.228`: OUT 00–03 OFF |
| Alr.7 | STALLO TRAVASO | no | `FLAG.229`: OUT 00–03 OFF |

Alr.6 e Alr.7 dipendono da `TIMEOUT MIN` (`DATA.4116`, 0–60 minuti), fabbrica **20**. Impostare `0` disattiva il watchdog (solo in prova).

---

## 8. Memoria H20 (file di lavoro)

Confronto Kernel: non esistono `GRT` / `EQU`. Si usa **CMP** e poi `SYS.03` (=), `SYS.04` (<), `SYS.05` (>). Ogni CMP incondizionato (`SYS.01`), SYS letto subito dopo.

`SYS.10` = 1 s. Salvataggio: **FB..0 Save EEPROM** (sola lettura) su fronte fine ricetta / ENT SETUP, non ogni ciclo. PDF CPU ARM: `SYS.20` + `DATA.58`/`59` salva un range EEPROM (4097–8191); `SYS.21`/`22` sono ricetta. Dettaglio: `doc/guide/02_hardware_TP320.md`.

`DATA.00`–`4095` **volatili**. I DATA 2004–2030 (e 1000, 2000–2003) si perdono allo spegnimento. Parametri SETUP (inclusi LTH battuti a mano) vanno in **`DATA.4096+`** (o NVDATA) prima del FB save. `DATA.6000`/`6001` sono già EEPROM.

### DATA nuovi (2004–2028, liberi, volatile)

| DATA | Nome | Default |
|---|---|---|
| 2004 | LT TARGET | 2300 L |
| 2005 | DUR TARGET | 8 °F |
| 2006 | LT TRAVASO | 330 L |
| 2007 | LT FILTRATO | — |
| 2008 | Vo OSMOSI | calc. |
| 2009 | Vn RETE | calc. |
| 2010 | ALLARME LIV | 2400 L |
| 2011 | CIRC CM | 399 |
| 2012 | LT TOT | 2500 L |
| 2013 | OFFSET L | 85 L |
| 2014 | DUR RETE | 22 F |
| 2015 | TOLL MIX | 20 L |
| 2016 | SMORZ SEC | 3 |
| 2017 | FS BAR | 20 (= 2,0 bar) |
| 2018 | LTH RETE | 22 L/m |
| 2019 | LTH OSMOSI | 7 L/m |
| 2020 | MAN MODE | 0/1 |
| 2021 | LTH TRAVASO | 26 L/m |
| 2022 | T STAB | 30 s |
| 2023 | PCT LIV | — |
| 2024 | ETA MIN | — |
| 2025 | FLOW LM | — |
| 2026 | CALO TRAVASO | — |
| 2027 | APPOGGIO | calc. |
| 2028 | LIV GREZZO | — |
| 2030 | ZERO | 0 (min barre REM, non scrivere) |

Riuso: `DATA.1000` livello storico, `2000` area, `2001` altezza, `2002`/`2003` max/min.

### FLAG nuovi (fascia libera)

| FLAG | Uso |
|---|---|
| 200 | FILL in corso |
| 201 | STEP1 OSMOSI |
| 202 | STEP2 RETE |
| 203 | TRAVASO in corso |
| 204 | MAN MODE |
| 210 | Allarme target |
| 211 | Allarme pieno |
| 212 | Allarme travaso vuoto |
| 268 | RESET FILL (abort job) |

Non usare `FLAG.00`–`12`, `20`–`21`, `50`, `70`–`71`, `80`–`81`, `100`–`104`, `300`, né `1998`–`2047` (FB).

---

## 9. Reti ladder da aggiungere in LogicPaint (UI)

1. Integrità FILL — CMP 2004 vs 2010, `SYS.05` → `FLAG.210`.
2. Sicurezza pieno — CMP 2007 vs 2010 → RES OUT.02/03, `FLAG.211`.
3. Smorzamento livello (`SMORZAMENTO SEC`) → `DATA.2007`.
4. Mix \(V_n\)/\(V_o\) con clamp, math 32 bit.
5. MAN MODE (`DATA.2020`) e toggle uscite; NC su pieno per OSMOSI/RETE.
6. FLOW/ETA da LTH di SETUP (niente `dL/dt`).
7. ETA step e totale.
8. Sequenza FILL e TRAVASO (flag 200–203).
9. Chiamata FB Save EEPROM su fronte fine ricetta / conferma SETUP (range A–B in **4096+**, non i DATA 2000 volatili).

Vincoli file `.lpk` da tenere presenti (da verificare in compile): variabili **prima** di `[Ladder]`; niente `°`; `Minimo ≠ Massimo`.

---

## 10. Grafica LogicPaint

Display 320×240 a colori. Manuale oggetti (palette, WORD, istogramma, elenco/menu, pulsante K) con screenshot: [`doc/guide/09_guida_grafica_hmi.md`](guide/09_guida_grafica_hmi.md).

Oggetti usati nel file:

| Tipo | Uso |
|---|---|
| 2 | Testo (`ObjText.Testo 0:` / `1:`) |
| 3 | Rettangolo |
| 11 | Bargraph / H-isto |
| 14 | Variabile numerica |
| 15 | V Istogramma (tino Pag.0) |
| 17 | Pulsante touch, macro `MAC_PAGE` |

Colori: −1 bianco, −16777216 nero, −16776961 blu, −16744448 verde, −65536 rosso, −256 giallo. Font `D11` / `D22` / `D33`.

Vincoli UI: **1 Menu per pagina**; picker filtrato per tipo (`WORD` ≠ `V_ISTO`). L’elenco va bene in SETUP per scegliere il trasduttore 0–2 / 0–0,3 bar (indice in un DATA dedicato, non `DATA.1000`).

Non generare mockup colorati con image-gen: non coincidono col rendering TP 320.

---

## 11. File del repository (`tp320-osmosi-tino-mix`)

Sorgente: [github.com/pierpidc-bot/tp320-osmosi-tino-mix](https://github.com/pierpidc-bot/tp320-osmosi-tino-mix).

| Percorso | Contenuto |
|---|---|
| `Proj/Tino_H20.lpk` | Progetto ladder/HMI corrente (v1.00) |
| `Proj/Tino_H20_AWL.lpk` | Variante AWL (lista istruzioni) |
| `doc/Tino_H20.md` | Specifica funzionale e parametri di fabbrica |
| `doc/guide/` | Guide tecniche (formato `.lpk`, compilazione, HMI) |
| `doc/*.webp` | Screenshot di riferimento layout pagine |
| `doc/manuale/` | Manuale d’uso terminale (PDF + figure) |
| `tools/` | Generatori Python e anteprima HMI `tp320_preview` |

Trasmissione: LogicPaint → Salva → Compila → Trasmetti (mini-USB). Se i font sul pannello non coincidono: *Font Management → Compile and Send Font*.
