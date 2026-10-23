# RAG-First Knowledge System: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the RAG-First Knowledge System, covering LlamaIndex setup with Pinecone integration, LiteLLM gateway configuration for embedding and generation routing, Pinecone index provisioning, LlamaParse document parsing, Firecrawl web crawling, and Braintrust evaluation scoring, with integration wiring scripts and end-to-end verification steps. -->

The [Architecture and Configuration](rag-first-knowledge-system-configuration.html) chapter explains the rationale behind each component selection, the dual-pipeline ingestion and query design, and why upstream retrieval precision governs downstream answer quality. This setup guide provides the installation commands, gateway configuration files, Python ingestion and query scripts, and Braintrust evaluation checks needed to bring that architecture to a working state. Each step installs and verifies one layer in isolation before the wiring section connects the tools into an evaluated retrieval pipeline over both static files and live web properties.

## Prerequisites

| Requirement | Details |
|---|---|
| Operating system | macOS, Linux, or Windows workstation with Python and network access |
| Python runtime | Python 3.10 or later with `pip` and virtual environment support |
| Node.js runtime | Node.js 18 or later with `npx` available for MCP servers |
| Pinecone account | Active `PINECONE_API_KEY` from the Pinecone console for serverless vector storage |
| LlamaCloud account | Active `LLAMA_CLOUD_API_KEY` from LlamaCloud for agentic PDF and DOCX parsing |
| Firecrawl account | Active `FIRECRAWL_API_KEY` from the Firecrawl dashboard for headless web crawling |
| Braintrust account | Active `BRAINTRUST_API_KEY` from the Braintrust console for evaluation datasets |
| LLM provider keys | Commercial provider keys (`OPENAI_API_KEY` and `ANTHROPIC_API_KEY`) for LiteLLM routing |

## Step 1: LlamaIndex

LlamaIndex provides the index abstractions, node splitters, query engines, and response synthesizers that drive both offline ingestion and online retrieval. Install the core framework alongside its Pinecone vector store, OpenAI model and embedding, and web reader integrations inside a dedicated virtual environment:

<details class="code-drop">
<summary><span class="code-drop__name">install-llamaindex.sh</span><span class="code-drop__meta">Bash · 7 lines</span></summary>

```bash
pip install llama-index llama-index-core \
  llama-index-vector-stores-pinecone \
  llama-index-llms-openai \
  llama-index-embeddings-openai \
  llama-index-embeddings-openai-like \
  llama-index-readers-web
```

</details>

Installing both `llama-index-embeddings-openai` and `llama-index-embeddings-openai-like` allows the pipeline to route OpenAI embedding models or third-party OpenAI-compatible encoders through the LiteLLM proxy without changing framework code. Keeping these namespace packages aligned inside a single virtual environment prevents version drift between the core `VectorStoreIndex` class and the Pinecone storage adapter.

**Verification**:

```bash
python -c \
  "import llama_index"
```

The command imports `llama_index` cleanly without import errors.

## Step 2: Pinecone

Pinecone provides managed serverless vector storage with namespace isolation and single-stage metadata filtering. Install the official Pinecone Python SDK and export the project API key into the shell environment so both the index provisioning script and the downstream ingestion jobs can authenticate:

```bash
pip install pinecone
export \
  PINECONE_API_KEY="pcsk.."
```

Save and run `scripts/init_pinecone.py` to provision a serverless `knowledge-base` index configured for 1,536-dimensional embeddings and cosine similarity scoring:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/init_pinecone.py</span><span class="code-drop__meta">Python · 16 lines</span></summary>

```python
import os
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pc.create_index(
    name="knowledge-base",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)
idx = pc.Index("knowledge-base")
stats = idx.describe_index_stats()
print(f"Index 'knowledge-base' ready: {stats.total_vector_count} vectors.")
```

</details>

```bash
python \
  scripts/init_pinecone.py
```

