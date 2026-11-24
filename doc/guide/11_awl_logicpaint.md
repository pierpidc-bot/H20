# Preparare un progetto AWL (Lista istruzioni) — LogicPaint TP 320

Verificato 2026-08-22 su LogicPaint **2.0.5.3** + `plc_comp` **1.45** (`Sys_Dlc\PLC_COMP.EXE`, target `0x4000 LITTLE noend`). Compila AWL = `Errors: None`. *Controlla dimensione* sul gemello H20: programma **19328 / 262143** byte (7 %), pagine 21680 / 67 108 863.

Istruzione Kernel (CMP, MOV, math, SET/RES): [05_ladder_kernel.md](05_ladder_kernel.md). HMI e sezioni `.lpk`: [03_formato_lpk_agente.md](03_formato_lpk_agente.md).

---

## 1. Scelta del linguaggio — irreversibile

All’apertura di un **progetto nuovo** LogicPaint chiede Ladder **oppure** Lista istruzioni (AWL). La scelta è nel file e **non si converte**.

| Non fare | Fare |
|---|---|
| Copiare `[Ladder]` / `[Network_*]` / `[FunctionBlock]` in un file AWL | Tenere solo `[Lista Istruzioni]` … `[End Lista Istruzioni]` |
| Aprire il ladder, poi *Salva* sopra il `.lpk` AWL | Due file distinti; se l’IDE ha già un file aperto, **non** risalvare sopra quello appena scritto a testo |
| Incollare mnemoniche IEC (`GRT`, `EQU`, `ADD` a tre operandi come Siemens) | Opcode Kernel: vedi §5 e help help ufficiale LogicPaint (scaricabile da [Kernel Sistemi](https://www.kernelsistemi.it/)) |

Per H20:

| File | Linguaggio | Ruolo |
|---|---|---|
| `Proj/Tino_H20.lpk` | Ladder | HMI + Net.0 (`h20_apply_plan.py`) |
| `Proj/Tino_H20_AWL.lpk` | AWL | Gemello IL (`h20_build_awl.py`) |

---

## 2. Come nasce un progetto AWL

### Da LogicPaint (progetto vuoto)

1. File nuovo → modello **TP_320** → linguaggio **Lista istruzioni**.
2. Disegnare HMI (o copiare pagine da un altro `.lpk` **dopo** aver creato lo scheletro AWL).
3. Scrivere IL nell’editor Lista istruzioni, **oppure** nel blocco `[Lista Istruzioni]` del `.lpk`.
4. Salva → **Compila** → *Controlla dimensione* → Trasmetti (mini-USB).

### Da testo (agente / editor)

1. Partire da uno scheletro AWL già compilabile (`Tino_H20_AWL.lpk`), **non** da un file ladder.
2. Copiare HMI (`[Pagina_0]` … `[Lista Immagini]`, allarmi, `[Variabile_N]`) dal gemello ladder se serve lo stesso pannello.
3. Sostituire solo il corpo tra `[Lista Istruzioni]` e `[End Lista Istruzioni]`.
4. Lasciare `[Term_Settings]` del file AWL (`Term_Nome=TP_320`, `Term_Ena_ANA=False`).
5. Ricaricare in LogicPaint **senza** sovrascrivere col buffer aperto, poi Compila.

Gemello H20: da root repo `python tools/h20_build_awl.py` — HMI da `Tino_H20.lpk`, IL da `tools/h20_awl_il.txt`, involucro AWL invariato. Non tocca il ladder.

---

## 3. Struttura `.lpk` AWL

Stesse sezioni HMI del ladder. In coda, al posto di `[Ladder]` / reti / FB:

```
[Lista Istruzioni]

; Area Programma Principale : ...
	LD    FLAG.00
	...
	END

	SBR   INITIALIZE
; Subroutine INITIALIZE (eseguita all'avvio) : ...
	ENDSBR

; Area Subroutine : Inserire QUI eventuali Subroutine (struttura "SBR" ... "ENDSBR")

[End Lista Istruzioni]
[Simbolici]
```

- `END` chiude il main. `SBR INITIALIZE` / `ENDSBR` ci sono **sempre** (anche vuoti): LogicPaint li genera nel progetto nuovo.
- Commenti `;` a inizio riga. Niente `°` nei simbolici (stesso vincolo del ladder).
- Identità in albero dopo Compila: `Pag.0 : HOME` (o il `NomePagina` di Pagina_0).

---

## 4. Sintassi per `plc_comp` (non copiare il `#` del help sul mnemonic)

L’help CHM usa spesso `# CMP` / `@LD` come convenzione **ladder/editor** (“istruzione forzata / fronte”). Il compilatore AWL legge `plc.plc` e tratta il token dopo i blank come **opcode**. `#CMP` e `#BOUT` sono opcode inesistenti → `Invalid OP code`.

`#` va **solo sulle costanti**, come primo operando.

| Ruolo | Forma che compila | Forma che fallisce |
|---|---|---|
| Riga incondizionata | `LD SYS.01` poi `CMP` / `MOV` / `ESUB` / … | `#CMP #0,DATA.08` |
| Costante | `MOV #450,DATA.4100` | `MOV 450,DATA.4100` (niente `#`) |
| Bit di un DATA (bobina) | `BOUT #0,DATA.08` | `BSET 0,DATA.08` (numero nudo) · `#BOUT 0,DATA.08` (`#` sull’opcode) |
| SET/RES | `RES FLAG.200` · `SET SYS.20` | `SET DATA.08` (SET/RES non accettano DATA) |
| Contatti | `LD` `LDNOT` `AND` `ANDNOT` `OR` `OUT` | mnemoniche IEC |

Bit 0…15: due forme nella tabella di `plc_comp`: `#n,DATA.xx` oppure `DATA.aa,DATA.bb` (numero bit in un DATA). Help `bsetbclrbnot.htm` dice “senza `#`”: **sbagliato per questo compilatore**.

Bobina su bit di word (allarmi `DATA.08`, beep `DATA.01`):

```
	LD    INP.00
	BOUT  #0,DATA.08
	LDNOT INP.01
	BOUT  #1,DATA.08
	LD    SYS.01
	CMP   #0,DATA.08
	LD    SYS.04
	BOUT  #1,DATA.01
```

`BOUT` segue l’accumulatore (come la bobina ladder). `BSET` / `BCLR` esistono ma vogliono comunque `#n,DATA.xx`.

CMP: sempre incondizionato, poi leggere `SYS.03`/`04`/`05` **prima** del CMP successivo ([05_ladder_kernel.md](05_ladder_kernel.md)).

```
	LD    SYS.01
	CMP   #0,DATA.08
	LD    SYS.04          ; 0 < DATA.08
	BOUT  #1,DATA.01
```

---

## 5. Math e istruzioni da non usare

- Solo il **primo** operando può essere costante (`#n`).
- `MOV` / `ADD`/`SUB`/… a 2 operandi: il risultato **sovrascrive il secondo**.
- `ESUB` / `LESUB` / `LEMUL` / `LEDIV`: tre operandi, risultato nel **terzo**. Prefisso `L` = LONG su due DATA consecutivi (basso = word meno significativa su CPU ARM).
- `EADD` / `LEADD`: in LogicPaint 2.0.5.3 su questo target → **KeyNotFound**. Somma = sottrarre da zero:

```
	LD    SYS.01
	MOV   #0,DATA.2030
	ESUB  DATA.2055,DATA.2030,DATA.08    ; DATA.08 = 0 - (-x) se 2055 è già -x
```

Ossia `dest = op2 - op1`. Per `a + b`: `ESUB b, DATA.2030, tmp` (`tmp = −b`) poi `ESUB tmp, a, dest`.

- Function Block: in AWL **non** c’è `[FunctionBlock]`. Salva EEPROM come il Net.0 ladder senza FB:

```
	LD    FLAG.220
	MOV   #4100,DATA.58
	MOV   #4125,DATA.59
	SET   SYS.20
	RES   FLAG.220
```

(`DATA.8142`/`8143` in H20 ripetono il range: stesso meccanismo Kernel.)

- Analogica: `Term_Ena_ANA=True` **nel file** → KeyNotFound in Compila. Lasciare `False` (come backup di campo con `DATA.417` attivo). Su TP 320 /SCT non c’è toggle analogica in *Opzioni progetto* LogicPaint.

---

## 6. Compilare

### In LogicPaint

1. File aperto = quello AWL (nome albero `Tino_H20_AWL` / `Term_Descrizione`).
2. **Compila**. Se l’agente ha riscritto il `.lpk` con l’IDE ancora aperto: chiudere **senza** salvare, riaprire, poi Compila.
3. Esito atteso: niente *Errore in Compilazione*; *Controlla dimensione* con barre verdi / grigie sotto tetto.
4. `plc.plc` di appoggio: `C:\Program Files (x86)\LogicPaint\bin\Sys_Dlc\TP_320\plc.plc`. Errori: `plc_comp.err` nella stessa cartella. Testo tipo `Invalid OP code: BSET  0,DATA.08` = opcode/forma, non “bit occupato”.

### Preflight da PC (stesso compilatore dell’IDE)

```
plc_comp plc.plc 0x4000 0 LITTLE noend
```

Eseguibile: `C:\Program Files (x86)\LogicPaint\bin\Sys_Dlc\PLC_COMP.EXE`. Il corpo da compilare è il testo **dentro** `[Lista Istruzioni]` (commenti + IL + `END` + `SBR INITIALIZE` + `ENDSBR`), non l’intero `.lpk`.

`GO.BAT` in `Sys_Dlc\TP_320` fa anche assembler H8: per validare solo l’IL basta `plc_comp`.

---

## 7. Checklist nuovo progetto AWL

- [ ] Linguaggio Lista istruzioni scelto **alla creazione** (non convertito da ladder)
- [ ] `Term_Nome=TP_320`, `Term_Ena_ANA=False` nel file
- [ ] Nessuna sezione `[Ladder]` / `[FunctionBlock]`
- [ ] Wrapper `END` + `SBR INITIALIZE` / `ENDSBR`
- [ ] Nessun `#` attaccato al mnemonic (`#MOV`, `#CMP`, `#BOUT`)
- [ ] Costanti e bit: `#450`, `BOUT #0,DATA.08`
- [ ] Niente `EADD`/`LEADD`; SET/RES non su DATA
- [ ] EEPROM: `MOV` range + `SET SYS.20`, non FB
- [ ] **Compila** + *Controlla dimensione* sotto tetto
- [ ] `Term_Ena_ANA=False` nel file (ADC su `DATA.417` ok su /SCT senza passi IDE)

H20 in più: non aggiungere `[Variabile_54]` / IDX HMI; allarmi 0–5 = bit di `DATA.08`; IL di riferimento `tools/h20_awl_il.txt`.
