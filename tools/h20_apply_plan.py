# -*- coding: utf-8 -*-
"""Apply H20 v1.00: memory map, HMI, rewrite Net.0 in Proj/Tino_H20.lpk."""
from __future__ import annotations

import re
from pathlib import Path

import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from h20_hmi import apply_hmi, finalize_hmi_compact

NET_ONLY = "--net-only" in sys.argv
VER = "1.00"
LPK = ROOT / "Proj" / "Tino_H20.lpk"
SRC = LPK
REFILL_L = REFILL_D = "7"
WARN_L = WARN_D = "8"
FILL_PAGE = "1"
TRAV_PAGE = "2"
WARN_LT = "9"
WARN_DUR = "10"
if not SRC.is_file():
    raise SystemExit(f"manca {SRC}")
text = SRC.read_text(encoding="utf-8", errors="replace")
_text_disk = text

def repl_var_field(src: str, vid: int, field: str, value: str) -> str:
    return re.sub(
        rf"(Var_{vid}_{field}=).*",
        rf"\g<1>{value}",
        src,
        count=1,
    )


# --- Term / HMI / variables (skip with --net-only: isolate ladder compile) ---
if not NET_ONLY:
    # Do not set Term_Ena_ANA=True in the .lpk: Compila throws KeyNotFound
    # at "Elaborazione finale". Enable analog in LogicPaint Opzioni if needed.
    # Field backup already ran ADC DATA.417 with Term_Ena_ANA=False.
    text = apply_hmi(text)
    text = re.sub(r"(Term_Descrizione=).*", r"\1Tino_H20", text, count=1)
    text = re.sub(r"(Term_Ena_ANA=).*", r"\1False", text, count=1)

# --- Variable anagrafiche ---
text = repl_var_field(text, 1, "IndirizzoVar", "DATA.2040")
text = repl_var_field(text, 1, "RFS", "True")
text = repl_var_field(text, 2, "IndirizzoVar", "DATA.2041")
text = repl_var_field(text, 2, "RFS", "True")
text = repl_var_field(text, 2, "Descrizione", "RETE")
text = repl_var_field(text, 3, "IndirizzoVar", "DATA.2042")
text = repl_var_field(text, 3, "RFS", "True")
text = repl_var_field(text, 3, "Descrizione", "OSMOSI")
text = repl_var_field(text, 4, "IndirizzoVar", "DATA.2043")
text = repl_var_field(text, 4, "RFS", "True")
text = repl_var_field(text, 4, "Nome", "LED_EV")
text = repl_var_field(text, 5, "Dimensione", "WORD_WIDE")
text = repl_var_field(text, 6, "Dimensione", "WORD_WIDE")
text = repl_var_field(text, 6, "ENA", "False")
text = repl_var_field(text, 6, "CifreDecimali", "0")
text = repl_var_field(text, 7, "ENA", "False")
text = repl_var_field(text, 7, "Descrizione", "H CM CALCOLATA")
text = repl_var_field(text, 21, "IndirizzoVar", "DATA.4112")
if True:
    text = repl_var_field(text, 20, "CifreDecimali", "0")
    text = repl_var_field(text, 20, "CifreIntere", "2")
    text = repl_var_field(text, 20, "Massimo", "50")
    text = repl_var_field(text, 20, "Minimo", "0")
text = repl_var_field(text, 25, "IndirizzoVar", "DATA.4103")
text = repl_var_field(text, 26, "IndirizzoVar", "DATA.4100")
text = repl_var_field(text, 27, "IndirizzoVar", "DATA.4101")
text = repl_var_field(text, 28, "IndirizzoVar", "DATA.4102")
text = repl_var_field(text, 29, "IndirizzoVar", "DATA.4104")
if True:
    text = repl_var_field(text, 29, "CifreDecimali", "0")
    text = repl_var_field(text, 29, "CifreIntere", "2")
    text = repl_var_field(text, 29, "Massimo", "50")
    text = repl_var_field(text, 29, "Minimo", "0")
text = repl_var_field(text, 30, "IndirizzoVar", "DATA.4105")
text = repl_var_field(text, 31, "IndirizzoVar", "DATA.4106")
text = repl_var_field(text, 31, "Nome", "SMORZAMENTO SEC")
text = repl_var_field(text, 31, "Descrizione", "SMORZAMENTO LIVELLO S")
text = repl_var_field(text, 31, "Minimo", "1")
text = repl_var_field(text, 31, "Massimo", "15")
text = text.replace("FILTRO ISTERESI %", "SMORZAMENTO SEC")
text = text.replace("DATA.2016=FILTRO %", "DATA.2016=SMORZ SEC")
text = repl_var_field(text, 32, "IndirizzoVar", "DATA.4107")
text = repl_var_field(text, 33, "IndirizzoVar", "DATA.4108")
text = repl_var_field(text, 33, "Descrizione", "PORTATA RETE L/M")
text = repl_var_field(text, 33, "Massimo", "99")
text = repl_var_field(text, 33, "CifreIntere", "2")
text = repl_var_field(text, 34, "IndirizzoVar", "DATA.4109")
text = repl_var_field(text, 34, "Descrizione", "PORTATA OSMOSI L/M")
text = repl_var_field(text, 34, "Massimo", "99")
text = repl_var_field(text, 34, "CifreIntere", "2")
text = repl_var_field(text, 36, "IndirizzoVar", "DATA.4110")
text = repl_var_field(text, 36, "Descrizione", "PORTATA TRAVASO L/M")
text = repl_var_field(text, 36, "Massimo", "99")
text = repl_var_field(text, 36, "CifreIntere", "2")
text = repl_var_field(text, 37, "IndirizzoVar", "DATA.4111")
text = repl_var_field(text, 40, "Nome", "FLOW LM")
text = repl_var_field(text, 40, "Descrizione", "PORTATA L/M")
text = repl_var_field(text, 40, "Massimo", "99")
text = repl_var_field(text, 40, "CifreIntere", "2")
# H_ISTO REMOTE max must stay RAM (2006/2012). EEPROM 4101/4112 → KeyNotFound in Compila.
text = repl_var_field(text, 44, "Massimo", "2006")
text = repl_var_field(text, 44, "RFS", "True")
text = repl_var_field(text, 45, "Massimo", "1")
text = repl_var_field(text, 46, "Massimo", "2012")
text = repl_var_field(text, 46, "RFS", "True")
text = repl_var_field(text, 46, "NormInv", "True")
text = repl_var_field(text, 47, "RFS", "True")
text = repl_var_field(text, 48, "RFS", "True")
text = repl_var_field(text, 48, "NormInv", "True")
text = repl_var_field(text, 49, "RFS", "True")
text = repl_var_field(text, 49, "NormInv", "True")
text = repl_var_field(text, 50, "IndirizzoVar", "DATA.4113")
text = repl_var_field(text, 51, "IndirizzoVar", "DATA.4114")
text = repl_var_field(text, 52, "IndirizzoVar", "DATA.4115")
text = repl_var_field(text, 53, "Massimo", "2012")
text = repl_var_field(text, 53, "RFS", "True")
if True:
    text = repl_var_field(text, 58, "CifreDecimali", "0")
    text = repl_var_field(text, 58, "CifreIntere", "2")
    text = repl_var_field(text, 58, "Massimo", "50")
    text = repl_var_field(text, 58, "Minimo", "0")
text = repl_var_field(text, 5, "RFS", "True")

VAR54 = """
[Variabile_54]
Var_54_Nome=IDX SENS
Var_54_TipoVar=WORD
Var_54_Descrizione=0=0.3 BAR 1=2.0 BAR
Var_54_AreaVar=None
Var_54_IndirizzoVar=DATA.4116
Var_54_Minimo=0
Var_54_Massimo=1
Var_54_ComPort=INTERNAL
Var_54_IndStrumento=0
Var_54_IndPLC=1
Var_54_Dimensione=WORD_WIDE
Var_54_CifreIntere=1
Var_54_CifreDecimali=0
Var_54_Bit_Index=0
Var_54_UpdateTime=0
Var_54_Num_Curve=1
Var_54_Num_Ref=0
Var_54_DivAsseX=0
Var_54_DivAsseY=0
Var_54_Ref_0=0
Var_54_Ref_1=0
Var_54_ENA=True
Var_54_RFS=False
Var_54_INIBIT=False
Var_54_PWD=False
Var_54_REMOTE=False
Var_54_RIC=False
Var_54_SWAP=False
Var_54_IMM=False
Var_54_OMR_HEX=False
Var_54_HIDDEN=False
Var_54_INDEX=False
Var_54_ENG=False
Var_54_SCALE=False
Var_54_IndIndice=00
Var_54_NumElementi=0
Var_54_NormInv=False
Var_54_DecHex=True
Var_54_Obj2D3D=False
Var_54_NumObjV=0
Var_54_NumObjF=0
Var_54_Lingua_0_NumStrV=0
Var_54_Lingua_0_NumStrF=0
"""
# Variabile_54 TIMEOUT + 55-57 LONG: tools/h20_hmi.py (apply_hmi).

# --- HMI macros ---
# MAC_TOGGLE sul TP320 fa bip ma non muove i FLAG.
# Impulso: SETFLG al tocco + RESFLG al rilascio (come i tasti originali).
# Invert in ladder sul fronte 0→1, altrimenti il dito tenuto toggla ogni scan.
# FLAG HMI < 250: 255 è 0xFF (spesso “vuoto”), 256+ può wrappare su FLAG.00.
# FILL OSM/RETE: tap OSM/RETE/TRA attivi; MAN abilita anche da pagina FILL.
if False:
    text = text.replace(
        "Pag_1_Obj_17_KeyTouch_0_Macro_P=MAC_TOGGLE",
        "Pag_1_Obj_17_KeyTouch_0_Macro_P=MAC_NULL",
    )
    text = text.replace(
        "Pag_1_Obj_23_KeyTouch_0_Macro_P=MAC_TOGGLE",
        "Pag_1_Obj_23_KeyTouch_0_Macro_P=MAC_NULL",
    )
    text = text.replace(
        "Pag_8_Obj_17_KeyTouch_0_Macro_P=MAC_TOGGLE",
        "Pag_8_Obj_17_KeyTouch_0_Macro_P=MAC_NULL",
    )
    text = text.replace(
        "Pag_8_Obj_23_KeyTouch_0_Macro_P=MAC_TOGGLE",
        "Pag_8_Obj_23_KeyTouch_0_Macro_P=MAC_NULL",
    )


def _force_pulse_key(src: str, pag: int, oid: int, flag: int) -> str:
    pfx = f"Pag_{pag}_Obj_{oid}_KeyTouch_0_"
    if f"{pfx}Nome=" not in src:
        return src
    if f"{pfx}Macro_P=" not in src:
        src = re.sub(
            rf"({pfx}Nome=.*\n)({pfx}IndPLC_P=)",
            rf"\1{pfx}Macro_P=MAC_SETFLG\n{pfx}PaginaDATA_P={flag}\n{pfx}ValoreBit_P=0\n\2",
            src,
            count=1,
        )
    else:
        src = src.replace(f"{pfx}Macro_P=MAC_TOGGLE", f"{pfx}Macro_P=MAC_SETFLG")
        src = src.replace(f"{pfx}Macro_P=MAC_RESFLG", f"{pfx}Macro_P=MAC_SETFLG")
        src = src.replace(f"{pfx}Macro_P=MAC_NULL", f"{pfx}Macro_P=MAC_SETFLG")
        src = re.sub(rf"({pfx}PaginaDATA_P=)\d+", rf"\g<1>{flag}", src)
    if f"{pfx}Macro_R=" not in src:
        src = re.sub(
            rf"({pfx}Immagine_R=.*\n)",
            rf"\1{pfx}Macro_R=MAC_RESFLG\n{pfx}PaginaDATA_R={flag}\n{pfx}ValoreBit_R=0\n",
            src,
            count=1,
        )
    else:
        src = src.replace(f"{pfx}Macro_R=MAC_NULL", f"{pfx}Macro_R=MAC_RESFLG")
        src = re.sub(rf"({pfx}PaginaDATA_R=)\d+", rf"\g<1>{flag}", src)
    return src


_pulse_keys = [
    (0, 25, 254),
    (0, 26, 185),
    (0, 27, 186),
    (0, 28, 187),
    (1, 2, 238),
    (1, 4, 198),
    (1, 38, 254),
    (2, 2, 196),
    (2, 4, 197),
    (2, 19, 187),
    (2, 34, 254),
    (3, 30, 253),
    (6, 15, 235),
    (6, 20, 236),
    (6, 25, 237),
    (7, 25, 254),
    (7, 26, 185),
    (7, 27, 186),
    (7, 28, 187),
    (8, 2, 238),
    (8, 4, 198),
    (8, 38, 254),
    (9, 2, 196),
    (9, 4, 197),
    (9, 19, 187),
    (9, 34, 254),
    (10, 30, 253),
    (13, 15, 235),
    (13, 20, 236),
    (13, 25, 237),
]
if True:
    _pulse_keys.extend(((8, 17, 185), (8, 23, 186)))
for pag, oid, new_fl in _pulse_keys:
    text = _force_pulse_key(text, pag, oid, new_fl)


def make_key(pag: int, oid: int, x: int, y: int, w: int, h: int, name: str, flag: int, code: int) -> str:
    p = f"Pag_{pag}_Obj_{oid}"
    return f"""{p}_IdObj={oid}
{p}_Tipo=17
{p}_Modo=DRAW
{p}_X={x}
{p}_Y={y}
{p}_Width={w}
{p}_Height={h}
{p}_Spessore=1
{p}_ForeColor=-1
{p}_BackColor=-16776961
{p}_BoxColor=-16776961
{p}_GraphColor=-256
{p}_Font=0
{p}_LAMPEGGIO=False
{p}_COL_DINAMICO=False
{p}_IdVar=0
{p}_DimCarattere=D11
{p}_FormaCursore=2
{p}_DataSavePos=2
{p}_Code={code}
{p}_Grandezza=D11
{p}_BOX=False
{p}_KeyTouch_0_Immagine_P=0
{p}_KeyTouch_0_Nome={name}
{p}_KeyTouch_0_Macro_P=MAC_SETFLG
{p}_KeyTouch_0_PaginaDATA_P={flag}
{p}_KeyTouch_0_ValoreBit_P=0
{p}_KeyTouch_0_IndPLC_P=1
{p}_KeyTouch_0_PortaCOM_P=INTERNAL
{p}_KeyTouch_0_Immagine_R=0
{p}_KeyTouch_0_Macro_R=MAC_RESFLG
{p}_KeyTouch_0_PaginaDATA_R={flag}
{p}_KeyTouch_0_ValoreBit_R=0
{p}_KeyTouch_0_IndPLC_R=1
{p}_KeyTouch_0_PortaCOM_R=INTERNAL
{p}_KeyTouch_0_StatoLed=False
{p}_KeyTouch_0_Trasparente=True
{p}_KeyTouch_0_TextMenu=0:0
{p}_KeyTouch_0_TextMenu=1:0
"""


