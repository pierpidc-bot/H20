# -*- coding: utf-8 -*-
"""Genera il manuale PDF d'uso del terminale (HOME + FILL, H20 v1.00)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as RLImage,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "doc" / "manuale"
PDF_PATH = OUT_DIR / "Manuale_uso_terminale.pdf"

S = 4
PW, PH = 320 * S, 240 * S

BG = (0, 0, 0)
TITLE_BG = (0, 102, 200)
NAV = (0, 36, 88)
YELLOW = (255, 255, 0)
CYAN = (193, 245, 255)
WHITE = (255, 255, 255)
LIME = (0, 255, 0)
RED = (255, 0, 0)
BAR = (28, 164, 213)
BAR_BG = (0, 24, 39)
BOX = (0, 102, 200)
BTN = (48, 48, 48)
NAVY_BTN = (0, 36, 88)
PANEL = (28, 30, 34)
BEZEL = (18, 20, 24)

WIN = Path(r"C:\Windows\Fonts")
LINUX_FONTS = (
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
)


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = WIN / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    for alt in LINUX_FONTS:
        if alt.exists():
            return ImageFont.truetype(str(alt), size)
    return ImageFont.load_default()


def F_UI(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return _font("segoeuib.ttf" if bold else "segoeui.ttf", size)


def F_NUM(size: int) -> ImageFont.FreeTypeFont:
    for n in ("consolab.ttf", "consola.ttf", "lucon.ttf"):
        p = WIN / n
        if p.exists():
            return ImageFont.truetype(str(p), size)
    mono = Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
    if mono.exists():
        return ImageFont.truetype(str(mono), size)
    return F_UI(size, True)


def new_screen() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (PW, PH), BG)
    return im, ImageDraw.Draw(im)


def r(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, fill: tuple[int, int, int]) -> None:
    draw.rectangle([x * S, y * S, (x + w) * S - 1, (y + h) * S - 1], fill=fill)


def box(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    draw.rectangle([x * S, y * S, (x + w) * S - 1, (y + h) * S - 1], outline=BOX, width=max(2, S - 1))


def txt(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    fill: tuple[int, int, int],
    size: int = 16,
    bold: bool = True,
    num: bool = False,
) -> None:
    px = max(16, int(round(size * S * 0.88)))
    font = F_NUM(px) if num else F_UI(px, bold)
    draw.text((x * S + S // 2, y * S), text, fill=fill, font=font)


def led(draw: ImageDraw.ImageDraw, x: int, y: int, on: bool) -> None:
    r(draw, x, y, 24, 24, BAR if on else BAR_BG)


def hbar(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, frac: float) -> None:
    r(draw, x, y, w, h, BAR_BG)
    fw = max(0, min(w, int(w * frac)))
    if fw:
        r(draw, x, y, fw, h, BAR)
    box(draw, x, y, w, h)


def vbar(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, frac: float) -> None:
    r(draw, x, y, w, h, BAR_BG)
    fh = max(0, min(h, int(h * frac)))
    if fh:
        r(draw, x, y + h - fh, w, fh, BAR)
    box(draw, x, y, w, h)


def nav(draw: ImageDraw.ImageDraw, active: int) -> None:
    labels = ("HOME", "FILL", "TRAV", "SETUP")
    for i, lab in enumerate(labels):
        x = i * 80
        on = i == active
        r(draw, x, 216, 80, 24, YELLOW if on else NAV)
        tw = 36 if lab != "SETUP" else 42
        txt(draw, x + (80 - tw) // 2, 220, lab, (0, 0, 0) if on else WHITE, 13)


def chrome(im: Image.Image) -> Image.Image:
    pad, bezel = 18, 14
    out = Image.new("RGB", (PW + 2 * (pad + bezel), PH + 2 * (pad + bezel)), PANEL)
    d = ImageDraw.Draw(out)
    ox, oy = pad, pad
    d.rounded_rectangle(
        [ox, oy, ox + PW + 2 * bezel - 1, oy + PH + 2 * bezel - 1],
        radius=10,
        fill=BEZEL,
    )
    out.paste(im, (ox + bezel, oy + bezel))
    d.rounded_rectangle(
        [ox + bezel - 2, oy + bezel - 2, ox + bezel + PW + 1, oy + bezel + PH + 1],
        radius=2,
        outline=(80, 88, 98),
        width=2,
    )
    return out


def draw_home() -> Image.Image:
    im, d = new_screen()
    r(d, 12, 4, 48, 16, TITLE_BG)
    txt(d, 16, 5, "HOME", WHITE, 13)
    r(d, 126, 4, 60, 16, NAVY_BTN)
    txt(d, 134, 5, "RESET", WHITE, 13)
    r(d, 200, 2, 52, 24, NAV)
    txt(d, 210, 6, "OFF", WHITE, 14)
    r(d, 250, 4, 36, 16, TITLE_BG)
    txt(d, 254, 5, "MAN", WHITE, 13)

    box(d, 12, 34, 144, 32)
    txt(d, 28, 38, "1850", WHITE, 28, num=True)
    txt(d, 162, 40, "L", WHITE, 14)
    box(d, 84, 74, 72, 24)
    txt(d, 104, 76, "74", LIME, 18, num=True)
    txt(d, 162, 75, "%", LIME, 14)

    vbar(d, 216, 40, 84, 152, 0.74)

    for y, lab, on in ((104, "OSMOSI", True), (144, "RETE", False), (184, "TRAVASO", False)):
        r(d, 12, y, 168, 24, NAV)
        txt(d, 18, y + 4, lab, WHITE, 13)
        led(d, 144, y, on)
    nav(d, 0)
    return chrome(im)


def draw_fill() -> Image.Image:
    im, d = new_screen()
    r(d, 12, 4, 60, 16, TITLE_BG)
    txt(d, 16, 5, "RESET", WHITE, 12)
    r(d, 90, 4, 52, 16, BTN)
    txt(d, 94, 5, "START", LIME, 12)
    r(d, 148, 4, 44, 16, BTN)
    txt(d, 152, 5, "STOP", RED, 12)
    r(d, 210, 2, 44, 24, NAV)
    txt(d, 218, 6, "OFF", WHITE, 13)
    r(d, 256, 4, 40, 16, TITLE_BG)
    txt(d, 260, 5, "MAN", WHITE, 12)

    txt(d, 12, 44, "TARGET", WHITE, 13)
    txt(d, 90, 44, "L", CYAN, 13)
    box(d, 108, 42, 72, 24)
    txt(d, 118, 45, "2300", WHITE, 16, num=True)
    txt(d, 186, 44, "°F", CYAN, 13)
    box(d, 216, 36, 96, 32)
    txt(d, 248, 40, "8", WHITE, 22, num=True)

    r(d, 12, 72, 120, 24, NAV)
    txt(d, 18, 76, "OSMOSI", WHITE, 13)
    led(d, 96, 72, True)
    box(d, 124, 74, 70, 24)
    txt(d, 136, 77, "121", WHITE, 15, num=True)
    txt(d, 198, 76, "cm", CYAN, 12)
    box(d, 228, 74, 54, 24)
    txt(d, 232, 77, "1533", WHITE, 13, num=True)
    txt(d, 286, 76, "L", CYAN, 12)
    hbar(d, 12, 100, 276, 16, 0.55)

    r(d, 12, 128, 120, 24, NAV)
    txt(d, 18, 132, "RETE", WHITE, 13)
    led(d, 96, 128, False)
    box(d, 124, 130, 70, 24)
    txt(d, 142, 133, "61", WHITE, 15, num=True)
    txt(d, 198, 132, "cm", CYAN, 12)
    box(d, 228, 130, 54, 24)
    txt(d, 236, 133, "767", WHITE, 13, num=True)
    txt(d, 286, 132, "L", CYAN, 12)
    hbar(d, 12, 156, 276, 16, 0.0)

    txt(d, 12, 184, "ETA", WHITE, 13)
    box(d, 54, 182, 54, 24)
    txt(d, 64, 185, "90", WHITE, 15, num=True)
    txt(d, 112, 184, "min", WHITE, 12)
    txt(d, 162, 184, "LIV", WHITE, 13)
    box(d, 216, 182, 72, 24)
    txt(d, 230, 185, "900", WHITE, 15, num=True)
    nav(d, 1)
    return chrome(im)


def draw_refill() -> Image.Image:
    im, d = new_screen()
    r(d, 12, 4, 48, 16, TITLE_BG)
    txt(d, 16, 5, "FILL", WHITE, 13)
    txt(d, 12, 32, "SERBATOIO NON VUOTO", RED, 14)
    txt(d, 12, 52, "DUREZZA LITRI PRESENTI", WHITE, 13)
    box(d, 12, 68, 144, 40)
    txt(d, 60, 76, "8", WHITE, 24, num=True)
    txt(d, 164, 80, "F", WHITE, 14)
    txt(d, 12, 116, "PROCEDERE CON RABBOCCO", WHITE, 13)
    r(d, 24, 140, 48, 20, (0, 140, 0))
    txt(d, 36, 142, "SI", WHITE, 14)
    r(d, 120, 140, 48, 20, RED)
    txt(d, 132, 142, "NO", WHITE, 14)
    nav(d, 1)
    return chrome(im)


def register_pdf_fonts() -> dict[str, str]:
    regular_path = WIN / "segoeui.ttf"
    bold_path = WIN / "segoeuib.ttf"
    if not regular_path.exists():
        regular_path = LINUX_FONTS[0]
        bold_path = LINUX_FONTS[1]
    regular = str(regular_path)
    bold = str(bold_path)
    pdfmetrics.registerFont(TTFont("UI", regular))
    pdfmetrics.registerFont(TTFont("UI-Bold", bold))
    pdfmetrics.registerFontFamily("UI", normal="UI", bold="UI-Bold")
    return {"regular": "UI", "bold": "UI-Bold"}


BLUE = HexColor("#0066C8")
NAVY = HexColor("#0B1F3A")
INK = HexColor("#1A1F24")
MUTED = HexColor("#5A6570")
RULE = HexColor("#D4D8DE")
PALE = HexColor("#F3F6F9")
WARN_BG = HexColor("#FFF6E5")
WARN_BD = HexColor("#E6A100")
DANGER_BG = HexColor("#FDECEC")
DANGER_BD = HexColor("#C62828")
OK_BG = HexColor("#E8F6EE")
OK_BD = HexColor("#1B7A46")


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    s: dict[str, ParagraphStyle] = {}
    s["h1"] = ParagraphStyle(
        "h1",
        parent=base["Heading1"],
        fontName="UI-Bold",
        fontSize=16,
        leading=20,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=8,
    )
    s["h2"] = ParagraphStyle(
        "h2",
        parent=base["Heading2"],
        fontName="UI-Bold",
        fontSize=12.5,
        leading=16,
        textColor=BLUE,
        spaceBefore=9,
        spaceAfter=5,
    )
    s["body"] = ParagraphStyle(
        "body",
        parent=base["BodyText"],
        fontName="UI",
        fontSize=10,
        leading=13.6,
        textColor=INK,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    s["cap"] = ParagraphStyle(
        "cap",
        parent=base["BodyText"],
        fontName="UI",
        fontSize=8.5,
        leading=11,
        textColor=MUTED,
        alignment=TA_CENTER,
        spaceBefore=2,
        spaceAfter=8,
    )
    s["li"] = ParagraphStyle(
        "li",
        parent=base["BodyText"],
        fontName="UI",
        fontSize=10,
        leading=13.4,
        textColor=INK,
        leftIndent=2,
        spaceAfter=2,
    )
    s["th"] = ParagraphStyle(
        "th",
        fontName="UI-Bold",
        fontSize=8.8,
        leading=11.5,
        textColor=white,
    )
    s["td"] = ParagraphStyle(
        "td",
        fontName="UI",
        fontSize=8.8,
        leading=11.5,
        textColor=INK,
    )
    s["tdc"] = ParagraphStyle(
        "tdc",
        fontName="UI",
        fontSize=8.8,
        leading=11.5,
        textColor=INK,
        alignment=TA_CENTER,
    )
    s["note"] = ParagraphStyle(
        "note",
        fontName="UI",
        fontSize=9.2,
        leading=12.4,
        textColor=INK,
        leftIndent=4,
        rightIndent=4,
    )
    s["cover_kicker"] = ParagraphStyle(
        "cover_kicker",
        fontName="UI",
        fontSize=11,
        leading=14,
        textColor=HexColor("#C1F5FF"),
        alignment=TA_LEFT,
    )
    s["cover_title"] = ParagraphStyle(
        "cover_title",
        fontName="UI-Bold",
        fontSize=28,
        leading=34,
        textColor=white,
        alignment=TA_LEFT,
    )
    s["cover_sub"] = ParagraphStyle(
        "cover_sub",
        fontName="UI",
        fontSize=13,
        leading=18,
        textColor=HexColor("#E8EEF4"),
        alignment=TA_LEFT,
    )
    return s


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def bullets(items: list[str], style: ParagraphStyle) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=12, bulletColor=BLUE) for i in items],
        bulletType="bullet",
        start="•",
        leftIndent=14,
        bulletFontName="UI",
        bulletFontSize=10,
        spaceAfter=6,
    )


def numbered(items: list[str], style: ParagraphStyle) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(i, style), leftIndent=14) for i in items],
        bulletType="1",
        leftIndent=16,
        bulletFontName="UI-Bold",
        bulletFontSize=10,
        spaceAfter=6,
    )


def kv_table(rows: list[tuple[str, str]], col_w: list[float], s: dict[str, ParagraphStyle]) -> Table:
    data = [[p(a, s["td"]), p(b, s["td"])] for a, b in rows]
    t = Table(data, colWidths=col_w)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("BOX", (0, 0), (-1, -1), 0.4, RULE),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
                ("FONTNAME", (0, 0), (0, -1), "UI-Bold"),
            ]
        )
    )
    return t


def grid_table(
    header: list[str],
    rows: list[list[str]],
    col_w: list[float],
    s: dict[str, ParagraphStyle],
) -> Table:
    head = [p(h, s["th"]) for h in header]
    body = [[p(c, s["td"]) for c in row] for row in rows]
    t = Table([head] + body, colWidths=col_w)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BOX", (0, 0), (-1, -1), 0.4, NAVY),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, PALE]),
    ]
    t.setStyle(TableStyle(style))
    return t


def callout(text: str, kind: str, s: dict[str, ParagraphStyle]) -> Table:
    bg, bd = {
        "warn": (WARN_BG, WARN_BD),
        "danger": (DANGER_BG, DANGER_BD),
        "ok": (OK_BG, OK_BD),
    }[kind]
    t = Table([[p(text, s["note"])]], colWidths=[174 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.6, bd),
                ("LINEBEFORE", (0, 0), (0, -1), 3.2, bd),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def fig(path: Path, width: float, caption: str, s: dict[str, ParagraphStyle]) -> list:
    img = RLImage(str(path), width=width, height=width * path_stat_ratio(path))
    img.hAlign = "CENTER"
    return [img, p(caption, s["cap"])]


def path_stat_ratio(path: Path) -> float:
    with Image.open(path) as im:
        w, h = im.size
    return h / w


class _Footer:
    def __init__(self) -> None:
        self.page = 0

    def __call__(self, canv, doc) -> None:
        canv.saveState()
        page = canv.getPageNumber()
        if page == 1:
            canv.restoreState()
            return
        w, h = A4
        canv.setFillColor(NAVY)
        canv.rect(0, h - 12 * mm, w, 12 * mm, fill=1, stroke=0)
        canv.setFillColor(white)
        canv.setFont("UI", 8)
        canv.drawString(18 * mm, h - 7.4 * mm, "Tino H20  ·  Manuale d'uso del terminale")
        canv.drawRightString(w - 18 * mm, h - 7.4 * mm, "HOME e FILL  ·  H20 v1.00")
        canv.setFillColor(HexColor("#E8ECF0"))
        canv.rect(0, 0, w, 10 * mm, fill=1, stroke=0)
        canv.setFillColor(MUTED)
        canv.setFont("UI", 8)
        canv.drawString(18 * mm, 4.2 * mm, "Kernel TP 320  ·  birrificio artigianale (esempio)")
        canv.drawRightString(w - 18 * mm, 4.2 * mm, f"{page}")
        canv.restoreState()


def draw_cover(canv, doc, home_path: Path) -> None:
    w, h = A4
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, 0, w, h, fill=1, stroke=0)
    canv.setFillColor(BLUE)
    canv.rect(0, 0, 8 * mm, h, fill=1, stroke=0)
    canv.setFillColor(HexColor("#C1F5FF"))
    canv.setFont("UI", 10)
    canv.drawString(22 * mm, h - 28 * mm, "IMPIANTO ACQUA DI PROCESSO")
    canv.setFillColor(white)
    canv.setFont("UI-Bold", 32)
    canv.drawString(22 * mm, h - 46 * mm, "Tino H20")
    canv.setFont("UI", 16)
    canv.drawString(22 * mm, h - 58 * mm, "Manuale d'uso del terminale")
    canv.setStrokeColor(HexColor("#1CA4D5"))
    canv.setLineWidth(1.4)
    canv.line(22 * mm, h - 64 * mm, 92 * mm, h - 64 * mm)
    canv.setFillColor(HexColor("#E8EEF4"))
    canv.setFont("UI", 12)
    canv.drawString(22 * mm, h - 74 * mm, "Pagine HOME e FILL")
    canv.setFont("UI", 10)
    canv.drawString(22 * mm, h - 82 * mm, "Pannello Kernel TP 320  ·  H20 v1.00")
    canv.drawString(22 * mm, h - 88 * mm, "Impianto acqua di processo  ·  edizione pubblica 2026")

    img = Image.open(home_path)
    iw, ih = 128 * mm, 128 * mm * (img.size[1] / img.size[0])
    canv.drawImage(str(home_path), 22 * mm, 38 * mm, width=iw, height=ih, mask="auto")
    canv.setFillColor(HexColor("#9AA6B2"))
    canv.setFont("UI", 8.5)
    canv.drawString(22 * mm, 28 * mm, "Prima edizione: solo HOME e FILL. TRAVASO e SETUP arriveranno in un aggiornamento.")
    canv.drawString(22 * mm, 22 * mm, "I numeri nelle figure sono di esempio, non una ricetta da copiare alla cieca.")
    canv.restoreState()


def build_pdf(home: Path, fill: Path, refill: Path) -> None:
    register_pdf_fonts()
    s = styles()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    footer = _Footer()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=16 * mm,
        title="Tino H20 — Manuale d'uso del terminale (HOME e FILL)",
        author="Tino H20",
        subject="Uso del pannello TP 320: pagine HOME e FILL",
    )
    W = 174 * mm
    story: list = [Spacer(1, 220 * mm), PageBreak()]

    story += [
        p("1. A chi serve questo foglio", s["h1"]),
        p(
            "Questo è il manuale <b>per chi sta davanti al pannello</b> in sala cottura: "
            "come si legge lo stato del tino, come si accendono le uscite a mano e come si "
            "lancia un riempimento automatico (miscela osmosi + rete). "
            "Non è il manuale di programmazione né quello di SETUP.",
            s["body"],
        ),
        p(
            "Il terminale è un <b>Kernel TP 320</b>: schermo touch 320 × 240. "
            "Si tocca con il dito; i numeri si battono sulla tastiera che compare quando "
            "si preme un riquadro con bordo blu. Un tocco vale un comando: non serve tenere premuto.",
            s["body"],
        ),
        callout(
            "<b>Due RESET diversi.</b> Su HOME, RESET riarma il quadro dopo un’emergenza. "
            "Su FILL, la scritta RESET in alto a sinistra <i>interrompe il riempimento in corso</i> "
            "e non ha niente a che vedere con il fungo di emergenza. "
            "Si riconosce la pagina dalla linguetta gialla in basso.",
            "warn",
            s,
        ),
        Spacer(1, 4),
        p("2. Barra in basso — sempre visibile", s["h1"]),
        p(
            "In ogni pagina, in basso, ci sono quattro linguette. Quella della pagina aperta "
            "è <b>gialla con testo nero</b>; le altre sono blu scuro.",
            s["body"],
        ),
        grid_table(
            ["Linguetta", "Apre", "In questo manuale"],
            [
                ["HOME", "Stato del tino e comando manuale", "Sì, capitolo 3"],
                ["FILL", "Riempimento automatico (miscela)", "Sì, capitolo 4"],
                ["TRAV", "Travaso verso la sala cottura", "Non ancora"],
                ["SETUP", "Parametri di impianto (TANK, MIX, TRASD, TOT)", "Non ancora"],
            ],
            [28 * mm, 78 * mm, 68 * mm],
            s,
        ),
        Spacer(1, 4),
        p(
            "Si può cambiare pagina anche a ciclo in corso: il FILL continua in background. "
            "Per fermarlo si torna su FILL e si preme STOP oppure RESET.",
            s["body"],
        ),
        p("3. Pagina HOME", s["h1"]),
        p(
            "HOME è la pagina di stato. All’accensione il pannello apre qui. "
            "Non si impostano ricette: si guarda quanto c’è nel tino e, se serve, si comandano "
            "osmosi, rete e pompa di travaso a mano.",
            s["body"],
        ),
    ]
    story += fig(home, 158 * mm, "Figura 1. Schermata HOME (valori di esempio: 1850 L, 74 %).", s)

    story += [
        p("3.1 Cosa si vede", s["h2"]),
        grid_table(
            ["Zona", "Cosa indica", "Si tocca?"],
            [
                [
                    "HOME (alto sx)",
                    "Titolo di pagina. Non è un tasto.",
                    "No",
                ],
                [
                    "RESET",
                    "Riarmo dopo emergenza (stesso effetto del tasto blu sul quadro).",
                    "Sì, solo dopo il fungo",
                ],
                [
                    "OFF/ON + MAN",
                    "Stato del comando manuale. OFF = automatico / riposo; ON = si possono toccare le tre uscite.",
                    "Sì: un tap su MAN (o sul testo OFF/ON)",
                ],
                [
                    "Numero grande + L",
                    "Litri nel tino (misura filtrata). È il valore ufficiale.",
                    "No, sola lettura",
                ],
                [
                    "Numero + %",
                    "Riempimento rispetto alla capacità impostata (di fabbrica 2500 L). Se i litri superano 2500, la % resta 100.",
                    "No",
                ],
                [
                    "Colonna a destra",
                    "Stesso livello, disegnato come tino. Si riempie dal basso. Non è un tasto.",
                    "No",
                ],
                [
                    "OSMOSI / RETE / TRAVASO",
                    "Uscita fisica. Quadratino ciano = ON, scuro = OFF.",
                    "Sì, ma solo con MAN ON",
                ],
            ],
            [38 * mm, 96 * mm, 40 * mm],
            s,
        ),
        Spacer(1, 6),
        p("3.2 Come leggere i litri", s["h2"]),
        p(
            "Il numero grande è il livello <b>già filtrato</b>: il pelo libero dopo un getto "
            "si sistema in pochi secondi, il valore a video lo segue con un piccolo ritardo "
            "(di fabbrica circa 3 secondi). Non è un guasto se i litri non saltano a ogni goccia.",
            s["body"],
        ),
        p(
            "A tino «vuoto» <b>non compare 0</b>. Il trasduttore è montato dove finisce il cono: "
            "sotto di lui restano circa <b>85 L</b> (cono + rubinetteria) che il sensore non vede. "
            "Quindi il minimo visibile è 85 L, e la barra / la % partono da lì "
            "(85 / 2500 ≈ 3 %). Gli ultimi 85 litri non si misurano: è così per costruzione.",
            s["body"],
        ),
        callout(
            "<b>Troppo pieno (2400 L).</b> Se i litri superano la soglia di allarme, "
            "osmosi e rete si spengono da sole — anche in manuale — e un FILL non parte. "
            "La pompa di travaso resta comandabile, per svuotare. "
            "Non compare una pagina rossa: lo si vede dalle lampade OSMOSI/RETE spente "
            "e dai litri sopra 2400. Appena si torna a 2400 o sotto, osmosi e rete tornano permessi.",
            "danger",
            s,
        ),
        Spacer(1, 4),
        p("3.3 Comando manuale", s["h2"]),
        numbered(
            [
                "Toccare <b>MAN</b> (in alto a destra). Il testo passa da OFF a ON.",
                "Toccare la riga <b>OSMOSI</b>, <b>RETE</b> o <b>TRAVASO</b> (scritta o quadratino: è la stessa area). Ogni tap inverte l’uscita.",
                "Per tornare in automatico/riposo: toccare di nuovo <b>MAN</b> (ON → OFF). Si spengono tutte le uscite e si abortiscono FILL e TRAVASO in corso.",
            ],
            s["li"],
        ),
        bullets(
            [
                "Con MAN <b>OFF</b> i tap sulle tre righe non fanno nulla: non si «accodano» comandi.",
                "Entrare in MAN mentre gira un FILL o un TRAVASO <b>li interrompe</b>.",
                "A tino troppo pieno OSMOSI e RETE non partono (il tap si azzera). TRAVASO sì.",
                "Il fungo di emergenza spegne comunque tutto, anche in MAN.",
            ],
            s["li"],
        ),
        p("3.4 RESET su HOME e pagina rossa", s["h2"]),
        p(
            "L’unico allarme che <b>blocca lo schermo</b> è <b>EMERGENZA PREMUTA</b> (fungo). "
            "Tutte le uscite si spengono. Quando il fungo è di nuovo a riposo le uscite "
            "<b>non ripartono da sole</b>: serve un RESET.",
            s["body"],
        ),
        numbered(
            [
                "Rilasciare il fungo di emergenza.",
                "Toccare <b>RESET</b> in HOME, oppure premere il <b>tasto blu</b> sul quadro (stesso comando).",
                "A quel punto il quadro è riarmato. Per muovere le uscite si usa MAN, oppure si lancia un FILL/TRAV.",
            ],
            s["li"],
        ),
        callout(
            "Il RESET di HOME <b>non</b> azzera i litri, non ferma un FILL (per quello si usa STOP/RESET su FILL) "
            "e non carica i default di SETUP.",
            "ok",
            s,
        ),
        PageBreak(),
        p("4. Pagina FILL", s["h1"]),
        p(
            "FILL prepara l’acqua di birrificazione: prima entra l’<b>osmosi</b> (0 °F), "
            "poi, dopo una pausa di circa 30 secondi, la <b>rete</b>, fino ai litri e alla "
            "durezza scelti. Non si batte una percentuale osmosi/rete: si battono "
            "<b>litri totali</b> e <b>durezza target in °F</b>. Il pannello calcola da solo "
            "quanto osmosi e quanta rete servono, usando la durezza rete impostata in SETUP "
            "(di fabbrica <b>24 °F</b>).",
            s["body"],
        ),
        p(
            "In alto a sinistra, al posto del titolo «FILL», c’è il tasto <b>RESET</b>. "
            "Si capisce di essere in FILL perché la linguetta in basso è gialla.",
            s["body"],
        ),
    ]
    story += fig(fill, 158 * mm, "Figura 2. Schermata FILL (esempio: 2300 L a 8 °F, step osmosi in corso).", s)

    story += [
        p("4.1 Mappa dei comandi", s["h2"]),
        grid_table(
            ["Elemento", "Ruolo"],
            [
                ["RESET (alto sx)", "Interrompe il FILL in corso. Osmosi e rete si spengono. I target restano: si può ridare START."],
                ["START (verde)", "Avvia il riempimento. Se il tino non è vuoto, prima compare REFILL (cap. 4.5)."],
                ["STOP (rosso)", "Ferma il FILL, come un interruzione pulita dello step."],
                ["OFF/ON MAN", "Stesso manuale di HOME. Su FILL si possono toccare OSMOSI e RETE solo con MAN ON."],
                ["TARGET L", "Litri da raggiungere. Toccare il riquadro e battere il numero (0–5000). Default all’accensione: 2300."],
                ["°F (riquadro grande)", "Durezza target, intera, 0–50. Default all’accensione: 8. Sul pannello la scritta è «°F» (in file può comparire come ßF)."],
                ["Riga OSMOSI", "LED, cm di colonna, litri di osmosi, barra di avanzamento dello step."],
                ["Riga RETE", "Come sopra, per l’acqua di rete."],
                ["cm (editabili)", "Altra faccia della stessa ricetta. Se si battono i cm, il pannello ricalcola litri e °F."],
                ["ETA / min", "Minuti stimati a fine step, dalle portate di SETUP (non da un flussimetro)."],
                ["LIV", "Litri attuali nel tino (lo stesso valore di HOME)."],
            ],
            [42 * mm, 132 * mm],
            s,
        ),
        Spacer(1, 6),
        p("4.2 Come si imposta la ricetta", s["h2"]),
        p(
            "Il modo normale, a FILL fermo:",
            s["body"],
        ),
        numbered(
            [
                "Toccare il riquadro dei <b>litri TARGET</b>, battere il volume voluto, confermare.",
                "Toccare il riquadro dei <b>°F</b>, battere la durezza voluta (numero intero: 8, non 8,0).",
                "Controllare che i <b>cm</b> e i litri di OSMOSI / RETE si aggiornino da soli.",
            ],
            s["li"],
        ),
        p(
            "Se invece si ragiona in <b>centimetri di colonna</b> (asta del tino): si batte il cm "
            "osmosi e/o il cm rete. Quei due cm diventano la verità: il pannello ricalcola "
            "litri di ciascuna acqua, i litri totali e i °F. Se poi si ritocca TARGET L, °F "
            "oppure la durezza rete in SETUP, si torna al calcolo in avanti (dai target ai cm).",
            s["body"],
        ),
        callout(
            "<b>La ricetta non sopravvive allo spegnimento.</b> TARGET L e °F stanno in memoria volatile. "
            "A ogni accensione tornano <b>2300 L / 8 °F</b>. Se ieri si era battuto un altro valore, "
            "va reinserito. Non esiste ancora il database ricette («Pils», «IPA», …).",
            "warn",
            s,
        ),
        Spacer(1, 4),
        p(
            "Con i valori di fabbrica (rete 24 °F) la coppia 2300 L / 8 °F produce circa "
            "<b>1533 L di osmosi</b> (121 cm) e <b>767 L di rete</b> (61 cm). "
            "Se la durezza target è 0, o la durezza rete in SETUP è 0, il mix è 100 % osmosi. "
            "Se la durezza target è maggiore di quella di rete, il mix è 100 % rete "
            "(non si può «indurire» oltre l’acqua di arrivo).",
            s["body"],
        ),
        p("4.3 Sequenza automatica", s["h2"]),
        numbered(
            [
                "<b>Step 1 — OSMOSI.</b> Si apre il consenso all’osmosi. Il tino sale fino ai litri di osmosi calcolati (tolleranza di fabbrica ±20 L). La barra OSMOSI avanza; il LED OSMOSI è acceso.",
                "<b>Pausa di stabilizzazione</b> (di fabbrica 30 s). Serve all’osmosi per chiudere il ciclo di arresto/lavaggio. Le barre stanno ferme; non è un blocco.",
                "<b>Step 2 — RETE.</b> Si apre l’elettrovalvola di rete fino ai litri TARGET. Poi STOP, uscite spente.",
            ],
            s["li"],
        ),
        p(
            "ETA usa le portate battute in SETUP (osmosi ≈ 7 L/min, rete ≈ 22 L/min), non un contalitri. "
            "Se una portata in SETUP è 0, ETA mostra 999. LIV a destra è sempre il livello reale.",
            s["body"],
        ),
        p("4.4 START, STOP, RESET", s["h2"]),
        bullets(
            [
                "<b>START</b> — tino praticamente vuoto (livello ≤ 85 L + tolleranza ≈ 105 L): il FILL parte subito.",
                "<b>START</b> — tino già parzialmente pieno: non parte; si apre la pagina REFILL (paragrafo successivo).",
                "<b>START rifiutato in silenzio</b> se i litri TARGET superano l’allarme pieno (2400 L), oppure se si è già in troppo-pieno. Abbassare il target o travasare.",
                "<b>STOP</b> — interrompe il job. I target restano.",
                "<b>RESET</b> (scritta in alto a sinistra) — abortisce il job come STOP: osmosi/rete off, si può ridare START. Non è il RESET di HOME.",
                "Durante FILL/REFILL i cm e i litri di mix <b>non si riscrivono</b> da soli se si tocca un target: si aspetta la fine.",
            ],
            s["li"],
        ),
        p("4.5 Tino non vuoto — pagina REFILL", s["h2"]),
        p(
            "Se nel tino c’è già acqua sopra la soglia di «vuoto», START non può fingere un tino a zero. "
            "Compare una pagina intera (sul TP 320 non esistono finestre a comparsa):",
            s["body"],
        ),
    ]
    story += fig(refill, 150 * mm, "Figura 3. Pagina REFILL, aperta da START su tino non vuoto.", s)
    story += [
        numbered(
            [
                "Battere la <b>durezza in °F dell’acqua già presente</b> (quella che c’è ora, non il target).",
                "Toccare <b>SI</b> per procedere al rabbocco: il pannello ricalcola quanta osmosi e quanta rete servono per arrivare a TARGET L e °F partendo da ciò che c’è.",
                "Toccare <b>NO</b> per tornare a FILL senza partire.",
            ],
            s["li"],
        ),
        p("SI può essere rifiutato. In quel caso si resta (o si torna) su una pagina di avviso, tasto <b>OK</b> → FILL:", s["body"]),
        grid_table(
            ["Messaggio in pratica", "Cosa fare"],
            [
                [
                    "TARGET LT MAGGIOR LIV / IMPOSSIBILE RABBOCCO",
                    "I litri già in tino sono ≥ del target. Alzare TARGET L sopra il livello attuale, oppure travasare.",
                ],
                [
                    "IMPOSSIBILE RAGGIUNGERE DUREZZA E LITRI TARGET",
                    "Con l’acqua già presente non si può ottenere insieme quel volume e quei °F "
                    "(troppo «dura» rispetto al target, oppure durezza rete a 0). Cambiare target, "
                    "correggere DUR RETE in SETUP, o svuotare e rifare da vuoto.",
                ],
            ],
            [78 * mm, 96 * mm],
            s,
        ),
        Spacer(1, 6),
        p("5. Cosa può fermare osmosi, rete o il FILL", s["h1"]),
        grid_table(
            ["Situazione", "Cosa succede a video / in campo", "Cosa fa l’operatore"],
            [
                [
                    "Fungo emergenza",
                    "Pagina rossa EMERGENZA PREMUTA. Tutto spento.",
                    "Rilasciare il fungo, poi RESET su HOME (o tasto blu).",
                ],
                [
                    "Blocco termico pompe",
                    "Pompa e ricette off. Nessuna pagina rossa.",
                    "Ripristinare il termico in quadro, poi ripartire.",
                ],
                [
                    "Allarme osmosi (se cablato)",
                    "Niente osmosi; se si era in step 1 il FILL esce dallo step.",
                    "Guardare l’S-RO, poi STOP/RESET e nuovo START.",
                ],
                [
                    "Target &gt; 2400 L",
                    "START non parte.",
                    "Abbassare TARGET L.",
                ],
                [
                    "Livello &gt; 2400 L",
                    "OSMOSI e RETE off; FILL non parte. Travaso ok.",
                    "Travasare sotto soglia.",
                ],
                [
                    "Stallo (livello fermo troppo a lungo)",
                    "Uscite off. Di fabbrica dopo 20 minuti senza movimento utile.",
                    "Capire perché non entra/esce acqua; poi nuovo START. In prova si può mettere TIMEOUT a 0 in SETUP TRASD.",
                ],
                [
                    "MAN ON",
                    "FILL e TRAVASO automatici abortiti.",
                    "Voluto: si comanda a mano. Non voluto: MAN OFF e rilanciare.",
                ],
            ],
            [38 * mm, 68 * mm, 68 * mm],
            s,
        ),
        Spacer(1, 8),
        p("6. Esempio di turno — FILL da tino vuoto", s["h1"]),
        numbered(
            [
                "HOME: verificare circa 85 L (tino vuoto visibile) e MAN OFF. Osmosi accesa e pronta.",
                "FILL: controllare TARGET <b>2300</b> e <b>8</b> °F, oppure battere i propri valori. Controllare i cm/L di OSMOSI e RETE.",
                "START. Deve accendersi il LED OSMOSI e muoversi la prima barra. LIV sale; ETA scende.",
                "Dopo lo step osmosi: circa 30 s di pausa, poi LED RETE e seconda barra.",
                "A fine ciclo le uscite sono off. HOME deve mostrare circa i litri target (tolleranza di mix ±20 L).",
                "Se qualcosa non torna: STOP o RESET su FILL, non il RESET di HOME.",
            ],
            s["li"],
        ),
        callout(
            "Tempi di ordine di grandezza, con le portate di fabbrica: ~1533 L di osmosi a 7 L/min ≈ <b>3 h 40 min</b>; "
            "~767 L di rete a 22 L/min ≈ <b>35 min</b>; più i 30 s di pausa. "
            "Il FILL è pensato per girare senza stare attaccati allo schermo: il watchdog ferma tutto se il livello non si muove.",
            "ok",
            s,
        ),
        Spacer(1, 8),
        p("7. Promemoria rapido", s["h1"]),
        kv_table(
            [
                ("Pagina di stato", "HOME — litri, %, tino, tre uscite"),
                ("Riempimento miscela", "FILL — TARGET L + °F, poi START"),
                ("Manuale", "MAN ON, poi tap sulla riga OSMOSI / RETE / TRAVASO"),
                ("Stop FILL", "STOP o RESET in FILL (linguetta gialla FILL)"),
                ("Riarmo emergenza", "Fungo a riposo + RESET in HOME o tasto blu"),
                ("Tino «vuoto» a video", "≈ 85 L, non 0"),
                ("Troppo pieno", "2400 L: stop osmosi/rete, travaso ok"),
                ("Dopo spegnimento", "TARGET torna a 2300 L / 8 °F"),
                ("Durezza", "Gradi francesi interi, non percentuale osmosi"),
            ],
            [48 * mm, 126 * mm],
            s,
        ),
        Spacer(1, 10),
        p(
            "Edizione 2026, allineata al programma <b>H20 v1.00</b>. "
            "TRAVASO e SETUP saranno oggetto di un fascicolo successivo.",
            s["cap"],
        ),
    ]

    def first_page(canv, doc_) -> None:
        draw_cover(canv, doc_, home)

    def later(canv, doc_) -> None:
        footer(canv, doc_)

    doc.build(story, onFirstPage=first_page, onLaterPages=later)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    home = OUT_DIR / "home.png"
    fill = OUT_DIR / "fill.png"
    refill = OUT_DIR / "refill.png"
    draw_home().save(home)
    draw_fill().save(fill)
    draw_refill().save(refill)
    build_pdf(home, fill, refill)
    print(PDF_PATH)


if __name__ == "__main__":
    main()
