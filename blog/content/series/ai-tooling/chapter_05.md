# Data Infrastructure

<!-- SUMMARY: An examination of the data storage and preparation layers supporting retrieval-augmented generation, covering five vector database implementations for semantic search and four knowledge management pipelines for parsing and structuring raw documents. -->

[Connectivity and Routing](ai-tooling-chapter_04.html) examined protocol layers connecting applications to external tools and model providers. Generating accurate, grounded responses requires a second category of infrastructure: systems that store, index, and prepare the data that models retrieve at query time. This chapter covers two tightly coupled layers of that data infrastructure.

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

Traditional relational databases retrieve records through deterministic predicate matching: SQL `WHERE` clauses, B-tree indexes, and lexical keyword lookups. Deterministic matching succeeds when schemas are fixed and queries use canonical terms. Natural language queries rarely share identical vocabulary with their target documents. A query for "machine learning deployment best practices" targets documents covering "ML model serving," "production inference pipelines," and "GPU latency optimization," even when those documents omit the literal query string.

Vector databases resolve vocabulary mismatch by indexing dense mathematical representations of meaning. An embedding model projects text segments into a high-dimensional coordinate space where semantically related passages cluster at small geometric distances (measured via cosine similarity, Euclidean L2 distance, or inner product).

At query time, the database executes Approximate Nearest Neighbor (ANN) search over the indexed vectors to return the top-k closest passages in milliseconds. Retrieval-Augmented Generation (RAG) relies on this retrieval primitive: before calling a language model, the application queries the vector index for relevant source passages and injects them into the prompt context, grounding generation in verifiable source documents rather than parametric model memory alone.