# HOME boxes: OSMOSI/RETE/TRAV → impulso SETFLG, TOGGLE in ladder (MAC_TOGGLE HMI è muto).
home_keys = (
    make_key(0, 26, 12, 104, 168, 24, "KEY.OSM", 185, 66)
    + make_key(0, 27, 12, 144, 168, 24, "KEY.RETE", 186, 67)
    + make_key(0, 28, 12, 184, 168, 24, "KEY.TRAV", 187, 68)
)
if "Pag_0_Obj_26_IdObj=26" not in text:
    text = text.replace("\n[Pagina_1]", "\n" + home_keys + "\n[Pagina_1]")

legacy_page7_keys = (
    make_key(7, 26, 12, 104, 168, 24, "KEY.OSM", 185, 66)
    + make_key(7, 27, 12, 144, 168, 24, "KEY.RETE", 186, 67)
    + make_key(7, 28, 12, 184, 168, 24, "KEY.TRAV", 187, 68)
)
if "Pag_7_Obj_26_IdObj=26" not in text:
    text = text.replace("\n[Pagina_8]", "\n" + legacy_page7_keys + "\n[Pagina_8]")

# IDX SENS WORD on TRASD (pag 5 obj 23) e gemella pag 12 — reuse last+1
# Pag 5 last is 22. Add label+word at y=168 if not present.


def make_text(pag: int, oid: int, x: int, y: int, w: int, h: int, label: str, fg: int, bg: int) -> str:
    p = f"Pag_{pag}_Obj_{oid}"
    return f"""{p}_IdObj={oid}
{p}_Tipo=2
{p}_Modo=DRAW
{p}_X={x}
{p}_Y={y}
{p}_Width={w}
{p}_Height={h}
{p}_Spessore=1
{p}_ForeColor={fg}
{p}_BackColor={bg}
{p}_BoxColor=-65536
{p}_GraphColor=-256
{p}_Font=0
{p}_LAMPEGGIO=False
{p}_COL_DINAMICO=False
{p}_IdVar=0
{p}_DimCarattere=D22
{p}_FormaCursore=0
{p}_DataSavePos=1000
{p}_Code=0
{p}_Grandezza=D11
{p}_BOX=False
{p}_ObjText.Testo=0:{label}
{p}_ObjText.ForeColor=0:{fg}
{p}_ObjText.BackColor=0:{bg}
{p}_ObjText.FontText=0:0
{p}_ObjText.X_Lang=0:{x}
{p}_ObjText.Y_Lang=0:{y}
{p}_ObjText.Dim_Lang=0:D22
{p}_ObjText.Testo=1:{label}
{p}_ObjText.ForeColor=1:{fg}
{p}_ObjText.BackColor=1:{bg}
{p}_ObjText.FontText=1:0
{p}_ObjText.X_Lang=1:{x}
{p}_ObjText.Y_Lang=1:{y}
{p}_ObjText.Dim_Lang=1:D22
"""


def make_word(pag: int, oid: int, x: int, y: int, vid: int, fg: int, bg: int, w: int = 72) -> str:
    p = f"Pag_{pag}_Obj_{oid}"
    return f"""{p}_IdObj={oid}
{p}_Tipo=11
{p}_Modo=DRAW
{p}_X={x}
{p}_Y={y}
{p}_Width={w}
{p}_Height=24
{p}_Spessore=1
{p}_ForeColor={fg}
{p}_BackColor={bg}
{p}_BoxColor=-65536
{p}_GraphColor=-256
{p}_Font=0
{p}_LAMPEGGIO=False
{p}_COL_DINAMICO=False
{p}_IdVar={vid}
{p}_DimCarattere=D11
{p}_FormaCursore=0
{p}_DataSavePos=1000
{p}_Code=0
{p}_Grandezza=D22
{p}_BOX=True
"""


# FLOW WORD più stretto per l'unità l/m a destra.
for pag, oid in ((1, 27), (2, 23), (8, 27), (9, 23)):
    text = re.sub(rf"(Pag_{pag}_Obj_{oid}_Width=)72", r"\g<1>48", text, count=1)

# Unità dopo ETA / FLOW (FILL 1/8, TRAVASO 2/9).
_fg_l, _bg_l = -16777216, -4144960
_fg_d, _bg_d = -1, -16777216
_unit_specs = (
    (1, 39, 40, _fg_l, _bg_l, "[Pagina_2]"),
    (2, 37, 38, _fg_l, _bg_l, "[Pagina_3]"),
    (8, 39, 40, _fg_d, _bg_d, "[Pagina_9]"),
    (9, 37, 38, _fg_d, _bg_d, "[Pagina_10]"),
)
for pag, oid_min, oid_lm, fg, bg, nxt in _unit_specs:
    if f"Pag_{pag}_Obj_{oid_min}_IdObj={oid_min}" not in text:
        text = text.replace(
            f"\n{nxt}",
            "\n"
            + make_text(pag, oid_min, 108, 184, 32, 16, "min", fg, bg)
            + make_text(pag, oid_lm, 256, 184, 36, 16, "l/m", fg, bg)
            + f"\n{nxt}",
        )

text = text.replace("FLOW OSMOSI LT/H", "FLOW OSMOSI L/M")
text = text.replace("FLOW RETE LT/H", "FLOW RETE L/M")
text = text.replace("FLOW TRAV LT/H", "FLOW TRAV L/M")

# TP320: i WORD si vedono più in alto nel riquadro che in LogicPaint → +2 px (idempotente).
def _bump_word_y(src: str, dy: int = 2) -> str:
    out = src
    for m in re.finditer(r"Pag_(\d+)_Obj_(\d+)_Tipo=11\n", src):
        pag, oid = m.group(1), m.group(2)
        key = f"Pag_{pag}_Obj_{oid}_Y="
        vm = re.search(rf"{key}(\d+)", out)
        if not vm:
            continue
        y = int(vm.group(1))
        if y % 8 in (0, 4):
            out = re.sub(rf"({key}){y}\b", rf"\g<1>{y + dy}", out, count=1)
    return out


text = _bump_word_y(text)
text = text.replace("DATA.2025=FLOW LH\n", "DATA.2025=FLOW LM\n")

# TIMEOUT / CONTAT HMI: apply_hmi() when not --net-only.

# --- Simbolici flags ---
if "FLAG.207=" not in text:
    text = text.replace(
        "FLAG.206=MAN RETE\nFLAG.210=",
        "FLAG.206=MAN RETE\nFLAG.207=MAN POMPA\nFLAG.208=FILL STAB\nFLAG.209=MAN PREV\nFLAG.210=",
    )
if "FLAG.220=" not in text:
    text = text.replace(
        "FLAG.212=ALR VUOTO\n",
        "FLAG.212=ALR VUOTO\nFLAG.220=SAVE EEPROM\nFLAG.221=EE VIRGIN\n",
    )

if "DATA.2040=" not in text:
    text = text.replace(
        "DATA.2029=ZERO 4mA\n",
        "DATA.2029=ZERO 4mA\nDATA.2040=LED POMPA\nDATA.2041=LED RETE\nDATA.2042=LED OSMOSI\nDATA.2043=LED EV\n",
    )
if "DATA.4100=" not in text:
    text = text.replace(
        "DATA.2043=LED EV\n",
        "DATA.2043=LED EV\nDATA.4100=CIRC CM\nDATA.4101=LT TOT\nDATA.4102=OFFSET L\nDATA.4103=ALLARME LIV\n"
        "DATA.4104=DUR RETE\nDATA.4105=TOLL MIX\nDATA.4106=SMORZ SEC\nDATA.4107=FS BAR\n"
        "DATA.4108=LTH RETE\nDATA.4109=LTH OSM\nDATA.4110=LTH TRAV\nDATA.4111=T STAB\n"
        "DATA.4112=LT TRAVASO\nDATA.4113=ZERO 4mA EE\nDATA.4114=BANDA MORTA\nDATA.4115=CAMP SEC\n"
        "DATA.4116=TIMEOUT MIN\nDATA.1200=SCRATCH L0\nDATA.1220=PROM A\nDATA.1222=PROM B\n"
        "DATA.2036=CAMP CNT\nDATA.2037=STAB CNT\nDATA.2050=TRAV REST\nDATA.2051=VO TOLL\n"
        "DATA.2052=FLOW DLT\nDATA.2053=DEAD LIV\nDATA.2054=ETA REST\nDATA.2055=ADC DLT\n"
        "DATA.2057=T FILT M1\n",
        1,
    )
if "DATA.2056=" not in text:
    text = text.replace("DATA.2055=ADC DLT\n", "DATA.2055=ADC DLT\nDATA.2056=T FILT M1\n")

# --net-only: keep the HMI that already compiles (TEST-207 era), rewrite only Net.0.
if NET_ONLY:
    text = _text_disk
text = text.replace("Pag_0_NomePagina=TEST-207", "Pag_0_NomePagina=HOME")


# =============================================================================
# Ladder generator
# =============================================================================

# Scan AWL: main in Net.0, END+SBR in Net.1 (come ladder che compila).
# Two 1-row rungs must not share columns on consecutive rows (vertical short).
# v1 puts OUT.04 on row 3; row 1-2 are the INP.03 OR we dropped.
MAX_NET_Y = 2000


class Net:
    def __init__(self, idx: int = 0):
        self.idx = idx
        self.lines: list[str] = []
        self.max_row = 0
        self.clines: dict[int, str] = {}

    def _cell(self, r: int, c: int, bmp: int, strum: int, addr: str = "", data: list | None = None, cas: int = 0, comment: str = "", incond: bool = False):
        p = f"Net_{self.idx:04d}_C_{r:04d};{c:04d}"
        self.max_row = max(self.max_row, r)
        self.lines.append(f"{p}_BitMap={bmp}")
        self.lines.append(f"{p}_Commento=")
        if data:
            for i, d in enumerate(data):
                self.lines.append(f"{p}_Data({i})={d}")
                self.lines.append(f"{p}_DecHex({i})=True")
                self.lines.append(f"{p}_ConSegno({i})=False")
                self.lines.append(f"{p}_Puntatore({i})=False")
        elif comment:
            self.lines.append(f"{p}_Data(0)={comment}")
            self.lines.append(f"{p}_DecHex(0)=True")
            self.lines.append(f"{p}_ConSegno(0)=False")
            self.lines.append(f"{p}_Puntatore(0)=False")
        self.lines.append(f"{p}_Fronte=0")
        self.lines.append(f"{p}_Incondizionato={'True' if incond else 'False'}")
        self.lines.append(f"{p}_Indirizzo={addr}")
        self.lines.append(f"{p}_Mascherato=False")
        self.lines.append(f"{p}_Strumento={strum}")
        self.lines.append(f"{p}_CasellaFunzione={cas}")

    def wire(self, r: int, c: int):
        self._cell(r, c, 30, 5)

    def no(self, r: int, c: int, addr: str, comment: str = "", bmp: int = 2):
        self._cell(r, c, bmp, 1, addr, comment=comment)

    def nc(self, r: int, c: int, addr: str, comment: str = ""):
        self._cell(r, c, 9, 2, addr, comment=comment)

    def coil(self, r: int, c: int, addr: str, data: list | None = None, comment: str = ""):
        if data:
            self._cell(r, c, 16, 3, addr, data=data)
        elif comment:
            self._cell(r, c, 16, 3, addr, comment=comment)
        else:
            self._cell(r, c, 16, 3, addr)

    def vor_up(self, r: int, c: int = 1):
        self._cell(r, c, 41, 9)

    def vor_dn(self, r: int, c: int = 1):
        self._cell(r, c, 40, 9)

    def fn(self, r: int, c: int, op: str, data: list, cmp=False, incond: bool = False):
        bmp2 = 46 if cmp else 45
        self._cell(r, c, 43, 6, op, data=data, cas=1, incond=incond)
        self._cell(r, c + 1, bmp2, 6, op, data=data, cas=2, incond=incond)
        self._cell(r + 1, c, 42, 6, op, data=data, cas=3, incond=incond)
        self._cell(r + 1, c + 1, 61, 6, op, data=data, cas=4, incond=incond)

    def rung_fn(
        self,
        r: int,
        contacts: list,
        op: str,
        data: list,
        cmp=False,
        fncol=None,
        result_coil=None,
        result_coil_data=None,
    ):
        """contacts: list of (type, addr, comment) type in no/nc.

        CMP without a same-row coil is emitted as two `LD SYS.0x` (stack leak).
        After enough of those, plc_comp reports Stack ERROR. Always coil the
        compare result: pass result_coil, or FLAG.249 as a dummy sink.
        """
        if fncol is None:
            fncol = max(4, len(contacts))
        for i, (kind, addr, com) in enumerate(contacts):
            if kind == "no":
                self.no(r, i, addr, com)
            else:
                self.nc(r, i, addr, com)
        for col in range(len(contacts), fncol):
            self.wire(r, col)
        self.fn(r, fncol, op, data, cmp=cmp)
        if cmp:
            self.coil(
                r,
                fncol + 2,
                result_coil if result_coil is not None else "FLAG.249",
                data=result_coil_data,
            )

    def rung_coil(self, r: int, contacts: list, coil_addr: str, coil_data=None, comment="", coilcol=None):
        if coilcol is None:
            coilcol = max(4, len(contacts))
        for i, (kind, addr, com) in enumerate(contacts):
            if kind == "no":
                self.no(r, i, addr, com)
            else:
                self.nc(r, i, addr, com)
        for col in range(len(contacts), coilcol):
            self.wire(r, col)
        self.coil(r, coilcol, coil_addr, data=coil_data, comment=comment)

    def cmt(self, r: int, s: str):
        self.clines[r] = s


if not NET_ONLY:
    text = finalize_hmi_compact(text)

n = Net()

