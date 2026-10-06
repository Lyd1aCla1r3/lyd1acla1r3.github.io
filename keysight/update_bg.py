import re
html_path = "/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/architecture.html"
with open(html_path, "r") as f:
    content = f.read()

content = content.replace("--bg-ai-solid: #f5e9d3;", "--bg-ai-solid: #ede1cb;")
content = content.replace("--bg-conn-solid: #f5dee4;", "--bg-conn-solid: #edd6dc;")
content = content.replace("--bg-phy-solid: #f2d5dc;", "--bg-phy-solid: #eacdd4;")

with open(html_path, "w") as f:
    f.write(content)