The 1,536 vector dimension matches OpenAI's `text-embedding-3-small` encoder routed through LiteLLM. Switching later to a 3,072-dimensional encoder (`text-embedding-3-large`) or a 1,024-dimensional encoder requires creating a new Pinecone index with the corresponding dimension parameter. Pinecone Serverless allocates storage and compute elastically inside the selected cloud region (`us-east-1`), so newly created indexes become ready for vector upserts within a few seconds without manual pod sizing.

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">verify_pinecone.py</span><span class="code-drop__meta">Python · 4 lines</span></summary>

```python
import os
from pinecone import Pinecone

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
print([idx.name for idx in pc.list_indexes()])
```

</details>

```bash
python verify_pinecone.py
```

The output list contains `knowledge-base`, confirming that the serverless control plane provisioned the index and accepted the API key.

## Step 3: LiteLLM Gateway

LiteLLM routes both batch embedding requests during document ingestion and chat completion requests during answer synthesis through a single local proxy on port 4000. Centralizing both model types behind one gateway ensures that ingestion scripts and query engines never embed raw vendor keys and that Braintrust receives unified latency and cost telemetry. Install the proxy extras from PyPI:

<details class="code-drop">
<summary><span class="code-drop__name">install-litellm.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
pip install "litellm[proxy]"
```

</details>

Create `litellm_config.yaml` with routes for `gpt-4o`, `claude-sonnet`, and `text-embedding-3-small`, plus the Braintrust telemetry callback and a monthly spend ceiling:

<details class="code-drop">
<summary><span class="code-drop__name">litellm_config.yaml</span><span class="code-drop__meta">YAML · 24 lines</span></summary>

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-latest
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: text-embedding-3-small
    litellm_params:
      model: openai/text-embedding-3-small
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  callbacks: ["braintrust"]
  max_budget: 500
  budget_duration: 30d

general_settings:
  master_key: sk-rag-master-key
```

</details>

Export the upstream provider keys and start the LiteLLM proxy server on port 4000. Enforcing `max_budget` across restarts requires pointing `DATABASE_URL` at a PostgreSQL instance; running without a database still routes traffic and logs callbacks cleanly during local development:

<details class="code-drop">
<summary><span class="code-drop__name">start-litellm-rag.sh</span><span class="code-drop__meta">Bash · 6 lines</span></summary>

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export BRAINTRUST_API_KEY="sk-..."
litellm --config litellm_config.yaml --host 0.0.0.0 --port 4000
```

</details>

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">verify-litellm-rag.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
curl -s http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-rag-master-key"
```

</details>

The proxy returns a JSON catalog containing `gpt-4o`, `claude-sonnet`, and `text-embedding-3-small`.

## Step 4: LlamaParse

LlamaParse extracts structured Markdown, nested tables, and section hierarchies from complex PDFs and Word documents through the `llama-cloud` SDK. The older standalone `llama-parse` package has been superseded by the unified `llama-cloud` client, which exposes agentic vision parsing directly on `client.parsing.parse`. Install the client package and export the LlamaCloud API key:

<details class="code-drop">
<summary><span class="code-drop__name">install-llamaparse.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
pip install "llama-cloud>=1.0"
export LLAMA_CLOUD_API_KEY="llx-..."
```

</details>

Save and run `verify_llamaparse.py` against a sample PDF to confirm that the `agentic` parsing tier returns page-level Markdown:

<details class="code-drop">
<summary><span class="code-drop__name">verify_llamaparse.py</span><span class="code-drop__meta">Python · 13 lines</span></summary>

```python
from llama_cloud import LlamaCloud

