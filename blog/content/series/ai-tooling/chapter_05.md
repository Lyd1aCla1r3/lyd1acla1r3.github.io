# Data Infrastructure

<!-- SUMMARY: An examination of the data storage and preparation layers supporting retrieval-augmented generation, covering five vector database implementations for semantic search and four knowledge management pipelines for parsing and structuring raw documents. -->

Gateways and routers handle connectivity between applications and model providers. Generating accurate, grounded responses requires a second category of infrastructure: systems that store, index, and prepare the data that models retrieve at query time. This post covers two tightly coupled layers of that data infrastructure.

<style>
.eco-profile-panel {
    border: 1.5px solid rgba(183,110,121,0.18);
    border-radius: 10px;
    padding: 14px 22px 18px 22px;
    margin-bottom: 1.5rem;
    background: rgba(255,255,255,0.85);
    transition: border-color 0.3s ease, background 0.3s ease;
}
.eco-profile-panel .post-tab-content h3 {
    margin-top: 0 !important;
}
.eco-profile-panel .post-tab-content.active {
    padding-top: 0;
}
</style>

<script>
var _ecoVectorColors = {
    'pinecone':  { border: 'rgba(183,110,121,0.35)', bg: 'rgba(251,243,244,0.6)' },
    'qdrant':    { border: 'rgba(192,120,136,0.35)', bg: 'rgba(251,241,243,0.6)' },
    'chroma':    { border: 'rgba(192,136,104,0.35)', bg: 'rgba(251,244,239,0.6)' },
    'weaviate':  { border: 'rgba(184,144,40,0.35)',  bg: 'rgba(252,247,236,0.6)' },
    'pgvector':  { border: 'rgba(168,104,104,0.35)', bg: 'rgba(250,241,239,0.6)' }
};
var _ecoKmColors = {
    'llamaparse':   { border: 'rgba(183,110,121,0.35)', bg: 'rgba(251,243,244,0.6)' },
    'unstructured': { border: 'rgba(192,120,136,0.35)', bg: 'rgba(251,241,243,0.6)' },
    'docling':      { border: 'rgba(192,136,104,0.35)', bg: 'rgba(251,244,239,0.6)' },
    'firecrawl':    { border: 'rgba(184,144,40,0.35)',  bg: 'rgba(252,247,236,0.6)' }
};

function _ecoBindPanel(panelId, colorMap) {
    var panel = document.getElementById(panelId);
    if (!panel) return;
    var btns = panel.parentElement.querySelectorAll('[data-tab]');
    btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var key = this.getAttribute('data-tab');
            var colors = colorMap[key];
            if (colors && panel) {
                panel.style.borderColor = colors.border;
                panel.style.background = colors.bg;
            }
        });
    });
    var keys = Object.keys(colorMap);
    if (keys.length > 0) {
        var firstColors = colorMap[keys[0]];
        if (firstColors && panel) {
            panel.style.borderColor = firstColors.border;
            panel.style.background = firstColors.bg;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    _ecoBindPanel('eco-vector-panel', _ecoVectorColors);
    _ecoBindPanel('eco-km-panel', _ecoKmColors);
});
</script>

## Vector Databases

Traditional databases search by exact matching: SQL `WHERE` clauses, keyword indexes, structured queries. This works for data with known schemas and precise lookup requirements. However, language is ambiguous. A search for "machine learning deployment best practices" should match documents about "ML model serving," "putting models into production," and "inference optimization," even if none of those documents contain the exact phrase "machine learning deployment best practices."

Vector databases solve this by storing mathematical representations of meaning. When a piece of text is processed by an embedding model, a neural network trained to convert text into a high-dimensional numerical vector, the resulting vector captures the semantic content of the text. Similar meanings produce vectors that are close together in the embedding space. A vector database indexes these vectors using approximate nearest neighbor (ANN) algorithms and retrieves the closest matches in milliseconds, enabling search by meaning rather than by keyword. The primary use case driving adoption is Retrieval-Augmented Generation (RAG): before generating a response, the system retrieves relevant context from a vector database and includes it in the prompt, grounding the model's output in actual source material rather than relying on the model's training data alone.

The five implementations below cover the main architectural approaches: fully managed cloud like Pinecone, self-hosted high-performance engines like Qdrant and Weaviate, developer-first embedded databases like Chroma, and adding vector search to an existing relational database via pgvector.

