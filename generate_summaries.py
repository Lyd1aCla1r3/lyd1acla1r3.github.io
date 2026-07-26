import os
from google import genai
import time

with open("/Users/lydia/enablement/api_key.txt", "r") as f:
    api_key = f.read().strip()
client = genai.Client(api_key=api_key)

CONTENT_DIR = "/Users/lydia/Desktop/personal/career/resumes/portfolio/blog/content"
IGNORE_FILES = {"body.md", "frontmatter.md", "transformer_ebook.md"}

def process_file(file_path):
    filename = os.path.basename(file_path)
    if filename in IGNORE_FILES:
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "<!-- SUMMARY:" in content:
        print(f"Skipping {filename}, already has summary.")
        return
        
    print(f"Processing {filename}...")
    
    prompt = (
        "Write a concise, 1-2 sentence summary of the following blog post. "
        "The summary should be engaging, technical, and accurately reflect the content. "
        "Do not include introductory phrases like 'This post explains' or 'In this article'. "
        "Just provide the summary text itself.\n\n"
        f"{content[:8000]}"
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        summary = response.text.strip().replace("\n", " ")
    except Exception as e:
        print(f"Error generating summary for {filename}: {e}")
        return
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith("# "):
            lines.insert(i + 1, f"\n<!-- SUMMARY: {summary} -->\n")
            break
            
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    print(f"Added summary to {filename}")
    time.sleep(1) # sleep briefly to avoid rate limits

if __name__ == "__main__":
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file))
