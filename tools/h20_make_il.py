# -*- coding: utf-8 -*-
"""Manutenzione IL AWL: il sorgente canonico è tools/h20_awl_il.txt (H20 v1.00)."""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "h20_awl_il.txt"


def main() -> None:
    out = HERE / "h20_awl_il.txt"
    if not out.is_file():
        raise SystemExit(f"manca {out}")
    print(
        "OK",
        out,
        "lines",
        len(out.read_text(encoding="utf-8").splitlines()),
        "(nessuna rigenerazione automatica)",
    )


if __name__ == "__main__":
    main()