from PIL import Image, ImageDraw, ImageFont
import os

PUML_DIR = os.path.dirname(__file__)
INPUT_FILES = [
    'accounts_class.puml', 'complaints_class.puml', 'system_components.puml',
    'seq_login.puml', 'seq_register.puml', 'seq_submit_complaint.puml', 'seq_notification.puml'
]
OUTPUT_DIR = os.path.join(PUML_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

W, H = 1200, 800
BG = (255,255,255)
BOX = (240,240,240)
TEXT = (20,20,20)

def load_font(size=14):
    try:
        return ImageFont.truetype('arial.ttf', size)
    except Exception:
        return ImageFont.load_default()

def draw_class_diagram(path, out_path):
    # Very simple parser: extract class blocks between 'class' and '}' and draw boxes
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    classes = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i].strip()
        if ln.startswith('class '):
            name = ln.split()[1]
            fields = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('}'): 
                l = lines[i].strip()
                if l and not l.startswith('//'):
                    fields.append(l)
                i += 1
            classes.append((name, fields))
        else:
            i += 1

    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = load_font(16)
    margin = 40
    box_w = (W - margin*2) // max(1, len(classes))
    x = margin
    for name, fields in classes:
        y = margin
        draw.rectangle([x, y, x+box_w-20, y+120], fill=BOX, outline=TEXT)
        draw.text((x+10, y+6), name, fill=TEXT, font=font)
        y += 36
        fnt = load_font(12)
        for f in fields[:10]:
            draw.text((x+10, y), f, fill=TEXT, font=fnt)
            y += 18
        x += box_w
    img.save(out_path)
    print('Wrote', out_path)

def draw_component_diagram(path, out_path):
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = load_font(14)
    boxes = ['Django Project (unicms)', 'Accounts App', 'Complaints App', 'SQLite (db.sqlite3)', 'Templates / Static', 'Email (SMTP)', 'Twilio (SMS)']
    x = 80
    y = 60
    for b in boxes:
        draw.rectangle([x, y, x+320, y+70], outline=TEXT, fill=BOX)
        draw.text((x+10, y+10), b, fill=TEXT, font=font)
        y += 100
    img.save(out_path)
    print('Wrote', out_path)

def draw_sequence_diagram(path, out_path):
    # Basic lifeline + arrows using actors from PlantUML files
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    lines = [l.strip() for l in text.splitlines() if l.strip() and not l.strip().startswith("'")]
    actors = []
    arrows = []
    for l in lines:
        if l.startswith('actor ') or l.startswith('participant '):
            parts = l.split()
            actors.append(parts[1])
        elif '->' in l:
            arrows.append(l)

    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)
    font = load_font(14)
    cols = max(1, len(actors))
    spacing = W // (cols+1)
    positions = {}
    for idx, a in enumerate(actors):
        x = spacing*(idx+1)
        positions[a] = x
        draw.text((x-40, 20), a, fill=TEXT, font=font)
        draw.line((x, 60, x, H-60), fill=(200,200,200))

    y = 100
    for arr in arrows:
        try:
            left, right = arr.split('->')
            left = left.strip().split()[-1]
            right = right.strip().split()[0]
            x1 = positions.get(left, 100)
            x2 = positions.get(right, W-100)
            draw.line((x1, y, x2, y), fill=TEXT, width=2)
            draw.polygon([(x2, y-6),(x2, y+6),(x2+8,y)], fill=TEXT)
            y += 40
        except Exception:
            y += 20

    img.save(out_path)
    print('Wrote', out_path)

def main():
    for fn in INPUT_FILES:
        path = os.path.join(PUML_DIR, fn)
        out = os.path.join(OUTPUT_DIR, os.path.splitext(fn)[0]+'.png')
        if not os.path.exists(path):
            print('Skipping missing', fn)
            continue
        if fn.endswith('_class.puml'):
            draw_class_diagram(path, out)
        elif fn == 'system_components.puml':
            draw_component_diagram(path, out)
        else:
            draw_sequence_diagram(path, out)

if __name__ == '__main__':
    main()
