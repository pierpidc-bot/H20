# -*- coding: utf-8 -*-
"""HMI Tino H20 v1.00: layout HMI compatto pagine 0–10, REFILL e avvisi."""
from __future__ import annotations

import re

# Palette
BG_L = -4144960
BG_D = -16777216
BLUE_L = -16776961
BLUE_D_TITLE = -16750904
NAV_D = -16767912
YELLOW = -256
WHITE = -1
BLACK = -16777216
CYAN = -4064769
BOX_D = -16750904
RED = -65536

TAB = (
    (80, 48, 86, "TANK"),
    (132, 44, 138, "MIX"),
    (180, 52, 182, "TRASD"),
    (236, 48, 242, "TOT"),
)
TAB_PAGE_L = (3, 4, 5, 6)
TAB_PAGE_D = (10, 11, 12, 13)
NAV_PAGES_L = (0, 1, 2, 3)
NAV_PAGES_D = (7, 8, 9, 10)
SHIPPING_NAV_PAGES = (0, 1, 2, 3)
SHIPPING_TAB_PAGES = (3, 4, 5, 6)
# mappa pagine gemelle espanse → layout compatto 0..10
EXPANDED_TO_COMPACT_PAGE_MAP = {7: 0, 8: 1, 9: 2, 10: 3, 11: 4, 12: 5, 13: 6, 15: 7, 17: 8}


def _set(src: str, pat: str, val: str, count: int = 1) -> str:
    return re.sub(pat, val, src, count=count)


def make_text(
    pag: int,
    oid: int,
    x: int,
    y: int,
    w: int,
    h: int,
    label: str,
    fg: int,
    bg: int,
    xlang: int | None = None,
    ylang: int | None = None,
) -> str:
    if xlang is None:
        xlang = x
    if ylang is None:
        ylang = y
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
{p}_BoxColor={RED}
{p}_GraphColor={YELLOW}
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
{p}_ObjText.X_Lang=0:{xlang}
{p}_ObjText.Y_Lang=0:{ylang}
{p}_ObjText.Dim_Lang=0:D22
{p}_ObjText.Testo=1:{label}
{p}_ObjText.ForeColor=1:{fg}
{p}_ObjText.BackColor=1:{bg}
{p}_ObjText.FontText=1:0
{p}_ObjText.X_Lang=1:{xlang}
{p}_ObjText.Y_Lang=1:{ylang}
{p}_ObjText.Dim_Lang=1:D22
"""


def make_word(
    pag: int,
    oid: int,
    x: int,
    y: int,
    vid: int,
    fg: int,
    bg: int,
    box: int,
    w: int = 72,
    h: int = 24,
) -> str:
    p = f"Pag_{pag}_Obj_{oid}"
    return f"""{p}_IdObj={oid}
{p}_Tipo=11
{p}_Modo=DRAW
{p}_X={x}
{p}_Y={y}
{p}_Width={w}
{p}_Height={h}
{p}_Spessore=1
{p}_ForeColor={fg}
{p}_BackColor={bg}
{p}_BoxColor={box}
{p}_GraphColor={YELLOW}
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


def make_key(
    pag: int,
    oid: int,
    x: int,
    y: int,
    w: int,
    h: int,
    name: str,
    macro: str,
    dest: int,
    fg: int,
    bg: int,
    code: int = 50,
    resflg: bool = False,
) -> str:
    p = f"Pag_{pag}_Obj_{oid}"
    release = ""
    if resflg and macro == "MAC_SETFLG":
        release = f"""{p}_KeyTouch_0_Macro_R=MAC_RESFLG
{p}_KeyTouch_0_PaginaDATA_R={dest}
{p}_KeyTouch_0_ValoreBit_R=0
"""
    return f"""{p}_IdObj={oid}
{p}_Tipo=17
{p}_Modo=DRAW
{p}_X={x}
{p}_Y={y}
{p}_Width={w}
{p}_Height={h}
{p}_Spessore=1
{p}_ForeColor={fg}
{p}_BackColor={bg}
{p}_BoxColor={bg}
{p}_GraphColor={YELLOW}
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
{p}_KeyTouch_0_Macro_P={macro}
{p}_KeyTouch_0_PaginaDATA_P={dest}
{p}_KeyTouch_0_ValoreBit_P=0
{p}_KeyTouch_0_IndPLC_P=1
{p}_KeyTouch_0_PortaCOM_P=INTERNAL
{p}_KeyTouch_0_Immagine_R=0
{release}{p}_KeyTouch_0_IndPLC_R=1
{p}_KeyTouch_0_PortaCOM_R=INTERNAL
{p}_KeyTouch_0_StatoLed=False
{p}_KeyTouch_0_Trasparente=True
{p}_KeyTouch_0_TextMenu=0:0
{p}_KeyTouch_0_TextMenu=1:0
"""


def make_image(pag: int, oid: int, img_id: int, bg: int) -> str:
    p = f"Pag_{pag}_Obj_{oid}"
    return f"""{p}_IdObj={oid}
{p}_Tipo=12
{p}_Modo=DEL
{p}_X=296
{p}_Y=0
{p}_Width=24
{p}_Height=24
{p}_Spessore=1
{p}_ForeColor={BLACK}
{p}_BackColor={bg}
{p}_BoxColor={RED}
{p}_GraphColor={YELLOW}
{p}_Font=0
{p}_LAMPEGGIO=False
{p}_COL_DINAMICO=False
{p}_IdVar={img_id}
{p}_DimCarattere=D11
{p}_FormaCursore=0
{p}_DataSavePos=1000
{p}_Code=0
{p}_Grandezza=D11
{p}_BOX=False
"""


HISTO_FILL_L = -16711936  # lime, barra livello chiara
HISTO_EMPTY_L = BG_L
HISTO_FILL_D = -14900267
HISTO_EMPTY_D = -16771033
NAVY_PAGE_SET = {7, 8, 9, 10, 11, 12, 13, 15, 17}
MAN_ONOFF_VID = 59