<div data-tab-group="vectordbs">
  <div class="post-tabs">
    <button class="post-tab-btn active" data-tab="pinecone">Pinecone</button>
    <button class="post-tab-btn" data-tab="qdrant">Qdrant</button>
    <button class="post-tab-btn" data-tab="chroma">Chroma</button>
    <button class="post-tab-btn" data-tab="weaviate">Weaviate</button>
    <button class="post-tab-btn" data-tab="pgvector">pgvector</button>
  </div>

  <div class="eco-profile-panel" id="eco-vector-panel">

  <div class="post-tab-content active" data-tab-content="pinecone">
    <h3>Pinecone</h3>
    <p><strong>Maker:</strong> Pinecone Systems, Inc.<br><strong>Hosting:</strong> Fully managed SaaS (no self-hosted option)</p>
    <p>Pinecone is a fully managed, cloud-native vector database with a serverless architecture. Serverless means the database scales compute resources up automatically during heavy query loads and scales them to zero when idle, ensuring users do not pay for idle infrastructure. It supports dense vectors that capture conceptual meaning and sparse vectors that capture exact keyword matches. Hybrid search fuses these two types, allowing a query to find documents that match both the exact keyword and the broader concept. Pinecone handles metadata filtering, for example, restricting a search to documents tagged "HR", alongside logical partitioning via namespaces, grouping documents by customer ID to guarantee data separation in multi-tenant systems. Pinecone is the simplest to operate since it is proprietary with no self-hosted option. Users do not perform index tuning, the manual configuration of memory limits and disk flushing behavior required by self-hosted databases to optimize performance. Pinecone integrates with LangChain, LlamaIndex, Haystack, Semantic Kernel, and embedding providers including OpenAI, Cohere, and Hugging Face.</p>
    <p><em>Pricing: Uses a consumption-based serverless model billing for storage and read/write units, with a free tier available for development.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="qdrant">
    <h3>Qdrant</h3>
    <p><strong>Maker:</strong> Qdrant Solutions GmbH<br><strong>Hosting:</strong> Self-hosted (Apache 2.0) or managed cloud</p>
    <p>Qdrant is an open-source vector search engine written in Rust. Its distinguishing technical feature is single-stage payload filtering. Vector search works as follows: the database builds a map of vectors called a Hierarchical Navigable Small World (HNSW) graph, connecting similar concepts together. When a query arrives, the search algorithm traverses this graph, hopping from node to node to find the closest matches. Often, a search requires filtering, for example, searching for "vacation policies" while filtering to only show documents from the "engineering" department. If a database applies this filter <em>before</em> searching the graph, known as pre-filtering, it frequently eliminates the vast majority of the index. The remaining valid points are now scattered so far apart that the graph traversal algorithm gets lost and fails to find them. If it searches first and filters later, known as post-filtering, it frequently retrieves ten results, applies the filter, and discards all ten, returning nothing. Qdrant avoids both problems by evaluating the metadata filter <em>during</em> the graph traversal. As the algorithm explores the map, it simply ignores paths that do not match the filter, ensuring it finds enough valid results without getting lost. It supports cosine, Euclidean, dot product, and Manhattan distance metrics, and offers scalar, product, and binary quantization for reducing memory consumption by up to 95%. Qdrant integrates with LangChain, LlamaIndex, Haystack, CrewAI, and includes FastEmbed, an in-house embedded vectorizer for zero-dependency embedding generation.</p>
    <p><em>Pricing: The core engine is free and open-source. The managed cloud offers a perpetual free tier, transitioning to capacity-based pricing for production.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="chroma">
    <h3>Chroma</h3>
    <p><strong>Maker:</strong> Chroma Inc.<br><strong>Hosting:</strong> In-process embedded, standalone server, or managed cloud (Apache 2.0)</p>
    <p>Chroma is an open-source embedding database designed for developer simplicity. It runs embedded directly inside a Python or JavaScript process using local disk persistence with no separate server, Docker container, or configuration required, making it the fastest option for local prototyping and testing. A developer can add vector search to an existing application with a few lines of code and no infrastructure changes. Chroma also provides automated embedding functions that convert raw text to vectors upon ingestion using integrated embedding wrappers, eliminating a separate embedding pipeline. Rich metadata filtering supports logical operators for precise result filtering. The same code transitions to a standalone client-server deployment or Chroma Cloud without changes. Chroma integrates with LangChain, LlamaIndex, Semantic Kernel, and the OpenAI Assistants API.</p>
    <p><em>Pricing: The open-source version is free to self-host. A managed cloud service is available for production workloads.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="weaviate">
    <h3>Weaviate</h3>
    <p><strong>Maker:</strong> Weaviate B.V.<br><strong>Type:</strong> AI-native vector search engine (open-source, BSD-3-Clause)</p>
    <p>Weaviate differentiates itself as an AI-native database that handles both the data and the embedding process. Rather than requiring the developer to chunk text, send it to OpenAI for embedding, and then store the vector, Weaviate's "vectorizer" modules handle the embedding automatically during data ingestion. It supports multi-tenant data isolation at the shard level, making it well suited for enterprise SaaS applications that must strictly separate customer data. It provides native modules for LangChain, LlamaIndex, and direct integration with OpenAI and Anthropic embedding APIs.</p>
    <p><em>Pricing: The open-source core is free. The managed cloud uses a consumption-based serverless model, with dedicated enterprise tiers available.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="pgvector">
    <h3>pgvector</h3>
    <p><strong>Maker:</strong> Andrew Kane / PostgreSQL Community<br><strong>Type:</strong> PostgreSQL extension (open-source, PostgreSQL License)</p>
    <p>For organizations that already use PostgreSQL, pgvector adds vector similarity search directly into the relational database. It supports exact and approximate nearest neighbor search via HNSW and IVFFlat algorithms using L2 distance, inner product, and cosine distance. It inherits ACID compliance, point-in-time recovery, and role-based access control by leveraging PostgreSQL's battle-tested infrastructure. Supported by nearly every major cloud SQL provider like AWS RDS, Google Cloud SQL, Supabase, and Neon, it is the default choice for teams that want to avoid adding a new vendor to their tech stack. It integrates directly with LangChain, LlamaIndex, and standard ORMs like SQLAlchemy.</p>
    <p><em>Pricing: The extension is completely free and open-source, with infrastructure costs dependent on your existing PostgreSQL hosting provider.</em></p>
  </div>

  </div>
