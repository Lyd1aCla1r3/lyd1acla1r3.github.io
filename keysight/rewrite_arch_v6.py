import re

with open('architecture.html', 'r') as f:
    html = f.read()

# Make the group colors Gold, Peach, Rose
html = html.replace('<div class="arch-super-group ks-color--pink">', '<div class="arch-super-group ks-color--gold">')
html = html.replace('<div class="arch-super-group ks-color--rose">', '<div class="arch-super-group ks-color--peach">')
html = html.replace('<div class="arch-super-group ks-color--dpink">', '<div class="arch-super-group ks-color--rose">')

# Modify the PHY svg zoom
# Find the PHY SVG block
if 'class="arch-super-group ks-color--rose"' in html:
    # Need to inject a custom scale for just the PHY image
    pass # Wait, let's just use CSS for this

# Also, update GPU svg
new_ai_svg = """<svg viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice" class="arch-bg-graphic gpu-svg" stroke="var(--c-text)" stroke-width="2" fill="none">
  <!-- Outer PCB traces/pads -->
  <path d="M 50 50 L 150 150 M 950 50 L 850 150 M 50 950 L 150 850 M 950 950 L 850 850" stroke-width="4" opacity="0.3"/>
  <path d="M 200 50 v 50 h -50 M 800 50 v 50 h 50 M 200 950 v -50 h -50 M 800 950 v -50 h 50" stroke-width="2" opacity="0.4"/>
  
  <!-- Memory Chips (GDDR) - 8 chips arranged around -->
  <rect x="350" y="100" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="530" y="100" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="350" y="780" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="530" y="780" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="100" y="350" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="100" y="530" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="780" y="350" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  <rect x="780" y="530" width="120" height="120" rx="4" fill="rgba(255,255,255,0.15)"/>
  
  <!-- Stiffener Frame -->
  <rect x="250" y="250" width="500" height="500" rx="10" stroke-width="6" fill="rgba(255,255,255,0.05)"/>
  <rect x="320" y="320" width="360" height="360" rx="6" stroke-width="6"/>
  <path d="M 250 250 L 320 320 M 750 250 L 680 320 M 250 750 L 320 680 M 750 750 L 680 680" stroke-width="3" opacity="0.6"/>
  
  <!-- Central Die -->
  <rect x="400" y="400" width="200" height="200" rx="2" stroke-width="4" fill="var(--c-text)" fill-opacity="0.15"/>
  <path d="M 400 450 h 200 M 400 500 h 200 M 400 550 h 200" stroke-width="2" opacity="0.3"/>
  <path d="M 450 400 v 200 M 500 400 v 200 M 550 400 v 200" stroke-width="2" opacity="0.3"/>
  
  <!-- Tiny SMD capacitors surrounding the central die -->
  <!-- Top -->
  <rect x="380" y="350" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="410" y="350" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="440" y="350" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="480" y="350" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="520" y="350" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="550" y="350" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="580" y="350" width="15" height="25" fill="var(--c-text)" opacity="0.6"/>
  <!-- Bottom -->
  <rect x="380" y="625" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="410" y="625" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="440" y="625" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="480" y="625" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="520" y="625" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="550" y="625" width="15" height="25" fill="var(--c-text)" opacity="0.6"/><rect x="580" y="625" width="15" height="25" fill="var(--c-text)" opacity="0.6"/>
  <!-- Left -->
  <rect x="350" y="380" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="350" y="410" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="350" y="440" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="350" y="480" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="350" y="520" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="350" y="550" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="350" y="580" width="25" height="15" fill="var(--c-text)" opacity="0.6"/>
  <!-- Right -->
  <rect x="625" y="380" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="625" y="410" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="625" y="440" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="625" y="480" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="625" y="520" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="625" y="550" width="25" height="15" fill="var(--c-text)" opacity="0.6"/><rect x="625" y="580" width="25" height="15" fill="var(--c-text)" opacity="0.6"/>
</svg>"""

# Replace old ai svg
# Find the old svg_ai using regex or split
start_idx = html.find('<div class="arch-image-card">') + len('<div class="arch-image-card">')
end_idx = html.find('<div class="arch-card-title">WORKLOADS</div>')
old_svg_ai = html[start_idx:end_idx]
html = html.replace(old_svg_ai, "\n              " + new_ai_svg + "\n              ")

# Add custom scale for phy svg and fix text color
# The user wants "the text in each of the expanded tabs should be the same darker color used for the title font."
# The title font is .arch-tab-content__title which uses `var(--c-text)`.
# The description text `.arch-tab-content__desc` uses `var(--ks-text-primary)`.
# So we need to change `.arch-tab-content__desc` color to `var(--c-text)`.

new_styles = """
    .arch-tab-content__desc {
      color: var(--c-text);
      font-size: 17px;
      line-height: 1.6;
      margin: 0;
    }
"""
html = html.replace("""    .arch-tab-content__desc {
      color: var(--ks-text-primary);
      font-size: 17px;
      line-height: 1.6;
      margin: 0;
    }""", new_styles)

# Add custom scale for the PHY SVG specifically (it's the 3rd super group)
phy_scale_css = """
    .arch-super-group:nth-child(3) .arch-bg-graphic {
      transform: scale(0.65);
    }
"""
# insert before </style>
style_end = html.find('/* --- Reset Button --- */')
html = html[:style_end] + phy_scale_css + html[style_end:]

with open('architecture.html', 'w') as f:
    f.write(html)