The five implementations below represent the primary architectural patterns in production: serverless cloud-native indexes (Pinecone), self-hosted Rust and Go search engines with integrated filtering and vectorization (Qdrant, Weaviate), embedded local-first stores (Chroma), and relational database vector extensions (pgvector).

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
    <p>Pinecone is a cloud-native, fully managed vector database built around a disaggregated serverless storage and compute architecture. Compute nodes scale automatically with query concurrency and scale down during idle periods without manual shard or memory provisioning. The index engine supports both dense semantic vectors and sparse lexical vectors (such as BM25 or SPLADE representations), fusing both scores in a single hybrid query to capture semantic intent alongside domain-specific identifiers, part numbers, or acronyms.</p>
    <p>Multi-tenant data isolation relies on logical namespaces that partition customer records within a single index without cross-tenant leakage, paired with structured metadata predicates for scoped retrieval. The proprietary SaaS model trades infrastructure portability for zero-maintenance index tuning. Native integrations span LangChain, LlamaIndex, Haystack, Semantic Kernel, and major embedding providers.</p>
    <p><em>Pricing: Uses consumption-based serverless billing across storage volume and read/write request units, with a free starter tier.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="qdrant">
    <h3>Qdrant</h3>
    <p><strong>Maker:</strong> Qdrant Solutions GmbH<br><strong>Hosting:</strong> Self-hosted (Apache 2.0) or managed cloud</p>
    <p>Qdrant is a high-performance open-source vector search engine implemented in Rust. Its core architectural differentiator is single-stage filtered Hierarchical Navigable Small World (HNSW) traversal. Standard HNSW indexes organize vectors into a multi-layer proximity graph navigated via greedy neighbor hops. Applying restrictive metadata predicates prior to graph search (pre-filtering) severs graph connectivity and degrades recall, whereas filtering only after retrieving the top-k candidates (post-filtering) frequently discards all returned matches when predicates are selective.</p>
    <p>Qdrant resolves this trade-off through condition-aware graph traversal: secondary payload indexes link directly to HNSW graph nodes so metadata predicates are evaluated inline during neighbor expansion, preserving graph reachability and recall under arbitrary filter selectivity. The engine supports cosine, Euclidean, dot-product, and Manhattan metrics, alongside scalar, product, and binary quantization that compress in-memory vector footprints by up to 95%. Native integrations include LangChain, LlamaIndex, Haystack, CrewAI, and FastEmbed for local embedding generation.</p>
    <p><em>Pricing: The Apache 2.0 engine is free to self-host. Qdrant Cloud provides a permanent free tier and capacity-based production clusters.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="chroma">
    <h3>Chroma</h3>
    <p><strong>Maker:</strong> Chroma Inc.<br><strong>Hosting:</strong> In-process embedded, standalone server, or managed cloud (Apache 2.0)</p>
    <p>Chroma is an open-source embedding database architected for zero-configuration local prototyping and embedded workflows. The engine runs in-process inside a Python or JavaScript runtime backed by local SQLite and HNSW persistence, requiring no external daemon, container orchestration, or cluster configuration to start indexing documents.</p>
    <p>Integrated embedding wrappers automatically vectorize raw text upon insertion and query execution, and metadata predicates combine with full-text regular expression filters. Applications promote the identical client API from local in-memory or disk-backed storage to a standalone client-server deployment or Chroma Cloud. Integrations cover LangChain, LlamaIndex, and Semantic Kernel.</p>
    <p><em>Pricing: The open-source library and server are free under Apache 2.0, with managed cloud hosting available for production workloads.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="weaviate">
    <h3>Weaviate</h3>
    <p><strong>Maker:</strong> Weaviate B.V.<br><strong>Type:</strong> AI-native vector search engine (open-source, BSD-3-Clause)</p>
    <p>Weaviate is an open-source vector search engine written in Go that integrates modular vectorization and hybrid retrieval directly into the storage layer. Built-in vectorizer modules automatically transform ingested objects into embeddings via external APIs or local transformer containers, and native BM25 inverted indexes combine with HNSW vector graphs via reciprocal rank fusion.</p>
    <p>For multi-tenant SaaS architectures, Weaviate isolates each tenant onto dedicated storage shards that can be independently loaded into memory, offloaded to warm object storage, or deleted for compliance without impacting co-located tenants. Integrations include LangChain, LlamaIndex, and GraphQL/gRPC client SDKs.</p>
    <p><em>Pricing: The BSD-3-Clause core is free to self-host. Weaviate Cloud offers serverless consumption billing and dedicated enterprise clusters.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="pgvector">
    <h3>pgvector</h3>
    <p><strong>Maker:</strong> Andrew Kane / PostgreSQL Community<br><strong>Type:</strong> PostgreSQL extension (open-source, PostgreSQL License)</p>
    <p>pgvector extends PostgreSQL with native vector data types and similarity indexing inside the relational database engine. It supports exhaustive brute-force (<code>flat</code> scan) search for 100% recall alongside Approximate Nearest Neighbor indexing via <code>HNSW</code> graphs and <code>IVFFlat</code> inverted lists across L2, inner-product, and cosine distance operators.</p>
    <p>Storing embeddings alongside relational columns in a single PostgreSQL instance preserves transactional ACID guarantees, write-ahead log (WAL) point-in-time recovery, relational <code>JOIN</code> semantics, and row-level security without synchronizing an external vector store. Every major managed PostgreSQL platform (AWS RDS, Google Cloud SQL, Azure Database, Supabase, and Neon) ships the extension natively.</p>
    <p><em>Pricing: Free and open-source under the PostgreSQL License; compute and storage costs follow the underlying PostgreSQL host.</em></p>
  </div>

  </div>
</div>

### Vector Database Architectural Comparison

The five implementations span four deployment topologies, trading operational simplicity against index control and transactional consistency.