client = LlamaCloud()
result = client.parsing.parse(
    upload_file="sample_document.pdf",
    tier="agentic",
    version="latest",
    expand=["markdown"],
)
pages = [p.markdown for p in result.markdown.pages if p.success]
print(f"Parsed {len(pages)} pages.")
print(f"Preview: {pages[0][:160]}")
```

</details>

```bash
python verify_llamaparse.py
```

Requesting `tier="agentic"` and `expand=["markdown"]` instructs LlamaParse to run vision layout analysis on multi-column pages and tables and return each page's reconstructed Markdown string ready for LlamaIndex node splitting.

**Verification**:

```bash
python -c \
  "import llama_cloud"
```

The command verifies that the `llama_cloud` package imports without errors, and `verify_llamaparse.py` confirms live API authentication and Markdown table extraction. Inspecting the printed page preview confirms that multi-column headers and table rows converted into clean Markdown syntax before indexing.

## Step 5: Firecrawl

Firecrawl crawls JavaScript-rendered documentation portals, knowledge bases, and changelogs in a headless browser and converts each page into clean Markdown with navigation chrome removed. Install the Python SDK and export the Firecrawl API key:

<details class="code-drop">
<summary><span class="code-drop__name">install-firecrawl.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
pip install firecrawl-py
export FIRECRAWL_API_KEY="fc-..."
```

</details>

Save `verify_firecrawl.py` to test both single-page scraping (`app.scrape`) and multi-page domain crawling (`app.crawl`) with `ScrapeOptions`:

<details class="code-drop">
<summary><span class="code-drop__name">verify_firecrawl.py</span><span class="code-drop__meta">Python · 16 lines</span></summary>

```python
import os
from firecrawl import Firecrawl
from firecrawl.types import ScrapeOptions

app = Firecrawl(api_key=os.environ["FIRECRAWL_API_KEY"])
single = app.scrape("https://docs.example.com/getting-started", formats=["markdown"])
print(f"Scraped {len(single.markdown or '')} chars.")

crawl = app.crawl(
    "https://docs.example.com",
    limit=25,
    scrape_options=ScrapeOptions(formats=["markdown"]),
    poll_interval=5,
)
print(f"Crawled {crawl.total} pages.")
```

</details>

Setting `limit=25` and `poll_interval=5` bounds the crawl breadth during initial testing and polls the asynchronous crawl job every five seconds until all discovered documentation pages finish rendering.

**Verification**:

```bash
python -c \
  "import firecrawl"
```

The import check confirms that the SDK is installed, and running `python verify_firecrawl.py` against a target documentation URL confirms headless browser rendering and Markdown conversion.

## Step 6: Braintrust

Braintrust manages versioned evaluation datasets, executes retrieval and faithfulness scoring functions, and compares pipeline experiments side by side across chunking and embedding revisions. Install the SDK and export the Braintrust API key:

<details class="code-drop">
<summary><span class="code-drop__name">install-braintrust.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
pip install braintrust
export BRAINTRUST_API_KEY="sk-..."
```

</details>

Save and run `scripts/init_braintrust.py` to create the `rag-knowledge-system` project and seed the `rag-eval-v1` benchmark dataset with ground-truth question-answer-source records:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/init_braintrust.py</span><span class="code-drop__meta">Python · 22 lines</span></summary>

```python
import braintrust

dataset = braintrust.init_dataset(
    project="rag-knowledge-system",
    name="rag-eval-v1",
    description="Golden benchmark for RAG retrieval and faithfulness scoring",
)
dataset.insert(
    input="What are the system requirements for deploying vLLM?",
    expected="vLLM requires Linux with NVIDIA GPU drivers, CUDA, and 24GB+ VRAM.",
    metadata={"category": "infrastructure", "source": "chapter_06.md"},
)
dataset.insert(
    input="How does LiteLLM handle cost governance?",
    expected="LiteLLM issues per-team virtual keys with monthly budget caps and spend tracking.",
    metadata={"category": "routing", "source": "chapter_04.md"},
)
dataset.flush()
print(f"Dataset '{dataset.name}' initialized with 2 benchmark records.")
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-init-braintrust.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
python scripts/init_braintrust.py
```

</details>

Storing the expected source filename (`chapter_06.md`, `chapter_04.md`) inside each record's `metadata` dictionary allows evaluation scripts to score both whether the retriever found the right document and whether the language model synthesized a faithful answer.

**Verification**:

```bash
python -c \
  "import braintrust"
