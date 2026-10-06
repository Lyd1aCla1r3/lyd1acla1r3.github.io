import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('width: calc(1% - (var(--ks-space-md) / 2));', 'width: 100%;')

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'w', encoding='utf-8') as f:
    f.write(html)
