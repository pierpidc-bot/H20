# Istruzioni ladder Kernel (TP320)

Fonte: help ufficiale help ufficiale LogicPaint (scaricabile da [Kernel Sistemi](https://www.kernelsistemi.it/)) + mappa documentazione PDF Kernel ([kernelsistemi.it](https://www.kernelsistemi.it/)) (non IEC 61131 generico). Prefisso **L** = operazione 32 bit su due DATA consecutivi: **indirizzo basso = word meno significativa**, alto = più significativa. Non mescolare math 16 e 32 bit sullo stesso valore.

## Confronto — niente GRT/EQU

`CMP op1, op2` scrive il risultato sui flag di sistema:

| SYS | Significato CPU ARM |
|---|---|
| `SYS.01` | Sempre vero (riga incondizionata) |
| `SYS.02` | Solo 1° ciclo (power-on) |
| `SYS.03` | op1 **=** op2 |
| `SYS.04` | op1 **<** op2 |
| `SYS.05` | op1 **>** op2 |

Regole Kernel (`help ufficiale LogicPaint (Kernel Sistemi)cmplcmp.htm`):

1. Ogni CMP va eseguito **sempre** (incondizionato `#` / `SYS.01`)
2. Subito dopo il CMP si usa il SYS interessato, prima del CMP successivo (i tre SYS sono globali e vengono sovrascritti)

Esempio “LT TARGET > ALLARME”:

In **ladder** l’editor accetta la FUN incondizionata. In **AWL** (`plc_comp`) `#CMP` non è un opcode: `LD SYS.01` poi `CMP`. Dettaglio: [11_awl_logicpaint.md](11_awl_logicpaint.md).

```
LD     SYS.01
CMP    DATA.2004,DATA.2010      ; target vs soglia pieno (# sul costante, non sul mnemonic)
LD     SYS.05                    ; target > soglia
SET    FLAG.210                  ; allarme integrità
```

Uguale (`EQU`): `SYS.03`. Minore: `SYS.04`.

## Math 16 bit

`ADD SUB MUL DIV` — il risultato **sovrascrive il secondo operando**. Solo il primo può essere costante.

Mix durezza: `Vn = Lt * Ht / Hn` va fatto in 32 bit per non saturare 65535:

```
LMOV / MOV copie
LMUL  Lt, temp     ; o LEMUL se con segno
LDIV  Hn, temp
```

Istruzione con segno: `ESUB EMUL EDIV` e versioni `LE*`. `EADD`/`LEADD` in questo IDE → KeyNotFound; somma da `DATA.2030=0` con ESUB.

Net.0 tipico usa già `LEMUL`, `LESUB`, `LEDIV` per la scalatura livello: copiare quello stile.

## Logica bit

| Istruzione | Effetto |
|---|---|
| `SET` | mette a 1 OUT/FLAG e **resta** |
| `RES` | mette a 0 e resta |
| bobina OUT | segue la riga (non latched) |
| `TOGGLE` / `NOT` | help `togglenot.htm` |

Operandi SET/RES: OUT, FLAG, SYS, LED, … — **non** DATA.

Allarme: bobina sul bit di `DATA.08`. In AWL: `BOUT #n,DATA.08` (`BSET 0,DATA.08` senza `#` → Invalid OP). SET/RES non accettano DATA.

## Movimento dati

- `MOV` / `LMOV` — copia word / long
- `MOVB` — byte
- Costante in AWL: `#1200` sul **valore**, mai `#MOV` / `#CMP` sull’opcode — in ladder il numero è senza `#`

## Tempo / flusso (ETA, auto-apprendimento)

Clock di sistema utili:

| SYS | Periodo |
|---|---|
| `SYS.08` | 10 ms |
| `SYS.09` | 100 ms |
| `SYS.10` | 1 s |
| `SYS.14` | 0,5 s ON / 0,5 s OFF (lampeggio allarmi) |

`dL/dt` in L/h **non si usa** (col RIB100 0–2 bar 1 count ≈ 7,9 L → un LSB in 1 s vale ±28 000 L/h). FLOW e ETA prendono i LTH di SETUP. Dettaglio: [08_sensore_livello.md](08_sensore_livello.md), [`Tino_H20.md`](../Tino_H20.md) §5.5.

## EEPROM

Dettaglio banche e SYS: documentazione CPU ARM su [kernelsistemi.it](https://www.kernelsistemi.it/).

- `DATA.00`–`4095` volatili; `4096`–`8191` EEPROM.
- `SYS.20` + `DATA.58`/`DATA.59` = salva un range EEPROM (PDF: indirizzi 4097–8191).
- `SYS.21` / `SYS.22` nel PDF = salva / ripristina **ricetta** (l’IDE etichetta `SYS.21` “Salva EEPROM”).
- In ladder: **FB..0 Save EEPROM**, su fronte (fine ricetta / ENT SETUP), non ogni ciclo.
- In AWL non c’è FB: `MOV` del range in `DATA.58`/`59` e `SET SYS.20`.

NVDATA: solo `MOV`. Esempio Kernel: ogni secondo `MOV DATA.1000 → NVDATA.00` (`SYS.10`); in INITIALIZE il `MOV` inverso. `RTF` = bit della stessa RAM: non usare `NVDATA.00` e `RTF.00`…`07` per cose diverse.

## Dove inserire il nuovo codice

Ladder:

- **Non** riempire Net.1 (è END + INITIALIZE).
- Aggiungere reti **dopo Net.0 e prima di END**, oppure nuove Network e CALL/SBR in Net.2.
- Abilitazioni analogiche / default parametri: in **SBR INITIALIZE** (Net.1, zona commentata).

AWL: stesso `END` + `SBR INITIALIZE`, ma il main è testo continuo in `[Lista Istruzioni]`. Procedura: [11_awl_logicpaint.md](11_awl_logicpaint.md).