```

## Wiring the Components

Four integration scripts connect LlamaParse, Firecrawl, LiteLLM, Pinecone, LlamaIndex, and Braintrust into a complete ingestion, retrieval, and evaluation workflow. Running the static and web ingestion scripts populates two isolated namespaces inside the same Pinecone index, and the query and evaluation scripts then measure how accurately the retriever surfaces those indexed passages.

### LlamaParse-to-Pinecone Ingestion Pipeline

Save `scripts/ingest_documents.py` to parse static files in `./knowledge_docs` through LlamaParse, split the returned Markdown into 512-token chunks with 50-token overlap, generate embeddings through LiteLLM, and upsert the vectors into Pinecone's `product-docs` namespace:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/ingest_documents.py</span><span class="code-drop__meta">Python · 38 lines</span></summary>

```python
import os
from llama_cloud import LlamaCloud
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone

DOCS_DIR, INDEX_NAME, NS = "./knowledge_docs", "knowledge-base", "product-docs"
EXTS = (".pdf", ".docx", ".md", ".txt")

parser = LlamaCloud(api_key=os.environ["LLAMA_CLOUD_API_KEY"])
embed = OpenAIEmbedding(model_name="text-embedding-3-small", api_base="http://localhost:4000/v1", api_key="sk-rag-master-key")
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
index = Pinecone(api_key=os.environ["PINECONE_API_KEY"]).Index(INDEX_NAME)

for root, _, files in os.walk(DOCS_DIR):
    for name in [f for f in files if f.endswith(EXTS)]:
        path = os.path.join(root, name)
        res = parser.parsing.parse(upload_file=path, tier="agentic", version="latest", expand=["markdown"])
        docs = [Document(text=p.markdown) for p in res.markdown.pages if p.success]
        nodes = splitter.get_nodes_from_documents(docs)
        vecs = [
            {
                "id": f"{name}-{i}",
                "values": embed.get_text_embedding(n.text),
                "metadata": {"content": n.text, "source": path, "doc_type": os.path.splitext(name)[1], "chunk_index": i},
            }
            for i, n in enumerate(nodes)
        ]
        for start in range(0, len(vecs), 100):
            index.upsert(vectors=vecs[start:start + 100], namespace=NS)
        print(f"Indexed {path}: {len(vecs)} chunks into '{NS}'.")
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-ingest-docs.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
mkdir -p knowledge_docs
python scripts/ingest_documents.py
```

</details>

Routing `OpenAIEmbedding` through `http://localhost:4000/v1` ensures that batch indexing token spend is tracked in LiteLLM alongside interactive query traffic. Upserting vectors in batches of 100 keeps request payloads well within Pinecone's gRPC and HTTP message size limits while storing the raw chunk text under the `content` metadata key for downstream synthesis.

### Firecrawl-to-Pinecone Web Ingestion Pipeline

Save `ingest_web_content.py` in `scripts/` to crawl a live documentation domain with Firecrawl, split each rendered Markdown page into chunks, and upsert the resulting vectors into Pinecone's `web-docs` namespace:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/ingest_web_content.py</span><span class="code-drop__meta">Python · 38 lines</span></summary>