def make_var(
    vid: int,
    nome: str,
    desc: str,
    addr: str,
    *,
    tipo: str = "WORD",
    dim: str = "WORD_WIDE",
    intere: str = "5",
    dec: str = "0",
    mn: str = "0",
    mx: str = "65535",
    ena: str = "False",
    rfs: str = "True",
    bit_index: str = "0",
) -> str:
    return f"""
[Variabile_{vid}]
Var_{vid}_Nome={nome}
Var_{vid}_TipoVar={tipo}
Var_{vid}_Descrizione={desc}
Var_{vid}_AreaVar=None
Var_{vid}_IndirizzoVar={addr}
Var_{vid}_Minimo={mn}
Var_{vid}_Massimo={mx}
Var_{vid}_ComPort=INTERNAL
Var_{vid}_IndStrumento=0
Var_{vid}_IndPLC=1
Var_{vid}_Dimensione={dim}
Var_{vid}_CifreIntere={intere}
Var_{vid}_CifreDecimali={dec}
Var_{vid}_Bit_Index={bit_index}
Var_{vid}_UpdateTime=0
Var_{vid}_Num_Curve=1
Var_{vid}_Num_Ref=0
Var_{vid}_DivAsseX=0
Var_{vid}_DivAsseY=0
Var_{vid}_Ref_0=0
Var_{vid}_Ref_1=0
Var_{vid}_ENA={ena}
Var_{vid}_RFS={rfs}
Var_{vid}_INIBIT=False
Var_{vid}_PWD=False
Var_{vid}_REMOTE=False
Var_{vid}_RIC=False
Var_{vid}_SWAP=False
Var_{vid}_IMM=False
Var_{vid}_OMR_HEX=False
Var_{vid}_HIDDEN=False
Var_{vid}_INDEX=False
Var_{vid}_ENG=False
Var_{vid}_SCALE=False
Var_{vid}_IndIndice=00
Var_{vid}_NumElementi=0
Var_{vid}_NormInv=False
Var_{vid}_DecHex=True
Var_{vid}_Obj2D3D=False
Var_{vid}_NumObjV=0
Var_{vid}_NumObjF=0
Var_{vid}_Lingua_0_NumStrV=0
Var_{vid}_Lingua_0_NumStrF=0
"""


def make_bit_str_var(vid: int) -> str:
    """OFF/ON su bit 0 di DATA.2020. IMM off: il tap resta KEY FLAG.254.

    LogicPaint memorizza le coppie in ElencoStringheV (bit=1) / ElencoStringheF (bit=0),
    non StrV_0/StrF_0 (quelli Compila li butta → rettangolo vuoto sul TP320).
    """
    blob = make_var(
        vid,
        "MAN ON OFF",
        "OFF=0 ON=1",
        "DATA.2020",
        tipo="BIT_STR",
        intere="3",
        mn="0",
        mx="1",
        ena="False",
        rfs="True",
        bit_index="0",
    )
    blob = blob.replace(
        f"Var_{vid}_Lingua_0_NumStrV=0\nVar_{vid}_Lingua_0_NumStrF=0\n",
        f"Var_{vid}_Lingua_0_NumStrV=1\n"
        f"Var_{vid}_Lingua_0_ValStrV0=ON\n"
        f"Var_{vid}_Lingua_0_ElencoStringheV_0=ON\n"
        f"Var_{vid}_Lingua_0_NumStrF=1\n"
        f"Var_{vid}_Lingua_0_ValStrF0=OFF\n"
        f"Var_{vid}_Lingua_0_ElencoStringheF_0=OFF\n"
        f"Var_{vid}_Lingua_1_NumStrV=1\n"
        f"Var_{vid}_Lingua_1_ValStrV0=ON\n"
        f"Var_{vid}_Lingua_1_NumStrF=1\n"
        f"Var_{vid}_Lingua_1_ValStrF0=OFF\n",
    )
    return blob


def _fill_man_bit_str_strings(text: str) -> str:
    """Var_59 con ValStr vuoti: Compila/round-trip li azzera se il nome campo è sbagliato."""
    vid = MAN_ONOFF_VID
    for lang in (0, 1):
        text = re.sub(
            rf"Var_{vid}_Lingua_{lang}_ValStrV0=.*",
            f"Var_{vid}_Lingua_{lang}_ValStrV0=ON",
            text,
        )
        text = re.sub(
            rf"Var_{vid}_Lingua_{lang}_ValStrF0=.*",
            f"Var_{vid}_Lingua_{lang}_ValStrF0=OFF",
            text,
        )
        if f"Var_{vid}_Lingua_{lang}_ValStrV0=" not in text:
            text = text.replace(
                f"Var_{vid}_Lingua_{lang}_NumStrV=1\n",
                f"Var_{vid}_Lingua_{lang}_NumStrV=1\nVar_{vid}_Lingua_{lang}_ValStrV0=ON\n",
            )
        if f"Var_{vid}_Lingua_{lang}_ValStrF0=" not in text:
            text = text.replace(
                f"Var_{vid}_Lingua_{lang}_NumStrF=1\n",
                f"Var_{vid}_Lingua_{lang}_NumStrF=1\nVar_{vid}_Lingua_{lang}_ValStrF0=OFF\n",
            )
    text = text.replace(f"Var_{vid}_Lingua_0_NumStrV=0\n", f"Var_{vid}_Lingua_0_NumStrV=1\n")
    text = text.replace(f"Var_{vid}_Lingua_0_NumStrF=0\n", f"Var_{vid}_Lingua_0_NumStrF=1\n")
    return text


def _set_obj(text: str, pag: int, oid: int, field: str, value: str) -> str:
    return _pf(text, pag, oid, field, value)


