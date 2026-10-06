import re

text = "Here is some math $V_S$) and $L=2$, at the end."
content = re.sub(r'(\$[^$\n]+\$)([.,;:)\]])', r'<span style="white-space: nowrap">\1\2</span>', text)
print(content)