| Database | Deployment Model | Index & Filtering Architecture | Multi-Tenancy Boundary | Primary Workload Fit |
| :--- | :--- | :--- | :--- | :--- |
| **Pinecone** | Managed Serverless SaaS | Disaggregated storage/compute with hybrid dense-sparse fusion | Logical namespaces | Zero-ops cloud scale and hybrid lexical-semantic search |
| **Qdrant** | Self-hosted (`Apache 2.0`) or Cloud | Rust `HNSW` with single-stage inline payload filtering | Payload-filtered or shard-isolated | High-selectivity metadata filtering and quantized memory efficiency |
| **Chroma** | Embedded in-process (`Apache 2.0`) or Cloud | Local SQLite + `HNSW` with integrated embedding wrappers | Collection-level separation | Local prototyping, embedded apps, and small-to-medium corpora |
| **Weaviate** | Self-hosted (`BSD-3`) or Cloud | Go `HNSW` + inverted `BM25` index with built-in vectorizers | Dedicated physical shards per tenant | Multi-tenant SaaS requiring strict tenant shard lifecycle isolation |
| **pgvector** | PostgreSQL extension (`PostgreSQL`) | Relational table storage with `HNSW` and `IVFFlat` indexes | Row-level security (`RLS`) and schemas | Existing PostgreSQL stacks (<50M vectors) requiring `ACID` joins |

Selecting between a relational vector extension and a dedicated vector engine depends on corpus scale, transactional requirements, and filter selectivity. Engineering teams operating PostgreSQL with datasets under 50 million vectors and strict `ACID` relational join requirements standardize on **pgvector** to avoid synchronizing a second datastore. Workloads exceeding 100 million vectors, requiring sub-10ms tail latency under high concurrency, or enforcing selective metadata predicates or per-tenant shard offloading benefit from purpose-built engines such as **Qdrant**, **Pinecone**, or **Weaviate**.

## Knowledge Management Pipelines

The previous sections assume clean, well-structured text that is ready for embedding and retrieval. Production enterprise corpora rarely arrive in that form. Internal documentation resides in PDFs with multi-column layouts, embedded tables, and scanned figures. Technical specifications span Confluence pages, Google Docs, Notion databases, and slide decks. Customer communications sit in email threads and chat archives.

Knowledge management pipelines handle the ingestion, structural extraction, and segmentation of raw source artifacts into normalized representations that vector databases can index and language models can reason over.

### Parsing and Chunking Phases

The pipeline separates into two sequential phases. **Parsing** is the extraction phase: decoding binary or markup formats (PDF byte streams, DOCX XML trees, HTML DOM graphs), reconstructing spatial reading order, headings, and multi-column table grids, and emitting a normalized intermediate representation in Markdown or structured JSON. **Chunking** is the segmentation phase: partitioning the parsed representation into bounded segments that fit within embedding context limits while preserving local semantic coherence.

Production retrieval pipelines rely on four core chunking strategies:

