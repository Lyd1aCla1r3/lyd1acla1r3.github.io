import re

with open('architecture.html', 'r') as f:
    html = f.read()

# 1. Update color variables
old_colors_start = html.find('/* Solid colors for clean tab UI */')
old_colors_end = html.find('.arch-layout {')
if old_colors_start != -1 and old_colors_end != -1:
    new_colors = """/* Four-tier color system */
    .ks-color--gold { 
      --c-tab-default: #f4ebd1; 
      --c-image-bg: #f8ecd0; 
      --c-group-bg: linear-gradient(135deg, #ebd8a7, #dfc68b); 
      --c-text: #9c7820; 
      --c-border: rgba(184,144,40,0.35); 
    }
    .ks-color--peach { 
      --c-tab-default: #f2e2d5; 
      --c-image-bg: #f6e4d8; 
      --c-group-bg: linear-gradient(135deg, #edccb6, #e3bba1); 
      --c-text: #a66d4b; 
      --c-border: rgba(192,136,104,0.35); 
    }
    .ks-color--rose { 
      --c-tab-default: #f5dce0; 
      --c-image-bg: #f4e0e3; 
      --c-group-bg: linear-gradient(135deg, #e8c5cb, #dfb4bb); 
      --c-text: #b76e79; 
      --c-border: rgba(183,110,121,0.35); 
    }
    
    """
    html = html[:old_colors_start] + new_colors + html[old_colors_end:]

# 2. Update CSS background assignments
# arch-super-group gets --c-group-bg
html = html.replace('background: var(--c-dark);', 'background: var(--c-group-bg);')
# Wait, I used var(--c-dark) for tabs and content box too! I need to distinguish them.
# Let's replace the specific class rules.
css_replacements = {
    '.arch-super-group {\n      background: var(--c-group-bg);': '.arch-super-group {\n      background: var(--c-group-bg);',
    '.arch-image-card {\n      background: var(--c-light);': '.arch-image-card {\n      background: var(--c-image-bg);',
    '.arch-tab {\n      background: var(--c-light);': '.arch-tab {\n      background: var(--c-tab-default);',
    '.arch-tab:not(.is-active):hover {\n      background: var(--c-group-bg);': '.arch-tab:not(.is-active):hover {\n      background: var(--c-image-bg);',
    '.arch-tab.is-active {\n      background: var(--c-group-bg);\n      border-bottom-color: var(--c-group-bg);': '.arch-tab.is-active {\n      background: var(--c-image-bg);\n      border-bottom-color: var(--c-image-bg);',
    '.arch-tab-content {\n      background: var(--c-group-bg);': '.arch-tab-content {\n      background: var(--c-image-bg);'
}
for old, new in css_replacements.items():
    html = html.replace(old, new)
    
# Manual fallback if regex/replace failed due to previous var(--c-dark)
html = html.replace('.arch-tab:not(.is-active):hover {\n      background: var(--c-dark);', '.arch-tab:not(.is-active):hover {\n      background: var(--c-image-bg);')
html = html.replace('.arch-tab.is-active {\n      background: var(--c-dark);\n      border-bottom-color: var(--c-dark);', '.arch-tab.is-active {\n      background: var(--c-image-bg);\n      border-bottom-color: var(--c-image-bg);')
html = html.replace('.arch-tab-content {\n      background: var(--c-dark);', '.arch-tab-content {\n      background: var(--c-image-bg);')

# 3. New SVGs
new_ai_svg = """<svg viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" class="arch-bg-graphic gpu-svg" stroke="var(--c-text)" stroke-width="2" fill="none" opacity="0.15">
  <path d="M 50 50 L 150 150 M 950 50 L 850 150 M 50 950 L 150 850 M 950 950 L 850 850" stroke-width="4" />
  <path d="M 200 50 v 50 h -50 M 800 50 v 50 h 50 M 200 950 v -50 h -50 M 800 950 v -50 h 50" stroke-width="2" />
  <rect x="350" y="100" width="120" height="120" rx="4" />
  <rect x="530" y="100" width="120" height="120" rx="4" />
  <rect x="350" y="780" width="120" height="120" rx="4" />
  <rect x="530" y="780" width="120" height="120" rx="4" />
  <rect x="100" y="350" width="120" height="120" rx="4" />
  <rect x="100" y="530" width="120" height="120" rx="4" />
  <rect x="780" y="350" width="120" height="120" rx="4" />
  <rect x="780" y="530" width="120" height="120" rx="4" />
  <rect x="250" y="250" width="500" height="500" rx="10" stroke-width="6" />
  <rect x="320" y="320" width="360" height="360" rx="6" stroke-width="6"/>
  <path d="M 250 250 L 320 320 M 750 250 L 680 320 M 250 750 L 320 680 M 750 750 L 680 680" stroke-width="3" />
  <rect x="400" y="400" width="200" height="200" rx="2" stroke-width="4" />
  <path d="M 400 450 h 200 M 400 500 h 200 M 400 550 h 200" stroke-width="2" />
  <path d="M 450 400 v 200 M 500 400 v 200 M 550 400 v 200" stroke-width="2" />
  <rect x="380" y="350" width="15" height="25" fill="var(--c-text)" /><rect x="410" y="350" width="15" height="25" fill="var(--c-text)" /><rect x="440" y="350" width="15" height="25" fill="var(--c-text)" /><rect x="480" y="350" width="15" height="25" fill="var(--c-text)" /><rect x="520" y="350" width="15" height="25" fill="var(--c-text)" /><rect x="550" y="350" width="15" height="25" fill="var(--c-text)" /><rect x="580" y="350" width="15" height="25" fill="var(--c-text)" />
  <rect x="380" y="625" width="15" height="25" fill="var(--c-text)" /><rect x="410" y="625" width="15" height="25" fill="var(--c-text)" /><rect x="440" y="625" width="15" height="25" fill="var(--c-text)" /><rect x="480" y="625" width="15" height="25" fill="var(--c-text)" /><rect x="520" y="625" width="15" height="25" fill="var(--c-text)" /><rect x="550" y="625" width="15" height="25" fill="var(--c-text)" /><rect x="580" y="625" width="15" height="25" fill="var(--c-text)" />
  <rect x="350" y="380" width="25" height="15" fill="var(--c-text)" /><rect x="350" y="410" width="25" height="15" fill="var(--c-text)" /><rect x="350" y="440" width="25" height="15" fill="var(--c-text)" /><rect x="350" y="480" width="25" height="15" fill="var(--c-text)" /><rect x="350" y="520" width="25" height="15" fill="var(--c-text)" /><rect x="350" y="550" width="25" height="15" fill="var(--c-text)" /><rect x="350" y="580" width="25" height="15" fill="var(--c-text)" />
  <rect x="625" y="380" width="25" height="15" fill="var(--c-text)" /><rect x="625" y="410" width="25" height="15" fill="var(--c-text)" /><rect x="625" y="440" width="25" height="15" fill="var(--c-text)" /><rect x="625" y="480" width="25" height="15" fill="var(--c-text)" /><rect x="625" y="520" width="25" height="15" fill="var(--c-text)" /><rect x="625" y="550" width="25" height="15" fill="var(--c-text)" /><rect x="625" y="580" width="25" height="15" fill="var(--c-text)" />
</svg>"""

