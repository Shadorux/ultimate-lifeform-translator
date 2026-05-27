from pathlib import Path
p = Path('shadowtranslator.png')
if not p.exists():
    raise SystemExit('File not found')
data = p.read_bytes()
if data[:8] != b'\x89PNG\r\n\x1a\n':
    raise SystemExit('Not a PNG')
width = int.from_bytes(data[16:20], 'big')
height = int.from_bytes(data[20:24], 'big')
print(width, height)