- **Fixed-Size Token Splitting:** Partitions text strictly by character or token count with a sliding overlap window, providing deterministic segment sizes at the cost of splitting mid-sentence or mid-table.
- **Recursive Delimiter Splitting:** Divides text along a prioritized hierarchy of structural separators (double newlines, single newlines, sentence boundaries, and whitespace) to keep paragraphs intact wherever token limits permit.
- **Semantic Similarity Splitting:** Computes sentence-level embeddings and inserts chunk boundaries where cosine similarity between adjacent sentences drops below a configured threshold, grouping topically cohesive sentences together.
- **Document-Structure-Aware Splitting:** Aligns chunk boundaries with explicit AST or markup landmarks (Markdown headers, HTML section tags, table blocks, and code fences) and attaches parent section headers as chunk metadata.

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
    <p>Complex enterprise documents such as financial filings, academic PDFs, and slide decks interleave multi-column text, nested tables, mathematical equations, and embedded figures. Heuristic PDF text extractors read raw character coordinates left-to-right across page boundaries, corrupting column reading order and flattening tabular relationships.</p>
    <p>LlamaParse resolves layout corruption through multimodal Vision-Language Model (VLM) page reconstruction. The parser evaluates visual page geometry alongside underlying text layers to reconstruct nested tables, charts, and hierarchical sections into clean Markdown or JSON tailored for downstream RAG indexing.</p>
    <p><em>Pricing: Uses a page-credit billing model scaled by extraction mode complexity, with a free daily page allocation and enterprise tiers.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="unstructured">
    <h3>Unstructured</h3>
    <p><strong>Maker:</strong> Unstructured Technologies, Inc.<br><strong>Type:</strong> Document ETL platform (open-source core, Apache 2.0)</p>
    <p>Enterprise knowledge rarely resides in a single local directory; source records span collaboration suites, ticketing systems, cloud object storage buckets, and internal wikis. Unstructured addresses multi-source ingestion as an Extract, Transform, Load (ETL) platform for unstructured data.</p>
    <p>Pre-built source and destination connectors pull raw documents from enterprise systems, classify document layout elements (<code>Title</code>, <code>NarrativeText</code>, <code>Table</code>, <code>ListItem</code>), strip repeating headers, footers, and navigation boilerplate, and emit normalized JSON elements ready for chunking and embedding.</p>
    <p><em>Pricing: The core Python library is free and open-source. The managed platform offers a free tier, per-page consumption pricing, and enterprise VPC deployments.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="docling">
    <h3>Docling</h3>
    <p><strong>Maker:</strong> IBM Research / LF AI and Data Foundation<br><strong>Type:</strong> Local document intelligence library (open-source, MIT License)</p>
    <p>Cloud-hosted parsing APIs require transmitting raw source documents over external networks. Organizations governed by strict data residency, healthcare privacy, or air-gapped security policies require local document extraction with zero external data egress.</p>
    <p>Docling executes layout analysis and table structure reconstruction entirely on local CPU or GPU hardware. Built by IBM Research, the library runs compact, specialized vision models (<code>DocLayNet</code> layout detectors and <code>TableFormer</code> table-structure models) in-process to extract reading order, bounding boxes, formulas, and complex table grids into structured Markdown, HTML, or JSON.</p>
    <p><em>Pricing: Completely free and open-source under the MIT License for self-hosted execution.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="firecrawl">
    <h3>Firecrawl</h3>
    <p><strong>Maker:</strong> Mendable.ai<br><strong>Type:</strong> Web scraping and crawling platform (open-source, AGPL-3.0)</p>
    <p>Modern web documentation and application portals rely on client-side JavaScript rendering, dynamic DOM hydration, cookie consent overlays, and anti-bot rate limiting. Static HTTP scrapers receive empty shell HTML rather than the rendered document content.</p>
    <p>Firecrawl orchestrates pool-managed headless browsers that execute client-side JavaScript, dismiss modal overlays, crawl linked subpages or sitemaps, and strip navigation chrome and advertisements to output clean Markdown or schema-validated structured JSON.</p>
    <p><em>Pricing: Free to self-host under AGPL-3.0 when managing local headless browser pools; the managed cloud service offers a free tier and monthly credit subscriptions.</em></p>
  </div>

  </div>
</div>

### Knowledge Management Pipeline Comparison

The four ingestion tools target distinct data sources and privacy boundaries across the extraction phase.

| Tool | Execution Boundary | Extraction Mechanism | Primary Input Modality | Output Representation |
| :--- | :--- | :--- | :--- | :--- |
| **LlamaParse** | Managed Cloud API (Proprietary) | Multimodal VLM spatial layout reconstruction | Complex PDFs, multi-column tables, slide decks | Markdown, structured JSON |
| **Unstructured** | Open-source (`Apache 2.0`) or Managed ETL | Source connectors + layout element classification | Enterprise SaaS apps, wikis, object storage | Normalized JSON document elements |
| **Docling** | Local in-process (`MIT`) | Compact local vision models (`DocLayNet`, `TableFormer`) | Air-gapped PDFs, DOCX, academic and regulated docs | Markdown, HTML, lossless JSON |
| **Firecrawl** | Self-hosted (`AGPL-3.0`) or Cloud | Headless browser DOM rendering and overlay dismissal | Client-side SPAs and dynamic web portals | Clean Markdown, schema-validated JSON |

The next chapter, [Runtime Infrastructure](ai-tooling-chapter_06.html), examines model serving engines, fine-tuning platforms, and observability tools.

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