def _restyle_hmi(text: str) -> str:
    """MAN ON/OFF, unita' vicine, WORD warning D22, lampade colori istogramma."""
    if f"[Variabile_{MAN_ONOFF_VID}]" not in text:
        text = _insert_before(text, "[Lista Immagini]", make_bit_str_var(MAN_ONOFF_VID) + "\n")

    text = _fill_man_bit_str_strings(text)

    # Lampade 24x24: ON = fill barra, OFF = vuoto barra, niente bordo.
    # MAN (IdVar=47) diventa BIT_STR; anche oggetti già convertiti (IdVar=59).
    man_oids: list[tuple[int, int]] = []
    for m in re.finditer(r"Pag_(\d+)_Obj_(\d+)_Tipo=14\n", text):
        pag, oid = int(m.group(1)), int(m.group(2))
        wm = re.search(rf"Pag_{pag}_Obj_{oid}_Width=(\d+)", text)
        hm = re.search(rf"Pag_{pag}_Obj_{oid}_Height=(\d+)", text)
        im = re.search(rf"Pag_{pag}_Obj_{oid}_IdVar=(\d+)", text)
        if not wm or not hm or not im:
            continue
        if wm.group(1) != "24" or hm.group(1) != "24":
            continue
        if im.group(1) in ("47", str(MAN_ONOFF_VID)):
            man_oids.append((pag, oid))
            continue
        navy_palette = pag in NAVY_PAGE_SET
        fill = str(HISTO_FILL_D if navy_palette else HISTO_FILL_L)
        empty = str(HISTO_EMPTY_D if navy_palette else HISTO_EMPTY_L)
        text = _set_obj(text, pag, oid, "ForeColor", fill)
        text = _set_obj(text, pag, oid, "BackColor", empty)
        text = _set_obj(text, pag, oid, "BoxColor", empty)
        text = _set_obj(text, pag, oid, "BOX", "False")

    for m in re.finditer(r"Pag_(\d+)_Obj_(\d+)_Tipo=11\n", text):
        pag, oid = int(m.group(1)), int(m.group(2))
        im = re.search(rf"Pag_{pag}_Obj_{oid}_IdVar=(\d+)", text)
        if im and im.group(1) == str(MAN_ONOFF_VID) and (pag, oid) not in man_oids:
            man_oids.append((pag, oid))

    # Quadrato MAN -> testo ON/OFF. MAN etichetta resta a destra.
    title_l, title_d = str(BLUE_L), str(NAV_D)
    for pag, oid in man_oids:
        navy_palette = pag in NAVY_PAGE_SET
        bg = title_d if navy_palette else title_l
        text = _set_obj(text, pag, oid, "Tipo", "11")
        text = _set_obj(text, pag, oid, "X", "200")
        text = _set_obj(text, pag, oid, "Width", "52")
        text = _set_obj(text, pag, oid, "ForeColor", str(WHITE))
        text = _set_obj(text, pag, oid, "BackColor", bg)
        text = _set_obj(text, pag, oid, "BoxColor", bg)
        text = _set_obj(text, pag, oid, "IdVar", str(MAN_ONOFF_VID))
        text = _set_obj(text, pag, oid, "DimCarattere", "D22")
        text = _set_obj(text, pag, oid, "Grandezza", "D11")
        text = _set_obj(text, pag, oid, "BOX", "False")

    # Hit-area MAN copre ON/OFF + MAN (senza sole c'è spazio fino a 320).
    for m in re.finditer(r"Pag_(\d+)_Obj_(\d+)_KeyTouch_0_PaginaDATA_P=254\n", text):
        pag, oid = int(m.group(1)), int(m.group(2))
        text = _set_obj(text, pag, oid, "X", "200")
        text = _set_obj(text, pag, oid, "Width", "88")

    # Unita' ETA/FLOW accostate al valore (come TRAVASO in campo).
    for pag, oid_min, oid_lm in ((1, 39, 40), (2, 37, 38), (8, 39, 40), (9, 37, 38)):
        if f"Pag_{pag}_Obj_{oid_min}_IdObj={oid_min}" not in text:
            continue
        text = _set_obj(text, pag, oid_min, "X", "108")
        text = _set_obj(text, pag, oid_min, "ObjText.X_Lang=0:", "108")
        text = _set_obj(text, pag, oid_min, "ObjText.X_Lang=1:", "108")
        text = _set_obj(text, pag, oid_lm, "X", "256")
        text = _set_obj(text, pag, oid_lm, "Width", "36")
        text = _set_obj(text, pag, oid_lm, "ObjText.X_Lang=0:", "256")
        text = _set_obj(text, pag, oid_lm, "ObjText.X_Lang=1:", "256")

    # Warning LIV/LT: stesso font dei WORD TRAVASO.
    for pag, oid in ((16, 7), (16, 9), (17, 7), (17, 9)):
        if f"Pag_{pag}_Obj_{oid}_IdObj={oid}" not in text:
            continue
        text = _set_obj(text, pag, oid, "DimCarattere", "D11")
        text = _set_obj(text, pag, oid, "Grandezza", "D22")

    return text


def make_alarm(n: int, name: str) -> str:
    p = f"Alr_{n}"
    return f"""[{p.replace('Alr_', 'Allarme_')}]
{p}_NomeAllarme={name}
{p}_ColoreSfondo={RED}
{p}_ColoreScritta={WHITE}
{p}_ColoreCornice=-16711681
{p}_ColoreSfondoScritta={RED}
{p}_ColoreGriglia={WHITE}
{p}_Obj_0_IdObj=0
{p}_Obj_0_Tipo=2
{p}_Obj_0_Modo=DRAW
{p}_Obj_0_X=24
{p}_Obj_0_Y=48
{p}_Obj_0_Width=180
{p}_Obj_0_Height=16
{p}_Obj_0_Spessore=1
{p}_Obj_0_ForeColor={WHITE}
{p}_Obj_0_BackColor={RED}
{p}_Obj_0_BoxColor={RED}
{p}_Obj_0_GraphColor={YELLOW}
{p}_Obj_0_Font=0
{p}_Obj_0_IdVar=0
{p}_Obj_0_DimCarattere=D22
{p}_Obj_0_FormaCursore=0
{p}_Obj_0_DataSavePos=1000
{p}_Obj_0_Code=0
{p}_Obj_0_ObjText.Testo=0:{name}
{p}_Obj_0_ObjText.ForeColor=0:{WHITE}
{p}_Obj_0_ObjText.BackColor=0:{RED}
{p}_Obj_0_ObjText.FontText=0:0
{p}_Obj_0_ObjText.X_Lang=0:24
{p}_Obj_0_ObjText.Y_Lang=0:48
{p}_Obj_0_ObjText.Dim_Lang=0:D22
{p}_Obj_0_ObjText.Testo=1:{name}
{p}_Obj_0_ObjText.ForeColor=1:{WHITE}
{p}_Obj_0_ObjText.BackColor=1:{RED}
{p}_Obj_0_ObjText.FontText=1:0
{p}_Obj_0_ObjText.X_Lang=1:24
{p}_Obj_0_ObjText.Y_Lang=1:48
{p}_Obj_0_ObjText.Dim_Lang=1:D22
"""


def _tab_pair(pag: int, start_oid: int, navy_palette: bool, active: int, dests: tuple[int, ...] | None = None) -> str:
    dests = dests or (TAB_PAGE_D if navy_palette else TAB_PAGE_L)
    idle_bg = NAV_D if navy_palette else BLUE_L
    parts = []
    oid = start_oid
    for i, (x, w, xlang, label) in enumerate(TAB):
        on = i == active
        fg = BLACK if on else WHITE
        bg = YELLOW if on else idle_bg
        parts.append(make_text(pag, oid, x, 0, w, 16, label, fg, bg, xlang=xlang, ylang=4))
        parts.append(
            make_key(pag, oid + 1, x, 0, w, 24, f"KEY.{label}", "MAC_PAGE", dests[i], fg, bg)
        )
        oid += 2
    return "".join(parts)


def _nav_bar(
    pag: int,
    start_oid: int,
    navy_palette: bool,
    active: int = 3,
    pages: tuple[int, ...] | None = None,
) -> str:
    idle_bg = NAV_D if navy_palette else BLUE_L
    pages = pages or (NAV_PAGES_D if navy_palette else NAV_PAGES_L)
    labels = ("HOME", "FILL", "TRAV", "SETUP")
    tx = (16, 96, 176, 256)
    kx = (0, 80, 160, 240)
    tw = (48, 48, 48, 60)
    parts = []
    oid = start_oid
    for i, lab in enumerate(labels):
        on = i == active
        fg = BLACK if on else WHITE
        bg = YELLOW if on else idle_bg
        parts.append(make_text(pag, oid, tx[i], 222, tw[i], 16, lab, fg, bg))
        parts.append(
            make_key(pag, oid + 1, kx[i], 216, 80, 24, f"KEY.{lab}", "MAC_PAGE", pages[i], fg, bg)
        )
        oid += 2
    return "".join(parts)


