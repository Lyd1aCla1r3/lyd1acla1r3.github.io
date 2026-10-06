import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update .detail-bento CSS to use Flexbox
html = html.replace('grid-template-columns: repeat(100, 1fr);', '')
html = html.replace('.detail-bento {\n      display: grid;', '.detail-bento {\n      display: flex;\n      flex-wrap: wrap;')

# 2. Update .detail-card--wide CSS
html = html.replace('grid-column: span 100;', 'width: 100%;')

# 3. Update the media query override
media_query_target = """      .detail-bento > .detail-card {
        grid-column: span 100 !important;
      }"""
media_query_replacement = """      .detail-bento > .detail-card {
        width: 100% !important;
      }"""
html = html.replace(media_query_target, media_query_replacement)

# 4. Replace the grid-column: span XX; with width: calc(XX% - (var(--ks-space-md) / 2));
def replace_span(match):
    pct = match.group(1)
    return f'width: calc({pct}% - (var(--ks-space-md) / 2));'

html = re.sub(r'grid-column: span (\d+);', replace_span, html)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'w', encoding='utf-8') as f:
    f.write(html)
