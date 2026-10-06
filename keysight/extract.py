import re

with open('architecture.html', 'r') as f:
    html = f.read()

# Extract SVGs
svgs = re.findall(r'(<svg viewBox="0 0 1000 1000" preserveAspectRatio="none" class="arch-bg-graphic".*?</svg>)', html, re.DOTALL)
print("Found", len(svgs), "SVGs")
with open('svgs.txt', 'w') as f:
    for i, svg in enumerate(svgs):
        f.write(f"=== SVG {i} ===\n{svg}\n")
