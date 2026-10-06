import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

overlays = re.findall(r'<article class="standard-detail-overlay".*?</article>', html, re.DOTALL)
print(f"Found {len(overlays)} overlays")

for i, overlay in enumerate(overlays):
    # Split by <div class="detail-card"> and <div class="detail-card detail-card--wide
    # The first element is prefix, the rest are cards.
    parts = re.split(r'<div class="detail-card">', overlay)
    
    print(f"Overlay {i+1}: {len(parts)-1} standard cards found")
    if len(parts) >= 5:
        # parts[1] is Card 1, parts[2] is Card 2, etc.
        text1 = re.sub(r'<[^>]+>', '', parts[1]).strip()
        text2 = re.sub(r'<[^>]+>', '', parts[2]).strip()
        text3 = re.sub(r'<[^>]+>', '', parts[3]).strip()
        text4 = re.sub(r'<[^>]+>', '', parts[4].split('<div class="detail-card detail-card--wide')[0]).strip()
        
        l1 = len(text1) + parts[1].count('<li>') * 50
        l2 = len(text2) + parts[2].count('<li>') * 50
        l3 = len(text3) + parts[3].count('<li>') * 50
        l4 = len(text4) + parts[4].count('<li>') * 50
        
        t1 = l1 + l2
        t2 = l3 + l4
        
        print(f"  Pair 1: {round(l1/t1*100)} / {round(l2/t1*100)}")
        print(f"  Pair 2: {round(l3/t2*100)} / {round(l4/t2*100)}")

