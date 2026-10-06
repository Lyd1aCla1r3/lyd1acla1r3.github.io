import re

css_target = """    .standard-row__subtitle {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: var(--ks-accent);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }"""

css_replacement = """    .standard-row__subtitle {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: var(--ks-accent);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .standard-row > div:first-child {
      padding-right: 32px;
    }"""

mobile_target = """    @media (max-width: 768px) {
      .standard-row {"""

mobile_replacement = """    @media (max-width: 768px) {
      .standard-row > div:first-child {
        padding-right: 0;
        margin-bottom: 12px;
      }
      .standard-row {"""

files = [
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/instruments.html',
    '/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/standards.html'
]

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if css_target in content:
        content = content.replace(css_target, css_replacement)
        content = content.replace(mobile_target, mobile_replacement)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file_path}")
    else:
        print(f"Target CSS not found in {file_path}")

