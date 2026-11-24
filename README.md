# tp320-osmosi-tino-mix — v1.00

Toolkit / **compilatore assistito** per PLC **Kernel TP 320** (LogicPaint `.lpk`): automazione per **osmosi**, **tino**, **miscelazione** (rete + osmosi, durezza °F, travaso) con generatori Python, corpi **AWL/IL** e anteprima HMI **320×240** (`tools/tp320_preview`).

Il caso d’uso di riferimento è un tino acqua (~2500 L) in birrificio artigianale. I file progetto restano `Proj/Tino_H20.lpk` / `Tino_H20_AWL.lpk` (nome storico del ladder).

> Nato in *vibecoding* con l’AI da **Manuel Piergigli** (non programmatore PLC). Punto di forza: script che **generano e modificano** `.lpk` senza solo “disegnare a mano” in LogicPaint.

**Repository:** [github.com/pierpidc-bot/tp320-osmosi-tino-mix](https://github.com/pierpidc-bot/tp320-osmosi-tino-mix) (release **v1.00**).

```bash
git clone https://github.com/pierpidc-bot/tp320-osmosi-tino-mix.git
cd tp320-osmosi-tino-mix
```

## Prerequisiti

LogicPaint 2.0.5.x e TP 320 (/SCT per 0–20 mA) da [Kernel Sistemi](https://www.kernelsistemi.it/). Python 3.10+ opzionale per i generatori.

## Quick start

1. Apri `Proj/Tino_H20.lpk` in LogicPaint → **Compila** → **Trasmetti**.
2. Compilazione e HMI: [`doc/guide/12_h20.md`](doc/guide/12_h20.md).
3. Generatori (opz.): `pip install -r tools/requirements.txt` poi `python tools/h20_apply_plan.py`, `python tools/h20_build_awl.py`.
4. Anteprima: `python tools/tp320_preview/preview.py Proj/Tino_H20.lpk`.

## Struttura

```
Proj/Tino_H20.lpk       # ladder + HMI v1.00
Proj/Tino_H20_AWL.lpk   # AWL
doc/Tino_H20.md         # specifica impianto
doc/guide/              # guide 03–12
tools/                  # generatori + tp320_preview
```

Non affiliato a Kernel Sistemi — usare a proprio rischio su impianti reali. Licenza MIT — Copyright (c) 2026 Manuel Piergigli.