import re

# Update Standards
with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    standards_html = f.read()

standards_html = standards_html.replace(
    '<title>Standards | Lydia Pedersen × Keysight</title>', 
    '<title>Hardware Standards Deep Dive | Lydia Pedersen × Keysight</title>'
)
standards_html = standards_html.replace(
    '<h1 class="ks-page-header__title metallic-text">Hardware Standards: Why They Exist</h1>',
    '<h1 class="ks-page-header__title metallic-text">Hardware Standards Deep Dive</h1>'
)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'w', encoding='utf-8') as f:
    f.write(standards_html)

# Update Instruments
with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'r', encoding='utf-8') as f:
    instruments_html = f.read()

instruments_html = instruments_html.replace(
    '<title>Instruments | Lydia Pedersen × Keysight</title>', 
    '<title>Instruments Deep Dive | Lydia Pedersen × Keysight</title>'
)
instruments_html = instruments_html.replace(
    '<h1 class="ks-page-header__title metallic-text">Instrument Classes: When to Use Each</h1>',
    '<h1 class="ks-page-header__title metallic-text">Instruments Deep Dive</h1>'
)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'w', encoding='utf-8') as f:
    f.write(instruments_html)