# ----- 0 emergency latch (same as original) -----
n.cmt(0, "Emergenza latch")
n.no(0, 0, "FLAG.00", "RESET EMERG")
n.no(0, 1, "INP.01", "EMERGENZA")
# BitMap 6 = NO with vertical OR down. v1 has vor_up at (1,1); without it Compila
# reports Net.0 Riga 0 Colonna 1. Plain contact is BitMap 2 (default).
n.wire(0, 2)
n.wire(0, 3)
n.coil(0, 4, "FLAG.01", comment="EMERGENZA OK")
# Same row as v1 (3). Rows 1-2 stay empty: a 1-row rung on row 1 under the
# latch shares columns with INP.01 and Compila reports Riga 0 Colonna 1.
n.no(3, 0, "FLAG.01", "EMERGENZA OK")
n.wire(3, 1)
n.wire(3, 2)
n.wire(3, 3)
n.coil(3, 4, "OUT.04")

# ----- 5 emergency kill -----
n.cmt(5, "Emergenza DOWN: spegne ricette e uscite")
rr = 5
for fl in [
        "FLAG.200",
        "FLAG.201",
        "FLAG.202",
        "FLAG.203",
        "FLAG.205",
        "FLAG.206",
        "FLAG.207",
        "FLAG.208",
        "FLAG.228",
        "FLAG.229",
        "FLAG.234",
        "FLAG.185",
        "FLAG.186",
        "FLAG.187",
        "FLAG.188",
        "FLAG.189",
        "FLAG.190",
        "FLAG.191",
        "FLAG.192",
        "FLAG.193",
        "FLAG.194",
        "FLAG.195",
        "FLAG.182",
        "FLAG.183",
        "FLAG.184",
        "FLAG.196",
        "FLAG.197",
        "FLAG.198",
        "FLAG.199",
        "FLAG.254",
    "FLAG.00",
    "FLAG.238",
    "FLAG.240",
        "FLAG.241",
        "FLAG.242",
        "FLAG.169",
        "FLAG.174",
        "FLAG.175",
        "FLAG.176",
        "FLAG.177",
        "FLAG.178",
        "FLAG.180",
        "FLAG.181",
]:
    n.rung_fn(rr, [("nc", "FLAG.01", "")], "RES", [fl])
    rr += 2

n.rung_fn(rr, [("nc", "FLAG.01", "")], "RES", ["OUT.00"])
rr += 2
n.rung_fn(rr, [("nc", "FLAG.01", "")], "RES", ["OUT.01"])
rr += 2
n.rung_fn(rr, [("nc", "FLAG.01", "")], "RES", ["OUT.02"])
rr += 2
n.rung_fn(rr, [("nc", "FLAG.01", "")], "RES", ["OUT.03"])
rr += 3

n.cmt(rr, "Solo emergenza su DATA.08 (pagina Alr blocca il touch)")
n.rung_coil(rr, [("nc", "INP.01", "EMERGENZA")], "DATA.08", coil_data=["ALRM 000-015", "1"], coilcol=2)
rr += 3

n.cmt(rr, "INP.00 termico: pompa e ricette off")
for fl in [
    "FLAG.200",
    "FLAG.201",
    "FLAG.202",
    "FLAG.203",
    "FLAG.205",
    "FLAG.206",
    "FLAG.207",
    "FLAG.208",
    "FLAG.228",
    "FLAG.229",
    "FLAG.234",
    "FLAG.238",
    "FLAG.240",
    "FLAG.241",
    "FLAG.242",
    "FLAG.169",
    "FLAG.176",
    "FLAG.177",
    "FLAG.185",
    "FLAG.186",
    "FLAG.187",
    "FLAG.188",
    "FLAG.189",
    "FLAG.190",
    "FLAG.191",
    "FLAG.192",
    "FLAG.193",
    "FLAG.194",
    "FLAG.195",
    "FLAG.182",
    "FLAG.183",
    "FLAG.184",
    "FLAG.196",
    "FLAG.197",
    "FLAG.198",
    "FLAG.199",
    "FLAG.254",
    "FLAG.178",
    "FLAG.180",
    "FLAG.181",
]:
    n.rung_fn(rr, [("no", "INP.00", "TERMICO POMPE")], "RES", [fl])
    rr += 2

# ----- recipe alarms bits -----
# Solo Alr.1 emergenza su DATA.08. Termico, OSM, target, pieno, vuoto, stallo:
# warning + sicurezze in ladder, pagine usabili.
# DATA.01 e' la word comandi HMI (bit 3 = tastiera aperta). Bobina CMP sul
# DATA intero azzera quel bit ogni scan → tastiera Γ e buzzer. Come DATA.08:
# CMP su FLAG, poi BOUT sul bit.
n.cmt(rr, "Beep se emergenza (DATA.08)")
n.rung_fn(
    rr,
    [("no", "SYS.01", "Sempre Vero")],
    "CMP",
    ["0", "DATA.08", "2"],
    cmp=True,
    result_coil="FLAG.265",
)
rr += 4
n.rung_coil(rr, [("no", "FLAG.265", "")], "DATA.01", coil_data=["Comandi", "1"])
rr += 2

# ----- EEPROM virgin defaults -----
# Dopo Full Erase / OS update la EEPROM e' FFFF, non 0: il solo CMP vs 0
# saltava i default e LIV/ALLARME restavano fuori scala.
n.cmt(rr, "EEPROM virgin: CIRC=0 o FFFF (ogni scan)")
n.rung_fn(
    rr,
    [("no", "SYS.01", "Sempre Vero")],
    "CMP",
    ["0", "DATA.4100", "1"],
    cmp=True,
    result_coil="FLAG.221",
)
rr += 3
n.rung_fn(
    rr,
    [("no", "SYS.01", "")],
    "CMP",
    ["65535", "DATA.4100", "1"],
    cmp=True,
    result_coil="FLAG.252",
)
rr += 3
n.rung_fn(rr, [("no", "FLAG.252", "")], "SET", ["FLAG.221"])
rr += 2
# CARICA DEFAULT: fronte FLAG.253 (HMI SETFLG/RESFLG), non ogni scan col dito tenuto.
n.rung_fn(rr, [("no", "FLAG.253", ""), ("nc", "FLAG.195", "")], "SET", ["FLAG.221"])
rr += 2

defaults = [
    ("399", "DATA.4100"),
    ("2500", "DATA.4101"),
    ("85", "DATA.4102"),
    ("2400", "DATA.4103"),
    ("24", "DATA.4104"),
    ("20", "DATA.4105"),
    ("3", "DATA.4106"),
    ("20", "DATA.4107"),
    ("22", "DATA.4108"),
    ("7", "DATA.4109"),
    ("26", "DATA.4110"),
    ("30", "DATA.4111"),
    ("330", "DATA.4112"),
    ("786", "DATA.4113"),
    ("20", "DATA.4114"),
    ("3", "DATA.4115"),
    ("20", "DATA.4116"),
    ("2300", "DATA.2004"),
    ("8", "DATA.2005"),
]
r = rr
for src, dst in defaults:
    n.rung_fn(r, [("no", "FLAG.221", "")], "MOV", [src, dst])
    r += 2
n.rung_fn(r, [("no", "FLAG.221", "")], "SET", ["FLAG.220"])
r += 2
n.rung_fn(r, [("no", "FLAG.253", "")], "SET", ["FLAG.195"])
r += 2
n.rung_fn(r, [("nc", "FLAG.253", "")], "RES", ["FLAG.195"])
r += 2
n.rung_fn(r, [("no", "FLAG.221", "")], "RES", ["FLAG.253"])
r += 2

