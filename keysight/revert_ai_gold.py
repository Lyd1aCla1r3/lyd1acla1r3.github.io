import re
html_path = "/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/architecture.html"
with open(html_path, "r") as f:
    content = f.read()

content = content.replace("--bg-ai-solid: #eedacf;", "--bg-ai-solid: #ede1cb;")
content = content.replace(
    "--grad-ai-solid: linear-gradient(90deg, #f7e6dc, #f4dfd3);", 
    "--grad-ai-solid: linear-gradient(90deg, #faf5e8, #f9ebe4);"
)

with open(html_path, "w") as f:
    f.write(content)
