import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html', 'r', encoding='utf-8') as f:
    html = f.read()

overlays = re.findall(r'<article class="standard-detail-overlay" id="(.*?)".*?>\s*(.*?)\s*</article>', html, re.DOTALL)

for overlay_id, overlay_content in overlays:
    cards = re.findall(r'<div class="detail-card">(.*?)</div>\s*(?=<div class="detail-card"|<div class="detail-card detail-card--wide)', overlay_content, re.DOTALL)
    if len(cards) >= 2:
        text1 = re.sub(r'<[^>]+>', '', cards[0])
        text2 = re.sub(r'<[^>]+>', '', cards[1])
        len1 = len(text1.strip())
        len2 = len(text2.strip())
        
        # Add weights for line breaks
        len1 += text1.count('li') * 50
        len2 += text2.count('li') * 50
        
        total = len1 + len2
        pct1 = round((len1 / total) * 100)
        pct2 = 100 - pct1
        
        print(f"Overlay ID: {overlay_id}")
        print(f"Ratio: {pct1}fr {pct2}fr")

