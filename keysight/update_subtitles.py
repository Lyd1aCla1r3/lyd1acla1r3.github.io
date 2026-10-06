import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Category 2
html = html.replace('<div class="standard-row__subtitle">IEEE, OIF, LPO</div>', 
                    '<div class="standard-row__subtitle">IEEE 802.3 Ethernet, OIF CEI, Linear Pluggable Optics, Co-Packaged Optics</div>')

# Category 3
# There are two instances in the file: the main card and the overlay header
html = html.replace('<div class="standard-row__subtitle">DDR (Design and Test)</div>', 
                    '<div class="standard-row__subtitle">DDR5, LPDDR5X, GDDR6, HBM3</div>')

# Category 4
html = html.replace('<div class="standard-row__subtitle">MIPI D/M/C-PHY</div>', 
                    '<div class="standard-row__subtitle">MIPI D-PHY v2.5, MIPI C-PHY v2.0, MIPI M-PHY v4.1</div>')

# Category 5
html = html.replace('<div class="standard-row__subtitle">Automotive Electrical Communication Interfaces</div>', 
                    '<div class="standard-row__subtitle">100BASE-T1, 1000BASE-T1, 10GBASE-T1, CAN (Legacy)</div>')

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'w', encoding='utf-8') as f:
    f.write(html)

