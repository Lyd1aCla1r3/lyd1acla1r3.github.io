import re
import math

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'r', encoding='utf-8') as f:
    html = f.read()

def process_overlay(match):
    overlay = match.group(0)
    parts = re.split(r'<div class="detail-card"(?: style="[^"]*")?>', overlay)
    
    if len(parts) >= 5:
        # parts[0] is prefix
        # parts[1] is card 1 content
        # parts[2] is card 2 content
        # parts[3] is card 3 content
        # parts[4] is card 4 content (up to the next detail-card--wide)
        
        text1 = re.sub(r'<[^>]+>', '', parts[1]).strip()
        text2 = re.sub(r'<[^>]+>', '', parts[2]).strip()
        text3 = re.sub(r'<[^>]+>', '', parts[3]).strip()
        text4 = re.sub(r'<[^>]+>', '', parts[4].split('<div class="detail-card detail-card--wide')[0]).strip()
        
        l1 = len(text1) + parts[1].count('<li>') * 60
        l2 = len(text2) + parts[2].count('<li>') * 60
        l3 = len(text3) + parts[3].count('<li>') * 60
        l4 = len(text4) + parts[4].count('<li>') * 60
        
        # Soften with square root
        s1 = math.sqrt(l1)
        s2 = math.sqrt(l2)
        s3 = math.sqrt(l3)
        s4 = math.sqrt(l4)
        
        t1 = s1 + s2
        t2 = s3 + s4
        
        pct1 = round(s1/t1*100)
        pct2 = 100 - pct1
        pct3 = round(s3/t2*100)
        pct4 = 100 - pct3
        
        # Add bounds to prevent extreme narrowness (min 38%)
        pct1 = max(38, min(62, pct1))
        pct2 = 100 - pct1
        
        pct3 = max(38, min(62, pct3))
        pct4 = 100 - pct3
        
        new_overlay = parts[0] + \
                      f'<div class="detail-card" style="width: calc({pct1}% - (var(--ks-space-md) / 2));">' + parts[1] + \
                      f'<div class="detail-card" style="width: calc({pct2}% - (var(--ks-space-md) / 2));">' + parts[2] + \
                      f'<div class="detail-card" style="width: calc({pct3}% - (var(--ks-space-md) / 2));">' + parts[3] + \
                      f'<div class="detail-card" style="width: calc({pct4}% - (var(--ks-space-md) / 2));">' + parts[4]
                      
        return new_overlay
    return overlay

html = re.sub(r'<article class="standard-detail-overlay".*?</article>', process_overlay, html, flags=re.DOTALL)

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html', 'w', encoding='utf-8') as f:
    f.write(html)

