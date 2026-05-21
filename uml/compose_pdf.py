from PIL import Image
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
PDF_PATH = os.path.join(os.path.dirname(__file__), 'UniCMS_diagrams.pdf')

pngs = sorted([os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.lower().endswith('.png')])
if not pngs:
    print('No PNGs found in output/ to compose PDF.')
    raise SystemExit(1)

try:
    # Prefer reportlab for robust PDF creation
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader

    c = canvas.Canvas(PDF_PATH, pagesize=landscape(A4))
    w, h = landscape(A4)
    for p in pngs:
        img = Image.open(p)
        aspect = img.width / img.height
        # fit to page width minus margins
        target_w = w - 72
        target_h = target_w / aspect
        if target_h > (h - 72):
            target_h = h - 72
            target_w = target_h * aspect
        x = (w - target_w) / 2
        y = (h - target_h) / 2
        c.drawImage(ImageReader(p), x, y, width=target_w, height=target_h)
        c.showPage()
    c.save()
    print(f'Wrote {PDF_PATH} containing {len(pngs)} pages (reportlab).')
except Exception as e:
    print('reportlab not available or failed:', e)
    # Fallback to PIL - try converting to RGB then saving
    imgs = []
    for p in pngs:
        img = Image.open(p).convert('RGB')
        imgs.append(img)
    try:
        first, rest = imgs[0], imgs[1:]
        first.save(PDF_PATH, save_all=True, append_images=rest)
        print(f'Wrote {PDF_PATH} containing {len(imgs)} pages (PIL).')
    except Exception as e2:
        print('Failed to save PDF with PIL:', e2)
        print('Files are available as PNGs in', OUTPUT_DIR)