def make_contat_page(pag: int, navy_palette: bool) -> str:
    bg = BG_D if navy_palette else BG_L
    title_bg = BLUE_D_TITLE if navy_palette else BLUE_L
    idle_bg = NAV_D if navy_palette else BLUE_L
    lab_fg = WHITE if navy_palette else BLACK
    lab_bg = bg
    word_fg = WHITE if navy_palette else BLACK
    word_bg = BG_D if navy_palette else WHITE
    word_box = BOX_D if navy_palette else RED
    unit_fg = CYAN if navy_palette else BLACK
    img = 2 if navy_palette else 1
    img_bg = WHITE if not navy_palette else BLACK
    theme_to = 6 if navy_palette else 13
    nome = "CONTAT"
    grid = NAV_D if navy_palette else WHITE
    parts = [
        f"[Pagina_{pag}]\n",
        f"Pag_{pag}_NomePagina={nome}\n",
        f"Pag_{pag}_Attributi=2\n",
        f"Pag_{pag}_ColoreSfondo={bg}\n",
        f"Pag_{pag}_ColoreEditorVar={WHITE}\n",
        f"Pag_{pag}_ColoreGriglia={grid}\n",
        make_text(pag, 0, 12, 4, 60, 16, "SETUP", WHITE, title_bg),
        _tab_pair(pag, 1, navy_palette, active=3),
        make_image(pag, 9, img, img_bg),
        make_key(pag, 10, 296, 0, 24, 24, "KEY.THEME", "MAC_PAGE", theme_to, WHITE, bg),
    ]
    oid = 11
    rows = ((48, "OSMOSI", 55, 235), (104, "RETE", 56, 236), (160, "TRAVASO", 57, 237))
    for y, label, vid, fl in rows:
        parts.append(make_text(pag, oid, 12, y, 96, 16, label, lab_fg, lab_bg))
        oid += 1
        parts.append(make_word(pag, oid, 120, y - 4, vid, word_fg, word_bg, word_box, w=120))
        oid += 1
        parts.append(make_text(pag, oid, 242, y, 16, 16, "L", unit_fg, lab_bg))
        oid += 1
        parts.append(make_text(pag, oid, 258, y, 62, 16, "AZZERA", WHITE, idle_bg))
        oid += 1
        parts.append(
            make_key(
                pag, oid, 258, y - 4, 62, 24, f"KEY.AZZ.{fl}", "MAC_SETFLG", fl, WHITE, idle_bg, code=40, resflg=True
            )
        )
        oid += 1
    parts.append(_nav_bar(pag, oid, navy_palette, active=3))
    return "".join(parts)


def make_refill_page(pag: int, navy_palette: bool, peer: int, fill_page: int, vid: int = 58, *, theme: bool = True) -> str:
    bg = BG_D if navy_palette else BG_L
    title_bg = BLUE_D_TITLE if navy_palette else BLUE_L
    idle_bg = NAV_D if navy_palette else BLUE_L
    lab_fg = WHITE if navy_palette else BLACK
    word_fg = WHITE if navy_palette else BLACK
    word_bg = BG_D if navy_palette else WHITE
    word_box = BOX_D if navy_palette else RED
    img = 2 if navy_palette else 1
    img_bg = WHITE if not navy_palette else BLACK
    nome = "REFILL"
    grid = NAV_D if navy_palette else WHITE
    green = -16744448
    nav_pages = SHIPPING_NAV_PAGES if not theme else None
    head = [
        f"[Pagina_{pag}]\n",
        f"Pag_{pag}_NomePagina={nome}\n",
        f"Pag_{pag}_Attributi=2\n",
        f"Pag_{pag}_ColoreSfondo={bg}\n",
        f"Pag_{pag}_ColoreEditorVar={WHITE}\n",
        f"Pag_{pag}_ColoreGriglia={grid}\n",
        make_text(pag, 0, 12, 4, 72, 16, "FILL", WHITE, title_bg),
    ]
    oid = 1
    if theme:
        head.append(make_image(pag, 1, img, img_bg))
        head.append(make_key(pag, 2, 296, 0, 24, 24, "KEY.THEME", "MAC_PAGE", peer, WHITE, bg))
        oid = 3
    body = [
        make_text(pag, oid, 12, 32, 296, 16, "SERBATOIO NON VUOTO", RED, bg),
        make_text(pag, oid + 1, 12, 52, 296, 16, "DUREZZA LITRI PRESENTI", lab_fg, bg),
        make_word(pag, oid + 2, 12, 68, vid, word_fg, word_bg, word_box, w=144, h=40),
        make_text(pag, oid + 3, 164, 80, 16, 16, "F", lab_fg, bg),
        make_text(pag, oid + 4, 12, 104, 296, 16, "PROCEDERE CON RABBOCCO", lab_fg, bg),
        make_text(pag, oid + 5, 24, 140, 48, 16, "SI", WHITE, green),
        make_key(pag, oid + 6, 12, 136, 72, 24, "KEY.SI", "MAC_SETFLG", 241, WHITE, green, code=40),
        make_text(pag, oid + 7, 120, 140, 48, 16, "NO", WHITE, RED),
        make_key(pag, oid + 8, 108, 136, 72, 24, "KEY.NO", "MAC_PAGE", fill_page, WHITE, RED, code=41),
        _nav_bar(pag, oid + 9, navy_palette, active=1, pages=nav_pages),
    ]
    return "".join(head + body)


def make_warn_vuoto_page(pag: int, navy_palette: bool, peer: int, *, theme: bool = True) -> str:
    """START TRAVASO rifiutato: LIV < LT. OK ripristina la pagina precedente."""
    bg = BG_D if navy_palette else BG_L
    title_bg = BLUE_D_TITLE if navy_palette else BLUE_L
    lab_fg = WHITE if navy_palette else BLACK
    word_fg = WHITE if navy_palette else BLACK
    word_bg = BG_D if navy_palette else WHITE
    word_box = BOX_D if navy_palette else RED
    img = 2 if navy_palette else 1
    img_bg = WHITE if not navy_palette else BLACK
    nome = "WARN VUOTO"
    grid = NAV_D if navy_palette else WHITE
    green = -16744448
    nav_pages = SHIPPING_NAV_PAGES if not theme else None
    head = [
        f"[Pagina_{pag}]\n",
        f"Pag_{pag}_NomePagina={nome}\n",
        f"Pag_{pag}_Attributi=2\n",
        f"Pag_{pag}_ColoreSfondo={bg}\n",
        f"Pag_{pag}_ColoreEditorVar={WHITE}\n",
        f"Pag_{pag}_ColoreGriglia={grid}\n",
        make_text(pag, 0, 12, 4, 96, 16, "TRAVASO", WHITE, title_bg),
    ]
    oid = 1
    if theme:
        head.append(make_image(pag, 1, img, img_bg))
        head.append(make_key(pag, 2, 296, 0, 24, 24, "KEY.THEME", "MAC_PAGE", peer, WHITE, bg))
        oid = 3
    body = [
        make_text(pag, oid, 12, 40, 296, 16, "LIVELLO TROPPO BASSO", RED, bg),
        make_text(pag, oid + 1, 12, 64, 296, 16, "Travaso non partito", lab_fg, bg),
        make_text(pag, oid + 2, 12, 88, 296, 16, "LIV sotto LT TRAVASO", lab_fg, bg),
        make_text(pag, oid + 3, 12, 120, 40, 16, "LIV", lab_fg, bg),
        make_word(pag, oid + 4, 56, 116, 5, word_fg, word_bg, word_box, w=72),
        make_text(pag, oid + 5, 148, 120, 32, 16, "LT", lab_fg, bg),
        make_word(pag, oid + 6, 184, 116, 21, word_fg, word_bg, word_box, w=72),
        make_text(pag, oid + 7, 140, 164, 40, 16, "OK", WHITE, green),
        make_key(
            pag, oid + 8, 116, 160, 88, 24, "KEY.OK", "MAC_SETFLG", 181, WHITE, green, code=44, resflg=True
        ),
        _nav_bar(pag, oid + 9, navy_palette, active=2, pages=nav_pages),
    ]
    return "".join(head + body)