new_conn_svg = """<svg viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" class="arch-bg-graphic" stroke="var(--c-text)" stroke-width="4" fill="none" opacity="0.15">
  <rect x="350" y="350" width="300" height="300" rx="20" stroke-width="6"/>
  <circle cx="500" cy="500" r="60" stroke-dasharray="10,10"/>
  <rect x="150" y="150" width="120" height="120" rx="10"/>
  <rect x="730" y="150" width="120" height="120" rx="10"/>
  <rect x="150" y="730" width="120" height="120" rx="10"/>
  <rect x="730" y="730" width="120" height="120" rx="10"/>
  <rect x="440" y="80" width="120" height="120" rx="10"/>
  <rect x="440" y="800" width="120" height="120" rx="10"/>
  <rect x="80" y="440" width="120" height="120" rx="10"/>
  <rect x="800" y="440" width="120" height="120" rx="10"/>
  <path d="M 270 270 L 350 350 M 730 270 L 650 350 M 270 730 L 350 650 M 730 730 L 650 650" />
  <path d="M 500 200 L 500 350 M 500 800 L 500 650 M 200 500 L 350 500 M 800 500 L 650 500" />
</svg>"""

new_phy_svg = """<svg viewBox="0 0 1000 1000" preserveAspectRatio="none" class="arch-bg-graphic" stroke="var(--c-text)" stroke-width="6" fill="none" opacity="0.15">
  <path d="M 0 150 H 100 V 50 H 250 V 150 H 400 V 50 H 550 V 150 H 700 V 50 H 850 V 150 H 1000" stroke-linejoin="bevel"/>
  <path d="M 0 350 H 150 V 250 H 300 V 350 H 450 V 250 H 600 V 350 H 750 V 250 H 900 V 350 H 1000" stroke-linejoin="bevel"/>
  <path d="M 0 550 H 80 V 450 H 220 V 550 H 380 V 450 H 520 V 550 H 680 V 450 H 820 V 550 H 1000" stroke-linejoin="bevel"/>
  <path d="M 0 750 H 200 V 650 H 350 V 750 H 500 V 650 H 650 V 750 H 800 V 650 H 950 V 750 H 1000" stroke-linejoin="bevel"/>
  <path d="M 0 950 H 120 V 850 H 280 V 950 H 420 V 850 H 580 V 950 H 720 V 850 H 880 V 950 H 1000" stroke-linejoin="bevel"/>
</svg>"""

# We need to replace the 3 SVGs in the HTML.
# Let's isolate the <div class="arch-image-card"> blocks and replace the SVG inside them.
def replace_svg_in_card(html, title_marker, new_svg):
    card_end = html.find(title_marker)
    card_start = html.rfind('<div class="arch-image-card">', 0, card_end)
    svg_start = html.find('<svg', card_start)
    svg_end = html.find('</svg>', svg_start) + 6
    if card_start != -1 and svg_start != -1 and svg_end != -1:
        return html[:svg_start] + new_svg + html[svg_end:]
    return html

html = replace_svg_in_card(html, '<div class="arch-card-title">WORKLOADS</div>', new_ai_svg)
html = replace_svg_in_card(html, '<div class="arch-card-title">OPERATIONAL<br>IMPACT</div>', new_conn_svg)
html = replace_svg_in_card(html, '<div class="arch-card-title">PHY<br>STANDARDS</div>', new_phy_svg)

# Remove the scale(0.65) hack for PHY svg since the new one scales perfectly
scale_hack = """    .arch-super-group:nth-child(3) .arch-bg-graphic {
      transform: scale(0.65);
    }"""
html = html.replace(scale_hack, "")

# Ensure global transform scale is removed from arch-bg-graphic, or keep it 1.0
html = html.replace('transform: scale(1.3);\n      transform-origin: center;', 'transform: scale(1.0);')

with open('architecture.html', 'w') as f:
    f.write(html)
