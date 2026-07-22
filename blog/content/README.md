# Blog Content Pipeline

This directory (`blog/content/`) is the source of truth for your blog articles. 

Instead of writing raw HTML, you write your articles here in standard Markdown (`.md`). The automated build pipeline will convert them into fully styled HTML pages and automatically update your blog index.

## How to add a new article

1. **Create a Markdown file**: Create a new `.md` file in this directory (e.g., `my-new-article.md`).
2. **Write your content**: 
   - Ensure the very first line is a top-level heading (e.g., `# My Article Title`). The build script extracts this to use as the official page title and the index link title.
   - The first paragraph of text beneath the heading will automatically be extracted and used as the "summary" snippet on the main blog index page.
3. **Run the build script**:
   Open your terminal in the root `portfolio` directory and run:
   ```bash
   npm run build:blog
   ```

## What the script does behind the scenes

When you run `npm run build:blog`, the `build_blog.mjs` script executes the following pipeline:
1. **Reads** all `.md` files in this `content/` folder.
2. **Parses** the Markdown into HTML using the lightweight `marked` library.
3. **Injects** the HTML into your beautifully styled `blog_template.html` shell.
4. **Saves** the finalized file to the parent `blog/` directory (e.g., `blog/my-new-article.html`).
5. **Updates** the `blog/index.html` page dynamically, inserting a formatted link block for your new article so it appears live immediately.

## Drafts

If you are working on an article but aren't ready to publish it, **do not save it in this folder**, as the build script compiles everything here. 

Instead, save works-in-progress to the `blog/drafts/` folder, which is untracked by Git and ignored by the build script. Once your draft is ready to publish, simply move it into this `content/` folder and run the build script.
