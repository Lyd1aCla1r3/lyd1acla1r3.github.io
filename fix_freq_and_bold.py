import re

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/chapter_05.md', 'r') as f:
    text = f.read()

# 1. Replace the Angular Frequency section exactly
old_freq_part1 = "### The Angular Frequency\n\nFrom Chapter 2, the frequency for pair $i = 0$ is:"
new_freq_part1 = "### Computing the Angular Frequency\n\nThe rotation angle depends on the frequency $\\theta_i$, which is determined by the dimension pair index $i$ and the total dimensions $d_{model}$. The formula for $\\theta_i$ is:\n\n$$\n\\theta_i = \\frac{1}{10000^{\\,2i / d_{model}}}\n$$\n\nFor the toy model ($d_{model} = 3$), the only complete dimension pair is $i = 0$. Plugging these values into the frequency formula yields exactly 1:"
text = text.replace(old_freq_part1, new_freq_part1)

old_freq_part2 = "The rotation angle at position $t$ is therefore $t \cdot \\theta_0 = t \cdot 1 = t$ radians."
new_freq_part2 = "The total rotation angle for a position $t$ is $t \cdot \\theta_i$. Because $\\theta_0 = 1$ for our toy model, the angle simplifies perfectly to $t \cdot 1 = t$ radians. This is why the matrices will compute $\\cos(t)$ and $\\sin(t)$ instead of dealing with complex fractional angles.\n\n"
text = text.replace(old_freq_part2, new_freq_part2)

old_freq_part3 = "All nine entries of each matrix are computed from $\\cos(t)$ and $\\sin(t)$."
new_freq_part3 = "Because the rotation angle is exactly $t$, the nine matrix entries are derived directly from $\\cos(t)$ and $\\sin(t)$."
text = text.replace(old_freq_part3, new_freq_part3)

# 2. Fix the bolding
text = text.replace(r"\mathbf{v_2}", "v_2")
text = text.replace(r"\mathbf{0.0000}", "0.0000")
text = text.replace(r"\mathbf{0.8415}", "0.8415")
text = text.replace(r"\mathbf{0.9093}", "0.9093")
text = text.replace(r"\mathbf{0.1411}", "0.1411")

with open('/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series/positional-encoding/chapter_05.md', 'w') as f:
    f.write(text)

print("Done")
