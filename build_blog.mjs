import fs from 'fs';
import path from 'path';
import { marked } from 'marked';

const CONTENT_DIR = path.join(process.cwd(), 'blog/content');
const TEMPLATE_PATH = path.join(process.cwd(), 'blog/blog_template.html');
const BLOG_DIR = path.join(process.cwd(), 'blog');
const INDEX_PATH = path.join(process.cwd(), 'blog/index.html');

const templateHtml = fs.readFileSync(TEMPLATE_PATH, 'utf-8');

if (!fs.existsSync(CONTENT_DIR)) {
  fs.mkdirSync(CONTENT_DIR, { recursive: true });
}

const files = fs.readdirSync(CONTENT_DIR).filter(file => file.endsWith('.md'));
const posts = [];

for (const file of files) {
  const filePath = path.join(CONTENT_DIR, file);
  const markdown = fs.readFileSync(filePath, 'utf-8');
  
  // Extract title
  const titleMatch = markdown.match(/^#\s+(.+)/m);
  const title = titleMatch ? titleMatch[1].trim() : 'Untitled Post';
  
  const body = markdown.replace(/^#\s+(.+)/m, '').trim();
  const paragraphs = body.split(/\n\s*\n/);
  let summary = '';
  for (const p of paragraphs) {
    if (!p.startsWith('#') && !p.startsWith('!') && !p.startsWith('<') && p.trim().length > 0) {
      summary = p.replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1') 
                 .replace(/[*_~`]/g, '')
                 .replace(/\n/g, ' ')
                 .trim();
      if (summary.length > 200) {
        summary = summary.substring(0, 197) + '...';
      }
      break;
    }
  }
  
  const contentHtml = marked.parse(markdown);
  
  const finalHtml = templateHtml
    .replace('{{TITLE}}', title)
    .replace('{{CONTENT}}', contentHtml);
    
  const outFilename = file.replace('.md', '.html');
  const outPath = path.join(BLOG_DIR, outFilename);
  fs.writeFileSync(outPath, finalHtml, 'utf-8');
  console.log(`Generated blog post: ${outFilename}`);
  
  posts.push({
    title,
    summary,
    url: outFilename
  });
}

// Update index
if (posts.length > 0) {
    let indexHtml = fs.readFileSync(INDEX_PATH, 'utf-8');
    
    const blogListHtml = posts.map(post => `
        <a href="${post.url}">
            <article class="blog-item">
                <h2>${post.title}</h2>
                <p>${post.summary}</p>
            </article>
        </a>`).join('');
        
    indexHtml = indexHtml.replace(
        /<!-- BLOG_LIST_START -->[\s\S]*?<!-- BLOG_LIST_END -->/,
        `<!-- BLOG_LIST_START -->${blogListHtml}\n        <!-- BLOG_LIST_END -->`
    );
    
    fs.writeFileSync(INDEX_PATH, indexHtml, 'utf-8');
    console.log(`Updated blog index with ${posts.length} articles.`);
} else {
    console.log("No markdown files found in blog/content/.");
}