def make_warn_msg_page(
    pag: int,
    nome: str,
    title: str,
    lines: tuple[str, ...],
    ok_flag: int,
    nav_active: int,
) -> str:
    """Pagina avviso: messaggi + OK (impulso SETFLG)."""
    bg = BG_D
    title_bg = BLUE_D_TITLE
    lab_fg = WHITE
    green = -16744448
    parts = [
        f"[Pagina_{pag}]\n",
        f"Pag_{pag}_NomePagina={nome}\n",
        f"Pag_{pag}_Attributi=2\n",
        f"Pag_{pag}_ColoreSfondo={bg}\n",
        f"Pag_{pag}_ColoreEditorVar={WHITE}\n",
        f"Pag_{pag}_ColoreGriglia={NAV_D}\n",
        make_text(pag, 0, 12, 4, 72, 16, title, WHITE, title_bg),
    ]
    oid = 1
    y = 40
    for i, line in enumerate(lines):
        fg = RED if i == 0 else lab_fg
        parts.append(make_text(pag, oid, 12, y, 296, 16, line, fg, bg))
        oid += 1
        y += 24
    y = max(y + 8, 152)
    parts.append(make_text(pag, oid, 140, y + 4, 40, 16, "OK", WHITE, green))
    parts.append(
        make_key(
            pag, oid + 1, 116, y, 88, 24, "KEY.OK", "MAC_SETFLG", ok_flag, WHITE, green, code=44, resflg=True
        )
    )
    parts.append(_nav_bar(pag, oid + 2, True, active=nav_active, pages=SHIPPING_NAV_PAGES))
    return "".join(parts)


def _move_setup_tabs(text: str) -> str:
    """TANK/MIX/TRASD geometry on pages that already have those three tabs."""
    for pag in (3, 4, 5, 10, 11, 12):
        specs = (
            (1, 80, 48, 86),
            (2, 80, 48, None),
            (3, 132, 44, 138),
            (4, 132, 44, None),
            (5, 180, 52, 182),
            (6, 180, 52, None),
        )
        for oid, x, w, xlang in specs:
            text = re.sub(rf"(Pag_{pag}_Obj_{oid}_X=)\d+", rf"\g<1>{x}", text, count=1)
            text = re.sub(rf"(Pag_{pag}_Obj_{oid}_Width=)\d+", rf"\g<1>{w}", text, count=1)
            if xlang is not None:
                text = re.sub(
                    rf"(Pag_{pag}_Obj_{oid}_ObjText\.X_Lang=0:)\d+",
                    rf"\g<1>{xlang}",
                    text,
                    count=1,
                )
                text = re.sub(
                    rf"(Pag_{pag}_Obj_{oid}_ObjText\.X_Lang=1:)\d+",
                    rf"\g<1>{xlang}",
                    text,
                    count=1,
                )
    return text


def _pf(text: str, pag: int, oid: int, field: str, value: str, n: int = 1) -> str:
    if field.endswith(":"):
        pat = rf"(Pag_{pag}_Obj_{oid}_{re.escape(field)}).*"
        repl = rf"\g<1>{value}"
    else:
        pat = rf"(Pag_{pag}_Obj_{oid}_{re.escape(field)}=).*"
        repl = rf"\g<1>{value}"
    t, c = re.subn(pat, repl, text, count=n)
    if c < 1:
        raise SystemExit(f"manca Pag_{pag}_Obj_{oid}_{field}")
    return t


def _fix_home_man_rows(text: str) -> str:
    """HOME chiaro/navy: tasti OSM/RETE/TRAV visibili da etichetta a lampada.

    Il KEY trasparente sul TP320 prende il tap solo dove c'è un Tipo 2 sotto.
    Le scritte erano 48–84 px; il KEY 168 px copriva il vuoto e l'H_ISTO
    mangiava il resto. Box 12×168×24 allineato alla lampada + KEY uguale.
    """
    rows = (
        (10, 26, 104),  # OSMOSI
        (12, 27, 144),  # RETE
        (14, 28, 184),  # TRAVASO
    )
    for pag, btn, lab_fg in ((0, BLUE_L, WHITE), (7, NAV_D, WHITE)):
        for text_oid, key_oid, y in rows:
            for oid in (text_oid, key_oid):
                text = _pf(text, pag, oid, "X", "12")
                text = _pf(text, pag, oid, "Y", str(y))
                text = _pf(text, pag, oid, "Width", "168")
                text = _pf(text, pag, oid, "Height", "24")
            text = _pf(text, pag, text_oid, "ForeColor", str(lab_fg))
            text = _pf(text, pag, text_oid, "BackColor", str(btn))
            text = _pf(text, pag, text_oid, "ObjText.ForeColor=0:", str(lab_fg))
            text = _pf(text, pag, text_oid, "ObjText.BackColor=0:", str(btn))
            text = _pf(text, pag, text_oid, "ObjText.ForeColor=1:", str(lab_fg))
            text = _pf(text, pag, text_oid, "ObjText.BackColor=1:", str(btn))
            text = _pf(text, pag, text_oid, "ObjText.X_Lang=0:", "18")
            text = _pf(text, pag, text_oid, "ObjText.X_Lang=1:", "18")
            text = _pf(text, pag, text_oid, "ObjText.Y_Lang=0:", str(y + 4))
            text = _pf(text, pag, text_oid, "ObjText.Y_Lang=1:", str(y + 4))
        # Non spostare MAN/RESET: geometria di campo (RESET X=126).
    return text


