import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update CSS for .detail-bento
html = html.replace('grid-template-columns: 1fr 1fr;', 'grid-template-columns: var(--bento-cols, 1fr 1fr);')

# Replace inline grid-template-columns with CSS custom variable
html = re.sub(r'style="grid-template-columns: (\d+fr \d+fr);"', r'style="--bento-cols: \1;"', html)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'w', encoding='utf-8') as f:
    f.write(html)
