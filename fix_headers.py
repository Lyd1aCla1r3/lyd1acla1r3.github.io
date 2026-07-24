import os
import glob

files_to_fix_h3 = [
    "article_04.md", "article_05.md", "article_06.md",
    "article_07.md", "article_11.md", "article_12.md"
]
files_to_fix_h4 = ["article_08.md"]

base_path = "/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/transformers"

for f in files_to_fix_h3:
    path = os.path.join(base_path, f)
    if os.path.exists(path):
        with open(path, 'r') as file:
            content = file.read()
        content = content.replace('\n### ', '\n## ')
        if content.startswith('### '):
             content = '## ' + content[4:]
        with open(path, 'w') as file:
            file.write(content)

for f in files_to_fix_h4:
    path = os.path.join(base_path, f)
    if os.path.exists(path):
        with open(path, 'r') as file:
            content = file.read()
        content = content.replace('\n#### ', '\n## ')
        if content.startswith('#### '):
             content = '## ' + content[5:]
        with open(path, 'w') as file:
            file.write(content)

print("Headers fixed.")