def _fix_fill_valve_taps(text: str) -> str:
    """FILL OSM/RETE: Tipo 2 sotto il KEY (tap TP320) + hit-area etichetta→lampada."""
    rows = (
        (12, 17, 72, "OSMOSI"),
        (18, 23, 128, "RETE"),
    )
    for pag in (1, 8):
        if f"Pag_{pag}_Obj_17_IdObj=17" not in text:
            continue
        for text_oid, key_oid, y, _lab in rows:
            if f"Pag_{pag}_Obj_{text_oid}_IdObj={text_oid}" not in text:
                continue
            if f"Pag_{pag}_Obj_{key_oid}_IdObj={key_oid}" not in text:
                continue
            for oid in (text_oid, key_oid):
                text = _pf(text, pag, oid, "X", "12")
                text = _pf(text, pag, oid, "Y", str(y))
                text = _pf(text, pag, oid, "Width", "120")
                text = _pf(text, pag, oid, "Height", "24")
            text = _pf(text, pag, text_oid, "ForeColor", str(WHITE))
            text = _pf(text, pag, text_oid, "BackColor", str(NAV_D if pag == 8 else BLUE_L))
            bg = str(NAV_D if pag == 8 else BLUE_L)
            text = _pf(text, pag, text_oid, "ObjText.ForeColor=0:", str(WHITE))
            text = _pf(text, pag, text_oid, "ObjText.BackColor=0:", bg)
            text = _pf(text, pag, text_oid, "ObjText.ForeColor=1:", str(WHITE))
            text = _pf(text, pag, text_oid, "ObjText.BackColor=1:", bg)
            text = _pf(text, pag, text_oid, "ObjText.X_Lang=0:", "18")
            text = _pf(text, pag, text_oid, "ObjText.X_Lang=1:", "18")
            text = _pf(text, pag, text_oid, "ObjText.Y_Lang=0:", str(y + 4))
            text = _pf(text, pag, text_oid, "ObjText.Y_Lang=1:", str(y + 4))
    return text


def _split_pages(text: str) -> tuple[str, dict[int, str], str]:
    start = text.find("[Pagina_0]")
    alarm = text.find("[Allarme_0]")
    if start < 0 or alarm < 0:
        raise SystemExit("pagine/allarmi mancanti")
    header, body, rest = text[:start], text[start:alarm], text[alarm:]
    matches = list(re.finditer(r"\[Pagina_(\d+)\]\n", body))
    pages: dict[int, str] = {}
    for i, m in enumerate(matches):
        n = int(m.group(1))
        a = m.start()
        b = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        pages[n] = body[a:b]
    return header, pages, rest


def _delete_obj(blob: str, pag: int, oid: int) -> str:
    return re.sub(rf"Pag_{pag}_Obj_{oid}_.*\n", "", blob)


def _page_oids(blob: str, pag: int) -> list[int]:
    return [int(x) for x in re.findall(rf"Pag_{pag}_Obj_(\d+)_IdObj=", blob)]


def _strip_theme_objs(blob: str, pag: int) -> str:
    for oid in _page_oids(blob, pag):
        drop = False
        if f"Pag_{pag}_Obj_{oid}_KeyTouch_0_Nome=KEY.THEME" in blob:
            drop = True
        else:
            tm = re.search(rf"Pag_{pag}_Obj_{oid}_Tipo=(\d+)", blob)
            xm = re.search(rf"Pag_{pag}_Obj_{oid}_X=(\d+)", blob)
            ym = re.search(rf"Pag_{pag}_Obj_{oid}_Y=(\d+)", blob)
            wm = re.search(rf"Pag_{pag}_Obj_{oid}_Width=(\d+)", blob)
            hm = re.search(rf"Pag_{pag}_Obj_{oid}_Height=(\d+)", blob)
            if (
                tm
                and tm.group(1) == "12"
                and xm
                and xm.group(1) == "296"
                and ym
                and ym.group(1) == "0"
                and wm
                and wm.group(1) == "24"
                and hm
                and hm.group(1) == "24"
            ):
                drop = True
        if drop:
            blob = _delete_obj(blob, pag, oid)
    return blob


def _remap_mac_page_dests(blob: str, pag: int, mapping: dict[int, int]) -> str:
    for oid_s in re.findall(rf"Pag_{pag}_Obj_(\d+)_KeyTouch_0_Macro_P=MAC_PAGE\n", blob):
        oid = int(oid_s)
        blob = re.sub(
            rf"(Pag_{pag}_Obj_{oid}_KeyTouch_0_PaginaDATA_P=)(\d+)",
            lambda mm: mm.group(1) + str(mapping.get(int(mm.group(2)), int(mm.group(2)))),
            blob,
            count=1,
        )
    return blob


def _enlarge_fill_dur(text: str) -> str:
    """FILL DUR TARGET (Obj_11, Var_20): più basso e meno alto."""
    if "Pag_1_Obj_11_IdObj=11" in text:
        text = _pf(text, 1, 11, "X", "216")
        text = _pf(text, 1, 11, "Y", "36")
        text = _pf(text, 1, 11, "Width", "96")
        text = _pf(text, 1, 11, "Height", "32")
    if "Pag_4_Obj_10_IdObj=10" in text:
        text = _pf(text, 4, 10, "Width", "72")
    return text


def _layout_fill_page(text: str) -> str:
    """RESET, cm editabili, L a destra dei litri, FLOW→LIV.

    Dopo compattazione REFILL (ex pag.8) su pag.1:
    0 titolo, 9 LT, 11 DUR, 12/18 OSM/RETE, 13/19 LED,
    14/20 L, 15/21 litri, 17/23 KEY MAN, 25 ETA, 26/27 FLOW.
    """
    if "Pag_1_Obj_0_IdObj=0" not in text:
        return text
    text = text.replace("Pag_1_Obj_0_ObjText.Testo=0:FILL", "Pag_1_Obj_0_ObjText.Testo=0:RESET")
    text = text.replace("Pag_1_Obj_0_ObjText.Testo=1:FILL", "Pag_1_Obj_0_ObjText.Testo=1:RESET")
    text = _pf(text, 1, 0, "Width", "60")
    text = _pf(text, 1, 0, "BackColor", str(BLUE_D_TITLE))
    text = _pf(text, 1, 0, "ObjText.BackColor=0:", str(BLUE_D_TITLE))
    text = _pf(text, 1, 0, "ObjText.BackColor=1:", str(BLUE_D_TITLE))
    text = _enlarge_fill_dur(text)
    text = _pf(text, 1, 13, "X", "96")
    text = _pf(text, 1, 13, "Width", "24")
    text = _pf(text, 1, 19, "X", "96")
    text = _pf(text, 1, 19, "Width", "24")
    text = _pf(text, 1, 17, "X", "12")
    text = _pf(text, 1, 17, "Width", "108")
    text = _pf(text, 1, 23, "X", "12")
    text = _pf(text, 1, 23, "Width", "108")
    text = _pf(text, 1, 15, "X", "228")
    text = _pf(text, 1, 15, "Width", "54")
    text = _pf(text, 1, 21, "X", "228")
    text = _pf(text, 1, 21, "Width", "54")
    text = _pf(text, 1, 14, "X", "286")
    text = _pf(text, 1, 14, "Width", "16")
    text = _pf(text, 1, 14, "ObjText.X_Lang=0:", "286")
    text = _pf(text, 1, 14, "ObjText.X_Lang=1:", "286")
    text = _pf(text, 1, 20, "X", "286")
    text = _pf(text, 1, 20, "Width", "16")
    text = _pf(text, 1, 20, "ObjText.X_Lang=0:", "286")
    text = _pf(text, 1, 20, "ObjText.X_Lang=1:", "286")
    text = text.replace("Pag_1_Obj_26_ObjText.Testo=0:FLOW", "Pag_1_Obj_26_ObjText.Testo=0:LIV")
    text = text.replace("Pag_1_Obj_26_ObjText.Testo=1:FLOW", "Pag_1_Obj_26_ObjText.Testo=1:LIV")
    text = _pf(text, 1, 27, "IdVar", "5")
    text = _pf(text, 1, 27, "X", "216")
    text = _pf(text, 1, 27, "Width", "72")
    text = text.replace("Pag_1_Obj_40_ObjText.Testo=0:l/m", "Pag_1_Obj_40_ObjText.Testo=0:")
    text = text.replace("Pag_1_Obj_40_ObjText.Testo=1:l/m", "Pag_1_Obj_40_ObjText.Testo=1:")
    if "Pag_1_Obj_41_IdObj=41" not in text:
        blob = (
            make_key(
                1,
                41,
                12,
                0,
                64,
                24,
                "KEY.FILLRST",
                "MAC_SETFLG",
                268,
                WHITE,
                BLUE_D_TITLE,
                code=42,
                resflg=True,
            )
            + make_word(1, 42, 124, 74, 60, WHITE, BG_D, BOX_D, w=70, h=24)
            + make_text(1, 43, 198, 76, 28, 16, "cm", CYAN, BG_D)
            + make_word(1, 44, 124, 130, 61, WHITE, BG_D, BOX_D, w=70, h=24)
            + make_text(1, 45, 198, 132, 28, 16, "cm", CYAN, BG_D)
        )
        text = text.replace("\n[Pagina_2]", "\n" + blob + "\n[Pagina_2]")
    if "[Variabile_60]" not in text:
        text = _insert_before(
            text,
            "[Lista Immagini]",
            make_var(
                60,
                "CM OSMOSI",
                "CM COLONNA OSMOSI",
                "DATA.2063",
                intere="3",
                mn="0",
                mx="250",
                ena="True",
                rfs="True",
            )
            + make_var(
                61,
                "CM RETE",
                "CM COLONNA RETE",
                "DATA.2064",
                intere="3",
                mn="0",
                mx="250",
                ena="True",
                rfs="True",
            )
            + "\n",
        )
    return text


