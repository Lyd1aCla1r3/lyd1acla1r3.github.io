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

function getFilesRecursively(dir, relativePath = '') {
  let results = [];
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    const fullPath = path.join(dir, file);
    const relPath = path.join(relativePath, file);
    const stat = fs.statSync(fullPath);
    if (stat && stat.isDirectory()) {
      results = results.concat(getFilesRecursively(fullPath, relPath));
    } else if (file.endsWith('.md')) {
      if (!['body.md', 'frontmatter.md', 'transformer_ebook_final.md', 'transformer_ebook.md'].includes(file)) {
        results.push({ fullPath, relPath, name: file });
      }
    }
  });
  return results;
}

const mdFiles = getFilesRecursively(CONTENT_DIR);
const postsData = [];

for (const fileObj of mdFiles) {
  const filePath = fileObj.fullPath;
  const relPath = fileObj.relPath;
  const parts = relPath.split(path.sep);
  const topLevelDir = parts.length > 1 ? parts[0] : 'uncategorized';
  let seriesName = null;
  if (topLevelDir === 'series' && parts.length > 2) {
    seriesName = parts[1]; // e.g. transformers
  }
  
  const markdown = fs.readFileSync(filePath, 'utf-8');
  
  // Extract title
  const titleMatch = markdown.match(/^#\s+(.+)/m);
  const title = titleMatch ? titleMatch[1].trim() : 'Untitled Post';
  
  const body = markdown.replace(/^#\s+(.+)/m, '').trim();
  const paragraphs = body.split(/\n\s*\n/);
  let summary = '';

  const summaryMatch = body.match(/<!--\s*SUMMARY:\s*([\s\S]*?)\s*-->/i);
  if (summaryMatch) {
    summary = summaryMatch[1].replace(/\n/g, ' ').trim();
  } else {
    for (const p of paragraphs) {
      if (!p.startsWith('#') && !p.startsWith('!') && !p.startsWith('<') && p.trim().length > 0) {
        summary = p.replace(/\[([^\]]+)\]\([^\)]+\)/g, '$1') 
                   .replace(/[*_~`]/g, '')
                   .replace(/\n/g, ' ')
                   .trim();
        break;
      }
    }
  }
  
  let mathBlocks = [];
  let processedMarkdown = markdown.replace(/\$\$([\s\S]*?)\$\$/g, (match) => {
      mathBlocks.push(match);
      return `MATHBLOCKREPLACEMENT${mathBlocks.length - 1}`;
  });
  processedMarkdown = processedMarkdown.replace(/\$([^\n$]+)\$/g, (match) => {
      mathBlocks.push(match);
      return `MATHINLINEREPLACEMENT${mathBlocks.length - 1}`;
  });

  let contentHtml = marked.parse(processedMarkdown);

  contentHtml = contentHtml.replace(/MATHBLOCKREPLACEMENT(\d+)/g, (match, i) => {
      return mathBlocks[i];
  });
  contentHtml = contentHtml.replace(/MATHINLINEREPLACEMENT(\d+)/g, (match, i) => {
      return mathBlocks[i];
  });
  
  let tierDisplay = topLevelDir.charAt(0).toUpperCase() + topLevelDir.slice(1).replace(/-/g, ' ');
  let breadcrumbHtml = `<nav aria-label="breadcrumb" class="breadcrumbs"><ol>
    <li><a href="../index.html">Home</a></li>
    <li><a href="index.html">Blog</a></li>`;
    
  let tabId = 'tab-perspectives';
  if (topLevelDir === 'series') tabId = 'tab-series';
  if (topLevelDir === 'validation-and-benchmarks') tabId = 'tab-methodology';

  if (topLevelDir === 'series' && seriesName) {
      let seriesDisplay = seriesName.charAt(0).toUpperCase() + seriesName.slice(1).replace(/-/g, ' ');
      breadcrumbHtml += `<li><a href="index.html#${tabId}">Series: ${seriesDisplay}</a></li>`;
  } else if (topLevelDir !== 'uncategorized') {
      breadcrumbHtml += `<li><a href="index.html#${tabId}">${tierDisplay}</a></li>`;
  }
  
  breadcrumbHtml += `<li aria-current="page">${title}</li></ol></nav>`;

  let outFilename = fileObj.name.replace('.md', '.html');
  if (seriesName) {
    outFilename = `${seriesName}-${outFilename}`;
  }
  
  postsData.push({
    title,
    summary,
    url: outFilename,
    tier: topLevelDir,
    seriesName: seriesName,
    contentHtml,
    breadcrumbHtml
  });
}

postsData.sort((a, b) => {
    if (a.tier !== b.tier) return a.tier.localeCompare(b.tier);
    if (a.seriesName !== b.seriesName) {
        if (!a.seriesName) return 1;
        if (!b.seriesName) return -1;
        return a.seriesName.localeCompare(b.seriesName);
    }
    const aName = path.basename(a.url).toLowerCase();
    const bName = path.basename(b.url).toLowerCase();
    if (aName.includes('preface') && !bName.includes('preface')) return -1;
    if (bName.includes('preface') && !aName.includes('preface')) return 1;
    return aName.localeCompare(bName);
});

const posts = [];
for (let i = 0; i < postsData.length; i++) {
  const post = postsData[i];
  const prevPost = i > 0 ? postsData[i - 1] : null;
  const nextPost = i < postsData.length - 1 ? postsData[i + 1] : null;

  let paginationHtml = '<div class="blog-pagination">';
  if (prevPost) {
    paginationHtml += `
      <a href="${prevPost.url}" class="pagination-link prev">
        <span class="pagination-label">Previous</span>
        <span class="pagination-title">${prevPost.title}</span>
      </a>`;
  } else {
    paginationHtml += `<div style="flex: 1;"></div>`;
  }
  
  if (nextPost) {
    paginationHtml += `
      <a href="${nextPost.url}" class="pagination-link next">
        <span class="pagination-label">Next</span>
        <span class="pagination-title">${nextPost.title}</span>
      </a>`;
  } else {
    paginationHtml += `<div style="flex: 1;"></div>`;
  }
  paginationHtml += '</div>';

  if (!prevPost && !nextPost) {
      paginationHtml = '';
  }

  const finalHtml = templateHtml
    .replace('{{TITLE}}', () => post.title)
    .replace('{{BREADCRUMBS}}', () => post.breadcrumbHtml)
    .replace('{{CONTENT}}', () => post.contentHtml)
    .replace('{{PAGINATION}}', () => paginationHtml)
    .replace('{{SERIES_CLASS}}', () => post.seriesName ? `series-${post.seriesName}` : '');
    
  const outPath = path.join(BLOG_DIR, post.url);
  fs.writeFileSync(outPath, finalHtml, 'utf-8');
  console.log(`Generated blog post: ${post.url}`);
  
  posts.push({
    title: post.title,
    summary: post.summary,
    url: post.url,
    tier: post.tier,
    seriesName: post.seriesName
  });
}

// Update index
if (posts.length > 0) {
    let indexHtml = fs.readFileSync(INDEX_PATH, 'utf-8');
    
    // Group posts
    const perspectives = posts.filter(p => p.tier === 'perspectives');
    const methodology = posts.filter(p => p.tier === 'validation-and-benchmarks');
    const seriesPosts = posts.filter(p => p.tier === 'series');
    const uncategorized = posts.filter(p => p.tier === 'uncategorized');
    
    // Group series by seriesName
    const seriesGroups = {};
    for (const p of seriesPosts) {
      if (!seriesGroups[p.seriesName]) seriesGroups[p.seriesName] = [];
      seriesGroups[p.seriesName].push(p);
    }
    
    function renderStandardList(list) {
        if (list.length === 0) return '<p style="text-align: center; color: var(--text-muted); font-style: italic;">No posts yet in this category.</p>';
        return list.map(post => `
        <a href="${post.url}">
            <article class="blog-item">
                <h2>${post.title}</h2>
                <p>${post.summary}</p>
            </article>
        </a>`).join('');
    }
    
    let perspectivesHtml = renderStandardList([...perspectives, ...uncategorized]);
    let methodologyHtml = renderStandardList(methodology);
    
    let seriesHtml = '';
    if (Object.keys(seriesGroups).length === 0) {
       seriesHtml = '<p style="text-align: center; color: var(--text-muted); font-style: italic;">No series available yet.</p>';
    } else {
       for (const [sName, sPosts] of Object.entries(seriesGroups)) {
          const seriesTitle = sName.charAt(0).toUpperCase() + sName.slice(1).replace(/-/g, ' ');
          seriesHtml += `
          <div class="series-group">
              <h3 class="series-title">${seriesTitle}</h3>
              <div class="series-items">
                  ${sPosts.map(post => `
                  <a href="${post.url}">
                      <article class="blog-item series-item">
                          <h2>${post.title}</h2>
                          <p>${post.summary}</p>
                      </article>
                  </a>`).join('')}
              </div>
          </div>`;
       }
    }
    
    const blogListHtml = `
        <div class="blog-tabs">
            <input type="radio" id="tab-perspectives" name="blog-tabs" checked>
            <label for="tab-perspectives" class="tab-label">Perspectives</label>
            
            <input type="radio" id="tab-series" name="blog-tabs">
            <label for="tab-series" class="tab-label">Series</label>
            
            <input type="radio" id="tab-methodology" name="blog-tabs">
            <label for="tab-methodology" class="tab-label">Validation & Benchmarks</label>
            
            <div class="tab-content" id="content-perspectives">
                <p class="tab-desc">Observations on the evolving landscape of technical enablement, exploring how architectural shifts and emerging tools influence the craft of documentation.</p>
                ${perspectivesHtml}
            </div>
            
            <div class="tab-content" id="content-series">
                <p class="tab-desc">Sequential explorations born from personal curiosity. These collections document my process of deconstructing complex systems and sharing the resulting insights.</p>
                ${seriesHtml}
            </div>
            
            <div class="tab-content" id="content-methodology">
                <p class="tab-desc">Empirical investigations designed to resolve complex architectural questions through rigorous data analysis. Every benchmark is supported by a public repository so you can clone the infrastructure, run the tests, and independently reproduce the findings.</p>
                ${methodologyHtml}
            </div>
        </div>`;
        
    indexHtml = indexHtml.replace(
        /<!-- BLOG_LIST_START -->[\s\S]*?<!-- BLOG_LIST_END -->/,
        `<!-- BLOG_LIST_START -->\n${blogListHtml}\n        <!-- BLOG_LIST_END -->`
    );
    
    fs.writeFileSync(INDEX_PATH, indexHtml, 'utf-8');
    console.log(`Updated blog index with ${posts.length} articles.`);
} else {
    console.log("No markdown files found in blog/content/.");
}
