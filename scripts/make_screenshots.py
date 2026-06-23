import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACK = os.path.join(ROOT, "App", "Stickers.xcstickers", "Sticker Pack.stickerpack")
OUT = os.path.join(ROOT, "screenshots")
os.makedirs(OUT, exist_ok=True)

W, H = 1290, 2796  # 6.7" iPhone portrait

FONT_B = "C:/Windows/Fonts/YuGothB.ttc"
FONT_M = "C:/Windows/Fonts/YuGothM.ttc"

def font(path, size):
    return ImageFont.truetype(path, size, index=0)

def load_stickers():
    imgs = []
    for i in range(1, 33):
        p = os.path.join(PACK, f"{i:02d}.sticker", f"{i:02d}.png")
        if os.path.exists(p):
            imgs.append(Image.open(p).convert("RGBA"))
    return imgs

def vgradient(top, bottom):
    base = Image.new("RGB", (W, H), top)
    draw = ImageDraw.Draw(base)
    for y in range(H):
        t = y / H
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return base

def center_text(draw, cx, y, text, fnt, fill):
    bb = draw.textbbox((0, 0), text, font=fnt)
    w = bb[2] - bb[0]
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)

def rounded_card(img, box, radius, fill):
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle(box, radius=radius, fill=fill)

def paste_sticker(canvas, st, cx, cy, target):
    s = st.copy()
    s.thumbnail((target, target), Image.LANCZOS)
    canvas.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))

def grid(canvas, stickers, box, cols, cell, gap_extra=0):
    x0, y0, x1, y1 = box
    gw = (x1 - x0)
    rows = (len(stickers) + cols - 1) // cols
    cw = gw / cols
    for idx, st in enumerate(stickers):
        c = idx % cols
        r = idx // cols
        cx = x0 + cw * (c + 0.5)
        cy = y0 + cw * (r + 0.5)
        paste_sticker(canvas, st, cx, cy, cell)

stickers = load_stickers()

# ---- Screenshot 1: Hero ----
def shot1():
    bg = vgradient((250, 244, 228), (214, 226, 196)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    center_text(d, W/2, 150, "クール農家スタンプ", font(FONT_B, 92), (60, 70, 40))
    center_text(d, W/2, 300, "サングラス農家のクールな", font(FONT_M, 52), (90, 100, 70))
    center_text(d, W/2, 372, "スタンプ32種", font(FONT_M, 52), (90, 100, 70))
    rounded_card(bg, (90, 560, W-90, H-180), 60, (255, 255, 255, 235))
    grid(bg, stickers[:9], (150, 640, W-150, 640 + (W-300)), 3, 320)
    bg.convert("RGB").save(os.path.join(OUT, "01_hero.png"))

# ---- Screenshot 2: iMessage drawer mock ----
def shot2():
    bg = vgradient((236, 240, 244), (222, 228, 236)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    # chat header
    rounded_card(bg, (0, 0, W, 230), 0, (247, 248, 250, 255))
    center_text(d, W/2, 110, "メッセージ", font(FONT_B, 58), (30, 30, 35))
    # incoming bubble + sticker
    rounded_card(bg, (90, 320, 760, 560), 50, (233, 233, 238, 255))
    center_text(d, 425, 400, "見て！このスタンプ", font(FONT_M, 46), (40, 40, 45))
    paste_sticker(bg, stickers[0], 980, 540, 360)
    # outgoing sticker
    paste_sticker(bg, stickers[4], 330, 980, 360)
    rounded_card(bg, (640, 900, W-90, 1080), 50, (40, 140, 250, 255))
    center_text(d, (640+W-90)/2, 955, "かわいい！", font(FONT_M, 46), (255, 255, 255))
    # sticker drawer panel
    rounded_card(bg, (0, 1500, W, H), 56, (255, 255, 255, 255))
    d.rounded_rectangle((W/2-70, 1540, W/2+70, 1556), radius=8, fill=(210, 210, 215))
    center_text(d, W/2, 1590, "クール農家スタンプ", font(FONT_M, 44), (90, 100, 70))
    grid(bg, stickers[8:20], (70, 1700, W-70, H-80), 4, 240)
    bg.convert("RGB").save(os.path.join(OUT, "02_drawer.png"))

# ---- Screenshot 3: Full grid ----
def shot3():
    bg = vgradient((245, 236, 220), (206, 222, 190)).convert("RGBA")
    d = ImageDraw.Draw(bg)
    center_text(d, W/2, 160, "全32種類", font(FONT_B, 96), (60, 70, 40))
    center_text(d, W/2, 300, "毎日のトークにクールをひとつまみ", font(FONT_M, 46), (90, 100, 70))
    rounded_card(bg, (70, 470, W-70, H-150), 56, (255, 255, 255, 235))
    grid(bg, stickers[:20], (120, 540, W-120, H-220), 4, 250)
    bg.convert("RGB").save(os.path.join(OUT, "03_grid.png"))

shot1()
shot2()
shot3()
print("done:", os.listdir(OUT))
