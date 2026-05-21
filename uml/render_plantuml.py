import os
import sys
import urllib.request
import urllib.error

PUML_DIR = os.path.dirname(__file__)
INPUT_DIR = PUML_DIR
OUTPUT_DIR = os.path.join(PUML_DIR, 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

PLANTUML_SERVER = 'https://www.plantuml.com/plantuml'


def render(puml_path: str):
    with open(puml_path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    name = os.path.splitext(os.path.basename(puml_path))[0]
    headers = { 'Content-Type': 'text/plain; charset=utf-8' }
    # Try POSTing raw PlantUML text to the server endpoints
    for fmt in ('svg', 'png'):
        url = f"{PLANTUML_SERVER}/{fmt}"
        out_path = os.path.join(OUTPUT_DIR, f"{name}.{fmt}")
        req = urllib.request.Request(url, data=text.encode('utf-8'), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            with open(out_path, 'wb') as out:
                out.write(data)
            print(f"Wrote {out_path}")
        except urllib.error.HTTPError as he:
            print(f"HTTP Error rendering {puml_path} -> {fmt}: {he.code} {he.reason}")
        except Exception as e:
            print(f"Failed to render {puml_path} -> {fmt}: {e}")

def main():
    puml_files = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) if f.endswith('.puml')]
    if not puml_files:
        print('No .puml files found')
        return 1
    for p in puml_files:
        render(p)
    return 0

if __name__ == '__main__':
    sys.exit(main())