n.rung_fn(r, [("no", "SYS.02", "")], "SET", ["FLAG.00"])
r += 2
# Tasto RESET blu quadro (E3 → INP.03): stesso SET del tap HOME.
n.rung_fn(r, [("no", "INP.03", "RESET BLU")], "SET", ["FLAG.00"])
r += 2
n.rung_fn(
    r,
    [("no", "SYS.02", "")],
    "CMP",
    ["0", "DATA.2004", "1"],
    cmp=True,
)
r += 3
n.rung_fn(
    r,
    [("no", "SYS.02", ""), ("no", "SYS.03", "")],
    "MOV",
    ["2300", "DATA.2004"],
)
r += 2
n.rung_fn(
    r,
    [("no", "SYS.02", "")],
    "CMP",
    ["0", "DATA.2005", "1"],
    cmp=True,
)
r += 3
n.rung_fn(
    r,
    [("no", "SYS.02", ""), ("no", "SYS.03", "")],
    "MOV",
    ["8", "DATA.2005"],
)
r += 2
if True:
    n.rung_fn(r, [("no", "SYS.02", "")], "CMP", ["50", "DATA.2005", "2"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.02", ""), ("no", "SYS.04", "")], "DIV", ["10", "DATA.2005"])
    r += 2

n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["0", "DATA.2030"])
r += 2

# Old FILTRO % (es. 90) non e' un tempo in secondi: riportalo a 3.
n.cmt(r, "SMORZ SEC: EEPROM fuori 1-15 (vecchio %) -> 3")
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["15", "DATA.4106", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["3", "DATA.4106"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["1", "DATA.4106", "4"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.05", "")], "MOV", ["3", "DATA.4106"])
r += 2

if True:
    # DUR RETE in °F interi. EEPROM con decimi (51-500) /10.
    n.cmt(r, "DUR RETE decimi 51-500 -> intero; 0 o >500 -> 24 (SYS.02)")
    n.rung_fn(
        r,
        [("no", "SYS.02", "")],
        "CMP",
        ["500", "DATA.4104", "2"],
        cmp=True,
        result_coil="FLAG.267",
    )
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.02", "")],
        "CMP",
        ["50", "DATA.4104", "2"],
        cmp=True,
        result_coil="FLAG.262",
    )
    r += 3
    n.rung_fn(r, [("no", "FLAG.262", ""), ("nc", "FLAG.267", "")], "DIV", ["10", "DATA.4104"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.262", ""), ("nc", "FLAG.267", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(
        r,
        [("no", "SYS.02", "")],
        "CMP",
        ["0", "DATA.4104", "1"],
        cmp=True,
        result_coil="FLAG.264",
    )
    r += 3
    n.rung_fn(r, [("no", "FLAG.264", "")], "MOV", ["24", "DATA.4104"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.267", "")], "MOV", ["24", "DATA.4104"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.264", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.267", "")], "SET", ["FLAG.220"])
    r += 3
else:
    n.cmt(r, "DUR RETE 1-50 (vecchio intero) -> decimi (SYS.02)")
    n.rung_fn(
        r,
        [("no", "SYS.02", "")],
        "CMP",
        ["51", "DATA.4104", "4"],
        cmp=True,
        result_coil="FLAG.262",
    )
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.02", "")],
        "CMP",
        ["0", "DATA.4104", "2"],
        cmp=True,
        result_coil="FLAG.263",
    )
    r += 3
    n.rung_fn(r, [("no", "FLAG.263", "")], "MUL", ["10", "DATA.4104"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.263", "")], "SET", ["FLAG.220"])
    r += 3
    n.cmt(r, "DUR RETE 0 o >500 (FFFF) -> 22.0 (SYS.02)")
    n.rung_fn(
        r,
        [("no", "SYS.02", "")],
        "CMP",
        ["0", "DATA.4104", "1"],
        cmp=True,
        result_coil="FLAG.264",
    )
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.02", "")],
        "CMP",
        ["500", "DATA.4104", "2"],
        cmp=True,
        result_coil="FLAG.267",
    )
    r += 3
    n.rung_fn(r, [("no", "FLAG.264", "")], "MOV", ["220", "DATA.4104"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.267", "")], "MOV", ["220", "DATA.4104"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.264", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.267", "")], "SET", ["FLAG.220"])
    r += 3

# ----- EEPROM -> RAM mirrors -----
n.cmt(r, "Copia SETUP EEPROM -> runtime RAM")
mirrors = [
    ("DATA.4100", "DATA.2011"),
    ("DATA.4101", "DATA.2012"),
    ("DATA.4102", "DATA.2013"),
    ("DATA.4103", "DATA.2010"),
    ("DATA.4104", "DATA.2014"),
    ("DATA.4105", "DATA.2015"),
    ("DATA.4106", "DATA.2016"),
    ("DATA.4107", "DATA.2017"),
    ("DATA.4108", "DATA.2018"),
    ("DATA.4109", "DATA.2019"),
    ("DATA.4110", "DATA.2021"),
    ("DATA.4111", "DATA.2022"),
    ("DATA.4112", "DATA.2006"),
    ("DATA.4113", "DATA.2029"),
    ("DATA.4114", "DATA.2033"),
    ("DATA.4115", "DATA.2034"),
    ("DATA.4116", "DATA.2044"),
]
for a, b in mirrors:
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", [a, b])
    r += 2

n.cmt(r, "Clamp FS 3..20 e TIMEOUT 0..60")
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["3", "DATA.4107", "4"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.05", "")], "MOV", ["3", "DATA.4107"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["20", "DATA.4107", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["20", "DATA.4107"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.4107", "DATA.2017"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["60", "DATA.4116", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["60", "DATA.4116"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.4116", "DATA.2044"])
r += 2


def prom(rr, src, dest, contacts=None):
    if contacts is None:
        contacts = [("no", "SYS.01", "")]
    hi = int(dest.split(".")[1]) + 1
    n.rung_fn(rr, contacts, "MOV", [src, dest])
    n.rung_fn(rr + 2, contacts, "MOV", ["0", f"DATA.{hi}"])
    return rr + 4


def klong(rr, const, dest, contacts=None):
    if contacts is None:
        contacts = [("no", "SYS.01", "")]
    hi = int(dest.split(".")[1]) + 1
    n.rung_fn(rr, contacts, "MOV", [str(const), dest])
    n.rung_fn(rr + 2, contacts, "MOV", ["0", f"DATA.{hi}"])
    return rr + 4


def l_to_cm(rr, contacts, liters, dest_cm):
    """cm = liters * 1000 / AREA (DATA.2000). Scratch 1200/1202/1220."""
    rr = prom(rr, liters, "DATA.1220", contacts)
    rr = klong(rr, 1000, "DATA.1222", contacts)
    n.rung_fn(rr, contacts, "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
    rr += 3
    rr = prom(rr, "DATA.2000", "DATA.1220", contacts)
    n.rung_fn(rr, contacts, "LEDIV", ["DATA.1220", "DATA.1200", "DATA.1202"])
    rr += 3
    n.rung_fn(rr, contacts, "MOV", ["DATA.1202", dest_cm])
    return rr + 2


def cm_to_l(rr, contacts, cm, dest_l):
    """L = cm * AREA / 1000. Scratch 1200/1202/1220."""
    rr = prom(rr, cm, "DATA.1220", contacts)
    rr = prom(rr, "DATA.2000", "DATA.1222", contacts)
    n.rung_fn(rr, contacts, "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
    rr += 3
    rr = klong(rr, 1000, "DATA.1220", contacts)
    n.rung_fn(rr, contacts, "LEDIV", ["DATA.1220", "DATA.1200", "DATA.1202"])
    rr += 3
    n.rung_fn(rr, contacts, "MOV", ["DATA.1202", dest_l])
    return rr + 2


# DATA.2030 = costante 0 (Var_45 ZERO). EADD/LEADD non sono nel set opcode di v1
# (KeyNotFoundException in Compila): dest = a + b  <=>  tmp = 0 - a ; dest = b - tmp
ZERO = "DATA.2030"
NEG16 = "DATA.2055"


def eadd16(rr, contacts, a, b, dest, tmp=NEG16):
    n.rung_fn(rr, contacts, "ESUB", [a, ZERO, tmp])
    n.rung_fn(rr + 3, contacts, "ESUB", [tmp, b, dest])
    return rr + 6


def leadd32(rr, a, b, dest, tmp="DATA.1222", contacts=None):
    if contacts is None:
        contacts = [("no", "SYS.01", "")]
    n.rung_fn(rr, contacts, "MOV", ["0", "DATA.1220"])
    n.rung_fn(rr + 2, contacts, "MOV", ["0", "DATA.1221"])
    n.rung_fn(rr + 4, contacts, "LESUB", [a, "DATA.1220", tmp])
    n.rung_fn(rr + 7, contacts, "LESUB", [tmp, b, dest])
    return rr + 10


def geq_set(rr, owner, a, b, dest_flag):
    """CMP always on SYS.01; SET dest only if owner AND a>=b (SYS letto subito)."""
    n.rung_fn(rr, [("no", "SYS.01", "")], "RES", [dest_flag])
    n.rung_fn(rr + 2, [("no", "SYS.01", "")], "CMP", [a, b, "4"], cmp=True)
    n.rung_fn(rr + 5, [("no", "SYS.05", ""), ("no", owner, "")], "SET", [dest_flag])
    n.rung_fn(rr + 7, [("no", "SYS.01", "")], "CMP", [a, b, "1"], cmp=True)
    n.rung_fn(rr + 10, [("no", "SYS.03", ""), ("no", owner, "")], "SET", [dest_flag])
    return rr + 12


# ----- LEVEL -----
n.cmt(r, "Livello: ADC417 - ZERO, h_cm, AREA, LIV (LONG solo su 1200+)")
# counts = max(0, ADC - ZERO) in 2055
n.rung_fn(r, [("no", "SYS.01", "")], "ESUB", ["DATA.2029", "DATA.417", "DATA.2055"])
r += 3
n.rung_fn(
    r,
    [("no", "SYS.01", "")],
    "CMP",
    ["DATA.417", "DATA.2029", "2"],
    cmp=True,
    result_coil="FLAG.214",
)
r += 3
n.rung_fn(r, [("no", "FLAG.214", "")], "MOV", ["0", "DATA.2055"])
r += 3
# h_cm = counts * FS * 1020 / 3280 / 10
r = prom(r, "DATA.2055", "DATA.1220")
r = prom(r, "DATA.2017", "DATA.1222")
n.rung_fn(r, [("no", "SYS.01", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
r += 3
r = klong(r, 1020, "DATA.1222")
n.rung_fn(r, [("no", "SYS.01", "")], "LEMUL", ["DATA.1200", "DATA.1222", "DATA.1202"])
r += 3
r = klong(r, 3280, "DATA.1220")
n.rung_fn(r, [("no", "SYS.01", "")], "LEDIV", ["DATA.1220", "DATA.1202", "DATA.1204"])
r += 3
r = klong(r, 10, "DATA.1220")
n.rung_fn(r, [("no", "SYS.01", "")], "LEDIV", ["DATA.1220", "DATA.1204", "DATA.1206"])
r += 3
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.1206", "DATA.2001"])
r += 2
# AREA = CIRC*CIRC*100/1257
r = prom(r, "DATA.2011", "DATA.1220")
n.rung_fn(r, [("no", "SYS.01", "")], "LEMUL", ["DATA.1220", "DATA.1220", "DATA.1208"])
r += 3
r = klong(r, 100, "DATA.1222")
n.rung_fn(r, [("no", "SYS.01", "")], "LEMUL", ["DATA.1208", "DATA.1222", "DATA.1210"])
r += 3
r = klong(r, 1257, "DATA.1220")
n.rung_fn(r, [("no", "SYS.01", "")], "LEDIV", ["DATA.1220", "DATA.1210", "DATA.1212"])
r += 3
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.1212", "DATA.2000"])
r += 2
# LIV_g = OFFSET + h_cm * AREA / 1000
r = prom(r, "DATA.2001", "DATA.1220")
r = prom(r, "DATA.2000", "DATA.1222")
n.rung_fn(r, [("no", "SYS.01", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1214"])
r += 3
r = klong(r, 1000, "DATA.1220")
n.rung_fn(r, [("no", "SYS.01", "")], "LEDIV", ["DATA.1220", "DATA.1214", "DATA.1216"])
r += 3
r = eadd16(r, [("no", "SYS.01", "")], "DATA.2013", "DATA.1216", "DATA.2028")
# SMORZAMENTO SEC (2016): IIR 1 Hz  2007 = (2007*(T-1) + 2028) / T
# T=1: passa il grezzo ogni scan. Seed se 2007=0 (power-on).
n.rung_fn(r, [("no", "SYS.01", "")], "ESUB", ["1", "DATA.2016", "DATA.2056"])
r += 3
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["0", "DATA.2007", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.03", "")], "MOV", ["DATA.2028", "DATA.2007"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["1", "DATA.2016", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.03", "")], "MOV", ["DATA.2028", "DATA.2007"])
r += 2
tick = [("no", "SYS.10", "")]
r = prom(r, "DATA.2007", "DATA.1220", tick)
r = prom(r, "DATA.2056", "DATA.1222", tick)
n.rung_fn(r, tick, "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1208"])
r += 3
r = prom(r, "DATA.2028", "DATA.1216", tick)
n.rung_fn(r, tick, "MOV", ["0", "DATA.1220"])
r += 2
n.rung_fn(r, tick, "MOV", ["0", "DATA.1221"])
r += 2
n.rung_fn(r, tick, "LESUB", ["DATA.1208", "DATA.1220", "DATA.1222"])
r += 3
n.rung_fn(r, tick, "LESUB", ["DATA.1222", "DATA.1216", "DATA.1212"])
r += 3
r = prom(r, "DATA.2016", "DATA.1220", tick)
n.rung_fn(r, tick, "LEDIV", ["DATA.1220", "DATA.1212", "DATA.1214"])
r += 3
n.rung_fn(r, tick, "MOV", ["DATA.1214", "DATA.2007"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2007", "DATA.1000"])
r += 2
# % = 1000*100/LT_TOT
r = prom(r, "DATA.1000", "DATA.1220")
r = klong(r, 100, "DATA.1222")
n.rung_fn(r, [("no", "SYS.01", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1218"])
r += 3
n.rung_fn(
    r,
    [("no", "SYS.01", "")],
    "CMP",
    ["0", "DATA.2012", "2"],
    cmp=True,
    result_coil="FLAG.216",
)
r += 3
r = prom(r, "DATA.2012", "DATA.1220")
n.rung_fn(r, [("no", "FLAG.216", "")], "LEDIV", ["DATA.1220", "DATA.1218", "DATA.1200"])
r += 3
n.rung_fn(r, [("no", "FLAG.216", "")], "MOV", ["DATA.1200", "DATA.2023"])
r += 2
n.rung_fn(r, [("nc", "FLAG.216", "")], "MOV", ["0", "DATA.2023"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["100", "DATA.2023", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["100", "DATA.2023"])
r += 3

# ----- ALARMS 210 211 -----
n.cmt(r, "FLAG.210 target>allarme  FLAG.211 liv>allarme")
n.rung_fn(
    r,
    [("no", "SYS.01", "")],
    "CMP",
    ["DATA.2004", "DATA.2010", "4"],
    cmp=True,
    result_coil="FLAG.210",
)
r += 3
n.rung_fn(
    r,
    [("no", "SYS.01", "")],
    "CMP",
    ["DATA.2007", "DATA.2010", "4"],
    cmp=True,
    result_coil="FLAG.211",
)
r += 3
n.rung_fn(r, [("no", "FLAG.211", "")], "RES", ["OUT.02"])
r += 2
n.rung_fn(r, [("no", "FLAG.211", "")], "RES", ["OUT.03"])
r += 2
n.rung_fn(r, [("no", "FLAG.211", "")], "RES", ["FLAG.205"])
r += 2
n.rung_fn(r, [("no", "FLAG.211", "")], "RES", ["FLAG.206"])
r += 2
n.rung_fn(r, [("no", "FLAG.200", ""), ("no", "FLAG.211", "")], "RES", ["FLAG.201"])
r += 2
n.rung_fn(r, [("no", "FLAG.200", ""), ("no", "FLAG.211", "")], "RES", ["FLAG.202"])
r += 2
n.rung_fn(r, [("no", "FLAG.200", ""), ("no", "FLAG.211", "")], "RES", ["FLAG.208"])
r += 2
n.rung_fn(r, [("no", "FLAG.200", ""), ("no", "FLAG.211", "")], "RES", ["FLAG.200"])
r += 3

# ----- MAN -----
# HMI: SETFLG al tocco, RESFLG al rilascio. Invert solo sul fronte 0→1
# (dito tenuto = SET ogni scan → senza prev il target oscilla e non si spegne).
# OSM/RETE/TRAV solo se MAN già ON; il fronte si consuma comunque (niente coda).
def pulse_toggle(row, pulse, target, prev, gate=None):
    g = [gate] if gate else []
    edge = [("no", pulse, ""), ("nc", prev, "")] + g
    n.rung_fn(row, edge + [("nc", target, "")], "SET", ["FLAG.260"])
    row += 2
    n.rung_fn(row, edge + [("no", target, "")], "SET", ["FLAG.261"])
    row += 2
    n.rung_fn(row, [("no", "FLAG.260", "")], "SET", [target])
    row += 2
    n.rung_fn(row, [("no", "FLAG.261", "")], "RES", [target])
    row += 2
    n.rung_fn(row, [("no", "SYS.01", "")], "RES", ["FLAG.260"])
    row += 2
    n.rung_fn(row, [("no", "SYS.01", "")], "RES", ["FLAG.261"])
    row += 2
    n.rung_fn(row, [("no", pulse, "")], "SET", [prev])
    row += 2
    n.rung_fn(row, [("nc", pulse, "")], "RES", [prev])
    row += 2
    return row


def pulse_prev(row, pulse, prev):
    n.rung_fn(row, [("no", pulse, "")], "SET", [prev])
    row += 2
    n.rung_fn(row, [("nc", pulse, "")], "RES", [prev])
    row += 2
    return row


n.cmt(r, "HMI pulse SETFLG/RESFLG -> invert MAN/OSM/RETE/TRAV on rising edge")
r = pulse_toggle(r, "FLAG.254", "FLAG.204", "FLAG.188")
r = pulse_toggle(r, "FLAG.185", "FLAG.205", "FLAG.189", ("no", "FLAG.204", ""))
r = pulse_toggle(r, "FLAG.186", "FLAG.206", "FLAG.190", ("no", "FLAG.204", ""))
r = pulse_toggle(r, "FLAG.187", "FLAG.207", "FLAG.191", ("no", "FLAG.204", ""))
r += 1

n.cmt(r, "MAN lamp + falling edge kill")
n.rung_fn(r, [("no", "FLAG.204", "")], "MOV", ["1", "DATA.2020"])
r += 2
n.rung_fn(r, [("nc", "FLAG.204", "")], "MOV", ["0", "DATA.2020"])
r += 2
n.rung_fn(r, [("nc", "FLAG.204", "")], "RES", ["FLAG.205"])
r += 2
n.rung_fn(r, [("nc", "FLAG.204", "")], "RES", ["FLAG.206"])
r += 2
n.rung_fn(r, [("nc", "FLAG.204", "")], "RES", ["FLAG.207"])
r += 3
# falling: FLAG.209 was prev, FLAG.204 now 0
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["OUT.00"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["OUT.01"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["OUT.02"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["OUT.03"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.200"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.201"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.202"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.203"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.205"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.206"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.207"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.208"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.228"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.229"])
r += 2
n.rung_fn(r, [("no", "FLAG.209", ""), ("nc", "FLAG.204", "")], "RES", ["FLAG.234"])
r += 3
n.rung_coil(r, [("no", "FLAG.204", "")], "FLAG.209")
r += 3

# abort FILL if 210 or MAN; mutua esclusione TRAVASO
n.rung_fn(r, [("no", "FLAG.200", ""), ("no", "FLAG.210", "")], "RES", ["FLAG.200"])
r += 2
n.rung_fn(r, [("no", "FLAG.210", "")], "RES", ["FLAG.201"])
r += 2
n.rung_fn(r, [("no", "FLAG.210", "")], "RES", ["FLAG.202"])
r += 2
n.rung_fn(r, [("no", "FLAG.210", "")], "RES", ["FLAG.208"])
r += 2
n.rung_fn(r, [("no", "FLAG.200", ""), ("no", "FLAG.204", "")], "RES", ["FLAG.200"])
r += 2
n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.204", "")], "RES", ["FLAG.203"])
r += 2
n.rung_fn(r, [("no", "FLAG.200", "")], "RES", ["FLAG.203"])
r += 3

# STOP FILL: impulso HMI 198 (SETFLG+RESFLG), poi fronte 1→0 di 200 spegne STEP/STAB
n.cmt(r, "STOP FILL impulso 198; fronte 200: RES 201/202/208")
n.rung_fn(r, [("no", "FLAG.198", ""), ("nc", "FLAG.199", "")], "RES", ["FLAG.200"])
r += 2
r = pulse_prev(r, "FLAG.198", "FLAG.199")
if True:
    n.cmt(r, "RESET FILL impulso 268: RES 200/240 (non FLAG.00)")
    n.rung_fn(r, [("no", "FLAG.268", ""), ("nc", "FLAG.277", "")], "RES", ["FLAG.200"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.268", ""), ("nc", "FLAG.277", "")], "RES", ["FLAG.240"])
    r += 2
    r = pulse_prev(r, "FLAG.268", "FLAG.277")
n.rung_fn(r, [("no", "FLAG.239", ""), ("nc", "FLAG.200", "")], "RES", ["FLAG.201"])
r += 2
n.rung_fn(r, [("no", "FLAG.239", ""), ("nc", "FLAG.200", "")], "RES", ["FLAG.202"])
r += 2
n.rung_fn(r, [("no", "FLAG.239", ""), ("nc", "FLAG.200", "")], "RES", ["FLAG.208"])
r += 2
n.rung_coil(r, [("no", "FLAG.200", "")], "FLAG.239")
r += 3

# ----- REFILL: AVVIA = FLAG.238 -----
n.cmt(r, "REFILL: vuoto=FILL, sennò pagina; SI mix rabbocco")
r = eadd16(r, [("no", "SYS.01", "")], "DATA.2013", "DATA.2015", "DATA.2059")
n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.251"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2059", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.04", "")], "SET", ["FLAG.251"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2059", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.03", "")], "SET", ["FLAG.251"])
r += 2

n.rung_fn(r, [("no", "FLAG.238", ""), ("nc", "FLAG.184", ""), ("no", "FLAG.210", "")], "RES", ["FLAG.238"])
r += 2
n.rung_fn(r, [("no", "FLAG.238", ""), ("nc", "FLAG.184", ""), ("no", "FLAG.211", "")], "RES", ["FLAG.238"])
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.238", ""), ("nc", "FLAG.184", ""), ("no", "FLAG.251", ""), ("nc", "FLAG.210", ""), ("nc", "FLAG.211", "")],
    "SET",
    ["FLAG.200"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.238", ""), ("nc", "FLAG.184", ""), ("no", "FLAG.251", ""), ("nc", "FLAG.210", ""), ("nc", "FLAG.211", "")],
    "RES",
    ["FLAG.240"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.238", ""), ("nc", "FLAG.184", ""), ("no", "FLAG.251", ""), ("nc", "FLAG.210", ""), ("nc", "FLAG.211", "")],
    "RES",
    ["FLAG.242"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.238", ""), ("nc", "FLAG.184", ""), ("no", "FLAG.251", ""), ("nc", "FLAG.210", ""), ("nc", "FLAG.211", "")],
    "RES",
    ["FLAG.238"],
)
r += 3

open_rf = [("no", "FLAG.238", ""), ("nc", "FLAG.184", ""), ("nc", "FLAG.251", ""), ("nc", "FLAG.210", ""), ("nc", "FLAG.211", "")]
n.rung_fn(r, open_rf, "MOV", ["DATA.00", "DATA.2060"])
r += 2
n.rung_fn(r, open_rf, "SET", ["FLAG.240"])
r += 2
n.rung_fn(r, open_rf, "RES", ["FLAG.242"])
r += 2
n.rung_fn(r, open_rf, "RES", ["FLAG.169"])
r += 2
if True:
    n.rung_fn(r, open_rf, "MOV", [REFILL_D, "DATA.00"])
    r += 2
else:
    n.rung_fn(r, open_rf, "CMP", ["1", "DATA.00", "1"], cmp=True)
    r += 3
    n.rung_fn(r, open_rf + [("no", "SYS.03", "")], "MOV", [REFILL_L, "DATA.00"])
    r += 2
    n.rung_fn(r, open_rf, "CMP", ["8", "DATA.00", "1"], cmp=True)
    r += 3
    n.rung_fn(r, open_rf + [("no", "SYS.03", "")], "MOV", [REFILL_D, "DATA.00"])
    r += 2
n.rung_fn(r, open_rf, "RES", ["FLAG.238"])
r += 3
r = pulse_prev(r, "FLAG.238", "FLAG.184")

if True:
    n.rung_fn(r, [("no", "FLAG.240", "")], "CMP", [FILL_PAGE, "DATA.00", "1"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "FLAG.240", ""), ("no", "SYS.03", "")], "RES", ["FLAG.242"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.240", ""), ("no", "SYS.03", "")], "RES", ["FLAG.169"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.240", ""), ("no", "SYS.03", "")], "RES", ["FLAG.240"])
    r += 3
else:
    n.rung_fn(r, [("no", "FLAG.240", "")], "CMP", ["1", "DATA.00", "1"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "FLAG.240", ""), ("no", "SYS.03", "")], "RES", ["FLAG.242"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.240", ""), ("no", "SYS.03", "")], "RES", ["FLAG.240"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.240", "")], "CMP", ["8", "DATA.00", "1"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "FLAG.240", ""), ("no", "SYS.03", "")], "RES", ["FLAG.242"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.240", ""), ("no", "SYS.03", "")], "RES", ["FLAG.240"])
    r += 3

# SI: mix rabbocco 32 bit; rifiuti → pagine avviso WARN o restano in REFILL
n.rung_fn(r, [("no", "FLAG.241", "")], "RES", ["FLAG.242"])
r += 2
n.rung_fn(r, [("no", "FLAG.241", "")], "RES", ["FLAG.169"])
r += 2
n.rung_fn(r, [("no", "FLAG.241", "")], "CMP", ["DATA.2007", "DATA.2004", "4"], cmp=True)
r += 3
n.rung_fn(r, [("no", "FLAG.241", ""), ("no", "SYS.05", "")], "SET", ["FLAG.242"])
r += 2
n.rung_fn(r, [("no", "FLAG.241", "")], "CMP", ["DATA.2007", "DATA.2004", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "FLAG.241", ""), ("no", "SYS.03", "")], "SET", ["FLAG.242"])
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.241", "")],
    "CMP",
    ["0", "DATA.2014", "1"],
    cmp=True,
    result_coil="FLAG.215",
)
r += 3
n.rung_fn(
    r,
    [("no", "FLAG.241", "")],
    "CMP",
    ["0", "DATA.2005", "1"],
    cmp=True,
    result_coil="FLAG.214",
)
r += 3
n.rung_fn(
    r,
    [("no", "FLAG.241", ""), ("no", "FLAG.215", ""), ("nc", "FLAG.214", "")],
    "SET",
    ["FLAG.242"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.241", ""), ("no", "FLAG.215", ""), ("nc", "FLAG.214", "")],
    "SET",
    ["FLAG.169"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.241", ""), ("no", "FLAG.214", ""), ("nc", "FLAG.242", "")],
    "MOV",
    ["DATA.2004", "DATA.2008"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.241", ""), ("no", "FLAG.214", ""), ("nc", "FLAG.242", "")],
    "MOV",
    ["0", "DATA.2009"],
)
r += 3
n.rung_coil(
    r,
    [("no", "FLAG.241", ""), ("nc", "FLAG.214", ""), ("nc", "FLAG.242", "")],
    "FLAG.217",
)
r += 3
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.2004", "DATA.1220"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["0", "DATA.1221"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.2005", "DATA.1222"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["0", "DATA.1223"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
r += 3
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.2007", "DATA.1220"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["0", "DATA.1221"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.2058", "DATA.1222"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["0", "DATA.1223"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1202"])
r += 3
n.rung_fn(r, [("no", "FLAG.217", "")], "CMP", ["DATA.1201", "DATA.1203", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "FLAG.217", ""), ("no", "SYS.04", "")], "SET", ["FLAG.242"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", ""), ("no", "SYS.04", "")], "SET", ["FLAG.169"])
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.217", "")],
    "CMP",
    ["DATA.1201", "DATA.1203", "1"],
    cmp=True,
    result_coil="FLAG.216",
)
r += 3
n.rung_fn(r, [("no", "FLAG.216", "")], "CMP", ["DATA.1200", "DATA.1202", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "FLAG.216", ""), ("no", "SYS.04", "")], "SET", ["FLAG.242"])
r += 2
n.rung_fn(r, [("no", "FLAG.216", ""), ("no", "SYS.04", "")], "SET", ["FLAG.169"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "LESUB", ["DATA.1202", "DATA.1200", "DATA.1204"])
r += 3
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "MOV", ["DATA.2014", "DATA.1220"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "MOV", ["0", "DATA.1221"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "LEDIV", ["DATA.1220", "DATA.1204", "DATA.1206"])
r += 3
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "MOV", ["DATA.1206", "DATA.2009"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "ESUB", ["DATA.2007", "DATA.2004", "DATA.2061"])
r += 3
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "CMP", ["DATA.2009", "DATA.2061", "4"], cmp=True)
r += 3
n.rung_fn(
    r,
    [("no", "FLAG.217", ""), ("nc", "FLAG.242", ""), ("no", "SYS.05", "")],
    "SET",
    ["FLAG.242"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.217", ""), ("no", "SYS.05", "")],
    "SET",
    ["FLAG.169"],
)
r += 2
n.rung_fn(r, [("no", "FLAG.217", ""), ("nc", "FLAG.242", "")], "ESUB", ["DATA.2009", "DATA.2004", "DATA.2008"])
r += 3
if True:
    n.rung_fn(r, [("no", "FLAG.241", ""), ("no", "FLAG.169", "")], "MOV", [WARN_DUR, "DATA.00"])
    r += 2
    n.rung_fn(
        r,
        [("no", "FLAG.241", ""), ("no", "FLAG.242", ""), ("nc", "FLAG.169", "")],
        "MOV",
        [WARN_LT, "DATA.00"],
    )
    r += 2
n.rung_fn(r, [("no", "FLAG.241", ""), ("no", "FLAG.211", "")], "RES", ["FLAG.241"])
r += 2
n.rung_fn(r, [("no", "FLAG.241", ""), ("nc", "FLAG.242", ""), ("nc", "FLAG.211", "")], "SET", ["FLAG.200"])
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.241", ""), ("nc", "FLAG.242", ""), ("nc", "FLAG.211", "")],
    "MOV",
    [FILL_PAGE, "DATA.00"],
)
r += 2
n.rung_fn(r, [("no", "FLAG.241", ""), ("nc", "FLAG.242", ""), ("nc", "FLAG.211", "")], "RES", ["FLAG.240"])
r += 2
n.rung_fn(r, [("no", "FLAG.241", ""), ("nc", "FLAG.242", ""), ("nc", "FLAG.211", "")], "RES", ["FLAG.241"])
r += 2
n.rung_fn(r, [("no", "FLAG.241", ""), ("no", "FLAG.242", "")], "RES", ["FLAG.241"])
r += 3
if True:
    n.rung_fn(r, [("no", "FLAG.176", ""), ("nc", "FLAG.174", "")], "MOV", [FILL_PAGE, "DATA.00"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.176", ""), ("nc", "FLAG.174", "")], "RES", ["FLAG.242"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.176", ""), ("nc", "FLAG.174", "")], "RES", ["FLAG.169"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.176", ""), ("nc", "FLAG.174", "")], "RES", ["FLAG.240"])
    r += 2
    r = pulse_prev(r, "FLAG.176", "FLAG.174")
    n.rung_fn(r, [("no", "FLAG.177", ""), ("nc", "FLAG.175", "")], "MOV", [FILL_PAGE, "DATA.00"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.177", ""), ("nc", "FLAG.175", "")], "RES", ["FLAG.242"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.177", ""), ("nc", "FLAG.175", "")], "RES", ["FLAG.169"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.177", ""), ("nc", "FLAG.175", "")], "RES", ["FLAG.240"])
    r += 2
    r = pulse_prev(r, "FLAG.177", "FLAG.175")

# ----- MIX (preview Vo/Vn; non sovrascrivere durante FILL/REFILL) -----
n.cmt(r, "Mix Vo/Vn 32bit")
if True:
    # 271 = cambiato Lt/Ht/Hn a FILL fermo; 274 = cambiato cm (i target vincono).
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.271"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.274"])
    r += 2
    n.rung_fn(
        r,
        [("no", "SYS.01", "")],
        "CMP",
        ["DATA.2004", "DATA.2065", "1"],
        cmp=True,
        result_coil="FLAG.272",
    )
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.01", "")],
        "CMP",
        ["DATA.2005", "DATA.2066", "1"],
        cmp=True,
        result_coil="FLAG.273",
    )
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.01", "")],
        "CMP",
        ["DATA.2014", "DATA.2069", "1"],
        cmp=True,
        result_coil="FLAG.278",
    )
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.01", "")],
        "CMP",
        ["DATA.2063", "DATA.2067", "1"],
        cmp=True,
        result_coil="FLAG.275",
    )
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.01", "")],
        "CMP",
        ["DATA.2064", "DATA.2068", "1"],
        cmp=True,
        result_coil="FLAG.276",
    )
    r += 3
    idle = [("nc", "FLAG.200", ""), ("nc", "FLAG.240", "")]
    n.rung_fn(r, idle + [("nc", "FLAG.272", "")], "SET", ["FLAG.271"])
    r += 2
    n.rung_fn(r, idle + [("nc", "FLAG.273", "")], "SET", ["FLAG.271"])
    r += 2
    n.rung_fn(r, idle + [("nc", "FLAG.278", "")], "SET", ["FLAG.271"])
    r += 2
    n.rung_fn(r, idle + [("nc", "FLAG.271", ""), ("nc", "FLAG.275", "")], "SET", ["FLAG.274"])
    r += 2
    n.rung_fn(r, idle + [("nc", "FLAG.271", ""), ("nc", "FLAG.276", "")], "SET", ["FLAG.274"])
    r += 2
    n.rung_coil(r, [("no", "FLAG.271", "")], "FLAG.250")
    r += 3
else:
    n.rung_coil(r, [("nc", "FLAG.200", ""), ("nc", "FLAG.240", "")], "FLAG.250")
    r += 3
n.rung_fn(
    r,
    [("no", "FLAG.250", "")],
    "CMP",
    ["0", "DATA.2014", "1"],
    cmp=True,
    result_coil="FLAG.215",
)  # Hn=0
r += 3
n.rung_fn(r, [("no", "FLAG.250", ""), ("no", "FLAG.215", "")], "MOV", ["DATA.2004", "DATA.2008"])
r += 2
n.rung_fn(r, [("no", "FLAG.250", ""), ("no", "FLAG.215", "")], "MOV", ["0", "DATA.2009"])
r += 3
n.rung_fn(
    r,
    [("no", "FLAG.250", "")],
    "CMP",
    ["0", "DATA.2005", "1"],
    cmp=True,
    result_coil="FLAG.214",
)
r += 3
n.rung_fn(r, [("no", "FLAG.250", ""), ("no", "FLAG.214", ""), ("nc", "FLAG.215", "")], "MOV", ["DATA.2004", "DATA.2008"])
r += 2
n.rung_fn(r, [("no", "FLAG.250", ""), ("no", "FLAG.214", ""), ("nc", "FLAG.215", "")], "MOV", ["0", "DATA.2009"])
r += 3
n.rung_fn(
    r,
    [("no", "FLAG.250", "")],
    "CMP",
    ["DATA.2005", "DATA.2014", "4"],
    cmp=True,
    result_coil="FLAG.216",
)
r += 3
n.rung_fn(r, [("no", "FLAG.250", ""), ("no", "FLAG.216", ""), ("nc", "FLAG.214", ""), ("nc", "FLAG.215", "")], "MOV", ["0", "DATA.2008"])
r += 2
n.rung_fn(r, [("no", "FLAG.250", ""), ("no", "FLAG.216", ""), ("nc", "FLAG.214", ""), ("nc", "FLAG.215", "")], "MOV", ["DATA.2004", "DATA.2009"])
r += 3
n.rung_coil(
    r,
    [("no", "FLAG.250", ""), ("nc", "FLAG.214", ""), ("nc", "FLAG.215", ""), ("nc", "FLAG.216", "")],
    "FLAG.217",
)
r += 3
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.2004", "DATA.1220"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["0", "DATA.1221"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.2005", "DATA.1222"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["0", "DATA.1223"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
r += 3
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.2014", "DATA.1220"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["0", "DATA.1221"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "LEDIV", ["DATA.1220", "DATA.1200", "DATA.1202"])
r += 3
n.rung_fn(r, [("no", "FLAG.217", "")], "MOV", ["DATA.1202", "DATA.2009"])
r += 2
n.rung_fn(r, [("no", "FLAG.217", "")], "ESUB", ["DATA.2009", "DATA.2004", "DATA.2008"])
r += 3
if True:
    fwd = [("no", "FLAG.250", "")]
    rev = [("no", "FLAG.274", "")]
    r = l_to_cm(r, fwd, "DATA.2008", "DATA.2063")
    r = l_to_cm(r, fwd, "DATA.2009", "DATA.2064")
    r = cm_to_l(r, rev, "DATA.2063", "DATA.2008")
    r = cm_to_l(r, rev, "DATA.2064", "DATA.2009")
    r = eadd16(r, rev, "DATA.2008", "DATA.2009", "DATA.2004")
    n.rung_fn(
        r,
        rev,
        "CMP",
        ["0", "DATA.2004", "1"],
        cmp=True,
        result_coil="FLAG.266",
    )
    r += 3
    n.rung_fn(r, [("no", "FLAG.274", ""), ("no", "FLAG.266", "")], "MOV", ["DATA.2065", "DATA.2004"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "MOV", ["DATA.2014", "DATA.1220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "MOV", ["DATA.2009", "DATA.1222"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "MOV", ["0", "DATA.1223"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
    r += 3
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "MOV", ["DATA.2004", "DATA.1220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "LEDIV", ["DATA.1220", "DATA.1200", "DATA.1202"])
    r += 3
    n.rung_fn(r, [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")], "MOV", ["DATA.1202", "DATA.2005"])
    r += 2
    n.rung_fn(
        r,
        [("no", "FLAG.274", ""), ("nc", "FLAG.266", "")],
        "CMP",
        ["50", "DATA.2005", "2"],
        cmp=True,
        result_coil="FLAG.263",
    )
    r += 3
    n.rung_fn(r, [("no", "FLAG.274", ""), ("no", "FLAG.263", "")], "MOV", ["50", "DATA.2005"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2004", "DATA.2065"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2005", "DATA.2066"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2063", "DATA.2067"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2064", "DATA.2068"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2014", "DATA.2069"])
    r += 3

# start STEP1 when FILL and not 201/202/208
n.cmt(r, "FILL sequenza")
n.rung_fn(
    r,
    [("no", "FLAG.200", ""), ("nc", "FLAG.201", ""), ("nc", "FLAG.202", ""), ("nc", "FLAG.208", ""), ("no", "FLAG.01", "")],
    "MOV",
    ["DATA.2007", "DATA.2039"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.200", ""), ("nc", "FLAG.201", ""), ("nc", "FLAG.202", ""), ("nc", "FLAG.208", ""), ("no", "FLAG.01", "")],
    "MOV",
    ["0", "DATA.2038"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.200", ""), ("nc", "FLAG.201", ""), ("nc", "FLAG.202", ""), ("nc", "FLAG.208", ""), ("no", "FLAG.01", "")],
    "RES",
    ["FLAG.228"],
)
r += 2
n.rung_fn(
    r,
    [("no", "FLAG.200", ""), ("nc", "FLAG.201", ""), ("nc", "FLAG.202", ""), ("nc", "FLAG.208", ""), ("no", "FLAG.01", "")],
    "SET",
    ["FLAG.201"],
)
r += 3
# INP.02: esci da OSM verso STAB
n.rung_fn(r, [("no", "INP.02", "ALLARME OSMOSI"), ("no", "FLAG.201", "")], "SET", ["FLAG.208"])
r += 2
n.rung_fn(r, [("no", "INP.02", "ALLARME OSMOSI"), ("no", "FLAG.201", "")], "MOV", ["0", "DATA.2037"])
r += 2
n.rung_fn(r, [("no", "INP.02", "ALLARME OSMOSI"), ("no", "FLAG.201", "")], "RES", ["FLAG.201"])
r += 3
# Vo=0 (100% rete): salta OSM, vai in STAB
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["0", "DATA.2008", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.03", ""), ("no", "FLAG.201", "")], "SET", ["FLAG.208"])
r += 2
n.rung_fn(r, [("no", "SYS.03", ""), ("no", "FLAG.201", "")], "MOV", ["0", "DATA.2037"])
r += 2
n.rung_fn(r, [("no", "SYS.03", ""), ("no", "FLAG.201", "")], "RES", ["FLAG.201"])
r += 3
# Vo-TOLL in 2051; se Vo < TOLL clamp a 0 (niente wrap 16 bit)
n.rung_fn(r, [("no", "FLAG.201", "")], "ESUB", ["DATA.2015", "DATA.2008", "DATA.2051"])
r += 3
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2008", "DATA.2015", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.04", ""), ("no", "FLAG.201", "")], "MOV", ["0", "DATA.2051"])
r += 3
r = geq_set(r, "FLAG.201", "DATA.2007", "DATA.2051", "FLAG.218")
n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.218", "")], "SET", ["FLAG.208"])
r += 2
n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.218", "")], "MOV", ["0", "DATA.2037"])
r += 2
n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.218", "")], "RES", ["FLAG.201"])
r += 3
r = eadd16(r, [("no", "FLAG.208", ""), ("no", "SYS.10", "")], "1", "DATA.2037", "DATA.2037")
r = geq_set(r, "FLAG.208", "DATA.2037", "DATA.2022", "FLAG.219")
n.rung_fn(r, [("no", "FLAG.208", ""), ("no", "FLAG.219", "")], "MOV", ["DATA.2007", "DATA.2039"])
r += 2
n.rung_fn(r, [("no", "FLAG.208", ""), ("no", "FLAG.219", "")], "MOV", ["0", "DATA.2038"])
r += 2
n.rung_fn(r, [("no", "FLAG.208", ""), ("no", "FLAG.219", "")], "SET", ["FLAG.202"])
r += 2
n.rung_fn(r, [("no", "FLAG.208", ""), ("no", "FLAG.219", "")], "RES", ["FLAG.208"])
r += 3
# STEP2 done when 2007 >= 2004
r = geq_set(r, "FLAG.202", "DATA.2007", "DATA.2004", "FLAG.218")
n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.218", "")], "SET", ["FLAG.220"])
r += 2
n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.218", "")], "RES", ["FLAG.200"])
r += 2
n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.218", "")], "RES", ["FLAG.202"])
r += 3

# bars FILL
n.rung_fn(r, [("no", "FLAG.201", "")], "MOV", ["DATA.2007", "DATA.2031"])
r += 2
n.rung_fn(r, [("no", "FLAG.202", "")], "MOV", ["DATA.2008", "DATA.2031"])
r += 2
n.rung_fn(r, [("no", "FLAG.202", "")], "ESUB", ["DATA.2008", "DATA.2007", "DATA.2032"])
r += 3

# ----- TRAVASO -----
n.cmt(r, "TRAVASO")
n.rung_fn(r, [("no", "FLAG.244", ""), ("nc", "FLAG.203", "")], "RES", ["FLAG.234"])
r += 2
n.rung_coil(r, [("no", "FLAG.203", "")], "FLAG.244")
r += 3
# 2050 = 2007-2006; valido solo se 2007 >= 2006 (FLAG.227). Wrap 16 bit = falso "pieno".
n.rung_fn(r, [("no", "SYS.01", "")], "ESUB", ["DATA.2006", "DATA.2007", "DATA.2050"])
r += 3
r = geq_set(r, "SYS.01", "DATA.2007", "DATA.2006", "FLAG.227")
n.rung_coil(r, [("nc", "FLAG.227", "")], "FLAG.212")
r += 2
n.cmt(r, "TRAVASO AVVIA/STOP impulso HMI 196/197")
n.rung_fn(
    r,
    [
        ("no", "FLAG.196", ""),
        ("nc", "FLAG.182", ""),
        ("nc", "FLAG.204", ""),
        ("nc", "FLAG.200", ""),
        ("nc", "FLAG.212", ""),
        ("no", "FLAG.01", ""),
    ],
    "SET",
    ["FLAG.203"],
)
r += 2
# START rifiutato per LIV < LT: pagina avviso (non Alr Kernel). OK = FLAG.181.
open_w = [("no", "FLAG.196", ""), ("nc", "FLAG.182", ""), ("no", "FLAG.212", "")]
n.rung_fn(r, open_w, "MOV", ["DATA.00", "DATA.2062"])
r += 2
n.rung_fn(r, open_w, "SET", ["FLAG.180"])
r += 2
if True:
    n.rung_fn(r, open_w, "MOV", [WARN_D, "DATA.00"])
    r += 2
else:
    n.rung_fn(r, open_w, "CMP", ["2", "DATA.00", "1"], cmp=True)
    r += 3
    n.rung_fn(r, open_w + [("no", "SYS.03", "")], "MOV", [WARN_L, "DATA.00"])
    r += 2
    n.rung_fn(r, open_w, "CMP", ["9", "DATA.00", "1"], cmp=True)
    r += 3
    n.rung_fn(r, open_w + [("no", "SYS.03", "")], "MOV", [WARN_D, "DATA.00"])
    r += 2
r = pulse_prev(r, "FLAG.196", "FLAG.182")
n.rung_fn(r, [("no", "FLAG.197", ""), ("nc", "FLAG.183", "")], "RES", ["FLAG.203"])
r += 2
r = pulse_prev(r, "FLAG.197", "FLAG.183")
n.rung_fn(r, [("no", "FLAG.181", ""), ("nc", "FLAG.178", "")], "MOV", ["DATA.2062", "DATA.00"])
r += 2
n.rung_fn(r, [("no", "FLAG.181", ""), ("nc", "FLAG.178", "")], "RES", ["FLAG.180"])
r += 2
r = pulse_prev(r, "FLAG.181", "FLAG.178")
n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.179"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", [WARN_L, "DATA.00", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.03", "")], "SET", ["FLAG.179"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", [WARN_D, "DATA.00", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.03", "")], "SET", ["FLAG.179"])
r += 2
n.rung_fn(r, [("no", "FLAG.180", ""), ("nc", "FLAG.179", "")], "RES", ["FLAG.180"])
r += 3
n.rung_fn(r, [("no", "FLAG.203", ""), ("nc", "FLAG.227", ""), ("nc", "FLAG.222", "")], "RES", ["FLAG.203"])
r += 3
n.rung_fn(r, [("nc", "FLAG.203", "")], "RES", ["FLAG.222"])
r += 2
n.rung_fn(r, [("no", "FLAG.203", ""), ("nc", "FLAG.212", ""), ("nc", "FLAG.222", "")], "MOV", ["DATA.2007", "DATA.2027"])
r += 2
n.rung_fn(r, [("no", "FLAG.203", ""), ("nc", "FLAG.212", ""), ("nc", "FLAG.222", "")], "MOV", ["DATA.2007", "DATA.2039"])
r += 2
n.rung_fn(r, [("no", "FLAG.203", ""), ("nc", "FLAG.212", ""), ("nc", "FLAG.222", "")], "MOV", ["0", "DATA.2038"])
r += 2
n.rung_fn(r, [("no", "FLAG.203", ""), ("nc", "FLAG.212", ""), ("nc", "FLAG.222", "")], "RES", ["FLAG.229"])
r += 2
n.rung_fn(r, [("no", "FLAG.203", ""), ("nc", "FLAG.212", ""), ("nc", "FLAG.222", "")], "SET", ["FLAG.222"])
r += 3
n.cmt(r, "2026 = calo solo se LIV non e' salito (niente wrap → fine finta)")
n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.225"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2027", "2"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.04", "")], "SET", ["FLAG.225"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2027", "1"], cmp=True)
r += 3
n.rung_fn(r, [("no", "SYS.03", "")], "SET", ["FLAG.225"])
r += 3
n.rung_fn(
    r,
    [("no", "FLAG.203", ""), ("nc", "FLAG.212", ""), ("nc", "FLAG.234", ""), ("no", "FLAG.225", "")],
    "ESUB",
    ["DATA.2007", "DATA.2027", "DATA.2026"],
)
r += 3
n.rung_fn(
    r,
    [("no", "FLAG.203", ""), ("nc", "FLAG.212", ""), ("nc", "FLAG.234", ""), ("nc", "FLAG.225", "")],
    "MOV",
    ["0", "DATA.2026"],
)
r += 3
r = geq_set(r, "FLAG.203", "DATA.2026", "DATA.2006", "FLAG.223")

if False:
    n.cmt(r, "Fine TRAVASO")
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", "")], "RES", ["FLAG.203"])
    r += 2
    n.rung_fn(r, [("nc", "FLAG.203", "")], "MOV", ["0", "DATA.2026"])
    r += 3

if True:
    n.cmt(r, "LIV <= OFFSET -> FLAG.243")
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.243"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2013", "2"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.04", "")], "SET", ["FLAG.243"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2013", "1"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.03", "")], "SET", ["FLAG.243"])
    r += 3

    enter = [
        ("no", "FLAG.203", ""),
        ("no", "FLAG.243", ""),
        ("nc", "FLAG.223", ""),
        ("nc", "FLAG.234", ""),
    ]
    n.cmt(r, "TRAVASO coda OFFSET: init t_s poi SET 234")
    n.rung_fn(r, enter, "ESUB", ["DATA.2026", "DATA.2006", "DATA.2048"])
    r += 3
    n.rung_fn(r, enter, "MOV", ["DATA.2021", "DATA.2049"])
    r += 2
    n.rung_fn(r, enter, "MOV", ["0", "DATA.2045"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.246"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["0", "DATA.2049", "1"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.03", "")], "SET", ["FLAG.246"])
    r += 3
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "MOV", ["DATA.2048", "DATA.1220"])
    r += 2
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "MOV", ["60", "DATA.1222"])
    r += 2
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "MOV", ["0", "DATA.1223"])
    r += 2
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
    r += 3
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "MOV", ["DATA.2049", "DATA.1220"])
    r += 2
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "LEDIV", ["DATA.1220", "DATA.1200", "DATA.1202"])
    r += 3
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "MOV", ["DATA.1202", "DATA.2046"])
    r += 2
    n.rung_fn(r, enter + [("no", "FLAG.246", "")], "MOV", ["DATA.2044", "DATA.1220"])
    r += 2
    n.rung_fn(r, enter + [("no", "FLAG.246", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, enter + [("no", "FLAG.246", "")], "MOV", ["60", "DATA.1222"])
    r += 2
    n.rung_fn(r, enter + [("no", "FLAG.246", "")], "MOV", ["0", "DATA.1223"])
    r += 2
    n.rung_fn(r, enter + [("no", "FLAG.246", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1204"])
    r += 3
    n.rung_fn(r, enter + [("no", "FLAG.246", "")], "MOV", ["DATA.1204", "DATA.2046"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["0", "DATA.2044", "1"], cmp=True)
    r += 3
    n.rung_fn(r, enter + [("no", "FLAG.246", ""), ("no", "SYS.03", "")], "RES", ["FLAG.203"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["0", "DATA.2044", "2"], cmp=True)
    r += 3
    n.rung_fn(r, enter + [("nc", "FLAG.246", "")], "SET", ["FLAG.234"])
    r += 2
    n.rung_fn(r, enter + [("no", "FLAG.246", ""), ("no", "SYS.04", "")], "SET", ["FLAG.234"])
    r += 3
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["0", "DATA.2044", "2"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["DATA.2044", "DATA.1220"])
    r += 2
    n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["60", "DATA.1222"])
    r += 2
    n.rung_fn(r, [("no", "SYS.04", "")], "MOV", ["0", "DATA.1223"])
    r += 2
    n.rung_fn(r, [("no", "SYS.04", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1204"])
    r += 3
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2046", "DATA.1204", "4"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.05", ""), ("no", "FLAG.234", "")], "MOV", ["DATA.1204", "DATA.2046"])
    r += 3
    r = eadd16(r, [("no", "FLAG.234", ""), ("no", "SYS.10", "")], "1", "DATA.2045", "DATA.2045")
    # coda done: SET 223 senza RES (il RES e nel geq calo; altrimenti si perde 223 da calo)
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2045", "DATA.2046", "4"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.05", ""), ("no", "FLAG.234", "")], "SET", ["FLAG.223"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2045", "DATA.2046", "1"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.03", ""), ("no", "FLAG.234", "")], "SET", ["FLAG.223"])
    r += 2
    n.cmt(r, "Fine TRAVASO: rest coda una volta, poi SET 220 e RES 203/234")
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", ""), ("no", "FLAG.234", "")], "ESUB", ["DATA.2026", "DATA.2006", "DATA.2048"])
    r += 3
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", ""), ("no", "FLAG.234", "")], "MOV", ["DATA.2048", "DATA.1200"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", ""), ("no", "FLAG.234", "")], "MOV", ["0", "DATA.1201"])
    r += 2
    r = leadd32(
        r,
        "DATA.4124",
        "DATA.1200",
        "DATA.4124",
        contacts=[("no", "FLAG.203", ""), ("no", "FLAG.223", ""), ("no", "FLAG.234", "")],
    )
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", "")], "RES", ["FLAG.234"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.203", ""), ("no", "FLAG.223", "")], "RES", ["FLAG.203"])
    r += 2
    n.rung_fn(r, [("nc", "FLAG.203", "")], "MOV", ["0", "DATA.2026"])
    r += 3

    n.cmt(r, "Watchdog stallo TIMEOUT (non MAN, non STAB, non coda)")
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.247"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["0", "DATA.2044", "2"], cmp=True)
    r += 3
    n.rung_fn(
        r,
        [("no", "SYS.04", ""), ("nc", "FLAG.204", ""), ("nc", "FLAG.208", ""), ("nc", "FLAG.234", "")],
        "SET",
        ["FLAG.247"],
    )
    r += 3
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.248"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2039", "4"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.05", "")], "SET", ["FLAG.248"])
    r += 3
    # FILL: 248 = LIV salito
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.201", ""), ("no", "SYS.10", ""), ("no", "FLAG.248", "")], "MOV", ["DATA.2007", "DATA.2039"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.201", ""), ("no", "SYS.10", ""), ("no", "FLAG.248", "")], "MOV", ["0", "DATA.2038"])
    r += 2
    r = eadd16(r, [("no", "FLAG.247", ""), ("no", "FLAG.201", ""), ("no", "SYS.10", ""), ("nc", "FLAG.248", "")], "1", "DATA.2038", "DATA.2038")
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.202", ""), ("no", "SYS.10", ""), ("no", "FLAG.248", "")], "MOV", ["DATA.2007", "DATA.2039"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.202", ""), ("no", "SYS.10", ""), ("no", "FLAG.248", "")], "MOV", ["0", "DATA.2038"])
    r += 2
    r = eadd16(r, [("no", "FLAG.247", ""), ("no", "FLAG.202", ""), ("no", "SYS.10", ""), ("nc", "FLAG.248", "")], "1", "DATA.2038", "DATA.2038")
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.248"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2039", "2"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.04", "")], "SET", ["FLAG.248"])
    r += 3
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.203", ""), ("no", "SYS.10", ""), ("no", "FLAG.248", "")], "MOV", ["DATA.2007", "DATA.2039"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.203", ""), ("no", "SYS.10", ""), ("no", "FLAG.248", "")], "MOV", ["0", "DATA.2038"])
    r += 2
    r = eadd16(r, [("no", "FLAG.247", ""), ("no", "FLAG.203", ""), ("no", "SYS.10", ""), ("nc", "FLAG.248", "")], "1", "DATA.2038", "DATA.2038")
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2044", "DATA.1220"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["60", "DATA.1222"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["0", "DATA.1223"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
    r += 3
    n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.243", "")], "MOV", ["DATA.2044", "DATA.1220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.243", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.243", "")], "MOV", ["120", "DATA.1222"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.243", "")], "MOV", ["0", "DATA.1223"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.201", ""), ("no", "FLAG.243", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
    r += 3
    n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.243", "")], "MOV", ["DATA.2044", "DATA.1220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.243", "")], "MOV", ["0", "DATA.1221"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.243", "")], "MOV", ["120", "DATA.1222"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.243", "")], "MOV", ["0", "DATA.1223"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.202", ""), ("no", "FLAG.243", "")], "LEMUL", ["DATA.1220", "DATA.1222", "DATA.1200"])
    r += 3
    n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.1200", "DATA.2057"])
    r += 2
    r = geq_set(r, "FLAG.247", "DATA.2038", "DATA.2057", "FLAG.213")
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.213", ""), ("no", "FLAG.201", "")], "SET", ["FLAG.228"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.213", ""), ("no", "FLAG.202", "")], "SET", ["FLAG.228"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.213", ""), ("no", "FLAG.203", "")], "SET", ["FLAG.229"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.213", ""), ("no", "FLAG.201", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.213", ""), ("no", "FLAG.202", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.247", ""), ("no", "FLAG.213", ""), ("no", "FLAG.203", "")], "SET", ["FLAG.220"])
    r += 3
    for fl in ["OUT.00", "OUT.01", "OUT.02", "OUT.03", "FLAG.200", "FLAG.201", "FLAG.202", "FLAG.203", "FLAG.205", "FLAG.206", "FLAG.207", "FLAG.208"]:
        n.rung_fn(r, [("no", "FLAG.228", "")], "RES", [fl])
        r += 2
        n.rung_fn(r, [("no", "FLAG.229", "")], "RES", [fl])
        r += 2

# ----- OUT arbiter: Q0 travaso, Q2 osmosi, Q3 rete; Q1 spare spento. Niente OR. -----
n.cmt(r, "Uscite auto/man: OSM Q2, RETE Q3, TRAV Q0")
n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.230"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.231"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.232"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["OUT.01"])
r += 3
# pompa auto / man
n.rung_fn(r, [("no", "FLAG.203", ""), ("nc", "FLAG.204", "")], "SET", ["FLAG.230"])
r += 2
n.rung_fn(r, [("no", "FLAG.204", ""), ("no", "FLAG.207", "")], "SET", ["FLAG.230"])
r += 3
# osmosi auto / man, blocco pieno + allarme osmosi
n.rung_fn(r, [("no", "FLAG.201", ""), ("nc", "FLAG.204", ""), ("nc", "FLAG.211", ""), ("nc", "INP.02", "ALLARME OSMOSI")], "SET", ["FLAG.232"])
r += 2
n.rung_fn(r, [("no", "FLAG.204", ""), ("no", "FLAG.205", ""), ("nc", "FLAG.211", ""), ("nc", "INP.02", "ALLARME OSMOSI")], "SET", ["FLAG.232"])
r += 3
# rete auto / man, blocco pieno
n.rung_fn(r, [("no", "FLAG.202", ""), ("nc", "FLAG.204", ""), ("nc", "FLAG.211", "")], "SET", ["FLAG.231"])
r += 2
n.rung_fn(r, [("no", "FLAG.204", ""), ("no", "FLAG.206", ""), ("nc", "FLAG.211", "")], "SET", ["FLAG.231"])
r += 3
n.rung_coil(r, [("no", "FLAG.01", ""), ("no", "FLAG.230", "")], "OUT.00", comment="TRAVASO")
r += 2
n.rung_coil(r, [("no", "FLAG.01", ""), ("no", "FLAG.232", "")], "OUT.02", comment="OSMOSI")
r += 2
n.rung_coil(r, [("no", "FLAG.01", ""), ("no", "FLAG.231", "")], "OUT.03", comment="RETE")
r += 3

# LED mirrors: 2040 TRAV, 2041 RETE (Q3), 2042 OSM (Q2). 2043 EV unused.
n.cmt(r, "LED specchio RAM 2040+")
for i, (out, dat) in enumerate(
    [("OUT.00", "DATA.2040"), ("OUT.03", "DATA.2041"), ("OUT.02", "DATA.2042")]
):
    n.rung_fn(r, [("no", out, "")], "MOV", ["1", dat])
    r += 2
    n.rung_fn(r, [("nc", out, "")], "MOV", ["0", dat])
    r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["0", "DATA.2043"])
r += 3

# ----- FLOW / ETA: LTH da SETUP (niente dL/dt, niente learn EEPROM) -----
n.cmt(r, "FLOW = LTH L/m SETUP; ETA = residuo/LTH")
n.rung_fn(r, [("no", "FLAG.201", "")], "MOV", ["DATA.2019", "DATA.2025"])
r += 2
n.rung_fn(r, [("no", "FLAG.202", "")], "MOV", ["DATA.2018", "DATA.2025"])
r += 2
n.rung_fn(r, [("no", "FLAG.203", "")], "MOV", ["DATA.2021", "DATA.2025"])
r += 3
n.rung_fn(r, [("no", "FLAG.200", "")], "ESUB", ["DATA.2007", "DATA.2004", "DATA.2054"])
r += 3
n.rung_fn(r, [("no", "FLAG.203", "")], "ESUB", ["DATA.2026", "DATA.2006", "DATA.2054"])
r += 3
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["DATA.2054", "DATA.1202"])
r += 2
n.rung_fn(r, [("no", "SYS.01", "")], "MOV", ["0", "DATA.1203"])
r += 2
n.rung_fn(
    r,
    [("no", "SYS.01", "")],
    "CMP",
    ["0", "DATA.2025", "2"],
    cmp=True,
    result_coil="FLAG.226",
)
r += 3
n.rung_fn(r, [("no", "FLAG.226", "")], "MOV", ["DATA.2025", "DATA.1220"])
r += 2
n.rung_fn(r, [("no", "FLAG.226", "")], "MOV", ["0", "DATA.1221"])
r += 2
n.rung_fn(r, [("no", "FLAG.226", "")], "LEDIV", ["DATA.1220", "DATA.1202", "DATA.1204"])
r += 3
n.rung_fn(r, [("no", "FLAG.226", "")], "MOV", ["DATA.1204", "DATA.2024"])
r += 2
n.rung_fn(r, [("nc", "FLAG.226", "")], "MOV", ["999", "DATA.2024"])
r += 3

if True:
    n.cmt(r, "Totalizzatori dL su LONG EEPROM 4120+")
    n.rung_fn(r, [("nc", "OUT.00", ""), ("nc", "OUT.02", ""), ("nc", "OUT.03", "")], "MOV", ["DATA.2007", "DATA.2047"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.248"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2047", "DATA.2007", "2"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.04", "")], "SET", ["FLAG.248"])
    r += 3
    n.rung_fn(r, [("no", "OUT.02", ""), ("no", "FLAG.248", "")], "ESUB", ["DATA.2047", "DATA.2007", "DATA.2048"])
    r += 3
    n.rung_fn(r, [("no", "OUT.02", ""), ("no", "FLAG.248", "")], "MOV", ["DATA.2048", "DATA.1200"])
    r += 2
    n.rung_fn(r, [("no", "OUT.02", ""), ("no", "FLAG.248", "")], "MOV", ["0", "DATA.1201"])
    r += 2
    r = leadd32(r, "DATA.4120", "DATA.1200", "DATA.4120", contacts=[("no", "OUT.02", ""), ("no", "FLAG.248", "")])
    n.rung_fn(r, [("no", "OUT.03", ""), ("no", "FLAG.248", "")], "ESUB", ["DATA.2047", "DATA.2007", "DATA.2048"])
    r += 3
    n.rung_fn(r, [("no", "OUT.03", ""), ("no", "FLAG.248", "")], "MOV", ["DATA.2048", "DATA.1200"])
    r += 2
    n.rung_fn(r, [("no", "OUT.03", ""), ("no", "FLAG.248", "")], "MOV", ["0", "DATA.1201"])
    r += 2
    r = leadd32(r, "DATA.4122", "DATA.1200", "DATA.4122", contacts=[("no", "OUT.03", ""), ("no", "FLAG.248", "")])
    n.rung_fn(r, [("no", "SYS.01", "")], "RES", ["FLAG.248"])
    r += 2
    n.rung_fn(r, [("no", "SYS.01", "")], "CMP", ["DATA.2007", "DATA.2047", "2"], cmp=True)
    r += 3
    n.rung_fn(r, [("no", "SYS.04", "")], "SET", ["FLAG.248"])
    r += 3
    n.rung_fn(r, [("no", "OUT.00", ""), ("no", "FLAG.248", "")], "ESUB", ["DATA.2007", "DATA.2047", "DATA.2048"])
    r += 3
    n.rung_fn(r, [("no", "OUT.00", ""), ("no", "FLAG.248", "")], "MOV", ["DATA.2048", "DATA.1200"])
    r += 2
    n.rung_fn(r, [("no", "OUT.00", ""), ("no", "FLAG.248", "")], "MOV", ["0", "DATA.1201"])
    r += 2
    r = leadd32(r, "DATA.4124", "DATA.1200", "DATA.4124", contacts=[("no", "OUT.00", ""), ("no", "FLAG.248", "")])
    n.rung_fn(r, [("no", "OUT.00", "")], "MOV", ["DATA.2007", "DATA.2047"])
    r += 2
    n.rung_fn(r, [("no", "OUT.02", "")], "MOV", ["DATA.2007", "DATA.2047"])
    r += 2
    n.rung_fn(r, [("no", "OUT.03", "")], "MOV", ["DATA.2007", "DATA.2047"])
    r += 3

    n.cmt(r, "AZZERA totali (fronte HMI SETFLG/RESFLG)")
    n.rung_fn(r, [("no", "FLAG.235", ""), ("nc", "FLAG.192", "")], "MOV", ["0", "DATA.4120"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.235", ""), ("nc", "FLAG.192", "")], "MOV", ["0", "DATA.4121"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.235", ""), ("nc", "FLAG.192", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.235", "")], "SET", ["FLAG.192"])
    r += 2
    n.rung_fn(r, [("nc", "FLAG.235", "")], "RES", ["FLAG.192"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.236", ""), ("nc", "FLAG.193", "")], "MOV", ["0", "DATA.4122"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.236", ""), ("nc", "FLAG.193", "")], "MOV", ["0", "DATA.4123"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.236", ""), ("nc", "FLAG.193", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.236", "")], "SET", ["FLAG.193"])
    r += 2
    n.rung_fn(r, [("nc", "FLAG.236", "")], "RES", ["FLAG.193"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.237", ""), ("nc", "FLAG.194", "")], "MOV", ["0", "DATA.4124"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.237", ""), ("nc", "FLAG.194", "")], "MOV", ["0", "DATA.4125"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.237", ""), ("nc", "FLAG.194", "")], "SET", ["FLAG.220"])
    r += 2
    n.rung_fn(r, [("no", "FLAG.237", "")], "SET", ["FLAG.194"])
    r += 2
    n.rung_fn(r, [("nc", "FLAG.237", "")], "RES", ["FLAG.194"])
    r += 3

# ----- EEPROM save on FLAG.220 -----
ee_hi = "4125"
n.cmt(r, f"Salva EEPROM 4100-{ee_hi} via SYS.20")
n.rung_fn(r, [("no", "FLAG.220", "")], "MOV", ["4100", "DATA.8142"])
r += 2
n.rung_fn(r, [("no", "FLAG.220", "")], "MOV", [ee_hi, "DATA.8143"])
r += 2
n.rung_fn(r, [("no", "FLAG.220", "")], "MOV", ["4100", "DATA.58"])
r += 2
n.rung_fn(r, [("no", "FLAG.220", "")], "MOV", [ee_hi, "DATA.59"])
r += 2
n.rung_fn(r, [("no", "FLAG.220", "")], "SET", ["SYS.20"])
r += 2
n.rung_fn(r, [("no", "FLAG.220", "")], "RES", ["FLAG.220"])
r += 2

# Un main in Net.0; END + SBR vuoto in Net.1 (contratto compilazione).
def format_net(idx: int, nome: str, titolo: str, commento: str, dimx: int, ymax: int, clines: dict[int, str], cells: list[str]) -> str:
    p = f"Net_{idx:04d}"
    header = [
        f"[Network_{idx:04d}]",
        f"{p}_Nome={nome}",
        f"{p}_Titolo={titolo}",
        f"{p}_Commento={commento}",
        f"{p}_Mascherato=False",
        f"{p}_Read_Only=False",
        f"{p}_Dimensione_X={dimx}",
        f"{p}_Dimensione_Y={ymax}",
    ]
    for rr, s in sorted(clines.items()):
        header.append(f"{p}_CLine_{rr:04d}={s}")
    return "\n".join(header + cells) + "\n"


ymax0 = n.max_row + 2
if ymax0 > MAX_NET_Y:
    raise SystemExit(f"Net.0 Y={ymax0} > {MAX_NET_Y}")

body0 = format_net(
    0,
    "Net.0",
    "Area Programma Principale",
    f"H20 v{VER}: emergenza, livello, MAN, FILL, TRAVASO, REFILL",
    9,
    ymax0,
    n.clines,
    n.lines,
)

m_tail = re.search(r"\[Network_0001\].*?(?=\[FunctionBlock\])", _text_disk, re.S)
if not m_tail:
    raise SystemExit("Network_0001 tail not found in sorgente")

m_lad = re.search(r"\[Network_0000\].*?(?=\[FunctionBlock\])", text, re.S)
if not m_lad:
    raise SystemExit("ladder networks not found")
text = text[: m_lad.start()] + body0 + "\n" + m_tail.group(0) + text[m_lad.end() :]

body = "\n".join(n.lines) + "\n"

# extra flags in simbolici (skip with --net-only: isolate Compila)
if not NET_ONLY:
    for fl, lab in [
        ("FLAG.213", "STALL TMO"),
        ("FLAG.214", "TMP A"),
        ("FLAG.215", "HN ZERO"),
        ("FLAG.216", "HT GT HN"),
        ("FLAG.217", "MIX NORM"),
        ("FLAG.218", "STEP DONE"),
        ("FLAG.219", "STAB DONE"),
        ("FLAG.222", "TRAV SNAP"),
        ("FLAG.223", "TRAV DONE"),
        ("FLAG.225", "LIV DROP OK"),
        ("FLAG.226", "LTH NZ"),
        ("FLAG.227", "TRAV LIV OK"),
        ("FLAG.228", "STALLO FILL"),
        ("FLAG.229", "STALLO TRAV"),
        ("FLAG.230", "REQ POMPA"),
        ("FLAG.231", "REQ RETE"),
        ("FLAG.232", "REQ OSM"),
        ("FLAG.233", "REQ EV"),
        ("FLAG.253", "CARICA DEF"),
        ("FLAG.254", "PULSE MAN"),
        ("FLAG.185", "PULSE OSM"),
        ("FLAG.186", "PULSE RETE"),
        ("FLAG.187", "PULSE TRAV"),
        ("FLAG.188", "PREV MAN"),
        ("FLAG.189", "PREV OSM"),
        ("FLAG.190", "PREV RETE"),
        ("FLAG.191", "PREV TRAV"),
        ("FLAG.192", "PREV AZZ OSM"),
        ("FLAG.193", "PREV AZZ RETE"),
        ("FLAG.194", "PREV AZZ TRAV"),
        ("FLAG.195", "PREV CARICA"),
        ("FLAG.260", "TOG WANT ON"),
        ("FLAG.261", "TOG WANT OFF"),
        ("FLAG.234", "TRAV CODA"),
        ("FLAG.235", "AZZ OSM"),
        ("FLAG.236", "AZZ RETE"),
        ("FLAG.237", "AZZ TRAV"),
        ("FLAG.182", "PREV AVV TRAV"),
        ("FLAG.183", "PREV STOP TRAV"),
        ("FLAG.184", "PREV AVV FILL"),
        ("FLAG.196", "PULSE AVV TRAV"),
        ("FLAG.197", "PULSE STOP TRAV"),
        ("FLAG.198", "PULSE STOP FILL"),
        ("FLAG.199", "PREV STOP FILL"),
        ("FLAG.238", "FILL REQ"),
        ("FLAG.239", "FILL PREV"),
        ("FLAG.178", "PREV OK VUOTO"),
        ("FLAG.179", "ON WARN PAG"),
        ("FLAG.180", "WARN VUOTO PAG"),
        ("FLAG.181", "PULSE OK VUOTO"),
        ("FLAG.240", "REFILL PEND"),
        ("FLAG.262", "DUR OLD INT"),
        ("FLAG.263", "HT CLAMP"),
        ("FLAG.264", "DUR RETE 0"),
        ("FLAG.265", "ALR BEEP"),
        ("FLAG.266", "CM LT ZERO"),
        ("FLAG.267", "DUR RETE HI"),
        ("FLAG.268", "PULSE RST FILL"),
        ("FLAG.271", "TGT CHANGED"),
        ("FLAG.272", "LT EQ PREV"),
        ("FLAG.273", "HT EQ PREV"),
        ("FLAG.274", "CM CHANGED"),
        ("FLAG.275", "CM OSM EQ"),
        ("FLAG.276", "CM RETE EQ"),
        ("FLAG.277", "PREV RST FILL"),
        ("FLAG.278", "HN EQ PREV"),
        ("FLAG.241", "REFILL SI"),
        ("FLAG.242", "REFILL FAIL"),
        ("FLAG.169", "REFILL MIX FAIL"),
        ("FLAG.174", "PREV OK LT"),
        ("FLAG.175", "PREV OK DUR"),
        ("FLAG.176", "PULSE OK LT"),
        ("FLAG.177", "PULSE OK DUR"),
        ("FLAG.243", "LIV LE OFFSET"),
        ("FLAG.244", "TRAV PREV"),
        ("FLAG.246", "FLOW CODA 0"),
        ("FLAG.247", "STALL ENA"),
        ("FLAG.248", "LIV PROG"),
        ("FLAG.249", "CMP SINK"),
        ("FLAG.250", "MIX ENA"),
        ("FLAG.251", "LIV VUOTO MIX"),
        ("FLAG.252", "EE FFFF"),
        ("DATA.2038", "STALL SEC"),
        ("DATA.2039", "STALL LIV"),
        ("DATA.2044", "TIMEOUT MIN"),
        ("DATA.2045", "CODA SEC"),
        ("DATA.2046", "CODA TS"),
        ("DATA.2047", "TOT LIV"),
        ("DATA.2048", "TOT DL"),
        ("DATA.2049", "CODA FLOW"),
        ("DATA.2058", "DUR PRESENTE"),
        ("DATA.2059", "OFF TOLL"),
        ("DATA.2060", "REFILL PAG"),
        ("DATA.2061", "REFILL REST"),
        ("DATA.2062", "WARN PAG"),
        ("DATA.2063", "CM OSMOSI"),
        ("DATA.2064", "CM RETE"),
        ("DATA.2065", "PREV LT TGT"),
        ("DATA.2066", "PREV HT TGT"),
        ("DATA.2067", "PREV CM OSM"),
        ("DATA.2068", "PREV CM RETE"),
        ("DATA.2069", "PREV HN"),
        ("DATA.4120", "TOT OSMOSI"),
        ("DATA.4122", "TOT RETE"),
        ("DATA.4124", "TOT TRAVASO"),
    ]:
        if f"{fl}=" not in text:
            text = text.replace("FLAG.220=SAVE EEPROM\n", f"FLAG.220=SAVE EEPROM\n{fl}={lab}\n")
    if "INP.00=" not in text:
        text = text.replace(
            "INP.01=EMERGENZA\n",
            "INP.00=TERMICO POMPE\nINP.01=EMERGENZA\nINP.02=ALLARME OSMOSI\nINP.03=RESET BLU\n",
        )
    text = text.replace("DATA.4116=IDX SENS\n", "DATA.4116=TIMEOUT MIN\n")
    text = text.replace("FLAG.210=ALR TARGET\n", "FLAG.210=WARN TARGET\n")
    text = text.replace("FLAG.212=ALR VUOTO\n", "FLAG.212=WARN VUOTO\n")
    text = text.replace("FLAG.211=ALR PIENO\n", "FLAG.211=WARN PIENO\n")
    for stale in ("FLAG.255=PULSE OSM\n", "FLAG.256=PULSE RETE\n", "FLAG.257=PULSE TRAV\n"):
        text = text.replace(stale, "")

# CMP/ESUB: costante solo su Data(0); Data(2) di CMP è il codice 1/2/4
bad = []
for line in body.splitlines():
    m = re.match(r"Net_0000_C_(\d+);(\d+)_Data\((\d+)\)=(.+)$", line)
    if not m:
        continue
    row, col, idx, val = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)
    if not val.isdigit():
        continue
    if idx == 0:
        continue
    # look back in body for Indirizzo of this cell
    key = f"Net_0000_C_{row:04d};{col:04d}_Indirizzo="
    op = ""
    for ln in body.splitlines():
        if ln.startswith(key):
            op = ln.split("=", 1)[1]
            break
    if op not in ("CMP", "ESUB", "LEMUL", "LEDIV", "LESUB", "MOV", "SET", "RES", "DIV", "MUL"):
        continue
    if op == "CMP" and idx == 2:
        continue
    bad.append(f"R{row} C{col} {op} Data({idx})={val}")
if bad:
    raise SystemExit("costanti nel posto sbagliato:\n" + "\n".join(bad[:20]))

# Two 1-row rungs on consecutive rows that share >1 column = vertical short.
# v1 emergency OR shares only column 0 (contact + vor).
_cells: dict[tuple[int, int], dict[str, str]] = {}
for ln in n.lines:
    m = re.match(r"Net_0000_C_(\d{4});(\d{4})_(Strumento|CasellaFunzione)=(.*)$", ln)
    if not m:
        continue
    _cells.setdefault((int(m.group(1)), int(m.group(2))), {})[m.group(3)] = m.group(4)
_by_row: dict[int, set[int]] = {}
for (r, c), d in _cells.items():
    if d.get("CasellaFunzione") == "0" and d.get("Strumento") in ("1", "2", "3", "5"):
        _by_row.setdefault(r, set()).add(c)
_stack = []
for r in sorted(_by_row):
    if r + 1 in _by_row:
        shared = _by_row[r] & _by_row[r + 1]
        if len(shared) >= 2:
            _stack.append(f"row {r}/{r+1} cols {sorted(shared)}")
if _stack:
    raise SystemExit("rung a 1 riga attaccati (corto verticale):\n" + "\n".join(_stack[:10]))

LPK.write_text(text, encoding="utf-8")
print("OK", LPK, "ver", VER, "net0 rows", ymax0, "bytes", LPK.stat().st_size)
