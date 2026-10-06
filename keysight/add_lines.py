import re

css_target = """    .detail-card__content p {
      margin-bottom: 12px;
    }
    
    .detail-card__content p:last-child {
      margin-bottom: 0;
    }
    
    .detail-card__content ul {
      margin: 0;
      padding-left: 20px;
    }
    
    .detail-card__content li {
      margin-bottom: 6px;
    }"""

css_replacement = """    .detail-card__content p {
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(var(--theme-rgb), 0.15);
    }
    
    .detail-card__content p:last-child {
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }
    
    .detail-card__content ul {
      margin: 0;
      padding-left: 20px;
    }
    
    .detail-card__content li {
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid rgba(var(--theme-rgb), 0.15);
    }
    
    .detail-card__content li:last-child {
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }"""

files = [
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html',
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if css_target in content:
        content = content.replace(css_target, css_replacement)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")
    else:
        print(f"Target CSS not found in {file_path}")

