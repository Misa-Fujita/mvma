#!/usr/bin/env python3
"""
HTML Formatter: Converts minified HTML into readable multi-line format
"""
import re
from html.parser import HTMLParser

class HTMLFormatter(HTMLParser):
    def __init__(self):
        super().__init__()
        self.indent_level = 0
        self.output = []
        self.indent_str = "  "
        self.inline_tags = {'span', 'a', 'img', 'br', 'strong', 'em', 'b', 'i', 'svg', 'path'}
        self.last_was_text = False
        
    def handle_starttag(self, tag, attrs):
        if tag in self.inline_tags:
            attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs)
            if attr_str:
                self.output.append(f'<{tag} {attr_str}>')
            else:
                self.output.append(f'<{tag}>')
        else:
            indent = self.indent_str * self.indent_level
            attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs)
            if attr_str:
                self.output.append(f'{indent}<{tag} {attr_str}>\n')
            else:
                self.output.append(f'{indent}<{tag}>\n')
            self.indent_level += 1
            self.last_was_text = False
    
    def handle_endtag(self, tag):
        if tag not in self.inline_tags:
            self.indent_level -= 1
            indent = self.indent_str * self.indent_level
            self.output.append(f'{indent}</{tag}>\n')
        else:
            self.output.append(f'</{tag}>')
        self.last_was_text = False
    
    def handle_data(self, data):
        data = data.strip()
        if data:
            self.output.append(data)
            self.last_was_text = True

# Read input
with open('/Users/mfmacbook2/Sites/localhost/mvma/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and format only the main content section
# Split at <main> tag
main_start = content.find('<main')
if main_start > -1:
    before_main = content[:main_start]
    main_end = content.rfind('</main>')
    if main_end > -1:
        main_content = content[main_start:main_end + 7]
        after_main = content[main_end + 7:]
        
        # Apply basic formatting by inserting newlines at strategic points
        # Insert newline after > for non-inline tags
        formatted_main = main_content
        
        # Add newlines after closing tags
        formatted_main = re.sub(r'(</(?:section|article|div|header|footer|main)>)(<)',  r'\1\n        <', formatted_main)
        
        # Add newlines after opening block tags
        formatted_main = re.sub(r'(^|>)(<(?:section|article|div|header|footer|h[1-6]|p)\s[^>]*>)',  r'\1\n        \2', formatted_main, flags=re.MULTILINE)
        
        result = before_main + formatted_main + after_main
        
        with open('/Users/mfmacbook2/Sites/localhost/mvma/index.html', 'w', encoding='utf-8') as f:
            f.write(result)
        
        print("✓ HTML formatting complete")
    else:
        print("Could not find </main>")
else:
    print("Could not find <main>")
