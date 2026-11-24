"""lpk-tp320 — preview HMI per code agent: .lpk LogicPaint → canvas TP 320.

L'agente scrive il .lpk; questo tool mostra le pagine (320x240); LogicPaint
resta per Compila/Invio. Non emula ladder ne' allarmi.
"""
from __future__ import annotations

import argparse
import json
import webbrowser
from pathlib import Path

from PIL import Image, ImageDraw

__version__ = "0.1.0"

HERE = Path(__file__).resolve().parent
W, H = 320, 240
GRID_X, GRID_Y = 6, 8


def _rows(ch: str) -> list[int]:
    # hand bitmaps 7 rows, 5 bits
    table = {
        " ": [0, 0, 0, 0, 0, 0, 0],
        "0": [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
        "1": [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
        "2": [0x0E, 0x11, 0x02, 0x04, 0x08, 0x10, 0x1F],
        "3": [0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E],
        "4": [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
        "5": [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
        "6": [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
        "7": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
        "8": [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
        "9": [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],
        "A": [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
        "B": [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
        "C": [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
        "D": [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E],
        "E": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
        "F": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
        "G": [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0E],
        "H": [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
        "I": [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
        "J": [0x01, 0x01, 0x01, 0x01, 0x11, 0x11, 0x0E],
        "K": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
        "L": [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
        "M": [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
        "N": [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
        "O": [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
        "P": [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
        "Q": [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
        "R": [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
        "S": [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
        "T": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
        "U": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
        "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
        "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
        "X": [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
        "Y": [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
        "Z": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
        "-": [0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00],
        ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04],
        "/": [0x01, 0x02, 0x04, 0x04, 0x08, 0x10, 0x10],
        ":": [0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00],
        "%": [0x19, 0x1A, 0x04, 0x08, 0x13, 0x03, 0x00],
        "!": [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
        "*": [0x00, 0x15, 0x0E, 0x1F, 0x0E, 0x15, 0x00],
        "+": [0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00],
        "'": [0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00],
        "(": [0x04, 0x08, 0x10, 0x10, 0x10, 0x08, 0x04],
        ")": [0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08],
        "_": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F],
        ",": [0x00, 0x00, 0x00, 0x00, 0x04, 0x04, 0x08],
        "=": [0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00],
        "°": [0x0E, 0x11, 0x11, 0x0E, 0x00, 0x00, 0x00],
        "ß": [0x0E, 0x11, 0x11, 0x0E, 0x00, 0x00, 0x00],
        "h": [0x10, 0x10, 0x1E, 0x11, 0x11, 0x11, 0x11],
        "i": [0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E],
        "n": [0x00, 0x00, 0x1E, 0x11, 0x11, 0x11, 0x11],
        "m": [0x00, 0x00, 0x1B, 0x15, 0x15, 0x11, 0x11],
    }
    return table.get(ch, [0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F])


def argb(n) -> tuple[int, int, int]:
    v = int(n)
    if v < 0:
        v += 2**32
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255)


def g(obj: dict, key: str, default: str = "") -> str:
    return obj.get(key, default)


def gi(obj: dict, key: str, default: int = 0) -> int:
    try:
        return int(g(obj, key, str(default)))
    except ValueError:
        return default


def gb(obj: dict, key: str) -> bool:
    return g(obj, key, "False") == "True"


def parse_lpk(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    pages: dict[int, dict] = {}
    variables: dict[int, dict] = {}
    images: dict[int, Image.Image] = {}

    cur_page = None
    cur_obj = None
    cur_var = None
    var_id = None

    for raw in text.splitlines():
        line = raw.rstrip("\r")
        if line.startswith("[Pagina_"):
            cur_page = int(line[8:-1])
            pages[cur_page] = {
                "id": cur_page,
                "name": f"Pag.{cur_page}",
                "bg": "-4144960",
                "grid": "-1",
                "objects": [],
            }
            cur_obj = None
            cur_var = None
            continue
        if line.startswith("[Variabile_"):
            var_id = int(line[11:-1])
            variables[var_id] = {"id": var_id}
            cur_var = variables[var_id]
            cur_page = None
            cur_obj = None
            continue
        if line.startswith("[Lista Immagini]"):
            cur_page = cur_obj = cur_var = None
            continue
        if line.startswith("[") and line.endswith("]"):
            cur_page = cur_obj = cur_var = None
            continue

        if cur_page is not None and line.startswith(f"Pag_{cur_page}_"):
            rest = line[len(f"Pag_{cur_page}_") :]
            if rest.startswith("Obj_"):
                idx_s, _, kv = rest[4:].partition("_")
                key, _, val = kv.partition("=")
                idx = int(idx_s)
                objs = pages[cur_page]["objects"]
                while len(objs) <= idx:
                    objs.append({"idx": len(objs), "_pairs": []})
                cur_obj = objs[idx]
                cur_obj["_pairs"].append((key, val))
                if not key.startswith("ObjText."):
                    cur_obj[key] = val
            else:
                key, _, val = rest.partition("=")
                if key == "NomePagina":
                    pages[cur_page]["name"] = val
                elif key == "ColoreSfondo":
                    pages[cur_page]["bg"] = val
                elif key == "ColoreGriglia":
                    pages[cur_page]["grid"] = val
            continue

        if cur_var is not None and var_id is not None and line.startswith(f"Var_{var_id}_"):
            key, _, val = line[len(f"Var_{var_id}_") :].partition("=")
            cur_var[key] = val
            continue

        if line.startswith("ImgGrafica_"):
            k, _, val = line.partition("=")
            idx = int(k.split("_")[1])
            images[idx] = decode_img(val)

    # attach lang text onto objects
    for page in pages.values():
        for obj in page["objects"]:
            texts = {"0": "", "1": ""}
            xy = {"0": (None, None), "1": (None, None)}
            for k, v in obj.get("_pairs", []):
                if k == "ObjText.Testo" and ":" in v:
                    lang_id, t = v.split(":", 1)
                    texts[lang_id] = t
                elif k == "ObjText.X_Lang" and ":" in v:
                    lang_id, t = v.split(":", 1)
                    xy[lang_id] = (t, xy[lang_id][1])
                elif k == "ObjText.Y_Lang" and ":" in v:
                    lang_id, t = v.split(":", 1)
                    xy[lang_id] = (xy[lang_id][0], t)
            obj["text0"] = texts.get("0", "")
            obj["tx"] = int(xy["0"][0]) if xy["0"][0] else gi(obj, "X")
            obj["ty"] = int(xy["0"][1]) if xy["0"][1] else gi(obj, "Y")

    return {"pages": pages, "variables": variables, "images": images}


def decode_img(body: str) -> Image.Image:
    w = int(body[0:5])
    h = int(body[5:10])
    hexpx = body[10:]
    im = Image.new("RGB", (w, h), (0, 0, 0))
    px = im.load()
    i = 0
    for y in range(h):
        for x in range(w):
            chunk = hexpx[i : i + 6]
            i += 6
            if len(chunk) < 6:
                break
            r = int(chunk[0:2], 16)
            g = int(chunk[2:4], 16)
            b = int(chunk[4:6], 16)
            px[x, y] = (r, g, b)
    return im


def font_scale(dim: str) -> int:
    d = (dim or "D22").upper()
    if d.startswith("D33") or d.startswith("D3"):
        return 3
    if d.startswith("D11") or d.startswith("D1"):
        return 1
    return 2


def put_glyph(px, ox, oy, rows, color, scale, clip):
    cw, ch, x0, y0, x1, y1 = clip
    for ry, bits in enumerate(rows):
        for rx in range(5):
            if bits & (1 << (4 - rx)):
                for dy in range(scale):
                    for dx in range(scale):
                        x = ox + rx * scale + dx
                        y = oy + ry * scale + dy
                        if x0 <= x < x1 and y0 <= y < y1:
                            px[x, y] = color


def draw_text(im, x, y, text, color, dim="D22", clip=None):
    px = im.load()
    scale = font_scale(dim)
    cell_w, cell_h = 6 * scale, 8 * scale
    if clip is None:
        clip = (W, H, 0, 0, W, H)
    else:
        x0, y0, w, h = clip
        clip = (w, h, x0, y0, x0 + w, y0 + h)
    cx = x
    text = text.replace("ß", "°")
    for ch in text:
        put_glyph(px, cx, y, _rows(ch), color, scale, clip)
        cx += cell_w
    return cx


def draw_hearts(im, x, y, n, color, dim, clip):
    """Placeholder cifre LogicPaint (cuoricini / V)."""
    scale = font_scale(dim)
    heart = [0x0A, 0x1F, 0x1F, 0x0E, 0x04, 0x00, 0x00]
    px = im.load()
    x0, y0, w, h = clip
    c = (w, h, x0, y0, x0 + w, y0 + h)
    cx = x
    for _ in range(max(n, 0)):
        put_glyph(px, cx, y, heart, color, scale, c)
        cx += 6 * scale


def hatch(im, x, y, w, h, color):
    """Retino KEY dell'editor: diagonali 45°, una ogni 6 px (il testo sotto resta leggibile)."""
    if w <= 0 or h <= 0:
        return
    px = im.load()
    for yy in range(max(0, y), min(H, y + h)):
        for xx in range(max(0, x), min(W, x + w)):
            if (xx - yy) % 6 == 0:
                px[xx, yy] = color


def box(draw: ImageDraw.ImageDraw, x, y, w, h, color):
    if w <= 0 or h <= 0:
        return
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=color)


def fill(draw: ImageDraw.ImageDraw, x, y, w, h, color):
    if w <= 0 or h <= 0:
        return
    draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)


def draw_h_stripes(im, x, y, w, h, fg, bg, vertical: bool):
    """Barra editor: riempimento Fore + scanline sottili (non bande spesse)."""
    draw = ImageDraw.Draw(im)
    fill(draw, x, y, w, h, fg)
    if vertical:
        xx = x
        while xx < x + w:
            fill(draw, xx, y, 1, h, bg)
            xx += 4
    else:
        yy = y
        while yy < y + h:
            fill(draw, x, yy, w, 1, bg)
            yy += 4


def key_fills_back(obj: dict) -> bool:
    """Heuristic editor: nav in basso e tasti SET/RES riempiono il BackColor.
    KEY 24×24 sopra un'immagine (tema luna/sole) restano solo retino."""
    if g(obj, "Tipo") != "17":
        return False
    y, w, h = gi(obj, "Y"), gi(obj, "Width"), gi(obj, "Height")
    if y + h >= H - 8 and w >= 70:
        return True
    macro = g(obj, "KeyTouch_0_Macro_P")
    return macro in ("MAC_SETFLG", "MAC_RESFLG") and w >= 60


def hatch_color(obj: dict) -> tuple[int, int, int]:
    # Tab gialla: retino nero (come LogicPaint). Altri KEY: ForeColor.
    if g(obj, "BackColor") == "-256":
        return (0, 0, 0)
    return argb(g(obj, "ForeColor", "-1"))


def addr_label(var: dict | None) -> str:
    if not var:
        return ""
    return var.get("IndirizzoVar", "") or ""


def addr_short(var: dict | None) -> str:
    a = addr_label(var)
    if a.startswith("DATA."):
        return a[5:]
    return a


def digits_of(var: dict | None) -> int:
    if not var:
        return 4
    raw = (var.get("CifreIntere") or "").strip()
    if not raw:
        return 4
    try:
        return int(raw)
    except ValueError:
        return 4


def render_page(data: dict, page_id: int) -> tuple[Image.Image, list]:
    page = data["pages"][page_id]
    vars_ = data["variables"]
    images = data["images"]
    im = Image.new("RGB", (W, H), argb(page["bg"]))
    draw = ImageDraw.Draw(im)
    page_bg = argb(page["bg"])

    # 1) riempi i KEY "solidi" (nav / AVVIA / STOP) PRIMA del testo
    for obj in page["objects"]:
        if not key_fills_back(obj):
            continue
        x, y = gi(obj, "X"), gi(obj, "Y")
        w, h = gi(obj, "Width"), gi(obj, "Height")
        fill(draw, x, y, w, h, argb(g(obj, "BackColor", "-16776961")))

    hits = []
    keys = []
    for obj in page["objects"]:
        tipo = g(obj, "Tipo")
        x, y = gi(obj, "X"), gi(obj, "Y")
        w, h = gi(obj, "Width"), gi(obj, "Height")
        if w <= 0 or h <= 0:
            continue
        fg = argb(g(obj, "ForeColor", "-1"))
        bg = argb(g(obj, "BackColor", "-16777216"))
        bx = argb(g(obj, "BoxColor", "-65536"))
        idvar = gi(obj, "IdVar")
        var = vars_.get(idvar)

        if tipo == "17":
            keys.append(obj)
            hits.append(
                {
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "macro": g(obj, "KeyTouch_0_Macro_P"),
                    "dest": g(obj, "KeyTouch_0_PaginaDATA_P"),
                }
            )
            continue

        if tipo == "2":
            fill(draw, x, y, w, h, bg)
            if gb(obj, "BOX"):
                box(draw, x, y, w, h, bx)
            tx, ty = obj.get("tx", x), obj.get("ty", y)
            dim = g(obj, "DimCarattere", "D22") or "D22"
            draw_text(im, tx, ty, obj.get("text0", ""), fg, dim, clip=(x, y, w, h))

        elif tipo == "3":
            draw.line([x, y, w, h], fill=fg, width=max(1, gi(obj, "Spessore", 1)))

        elif tipo == "11":
            fill(draw, x, y, w, h, bg)
            if gb(obj, "BOX"):
                box(draw, x, y, w, h, bx)
            lab = addr_label(var)
            draw_text(im, x + 2, y + 1, lab, fg, "D11", clip=(x, y, w, h))
            dim = g(obj, "DimCarattere", "D22") or "D22"
            if dim == "D11":
                dim = g(obj, "Grandezza", "D22") or "D22"
            gy = y + (10 if h >= 28 else 8)
            if gy + 8 * font_scale(dim) > y + h:
                gy = y + max(1, h - 8 * font_scale(dim) - 1)
            draw_hearts(im, x + 4, gy, digits_of(var), fg, dim, clip=(x, y, w, h))

        elif tipo == "12":
            src = images.get(idvar)
            if src is not None:
                im.paste(src.resize((w, h), Image.NEAREST) if src.size != (w, h) else src, (x, y))

        elif tipo == "14":
            if w <= 28 and h <= 28:
                fill(draw, x, y, w, h, fg)
                bar_w = max(2, (w - 6) // 4)
                for i in range(4):
                    bx0 = x + 2 + i * (bar_w + 1)
                    fill(draw, bx0, y + 10, bar_w, h - 12, bg)
                if gb(obj, "BOX"):
                    box(draw, x, y, w, h, bx)
                # overlay indirizzo: chiaro su rosso, scuro su lime
                lab_c = (255, 255, 255) if fg[0] > 200 else (0, 0, 0)
                draw_text(im, x + 1, y + 1, addr_short(var), lab_c, "D11", clip=(x, y, w, h))
            else:
                draw_h_stripes(im, x, y, w, h, fg, bg, vertical=True)
                if gb(obj, "BOX"):
                    box(draw, x, y, w, h, bx)
                draw_text(im, x + 2, y + 1, addr_label(var), (255, 255, 255), "D11", clip=(x, y, w, h))

        elif tipo == "15":
            draw_h_stripes(im, x, y, w, h, fg, bg, vertical=False)
            if gb(obj, "BOX"):
                box(draw, x, y, w, h, bx)
            draw_text(im, x + 2, y + 2, addr_label(var), (255, 255, 255), "D11", clip=(x, y, w, h))

        elif tipo == "16":
            fill(draw, x, y, w, h, bg)
            box(draw, x, y, w, h, bx)

    for obj in keys:
        x, y = gi(obj, "X"), gi(obj, "Y")
        w, h = gi(obj, "Width"), gi(obj, "Height")
        hatch(im, x, y, w, h, hatch_color(obj))

    return im, hits, page_bg, argb(page["grid"])


HTML = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>TP 320 preview</title>
<style>
  body { font-family: Segoe UI, sans-serif; background:#1a1a1a; color:#ddd; margin:16px; }
  h1 { font-size:16px; font-weight:600; }
  .row { display:flex; gap:16px; flex-wrap:wrap; align-items:flex-start; }
  #wrap { image-rendering: pixelated; border:1px solid #444; }
  #screen { width:640px; height:480px; display:block; cursor:crosshair; }
  nav button { margin:0 4px 8px 0; padding:6px 10px; background:#333; color:#eee;
    border:1px solid #555; cursor:pointer; }
  nav button.on { background:#c90; color:#111; border-color:#fc0; }
  #meta { font-size:12px; color:#aaa; margin-top:8px; }
</style>
</head>
<body>
<h1>lpk-tp320 — LogicPaint .lpk → TP 320 (320×240 ×2)</h1>
<nav id="nav"></nav>
<div class="row">
  <div id="wrap"><img id="screen" alt="pagina"></div>
</div>
<div id="meta"></div>
<script>
const PAGES = __PAGES__;
const HITS = __HITS__;
let cur = PAGES.includes(0) ? 0 : PAGES[0];
const nav = document.getElementById('nav');
const img = document.getElementById('screen');
const meta = document.getElementById('meta');
const names = __NAMES__;
function show(id) {
  cur = id;
  img.src = 'pag_' + id + '.png';
  meta.textContent = 'Pag.' + id + '  ' + (names[id] || '') + '  — click sui tasti MAC_PAGE';
  [...nav.children].forEach(b => b.classList.toggle('on', +b.dataset.id === id));
}
PAGES.forEach(id => {
  const b = document.createElement('button');
  b.dataset.id = id;
  b.textContent = (names[id] || ('Pag.'+id));
  b.onclick = () => show(id);
  nav.appendChild(b);
});
img.addEventListener('click', ev => {
  const r = img.getBoundingClientRect();
  const x = Math.floor((ev.clientX - r.left) * 320 / r.width);
  const y = Math.floor((ev.clientY - r.top) * 240 / r.height);
  const list = (HITS[cur] || []).slice().reverse();
  for (const h of list) {
    if (x>=h.x && y>=h.y && x<h.x+h.w && y<h.y+h.h && h.macro === 'MAC_PAGE') {
      const dest = parseInt(h.dest, 10);
      if (PAGES.includes(dest)) show(dest);
      return;
    }
  }
});
show(cur);
</script>
</body>
</html>
"""


def default_lpk() -> Path | None:
    """Se il tool vive ancora nel repo H20, usa il .lpk di lavoro."""
    candidate = HERE.parents[1] / "Proj" / "Tino_H20.lpk"
    return candidate if candidate.is_file() else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="lpk-tp320",
        description="Anteprima editor-like di un .lpk LogicPaint su canvas TP 320 (320x240).",
    )
    ap.add_argument(
        "lpk",
        nargs="?",
        type=Path,
        help="File .lpk (testo). Se omesso, cerca Proj/Tino_H20.lpk nel repo ospite.",
    )
    ap.add_argument(
        "-o",
        "--out",
        type=Path,
        default=HERE / "out",
        help="Cartella PNG + index.html (default: ./out)",
    )
    ap.add_argument(
        "--scale",
        type=int,
        default=2,
        metavar="N",
        help="Fattore di scala dei PNG (default: 2 = 640x480)",
    )
    ap.add_argument("--open", action="store_true", help="Apri index.html nel browser")
    ap.add_argument("--version", action="version", version=f"lpk-tp320 {__version__}")
    args = ap.parse_args(argv)

    lpk = args.lpk or default_lpk()
    if lpk is None or not lpk.is_file():
        ap.error("specifica un file .lpk (es. lpk-tp320 mio_progetto.lpk)")
    lpk = lpk.resolve()
    out = args.out
    scale = max(1, args.scale)

    print(f"lpk-tp320 {__version__}")
    print("parse", lpk)
    data = parse_lpk(lpk)
    out.mkdir(parents=True, exist_ok=True)
    hits_all = {}
    names = {}
    ids = sorted(data["pages"])
    if not ids:
        raise SystemExit("nessuna [Pagina_N] nel file")
    for pid in ids:
        im, hits, _page_bg, grid_c = render_page(data, pid)
        big = im.resize((W * scale, H * scale), Image.NEAREST)
        gpx = big.load()
        for yy in range(0, H * scale, GRID_Y * scale):
            for xx in range(0, W * scale, GRID_X * scale):
                gpx[xx, yy] = grid_c
        dest = out / f"pag_{pid}.png"
        big.save(dest)
        hits_all[str(pid)] = hits
        names[str(pid)] = data["pages"][pid]["name"]
        nobj = len(data["pages"][pid]["objects"])
        print(f"  Pag.{pid} {names[str(pid)]!r} objects={nobj} -> {dest.name}")
    html = (
        HTML.replace("__PAGES__", json.dumps(ids))
        .replace("__HITS__", json.dumps(hits_all))
        .replace("__NAMES__", json.dumps(names))
    )
    index = out / "index.html"
    index.write_text(html, encoding="utf-8")
    print("wrote", index)
    if args.open:
        webbrowser.open(index.as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