</div>

**When to choose which**: The decision between a dedicated vector database and a vector extension depends on scale, consistency requirements, and operational complexity. Teams with existing PostgreSQL infrastructure, datasets under 50 million vectors, and strong ACID requirements often find pgvector sufficient, avoiding the operational overhead of a separate system. Teams with datasets exceeding 100 million vectors, extreme throughput requirements, such as thousands of concurrent searches per second, or multimodal search needs typically benefit from a purpose-built vector database that is architecturally optimized for these workloads.

## Knowledge Management Pipelines

The previous sections assume clean, well-structured text that is ready for embedding and retrieval. In practice, the data that organizations need to make searchable rarely arrives in that form. Internal documentation lives in PDFs with multi-column layouts, embedded tables, and scanned images. Technical references are scattered across Confluence pages, Google Docs, and Notion databases. Product specifications exist as PowerPoint decks with diagrams. Customer communications sit in email threads and Slack archives.

Knowledge management pipelines handle the ingestion, parsing, and preparation of these messy source materials into clean, structured content that vector databases can index and LLM applications can retrieve.

The pipeline has two distinct phases. **Parsing** is the extraction phase: interpreting binary or markup encodings like PDF byte streams, DOCX XML, and HTML DOM; recognizing structural features like headings, tables, reading order, and embedded images; and producing a clean intermediate representation, typically Markdown or structured JSON. **Chunking** is the segmentation phase: dividing the parsed output into bounded segments that fit within embedding model token limits while preserving semantic coherence. The main chunking strategies are fixed-size, splitting by character or token count for a simple but structure-unaware approach; recursive, splitting by hierarchical delimiters like paragraph breaks and then sentence breaks; semantic, splitting where embedding similarity between adjacent blocks drops below a threshold; and document-structure-aware, splitting at heading and section boundaries to preserve the document's logical hierarchy.

