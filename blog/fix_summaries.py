import os
import re

dir_path = '/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content/series'

replacements = [
    ("The most striking emergent property—linear substructures where vector arithmetic captures semantic relationships—is demonstrated",
     "The emergent property (linear substructures where vector arithmetic captures semantic relationships) is demonstrated"),
    ("The fundamental limits of static embeddings—context-blindness and order-agnosticism—are identified",
     "The fundamental limits of static embeddings (context-blindness and order-agnosticism) are identified"),
    ("marks a profound shift", "marks a shift"),
    ("radically simplifies", "simplifies"),
    ("reveals exactly how", "reveals how"),
    ("highly refined", "refined"),
    ("precisely measure", "measure"),
    ("catastrophic softmax saturation", "softmax saturation"),
    ("deeply contextualized", "contextualized"),
    ("perfectly encapsulating", "encapsulating"),
    ("—", " ") # Catch any lingering em-dashes in summaries just in case! Wait, I shouldn't replace all em dashes in the whole file.
]

for root, _, files in os.walk(dir_path):
    for f in files:
        if f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
            
            # We only want to process the SUMMARY block to avoid changing the body text where em-dashes might be used in other contexts (though the user said "remove the em dashes / AI tells in all of the card descriptions for the series/posts").
            def replace_in_summary(match):
                summary = match.group(0)
                for old, new in replacements:
                    summary = summary.replace(old, new)
                return summary
            
            new_content = re.sub(r'<!--\s*SUMMARY:[\s\S]*?-->', replace_in_summary, content)
            
            if new_content != content:
                with open(path, 'w') as file:
                    file.write(new_content)
                print(f"Updated {path}")