def finalize_hmi_compact(text: str) -> str:
    """Migra al layout compatto 0..10 con WARN LT/DUR."""
    if _has_compact_hmi_pages(text):
        text = re.sub(r"(InfoVersione=).*", r"\1H20-v1.00", text, count=1)
        text = _layout_fill_page(text)
        text = _fill_man_bit_str_strings(text)
        return text
    header, pages, rest = _split_pages(text)
    out_pages: list[str] = []
    for old, new in sorted(EXPANDED_TO_COMPACT_PAGE_MAP.items(), key=lambda kv: kv[1]):
        if old not in pages:
            raise SystemExit(f"manca Pagina_{old} per la migrazione layout compatto")
        blob = pages[old]
        blob = _strip_theme_objs(blob, old)
        blob = _remap_mac_page_dests(blob, old, EXPANDED_TO_COMPACT_PAGE_MAP)
        blob = blob.replace(f"[Pagina_{old}]", f"[Pagina_{new}]")
        blob = re.sub(rf"Pag_{old}_", f"Pag_{new}_", blob)
        blob = blob.replace(" " + "D" + "ARK", "")
        if not blob.endswith("\n"):
            blob += "\n"
        out_pages.append(blob)

    # REFILL (7) e WARN VUOTO (8) rigenerate senza tema; + WARN LT/DUR.
    refill = make_refill_page(7, True, 0, 1, 58, theme=False)
    refill = refill.replace("REFILL " + "D" + "ARK", "REFILL")
    warn_v = make_warn_vuoto_page(8, True, 0, theme=False)
    warn_v = warn_v.replace("WARN VUOTO " + "D" + "ARK", "WARN VUOTO")
    warn_lt = make_warn_msg_page(
        9,
        "WARN LT",
        "FILL",
        (
            "ATTENZIONE",
            "TARGET LT MAGGIOR LIV",
            "IMPOSSIBILE RABBOCCO",
        ),
        176,
        1,
    )
    warn_dur = make_warn_msg_page(
        10,
        "WARN DUR",
        "FILL",
        (
            "IMPOSSIBILE RAGGIUNGERE",
            "DUREZZA E LITRI TARGET",
        ),
        177,
        1,
    )
    # Sostituisci i blob 7 e 8 (REFILL, WARN VUOTO) con le versioni pulite.
    out_pages[7] = refill if refill.endswith("\n") else refill + "\n"
    out_pages[8] = warn_v if warn_v.endswith("\n") else warn_v + "\n"
    extra = warn_lt + "\n" + warn_dur + "\n"
    text = header + "".join(out_pages) + extra + rest
    text = text.replace("TOLLERANZA %", "TOLLERANZA LT")
    text = re.sub(r"(InfoVersione=).*", r"\1H20-v1.00", text, count=1)
    text = _fill_man_bit_str_strings(text)
    text = _layout_fill_page(text)
    return text


def _insert_before(text: str, marker: str, blob: str) -> str:
    if blob.strip() in text:
        return text
    i = text.find(marker)
    if i < 0:
        raise SystemExit(f"marker mancante: {marker}")
    return text[:i] + blob + text[i:]


def _replace_section(text: str, start: str, end: str, new: str) -> str:
    a = text.find(start)
    b = text.find(end)
    if a < 0 or b < 0 or b <= a:
        raise SystemExit(f"sezione {start} .. {end} non trovata")
    if not new.endswith("\n"):
        new += "\n"
    return text[:a] + new + text[b:]


def _has_compact_hmi_pages(text: str) -> bool:
    return "[Pagina_11]" not in text and "Pag_7_NomePagina=REFILL" in text