```python
import os
from firecrawl import Firecrawl
from firecrawl.types import ScrapeOptions
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone

CRAWL_URL, INDEX_NAME, NS = "https://docs.example.com", "knowledge-base", "web-docs"

fc = Firecrawl(api_key=os.environ["FIRECRAWL_API_KEY"])
embed = OpenAIEmbedding(model_name="text-embedding-3-small", api_base="http://localhost:4000/v1", api_key="sk-rag-master-key")
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)
index = Pinecone(api_key=os.environ["PINECONE_API_KEY"]).Index(INDEX_NAME)

crawl = fc.crawl(CRAWL_URL, limit=100, scrape_options=ScrapeOptions(formats=["markdown"]), poll_interval=5)
for p_idx, page in enumerate(crawl.data or []):
    md = (page.markdown or "").strip()
    if not md:
        continue
    url = (page.metadata and page.metadata.source_url) or f"page-{p_idx}"
    nodes = splitter.get_nodes_from_documents([Document(text=md)])
    vecs = [
        {
            "id": f"web-{p_idx}-{i}",
            "values": embed.get_text_embedding(n.text),
            "metadata": {"content": n.text, "source": url, "doc_type": "web", "chunk_index": i},
        }
        for i, n in enumerate(nodes)
    ]
    for start in range(0, len(vecs), 100):
        index.upsert(vectors=vecs[start:start + 100], namespace=NS)
    print(f"Indexed {url}: {len(vecs)} chunks into '{NS}'.")
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-ingest-web.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
python scripts/ingest_web_content.py
```

</details>

Separating `web-docs` from `product-docs` via Pinecone namespaces allows scheduled cron jobs to refresh crawled web pages daily without touching static PDF vectors. Both ingestion pipelines use the identical `SentenceSplitter` (`chunk_size=512`, `chunk_overlap=50`) and `text-embedding-3-small` configuration so vector similarity scores remain calibrated across namespaces.

### RAG Query Pipeline

Save `scripts/rag_query.py` to bind LlamaIndex's `PineconeVectorStore` to the indexed namespace, retrieve the top five matching chunks, and synthesize a cited answer through LiteLLM:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/rag_query.py</span><span class="code-drop__meta">Python · 31 lines</span></summary>

```python
import os
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone

Settings.llm = OpenAI(model="gpt-4o", api_base="http://localhost:4000/v1", api_key="sk-rag-master-key", temperature=0)
Settings.embed_model = OpenAIEmbedding(model_name="text-embedding-3-small", api_base="http://localhost:4000/v1", api_key="sk-rag-master-key")

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
store = PineconeVectorStore(pinecone_index=pc.Index("knowledge-base"), namespace="product-docs", text_key="content")
engine = VectorStoreIndex.from_vector_store(store).as_query_engine(similarity_top_k=5, response_mode="tree_summarize")

res = engine.query("What are the tradeoffs between self-hosted and managed vector databases?")
print(f"Answer:\n{res}\n\nSources ({len(res.source_nodes)} chunks):")
for idx, node in enumerate(res.source_nodes):
    print(f"  [{idx + 1}] {node.metadata.get('source', 'unknown')} (score: {node.score:.4f})")
```

</details>

```bash
python scripts/rag_query.py
```

Passing `text_key="content"` tells `PineconeVectorStore` which metadata field holds the chunk text upserted by the ingestion scripts, and `tree_summarize` response mode hierarchical-summarizes the top five retrieved chunks at temperature zero before printing each source path and cosine similarity score.

### Braintrust RAG Evaluation Pipeline

Save `scripts/evaluate_rag.py` to benchmark the live LlamaIndex query engine against the golden dataset in Braintrust and compute quantitative faithfulness and source-retrieval scores:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/evaluate_rag.py</span><span class="code-drop__meta">Python · 39 lines</span></summary>

