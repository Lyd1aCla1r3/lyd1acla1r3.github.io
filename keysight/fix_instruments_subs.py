import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove software from VNA
html = html.replace('PNA&#8209;X, ENA (E5080B), PLTS', 'PNA&#8209;X, ENA (E5080B)')

# Remove software from OMA
html = html.replace('N4391C, 89600 VSA Software', 'N4391C')

# Replace competitor LeCroy product with Keysight product
html = html.replace('U4301B, PXP&#8209;Series', 'P5500 Series, U4301B')

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'w', encoding='utf-8') as f:
    f.write(html)
