import re

files = [
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html',
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace('padding-right: 32px;', 'padding-right: var(--ks-space-xl);')
    content = content.replace('margin-bottom: 12px;', 'margin-bottom: var(--ks-space-md);')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

