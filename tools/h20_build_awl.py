# -*- coding: utf-8 -*-
"""Build Proj/Tino_H20_AWL.lpk from ladder Tino_H20.lpk (H20 v1.00).

Keep Term_Ena_ANA=False. In LogicPaint: aprire solo il file AWL, Compila, Trasmetti.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SRC = ROOT / "Proj" / "Tino_H20.lpk"
DST = ROOT / "Proj" / "Tino_H20_AWL.lpk"
IL_PATH = HERE / "h20_awl_il.txt"

SECTION_RE = re.compile(r"^\[([^\]]+)\]\s*$", re.M)
INSTR_RE = re.compile(r"^(?P<indent>\s*)(?P<hash>#)?(?P<op>[A-Z]+)(?P<rest>.*)$")
BIT_OPS = {
    "BSET", "BCLR", "BRES", "BOUT", "BOUTN", "BNOT",
    "BLD", "BLDN", "BOR", "BAND", "BORN", "BANDN", "BXOR", "BXORN",
}


def _hash_bit_operand(rest: str) -> str:
    """plc_comp matches BSET/BOUT only as '#n,DATA.xx' or 'DATA,DATA'."""
    if "," not in rest:
        return rest
    bit, addr = [p.strip() for p in rest.split(",", 1)]
    if bit.isdigit():
        bit = f"#{bit}"
    return f"{bit},{addr}"


def normalize_il(text: str) -> str:
    """plc_comp 1.45: #OP is not an opcode. Forced math needs LD SYS.01.
    Bit ops need # on the bit number (BOUT #0,DATA.08), never #BOUT.
    """
    out: list[str] = []
    have_sys01 = False
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(";"):
            out.append(line)
            have_sys01 = False
            continue
        m = INSTR_RE.match(line)
        if not m:
            out.append(line)
            have_sys01 = False
            continue
        indent = m.group("indent") or "\t"
        forced = bool(m.group("hash"))
        op = m.group("op")
        rest = m.group("rest").strip()

        if op in BIT_OPS:
            rest = _hash_bit_operand(rest)

        if op in ("LD", "LDNOT") and not forced:
            have_sys01 = rest == "SYS.01" and op == "LD"
            pad = max(1, 6 - len(op))
            out.append(f"{indent}{op}{' ' * pad}{rest}")
            continue

        if forced:
            if not have_sys01:
                out.append(f"{indent}LD    SYS.01")
                have_sys01 = True
            pad = max(1, 6 - len(op))
            out.append(f"{indent}{op}{' ' * pad}{rest}")
            continue

        have_sys01 = False
        pad = max(1, 6 - len(op))
        out.append(f"{indent}{op}{' ' * pad}{rest}")
    return "\n".join(out) + "\n"

H20_SYMS = [
    ("DATA.1000", "LIVELLO REAL"),
    ("DATA.1200", "SCRATCH L0"),
    ("DATA.1220", "PROM A"),
    ("DATA.1222", "PROM B"),
    ("DATA.2000", "AREA TANK"),
    ("DATA.2001", "ALTEZZA TANK"),
    ("DATA.2002", "LIVELLO MAX"),
    ("DATA.2003", "LIVELLO MINI"),
    ("DATA.2004", "LT TARGET"),
    ("DATA.2005", "DUR TARGET"),
    ("DATA.2006", "LT TRAVASO"),
    ("DATA.2007", "LT FILTRATO"),
    ("DATA.2008", "VO OSMOSI"),
    ("DATA.2009", "VN RETE"),
    ("DATA.2010", "ALLARME LIV"),
    ("DATA.2011", "CIRC CM"),
    ("DATA.2012", "LT TOT"),
    ("DATA.2013", "OFFSET L"),
    ("DATA.2014", "DUR RETE"),
    ("DATA.2015", "TOLL MIX"),
    ("DATA.2016", "SMORZ SEC"),
    ("DATA.2017", "FS BAR"),
    ("DATA.2018", "LTH RETE"),
    ("DATA.2019", "LTH OSMOSI"),
    ("DATA.2020", "MAN MODE"),
    ("DATA.2021", "LTH TRAVASO"),
    ("DATA.2022", "T STAB"),
    ("DATA.2023", "PCT LIV"),
    ("DATA.2024", "ETA MIN"),
    ("DATA.2025", "FLOW LH"),
    ("DATA.2026", "CALO TRAVASO"),
    ("DATA.2027", "APPOGGIO"),
    ("DATA.2028", "LIV GREZZO"),
    ("DATA.2029", "ZERO 4mA"),
    ("DATA.2030", "ZERO"),
    ("DATA.2031", "BAR OSM"),
    ("DATA.2032", "BAR RETE"),
    ("DATA.2033", "BANDA MORTA"),
    ("DATA.2034", "CAMPIONAMENT"),
    ("DATA.2035", "LIV PREC"),
    ("DATA.2036", "CAMP CNT"),
    ("DATA.2037", "STAB CNT"),
    ("DATA.2040", "LED POMPA"),
    ("DATA.2041", "LED RETE"),
    ("DATA.2042", "LED OSMOSI"),
    ("DATA.2043", "LED EV"),
    ("DATA.2050", "TRAV REST"),
    ("DATA.2051", "VO TOLL"),
    ("DATA.2052", "FLOW DLT"),
    ("DATA.2053", "DEAD LIV"),
    ("DATA.2054", "ETA REST"),
    ("DATA.2055", "ADC DLT"),
    ("DATA.2056", "T FILT M1"),
    ("DATA.4100", "CIRC CM EE"),
    ("DATA.4101", "LT TOT EE"),
    ("DATA.4102", "OFFSET EE"),
    ("DATA.4103", "ALLARME EE"),
    ("DATA.4104", "DUR RETE EE"),
    ("DATA.4105", "TOLL MIX EE"),
    ("DATA.4106", "SMORZ SEC EE"),
    ("DATA.4107", "FS BAR EE"),
    ("DATA.4108", "LTH RETE EE"),
    ("DATA.4109", "LTH OSM EE"),
    ("DATA.4110", "LTH TRAV EE"),
    ("DATA.4111", "T STAB EE"),
    ("DATA.4112", "LT TRAVASO EE"),
    ("DATA.4113", "ZERO 4mA EE"),
    ("DATA.4114", "BANDA MORTA EE"),
    ("DATA.4115", "CAMP SEC EE"),
    ("DATA.4116", "TIMEOUT MIN"),
    ("FLAG.00", "RESET EMERG"),
    ("FLAG.01", "EMERGENZA OK"),
    ("FLAG.200", "FILL RUN"),
    ("FLAG.201", "STEP1 OSM"),
    ("FLAG.202", "STEP2 RETE"),
    ("FLAG.203", "TRAVASO RUN"),
    ("FLAG.204", "MAN MODE"),
    ("FLAG.205", "MAN OSM"),
    ("FLAG.206", "MAN RETE"),
    ("FLAG.207", "MAN POMPA"),
    ("FLAG.208", "FILL STAB"),
    ("FLAG.209", "MAN PREV"),
    ("FLAG.210", "ALR TARGET"),
    ("FLAG.211", "ALR PIENO"),
    ("FLAG.212", "ALR VUOTO"),
    ("FLAG.213", "FLOW PRIMED"),
    ("FLAG.214", "TMP A"),
    ("FLAG.215", "HN ZERO"),
    ("FLAG.216", "HT GT HN"),
    ("FLAG.217", "MIX NORM"),
    ("FLAG.218", "STEP DONE"),
    ("FLAG.219", "STAB DONE"),
    ("FLAG.220", "SAVE EEPROM"),
    ("FLAG.221", "EE VIRGIN"),
    ("FLAG.222", "TRAV SNAP"),
    ("FLAG.223", "TRAV DONE"),
    ("FLAG.224", "FLOW TICK"),
    ("FLAG.225", "DEAD PT"),
    ("FLAG.226", "FLOW OK"),
    ("FLAG.227", "TRAV LIV OK"),
    ("FLAG.228", "STALLO FILL"),
    ("FLAG.229", "STALLO TRAV"),
    ("FLAG.230", "REQ POMPA"),
    ("FLAG.231", "REQ RETE"),
    ("FLAG.232", "REQ OSM"),
    ("FLAG.233", "REQ EV"),
    ("FLAG.234", "TRAV CODA"),
    ("FLAG.235", "AZZ OSM"),
    ("FLAG.236", "AZZ RETE"),
        ("FLAG.237", "AZZ TRAV"),
        ("FLAG.238", "FILL REQ"),
        ("FLAG.239", "FILL PREV"),
        ("FLAG.240", "REFILL PEND"),
        ("FLAG.241", "REFILL SI"),
        ("FLAG.242", "REFILL FAIL"),
        ("FLAG.243", "LIV LE OFFSET"),
        ("FLAG.244", "TRAV PREV"),
        ("FLAG.245", "FLOW IN BANDA"),
        ("FLAG.246", "FLOW CODA 0"),
        ("FLAG.247", "STALL ENA"),
        ("FLAG.248", "LIV PROG"),
        ("FLAG.250", "MIX ENA"),
        ("FLAG.251", "LIV VUOTO MIX"),
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
        ("DATA.4120", "TOT OSMOSI"),
        ("DATA.4122", "TOT RETE"),
        ("DATA.4124", "TOT TRAVASO"),
]


def section_spans(text: str) -> list[tuple[str, int, int]]:
    hits = [(m.group(1), m.start()) for m in SECTION_RE.finditer(text)]
    out: list[tuple[str, int, int]] = []
    for i, (name, start) in enumerate(hits):
        end = hits[i + 1][1] if i + 1 < len(hits) else len(text)
        out.append((name, start, end))
    return out


def first_span(text: str, name: str) -> tuple[int, int]:
    for n, start, end in section_spans(text):
        if n == name:
            return start, end
    raise SystemExit(f"sezione [{name}] non trovata")


def slice_until(text: str, start_name: str, end_name: str) -> str:
    start, _ = first_span(text, start_name)
    end, _ = first_span(text, end_name)
    return text[start:end]


def replace_span(text: str, start: int, end: int, new: str) -> str:
    if not new.endswith("\n"):
        new += "\n"
    return text[:start] + new + text[end:]


def replace_section(text: str, name: str, new_body: str) -> str:
    start, end = first_span(text, name)
    return replace_span(text, start, end, new_body)


def wrap_il(il: str) -> str:
    il = il.strip("\n") + "\n"
    return (
        "[Lista Istruzioni]\n"
        "\n"
        "; Area Programma Principale : Iniziare ad inserire da QUI le Istruzioni del programma principale\n"
        "\n"
        f"{il}\n"
        "\tEND\n"
        "\n"
        "\tSBR   INITIALIZE\n"
        "\n"
        "; Subroutine INITIALIZE (eseguita all'avvio) : Aggiungere QUI le ABILITAZIONI e le impostazioni iniziali\n"
        "\n"
        "\tLD    SYS.01\n"
        "\tSET   FLAG.00\n"
        "\n"
        "\tENDSBR\n"
        "\n"
        "; Area Subroutine : Inserire QUI eventuali Subroutine (struttura \"SBR\" ... \"ENDSBR\")\n"
        "\n"
        "\n"
        "[End Lista Istruzioni]\n"
    )


def merge_simbolici(text: str) -> str:
    start, end = first_span(text, "Simbolici")
    body = text[start:end]
    missing = [f"{k}={v}" for k, v in H20_SYMS if f"{k}=" not in body]
    if not missing:
        return text
    if not body.endswith("\n"):
        body += "\n"
    body += "\n".join(missing) + "\n"
    return replace_span(text, start, end, body)


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"manca {SRC}")
    if not DST.is_file():
        raise SystemExit(f"manca template AWL {DST}")
    if not IL_PATH.is_file():
        raise SystemExit(f"manca {IL_PATH}")
    src = SRC.read_text(encoding="utf-8", errors="replace")
    dst = DST.read_text(encoding="utf-8", errors="replace")
    il = normalize_il(IL_PATH.read_text(encoding="utf-8", errors="replace"))
    IL_PATH.write_text(il, encoding="utf-8")

    info = src[slice(*first_span(src, "Info"))]
    info = re.sub(r"(InfoVersione=).*", r"\1H20-v1.00", info, count=1)
    dst = replace_section(dst, "Info", info)

    dbg = src[slice(*first_span(src, "Variabili Debugger"))]
    dst = replace_section(dst, "Variabili Debugger", dbg)

    sim = src[slice(*first_span(src, "Simulatore Ingressi"))]
    dst = replace_section(dst, "Simulatore Ingressi", sim)

    hmi = slice_until(src, "Pagina_0", "Ladder")
    p0, li = first_span(dst, "Pagina_0")
    li_s, _ = first_span(dst, "Lista Istruzioni")
    dst = replace_span(dst, p0, li_s, hmi)

    li_s, li_e = first_span(dst, "Lista Istruzioni")
    end_s, end_e = first_span(dst, "End Lista Istruzioni")
    dst = replace_span(dst, li_s, end_e, wrap_il(il))

    dst = merge_simbolici(dst)

    dst = re.sub(r"(Term_Descrizione=).*", r"\1Tino_H20_AWL", dst, count=1)
    dst = re.sub(r"(Term_Ena_ANA=).*", r"\1False", dst, count=1)

    if re.search(r"^Term_Ena_ANA=True\s*$", dst, re.M):
        raise SystemExit("Term_Ena_ANA=True nel file — abort")
    if "[Ladder]" in dst:
        raise SystemExit("sezione [Ladder] finita nell'AWL — abort")
    if "[Lista Istruzioni]" not in dst:
        raise SystemExit("manca [Lista Istruzioni]")
    if "Pag_0_NomePagina=HOME" not in dst:
        raise SystemExit("HMI HOME non copiata")
    if "SET   SYS.20" not in dst and "SET   SYS.20" not in il:
        pass
    if "SET   SYS.20" not in dst:
        raise SystemExit("IL SYS.20 non inserita")
    if re.search(r"^\s*#[A-Z]+", dst, re.M):
        raise SystemExit("opcode con # prefisso (es. #BOUT) — abort")
    if re.search(r"^\s*(BSET|BCLR|BOUT|BOUTN)\s+[0-9]", dst, re.M):
        raise SystemExit("bit senza #: usare BOUT #0,DATA.08 — abort")

    DST.write_text(dst, encoding="utf-8")
    print("OK", DST, "bytes", DST.stat().st_size, "pagine HOME", dst.count("NomePagina="))


if __name__ == "__main__":
    main()
