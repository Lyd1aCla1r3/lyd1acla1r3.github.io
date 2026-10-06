const { marked } = require('marked');
const md = `
\`\`\`mermaid
graph LR
    A --> B

    B --> C
\`\`\`
`;
console.log(marked.parse(md));
