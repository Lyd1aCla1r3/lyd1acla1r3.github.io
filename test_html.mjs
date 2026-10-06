import fs from 'fs';
import MarkdownIt from 'markdown-it';
import mathjax3 from 'markdown-it-mathjax3';
const md = new MarkdownIt({ html: true });
md.use(mathjax3);
console.log(md.render("This is a test: <span style=\"white-space: nowrap\">$x = 5$)</span>"));
