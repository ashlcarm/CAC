"""Generate simple example assets (logo and nav icons) for the Lingrow app.

This script uses Pillow to draw a friendly logo and four small icons.
Run it from the project root (it will create `icons/` and `assets/`).

Usage:
  python3 scripts/generate_assets.py

If Pillow is not installed, install it first:
  pip install pillow

The generated images are simple programmatic designs intended as placeholders
you can replace later with real graphics from Canva.
"""
from PIL import Image, ImageDraw, ImageFont
import os


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def save(img, path):
    ensure_dir(os.path.dirname(path))
    img.save(path)
    print('Saved', path)


def make_logo(path, size=(420, 200)):
    w, h = size
    bg = (253, 232, 232)  # soft pink
    accent = (127, 166, 173)  # muted teal
    img = Image.new('RGBA', (w, h), bg)
    draw = ImageDraw.Draw(img)

    # draw a simple open-book icon on left
    book_w = int(w * 0.32)
    book_h = int(h * 0.7)
    bx = 28
    by = (h - book_h) // 2
    # left page
    draw.polygon([(bx, by + book_h//2), (bx + book_w//2, by), (bx + book_w//2, by + book_h)], fill=(255, 255, 255))
    # right page
    rx = bx + book_w//2
    draw.polygon([(rx, by), (rx + book_w//2, by + book_h//2), (rx, by + book_h)], fill=(255, 255, 255))
    # outline
    draw.line([(bx, by + book_h//2), (bx + book_w//2, by), (rx + book_w//2, by + book_h//2)], fill=accent, width=4)
    draw.line([(bx + book_w//2, by + book_h), (rx + book_w//2, by + book_h//2)], fill=accent, width=4)

    # text "Lingrow"
    try:
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', 48)
    except Exception:
        font = ImageFont.load_default()
    tx = bx + book_w + 20
    ty = h//2 - 24
    draw.text((tx, ty), 'Lingrow', font=font, fill=accent)

    save(img, path)


def make_icon(path, kind, size=(128, 128)):
    w, h = size
    bg = (255, 255, 255, 0)
    accent = (127, 166, 173)
    img = Image.new('RGBA', (w, h), bg)
    draw = ImageDraw.Draw(img)
    cx, cy = w//2, h//2

    if kind == 'home':
        # simple house
        roof_h = h//3
        draw.polygon([(cx, cy - roof_h), (cx - 36, cy), (cx + 36, cy)], fill=accent)
        draw.rectangle([cx - 40, cy, cx + 40, cy + 40], outline=accent, width=6)
    elif kind == 'explore':
        # globe: circle with simple grid
        r = 40
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=accent, width=6)
        draw.line([cx, cy - r, cx, cy + r], fill=accent, width=3)
        draw.line([cx - r, cy, cx + r, cy], fill=accent, width=3)
    elif kind == 'write':
        # pencil
        draw.line([cx - 36, cy + 18, cx + 36, cy - 18], fill=accent, width=8)
        draw.polygon([(cx + 36, cy - 18), (cx + 42, cy - 12), (cx + 30, cy - 6)], fill=accent)
    elif kind == 'profile':
        # head + shoulders
        draw.ellipse([cx - 28, cy - 34, cx + 28, cy + -6], outline=accent, width=6)
        draw.rectangle([cx - 36, cy - 6, cx + 36, cy + 30], outline=accent, width=6)
    else:
        draw.text((10, 10), kind, fill=accent)

    save(img, path)


def main():
    try:
        from PIL import Image
    except Exception:
        print('Pillow is required to generate assets. Install with: pip install pillow')
        return

    ensure_dir('icons')
    ensure_dir('assets')
    make_logo('assets/lingrow_logo.png')
    for k in ('home', 'explore', 'write', 'profile'):
        make_icon(f'icons/{k}.png', k)

    print('\nGenerated example assets in `assets/` and `icons/`.')


if __name__ == '__main__':
    main()
