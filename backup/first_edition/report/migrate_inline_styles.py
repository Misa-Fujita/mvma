#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / 'index.html'
BACKUP = ROOT / 'index.html.bak'

# exact mappings used by shim
mapping = {
    'font-size: 37.95px;': 'ex-style-1',
    'pointer-events: auto;': 'ex-style-2',
    'right: 0px; left: 0px;': 'ex-style-3',
    'display: none;': 'ex-style-4',
    'top: 20px; inset-inline-end: 0px;': 'ex-style-5',
    'min-width: 20px; min-height: 20px;': 'ex-style-6',
    'top: -999px; left: -999px;': 'ex-style-7',
    'text-align: left;': 'ex-style-8',
    'width: 100%; height: fit-content;': 'ex-style-9',
    'min-width: 16px; min-height: 16px; color: var(--theme-icon-quaternary);': 'ex-style-10',
    'width: 12px; height: 12px; border-radius: 50%;': 'ex-style-11',
    'min-width: 16px; min-height: 16px; margin-right: 4px;': 'ex-style-12',
    'min-width: 12px; min-height: 12px;': 'ex-style-13'
    , 'min-width: 16px; min-height: 16px;': 'ex-style-14'
}

if not HTML.exists():
    print('index.html not found')
    raise SystemExit(1)

content = HTML.read_text(encoding='utf-8')
# backup
if not BACKUP.exists():
    BACKUP.write_text(content, encoding='utf-8')
    print('Backup written to', BACKUP)

# Normalize spaces inside style attribute for matching
def normalize(s):
    return re.sub(r'\s+', ' ', s.strip()).rstrip(';') + ';'

# Step 1: replace matching style attributes with a temporary data attribute
pattern = re.compile(r'style\s*=\s*"([^"]*)"')
replacements = 0

def repl(m):
    global replacements
    orig = m.group(1)
    norm = normalize(orig)
    cls = mapping.get(norm)
    if cls:
        replacements += 1
        return f'data-migrated-class="{cls}"'
    else:
        return m.group(0)

content2 = pattern.sub(repl, content)

# Step 2: merge data-migrated-class into existing class attributes
# If element has class="..." followed by data-migrated-class, combine them
content3 = re.sub(r'(class\s*=\s*"([^"]*)")\s*(data-migrated-class\s*=\s*"([^"]*)")', lambda m: f'class="{m.group(2).strip()} {m.group(4).strip()}"', content2)
# If data-migrated-class remains on elements without class, replace it with class attr
content4 = re.sub(r'data-migrated-class\s*=\s*"([^"]*)"', lambda m: f'class="{m.group(1)}"', content3)

HTML.write_text(content4, encoding='utf-8')
print(f'Migration complete. Replaced {replacements} inline style attributes. index.html updated.')
print('Original backed up at index.html.bak')
