#!/usr/bin/env python3
"""
Reverse-migrate: find class attributes that include ex-style-* names and
replace them by inline style attributes using the inverse of the known mapping.
This preserves the visual rules after we delete the .ex-style-* CSS.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = list(ROOT.glob('*.html'))

# Inverted mapping (class -> style)
inv = {
    'ex-style-1': 'font-size: 37.95px;',
    'ex-style-2': 'pointer-events: auto;',
    'ex-style-3': 'right: 0px; left: 0px;',
    'ex-style-4': 'display: none;',
    'ex-style-5': 'top: 20px; inset-inline-end: 0px;',
    'ex-style-6': 'min-width: 20px; min-height: 20px;',
    'ex-style-7': 'top: -999px; left: -999px;',
    'ex-style-8': 'text-align: left;',
    'ex-style-9': 'width: 100%; height: fit-content;',
    'ex-style-10': 'min-width: 16px; min-height: 16px; color: var(--theme-icon-quaternary);',
    'ex-style-11': 'width: 12px; height: 12px; border-radius: 50%;',
    'ex-style-12': 'min-width: 16px; min-height: 16px; margin-right: 4px;',
    'ex-style-13': 'min-width: 12px; min-height: 12px;',
    'ex-style-14': 'min-width: 16px; min-height: 16px;'
}

cls_pattern = re.compile(r'class\s*=\s*"([^"]*)"')

for f in FILES:
    text = f.read_text(encoding='utf-8')
    modified = [False]

    def repl_class(m):
        classes = m.group(1).split()
        ex_classes = [c for c in classes if c.startswith('ex-style-')]
        if not ex_classes:
            return m.group(0)
        # build style from ex_classes
        styles = ' '.join(inv.get(c, '') for c in ex_classes).strip()
        # remove ex_classes from class list
        remaining = [c for c in classes if not c.startswith('ex-style-')]
        modified[0] = True
        if remaining:
            new_class_attr = 'class="' + ' '.join(remaining) + '"'
        else:
            new_class_attr = ''
        # inject style attribute after the class attr if styles exist
        if styles:
            style_attr = ' style="' + styles + '"'
        else:
            style_attr = ''
        if new_class_attr:
            return new_class_attr + style_attr
        else:
            return style_attr

    text2 = cls_pattern.sub(repl_class, text)

    # If any ex-style-* appear as standalone class="ex-style-1" (no other classes), cls_pattern handles it.
    if modified[0]:
        backup = f.with_suffix(f'.bak-before-reverse')
        backup.write_text(text, encoding='utf-8')
        f.write_text(text2, encoding='utf-8')
        print(f'Processed {f.name}: converted ex-style-* classes to inline styles. Backup at {backup.name}')

print('Reverse migration done.')
