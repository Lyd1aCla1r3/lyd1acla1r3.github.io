import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Linear Pluggable Optics with LPO in subtitles
html = html.replace(
    '<div class="standard-row__subtitle">IEEE 802.3 Ethernet, OIF CEI, Linear Pluggable Optics, Co-Packaged Optics</div>',
    '<div class="standard-row__subtitle">IEEE 802.3 Ethernet, OIF CEI, LPO, Co-Packaged Optics</div>'
)

# Strip versions from MIPI subtitle
html = html.replace(
    '<div class="standard-row__subtitle">MIPI D-PHY v2.5, MIPI C-PHY v2.0, MIPI M-PHY v4.1</div>',
    '<div class="standard-row__subtitle">MIPI D-PHY, MIPI C-PHY, MIPI M-PHY</div>'
)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'w', encoding='utf-8') as f:
    f.write(html)
