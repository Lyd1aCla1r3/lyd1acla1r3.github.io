import re
html_path = "/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/architecture.html"
with open(html_path, "r") as f:
    content = f.read()

content = content.replace(
    "--grad-ai-solid: linear-gradient(90deg, #fdfaf2, #fcf4ef);",
    "--grad-ai-solid: linear-gradient(90deg, #faf5e8, #f9ebe4);"
)
content = content.replace(
    "--grad-conn-solid: linear-gradient(90deg, #fcf4ef, #fdf0f4);",
    "--grad-conn-solid: linear-gradient(90deg, #f9ebe4, #fae8ec);"
)
content = content.replace(
    "--grad-phy-solid: linear-gradient(90deg, #fdf0f4, #fcebef);",
    "--grad-phy-solid: linear-gradient(90deg, #fae8ec, #f7e1e6);"
)

with open(html_path, "w") as f:
    f.write(content)