```python
import os
import braintrust
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone

Settings.llm = OpenAI(model="gpt-4o", api_base="http://localhost:4000/v1", api_key="sk-rag-master-key", temperature=0)
Settings.embed_model = OpenAIEmbedding(model_name="text-embedding-3-small", api_base="http://localhost:4000/v1", api_key="sk-rag-master-key")

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
store = PineconeVectorStore(pinecone_index=pc.Index("knowledge-base"), namespace="product-docs", text_key="content")
engine = VectorStoreIndex.from_vector_store(store).as_query_engine(similarity_top_k=5)

def rag_task(question):
    res = engine.query(question)
    return {
        "answer": str(res),
        "sources": [n.metadata.get("source", "") for n in res.source_nodes],
    }

def faithfulness_scorer(output, expected):
    phrases = [p.strip() for p in expected.lower().split(".") if p.strip()]
    hits = sum(1 for p in phrases if p in output["answer"].lower())
    return hits / max(len(phrases), 1)

braintrust.Eval(
    "rag-knowledge-system",
    data=braintrust.init_dataset(project="rag-knowledge-system", name="rag-eval-v1"),
    task=rag_task,
    scores=[faithfulness_scorer],
)
```

</details>

```bash
python \
  scripts/evaluate_rag.py
```

Passing `braintrust.init_dataset` directly to `braintrust.Eval` pulls the versioned benchmark records seeded in Step 6 rather than duplicating hardcoded test strings across scripts. Each run logs a new experiment comparison link to the terminal so engineers can verify whether a chunk-size, top-K, or encoder adjustment improved retrieval precision.

## Verification

| Check | Command | Expected Result |
|---|---|---|
| LlamaIndex core | `python -c "import llama_index"` | Exits with code zero and no import errors |
| Pinecone index | `python verify_pinecone.py` | Lists knowledge-base in active indexes |
| LiteLLM gateway | `curl -s localhost:4000/v1/models` | Returns JSON catalog of generation and embedding models |
| LlamaParse client | `python verify_llamaparse.py` | Prints parsed page count and Markdown preview |
| Firecrawl crawler | `python verify_firecrawl.py` | Scrapes and crawls target URL into Markdown |
| Braintrust dataset | `bash run-init-braintrust.sh` | Creates benchmark dataset with two records |
| Doc ingestion | `bash run-ingest-docs.sh` | Upserts chunk vectors into product-docs namespace |
| Web ingestion | `bash run-ingest-web.sh` | Upserts crawled vectors into web-docs namespace |
| Cited RAG query | `python scripts/rag_query.py` | Prints synthesized answer with source paths and scores |
| Evaluation suite | `python scripts/evaluate_rag.py` | Runs benchmark and logs experiment URL in Braintrust |

## Troubleshooting

| Symptom | Fix |
|---|---|
| Pinecone upsert raises dimension mismatch error | Confirm the index dimension (1,536) matches the output size of `text-embedding-3-small` |
| `PineconeVectorStore` returns empty node text | Pass `text_key="content"` when initializing `PineconeVectorStore` to match the ingested metadata key |
| LlamaParse returns empty pages on scanned PDFs | Set `tier="agentic"` in `client.parsing.parse` so vision layout and OCR models execute |
| LiteLLM global budget cap does not block spend | Configure `DATABASE_URL` with a PostgreSQL instance before starting the LiteLLM proxy |
| Braintrust evaluation run logs zero dataset rows | Run `init_braintrust.py` first and verify `dataset.flush()` completed without error |

The [RAG-First Knowledge System](rag-first-knowledge-system-configuration.html) is operational once all ten verification checks pass. That companion architecture chapter details the dual-ingestion design, retrieval quality tradeoffs, and layer substitution options. Teams iterating on production corpora should re-run the Braintrust evaluation script after every chunking, metadata filter, or encoder change so retrieval precision and citation faithfulness are verified quantitatively before deployment.

## References

1. LlamaIndex Installation Guide, LlamaIndex Inc.
2. Pinecone Getting Started Guide, Pinecone Systems Inc.
3. LiteLLM Proxy Documentation, BerriAI.
4. LlamaParse and LlamaCloud SDK Documentation, LlamaIndex Inc.
5. Firecrawl Python SDK Documentation, Mendable Inc.
6. Braintrust Evaluation Documentation, Braintrust Data Inc.
7. OpenAI Embeddings Guide, OpenAI.