<div data-tab-group="knowledge">
  <div class="post-tabs">
    <button class="post-tab-btn active" data-tab="llamaparse">LlamaParse</button>
    <button class="post-tab-btn" data-tab="unstructured">Unstructured</button>
    <button class="post-tab-btn" data-tab="docling">Docling</button>
    <button class="post-tab-btn" data-tab="firecrawl">Firecrawl</button>
  </div>

  <div class="eco-profile-panel" id="eco-km-panel">

  <div class="post-tab-content active" data-tab-content="llamaparse">
    <h3>LlamaParse</h3>
    <p><strong>Maker:</strong> LlamaIndex, Inc.<br><strong>Type:</strong> Managed cloud parsing service (proprietary)</p>
    <p>The core problem with documents like PDFs or PowerPoints is that they contain complex visual layouts: multi-column text, intricate tables, charts, and embedded images. Traditional text extractors blindly read left-to-right, turning tables and columns into unreadable word salad. LlamaParse solves this by using vision-language models, which are AI models that can "see". It looks at the document exactly like a human does, visually recognizing the layout and accurately recreating tables, charts, and reading orders as clean text like Markdown that the LLM can perfectly understand.</p>
    <p><em>Pricing: It uses a credit-based system depending on the complexity of the page, offering a free tier with paid upgrades for high volume and enterprise deployments.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="unstructured">
    <h3>Unstructured</h3>
    <p><strong>Maker:</strong> Unstructured Technologies, Inc.<br><strong>Type:</strong> Document ETL platform (open-source core, Apache 2.0)</p>
    <p>Enterprise data rarely lives in a single folder of PDFs. It is scattered across Slack, Salesforce, SharePoint, Confluence, and Amazon S3 buckets. Unstructured solves this fragmentation as an Extract, Transform, Load (ETL) platform. It provides over 40 pre-built "connectors", known as native integrations, that automatically reach into these enterprise tools, fetch the data, strip out the garbage such as watermarks, footers, and boilerplate navigation, and transform it all into one clean, standardized format.</p>
    <p><em>Pricing: The core Python library is free and open-source. The managed API offers a free tier for initial usage, transitioning to pay-as-you-go per page, with custom pricing for enterprise setups.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="docling">
    <h3>Docling</h3>
    <p><strong>Maker:</strong> IBM Research / LF AI and Data Foundation<br><strong>Type:</strong> Local document intelligence library (open-source, MIT License)</p>
    <p>Cloud parsers like LlamaParse and Unstructured's API require sending your documents over the internet. For organizations handling proprietary code, medical records, or classified data, this data egress is unacceptable. Docling solves this by bringing the intelligence entirely local. Built by IBM, it is an open-source library that runs its own specialized, compact vision models directly on your laptop or private server. It can accurately extract complex table grids and formulas without a single byte of data ever leaving your machine.</p>
    <p><em>Pricing: The open-source version is completely free to use and self-host. IBM offers a managed cloud version on watsonx priced per thousand pages.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="firecrawl">
    <h3>Firecrawl</h3>
    <p><strong>Maker:</strong> Mendable.ai<br><strong>Type:</strong> Web scraping and crawling platform (open-source, AGPL-3.0)</p>
    <p>Websites are no longer static text pages; they are complex JavaScript applications hidden behind cookie banners, email popups, and anti-bot protection. A standard web scraper will just hit a blank loading screen. Firecrawl solves this by spinning up actual, headless web browsers in the cloud. It visits the page, clicks past the popups, waits for the JavaScript to finish rendering, and extracts the clean text, stripping away the ads and navigation menus so the LLM only reads the actual content.</p>
    <p><em>Pricing: Free to self-host, though organizations must manage the browser infrastructure themselves. The managed cloud version offers a free tier with flat-rate monthly subscriptions for higher volumes.</em></p>
  </div>

  </div>
</div>

The next post examines runtime infrastructure, covering model serving engines, fine-tuning platforms, and observability tools.

## References

1. Pinecone Documentation, Pinecone Systems Inc.
2. Qdrant Documentation, Qdrant Solutions GmbH.
3. Chroma Documentation, Chroma Inc.
4. Weaviate Documentation, Weaviate B.V.
5. pgvector, Andrew Kane and PostgreSQL Community.
6. LlamaParse Documentation, LlamaIndex Inc.
7. Unstructured Documentation, Unstructured Technologies Inc.
8. Docling Documentation, IBM Research and LF AI and Data Foundation.
9. Firecrawl Documentation, Mendable.ai.
