import re

files = [
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html',
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Increase padding-right to push the wrap point further in
    html = html.replace('padding-right: var(--ks-space-xl);', 'padding-right: var(--ks-space-2xl);')

    # Find all subtitles and replace regular hyphens with non-breaking hyphens
    def replace_hyphens(match):
        # match.group(0) is the entire div
        # match.group(1) is the inner text
        inner_text = match.group(1)
        # replace hyphen with &#8209;
        safe_text = inner_text.replace('-', '&#8209;')
        return f'<div class="standard-row__subtitle">{safe_text}</div>'

    html = re.sub(r'<div class="standard-row__subtitle">(.*?)</div>', replace_hyphens, html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
