from pathlib import Path
lines=Path('templates/index.html').read_text(encoding='utf-8').splitlines()
for idx in [917, 921, 925]:
    line = lines[idx]
    print(idx+1, line)
    print([hex(ord(ch)) for ch in line])