def apply_hmi(text: str) -> str:
    text = re.sub(r"(InfoVersione=).*", r"\1H20-v1.00", text, count=1)
    if _has_compact_hmi_pages(text):
        text = _fix_fill_valve_taps(text)
        return text

    text = re.sub(r"(Var_32_Nome=).*", r"\1FS bar", text, count=1)
    text = re.sub(r"(Var_32_Descrizione=).*", r"\g<1>0.3=0.3BAR 2.0=2BAR", text, count=1)
    text = text.replace("Var_32_Minimo=3\nP\n", "Var_32_Minimo=3\nVar_32_Massimo=20\n")
    if "Var_32_Massimo=" not in text:
        text = text.replace("Var_32_Minimo=3\n", "Var_32_Minimo=3\nVar_32_Massimo=20\n")
    text = re.sub(r"(Var_32_Massimo=).*", r"\g<1>20", text, count=1)
    text = re.sub(r"(Var_32_RFS=).*", r"\1True", text, count=1)

    text = text.replace("FONDO SCALA BAR", "FS bar")
    # keep language-1 copies in sync (replace already hits both)

    text = _move_setup_tabs(text)

    for pag, navy_palette, next_oid in (
            (3, False, 27),
            (4, False, 29),
            (5, False, 25),
            (10, True, 27),
            (11, True, 29),
            (12, True, 25),
        ):
            dest = 13 if navy_palette else 6
            idle_bg = NAV_D if navy_palette else BLUE_L
            marker = f"\n[Pagina_{pag + 1}]" if pag != 12 else "\n[Allarme_0]"
            if pag == 4:
                marker = "\n[Pagina_5]"
            if pag == 5:
                marker = "\n[Pagina_6]"
            if pag == 10:
                marker = "\n[Pagina_11]"
            if pag == 11:
                marker = "\n[Pagina_12]"
            blob = make_text(
                pag, next_oid, 236, 0, 48, 16, "TOT", WHITE, idle_bg, xlang=242, ylang=4
            ) + make_key(
                pag, next_oid + 1, 236, 0, 48, 24, "KEY.TOT", "MAC_PAGE", dest, WHITE, idle_bg
            )
            key = f"Pag_{pag}_Obj_{next_oid}_IdObj={next_oid}"
            if key not in text:
                text = _insert_before(text, marker, blob)

    for pag, navy_palette in ((3, False), (10, True)):
        if f"Pag_{pag}_Obj_29_IdObj=29" in text:
            continue
        idle_bg = NAV_D if navy_palette else BLUE_L
        marker = "\n[Pagina_4]" if pag == 3 else "\n[Pagina_11]"
        blob = make_text(
            pag,
            29,
            12,
            184,
            168,
            16,
            "CARICA DEFAULT",
            WHITE,
            idle_bg,
            xlang=18,
            ylang=188,
        ) + make_key(
            pag, 30, 12, 180, 168, 24, "KEY.DEF", "MAC_SETFLG", 253, WHITE, idle_bg, code=43, resflg=True
        )
        text = _insert_before(text, marker, blob)

    for pag, navy_palette, oid in ((5, False, 23), (12, True, 23)):
        if f"Pag_{pag}_Obj_{oid}_IdObj={oid}" in text:
            continue
        lab_fg = WHITE if navy_palette else BLACK
        lab_bg = BG_D if navy_palette else BG_L
        wfg = WHITE if navy_palette else BLACK
        wbg = BG_D if navy_palette else WHITE
        wbox = BOX_D if navy_palette else RED
        marker = "\n[Pagina_6]" if pag == 5 else "\n[Allarme_0]"
        tot = f"Pag_{pag}_Obj_25_IdObj=25"
        blob = make_text(
            pag, oid, 12, 128, 204, 16, "TIMEOUT MIN", lab_fg, lab_bg
        ) + make_word(pag, oid + 1, 240, 124, 54, wfg, wbg, wbox, w=72)
        if tot in text:
            i = text.find(tot)
            text = text[:i] + blob + text[i:]
        else:
            text = _insert_before(text, marker, blob)

    text = _replace_section(text, "[Pagina_6]", "[Pagina_7]", make_contat_page(6, False))
    if "[Pagina_13]" in text:
        text = _replace_section(text, "[Pagina_13]", "[Allarme_0]", make_contat_page(13, True) + "\n")
    else:
        text = _insert_before(text, "[Allarme_0]", make_contat_page(13, True) + "\n")

    text = _replace_section(text, "[Allarme_6]", "[Allarme_7]", make_alarm(6, "STALLO FILL"))
    text = _replace_section(text, "[Allarme_7]", "[Allarme_8]", make_alarm(7, "STALLO TRAVASO"))

    if "[Variabile_54]" not in text:
        vars_blob = (
            make_var(
                54,
                "TIMEOUT MIN",
                "STALLO MIN 0=OFF",
                "DATA.4116",
                intere="2",
                mn="0",
                mx="60",
                ena="True",
                rfs="True",
            )
            + make_var(
                55,
                "TOT OSMOSI",
                "LITRI OSMOSI",
                "DATA.4120",
                dim="LONG_WIDE",
                intere="7",
                mn="0",
                mx="9999999",
            )
            + make_var(
                56,
                "TOT RETE",
                "LITRI RETE",
                "DATA.4122",
                dim="LONG_WIDE",
                intere="7",
                mn="0",
                mx="9999999",
            )
            + make_var(
                57,
                "TOT TRAVASO",
                "LITRI TRAVASO",
                "DATA.4124",
                dim="LONG_WIDE",
                intere="7",
                mn="0",
                mx="9999999",
            )
        )
        text = _insert_before(text, "[Lista Immagini]", vars_blob + "\n")

    refill_l, refill_d = 14, 15
    dur_vid = 58
    if f"[Pagina_{refill_l}]" not in text:
        blob = (
            make_refill_page(refill_l, False, refill_d, 1, dur_vid)
            + "\n"
            + make_refill_page(refill_d, True, refill_l, 8, dur_vid)
            + "\n"
        )
        text = _insert_before(text, "[Allarme_0]", blob)

    warn_l, warn_d = 16, 17
    if f"[Pagina_{warn_l}]" not in text:
        blob = (
            make_warn_vuoto_page(warn_l, False, warn_d)
            + "\n"
            + make_warn_vuoto_page(warn_d, True, warn_l)
            + "\n"
        )
        text = _insert_before(text, "[Allarme_0]", blob)

    if f"[Variabile_{dur_vid}]" not in text:
        text = _insert_before(
            text,
            "[Lista Immagini]",
            make_var(
                dur_vid,
                "DUR PRESENTE",
                "DUREZZA ACQUA IN TINO F",
                "DATA.2058",
                intere="2",
                dec="1",
                mn="0",
                mx="500",
                ena="True",
                rfs="True",
            )
            + "\n",
        )

    text = text.replace(
        "Pag_1_Obj_2_KeyTouch_0_PaginaDATA_P=200",
        "Pag_1_Obj_2_KeyTouch_0_PaginaDATA_P=238",
    )
    text = text.replace(
        "Pag_8_Obj_2_KeyTouch_0_PaginaDATA_P=200",
        "Pag_8_Obj_2_KeyTouch_0_PaginaDATA_P=238",
    )

    if "Pag_0_Obj_29_IdObj=29" not in text:
        idle = BLUE_L
        blob = (
            make_text(0, 29, 168, 4, 48, 16, "RESET", WHITE, idle)
            + make_key(0, 30, 164, 0, 56, 24, "KEY.RST", "MAC_SETFLG", 0, WHITE, idle, code=42)
        )
        text = text.replace("\n[Pagina_1]", "\n" + blob + "\n[Pagina_1]")
    if "Pag_7_Obj_29_IdObj=29" not in text:
        idle = NAV_D
        blob = (
            make_text(7, 29, 168, 4, 48, 16, "RESET", WHITE, idle)
            + make_key(7, 30, 164, 0, 56, 24, "KEY.RST", "MAC_SETFLG", 0, WHITE, idle, code=42)
        )
        text = text.replace("\n[Pagina_8]", "\n" + blob + "\n[Pagina_8]")

    text = _fix_home_man_rows(text)
    text = _fix_fill_valve_taps(text)
    text = _restyle_hmi(text)
    return text
