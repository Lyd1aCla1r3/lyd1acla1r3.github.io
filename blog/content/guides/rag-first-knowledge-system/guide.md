# RAG-First Knowledge System: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the RAG-First Knowledge System, covering LlamaIndex setup with Pinecone integration, LiteLLM gateway configuration for embedding and generation routing, Pinecone index provisioning, LlamaParse document parsing, Firecrawl web crawling, and Braintrust evaluation scoring, with integration wiring scripts and end-to-end verification steps. -->

The RAG-First Knowledge System architecture chapter explains the rationale behind each component selection, the dual-pipeline design, and the principle that retrieval quality dominates answer quality in knowledge-heavy applications. This guide provides the concrete installation commands, configuration snippets, and wiring steps needed to bring that architecture to a working state.

## Prerequisites

- **Operating system**: macOS, Linux, or Windows with Python support
- **Python**: Version 3.10 or later, with `pip` available
- **Node.js**: Version 18 or later, with `npx` available for MCP server execution
- **API keys**: The following service accounts are required before proceeding:
  - **Pinecone**: API key from the Pinecone console
  - **LlamaParse**: API key from LlamaCloud
  - **Firecrawl**: API key from the Firecrawl dashboard
  - **Braintrust**: API key from the Braintrust console
  - **LLM provider**: At least one commercial model provider API key for generation and embedding
- **Network**: Outbound internet access for API calls to Pinecone, LlamaParse, Firecrawl, and model providers

## Step 1: LlamaIndex

LlamaIndex provides the retrieval framework with native index abstractions and query engines. Install the core package and integrations:

```bash
pip install llama-index llama-index-core \
  llama-index-vector-stores-pinecone \
  llama-index-llms-openai \
  llama-index-embeddings-openai \
  llama-index-readers-web
```

For alternative embedding providers routed through LiteLLM, add the OpenAI-like adapter:

```bash
pip install llama-index-llms-openai-like
```

**Verification**:

```python
import llama_index.core
print(f"LlamaIndex Core: {llama_index.core.__version__}")
```

A successful installation prints the version number without import errors.

## Step 2: Pinecone

Pinecone provides the managed vector database. Install the Python client:

```bash
pip install pinecone
```

Create an index in the Pinecone console or programmatically:

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="PINECONE_API_KEY")

pc.create_index(
    name="knowledge-base",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

index = pc.Index("knowledge-base")
stats = index.describe_index_stats()
print(f"Index 'knowledge-base' created: {stats.total_vector_count} vectors.")
```

The `dimension=1536` parameter matches the output dimension of OpenAI's `text-embedding-3-small` model. Adjust if using a different embedding model. The metric should match the embedding model's recommended similarity function.

**Verification**:

```bash
python -c "from pinecone import Pinecone; pc = Pinecone(api_key='PINECONE_API_KEY'); print(pc.list_indexes())"
```

A successful deployment prints the list of available indexes including `knowledge-base`.

## Step 3: LiteLLM Gateway

LiteLLM provides unified routing for both generation and embedding model calls. Install the proxy:

```bash
pip install litellm uvicorn
```

Create `litellm_config.yaml` with generation and embedding model entries:

```yaml
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: claude-sonnet
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: text-embedding-3-small
    litellm_params:
      model: openai/text-embedding-3-small
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  success_callback: ["braintrust"]
  max_budget: 500
  budget_duration: 30d

general_settings:
  master_key: sk-rag-master-key
```

Set environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export BRAINTRUST_API_KEY="br-..."
```

Start the LiteLLM proxy:

```bash
litellm --config litellm_config.yaml --host 0.0.0.0 --port 4000
```

**Verification**:

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-rag-master-key"
```

A successful deployment returns a JSON list of the configured models.

## Step 4: LlamaParse

LlamaParse provides cloud-based document parsing for PDFs and structured documents. Install the client:

```bash
pip install llama-parse
```

Set the LlamaCloud API key:

```bash
export LLAMA_CLOUD_API_KEY="llx-..."
```

Test parsing with a sample document:

```python
from llama_parse import LlamaParse

parser = LlamaParse(
    result_type="markdown",
    num_workers=4,
    verbose=True,
)

documents = parser.load_data("sample_document.pdf")
print(f"Parsed {len(documents)} document sections.")
print(f"First section preview: {documents[0].text[:200]}")
```

LlamaParse returns parsed content as LlamaIndex `Document` objects, making them directly compatible with the LlamaIndex indexing pipeline without format conversion.

**Verification**:

```python
from llama_parse import LlamaParse
print("LlamaParse imported successfully.")
```

A successful installation prints the confirmation message. Full verification requires parsing a test PDF and confirming structured Markdown output.

## Step 5: Firecrawl

Firecrawl provides web crawling with JavaScript rendering. Install the Python SDK:

```bash
pip install firecrawl-py
```

Set the Firecrawl API key:

```bash
export FIRECRAWL_API_KEY="fc-..."
```

Test crawling with a documentation site:

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-...")

result = app.scrape_url(
    url="https://docs.example.com/getting-started",
    params={"formats": ["markdown"]}
)

print(f"Title: {result.get('metadata', {}).get('title', 'N/A')}")
print(f"Content length: {len(result.get('markdown', ''))} characters")
```

For crawling an entire documentation site:

```python
crawl_result = app.crawl_url(
    url="https://docs.example.com",
    params={
        "limit": 100,
        "scrapeOptions": {"formats": ["markdown"]}
    },
    poll_interval=5
)

print(f"Crawled {crawl_result.get('total', 0)} pages.")
```

**Verification**:

```python
from firecrawl import FirecrawlApp
print("Firecrawl imported successfully.")
```

A successful installation prints the confirmation message. Full verification requires scraping a test URL and confirming Markdown output.

## Step 6: Braintrust

Braintrust provides evaluation scoring and experiment management. Install the SDK:

```bash
pip install braintrust
```

Set the API key:

```bash
export BRAINTRUST_API_KEY="br-..."
```

Create a project and an initial evaluation dataset:

```python
import braintrust

client = braintrust.init(project="rag-knowledge-system")

dataset = client.create_dataset(
    name="rag-eval-v1",
    description="Evaluation dataset for RAG pipeline quality measurement"
)

dataset.insert(
    input="What are the system requirements for deploying vLLM?",
    expected="vLLM requires Linux with NVIDIA GPU drivers and CUDA toolkit. "
             "At least one GPU with 24GB+ VRAM is needed.",
    metadata={"category": "infrastructure", "source": "chapter_06.md"}
)

dataset.insert(
    input="How does LiteLLM handle cost governance?",
    expected="LiteLLM generates virtual API keys for each team with "
             "per-team budget caps, spend tracking, and usage analytics.",
    metadata={"category": "routing", "source": "chapter_04.md"}
)

print(f"Dataset '{dataset.name}' created with {dataset.num_records} records.")
```

**Verification**:

```python
import braintrust
print("Braintrust imported successfully.")
```

A successful installation prints the confirmation message. Full verification requires creating a project and inserting evaluation records through the SDK.

## Wiring the Components

With all components installed individually, the final step connects them into the integrated pipeline described in the architecture chapter.

### LlamaParse-to-Pinecone Ingestion Pipeline

Save the following script as `scripts/ingest_documents.py`. It parses documents with LlamaParse, chunks the output, generates embeddings, and loads vectors into Pinecone:

```python
import os
from llama_parse import LlamaParse
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone

DOCS_DIR = "./knowledge_docs"
INDEX_NAME = "knowledge-base"
NAMESPACE = "product-docs"

parser = LlamaParse(result_type="markdown", num_workers=4)
embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(INDEX_NAME)

doc_files = []
for root, dirs, files in os.walk(DOCS_DIR):
    for f in files:
        if f.endswith((".pdf", ".docx", ".md", ".txt")):
            doc_files.append(os.path.join(root, f))

print(f"Found {len(doc_files)} documents to process.")

for filepath in doc_files:
    print(f"Processing: {filepath}")
    documents = parser.load_data(filepath)

    nodes = splitter.get_nodes_from_documents(documents)
    print(f"  Split into {len(nodes)} chunks.")

    vectors = []
    for i, node in enumerate(nodes):
        embedding = embed_model.get_text_embedding(node.text)
        vectors.append({
            "id": f"{os.path.basename(filepath)}-{i}",
            "values": embedding,
            "metadata": {
                "content": node.text[:1000],
                "source": filepath,
                "doc_type": os.path.splitext(filepath)[1],
                "chunk_index": i,
            }
        })

    for batch_start in range(0, len(vectors), 100):
        batch = vectors[batch_start:batch_start + 100]
        index.upsert(vectors=batch, namespace=NAMESPACE)

    print(f"  Stored {len(vectors)} vectors in namespace '{NAMESPACE}'.")

stats = index.describe_index_stats()
print(f"\nTotal vectors in index: {stats.total_vector_count}")
```

### Firecrawl-to-Pinecone Web Ingestion Pipeline

Save the following script as `scripts/ingest_web_content.py`. It crawls a documentation site with Firecrawl and indexes the content into Pinecone:

```python
import os
from firecrawl import FirecrawlApp
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone

CRAWL_URL = "https://docs.example.com"
CRAWL_LIMIT = 100
INDEX_NAME = "knowledge-base"
NAMESPACE = "web-docs"

firecrawl = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])
embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
splitter = SentenceSplitter(chunk_size=512, chunk_overlap=50)

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(INDEX_NAME)

print(f"Crawling {CRAWL_URL} with limit {CRAWL_LIMIT}...")
crawl_result = firecrawl.crawl_url(
    url=CRAWL_URL,
    params={
        "limit": CRAWL_LIMIT,
        "scrapeOptions": {"formats": ["markdown"]}
    },
    poll_interval=5
)

pages = crawl_result.get("data", [])
print(f"Crawled {len(pages)} pages.")

from llama_index.core import Document

for page_idx, page in enumerate(pages):
    markdown = page.get("markdown", "")
    source_url = page.get("metadata", {}).get("sourceURL", f"page-{page_idx}")

    if not markdown.strip():
        continue

    doc = Document(text=markdown)
    nodes = splitter.get_nodes_from_documents([doc])

    vectors = []
    for i, node in enumerate(nodes):
        embedding = embed_model.get_text_embedding(node.text)
        vectors.append({
            "id": f"web-{page_idx}-{i}",
            "values": embedding,
            "metadata": {
                "content": node.text[:1000],
                "source": source_url,
                "doc_type": "web",
                "chunk_index": i,
            }
        })

    for batch_start in range(0, len(vectors), 100):
        batch = vectors[batch_start:batch_start + 100]
        index.upsert(vectors=batch, namespace=NAMESPACE)

    print(f"  [{page_idx + 1}/{len(pages)}] {source_url}: {len(vectors)} vectors.")

stats = index.describe_index_stats()
print(f"\nTotal vectors in index: {stats.total_vector_count}")
```

### RAG Query Pipeline

Save the following script as `scripts/rag_query.py`. It configures a LlamaIndex query engine to retrieve from Pinecone and generate answers through LiteLLM:

```python
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone
import os

llm = OpenAI(
    model="gpt-4o",
    api_base="http://localhost:4000/v1",
    api_key="sk-rag-master-key",
    temperature=0,
)

embed_model = OpenAIEmbedding(
    model_name="text-embedding-3-small",
    api_base="http://localhost:4000/v1",
    api_key="sk-rag-master-key",
)

Settings.llm = llm
Settings.embed_model = embed_model

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pc.Index("knowledge-base")

vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
    namespace="product-docs",
)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="tree_summarize",
)

response = query_engine.query(
    "What are the tradeoffs between self-hosted and managed vector databases?"
)

print("Answer:")
print(response)
print(f"\nSources: {len(response.source_nodes)} chunks retrieved.")
for i, node in enumerate(response.source_nodes):
    print(f"  [{i + 1}] {node.metadata.get('source', 'unknown')} "
          f"(score: {node.score:.4f})")
```

### Braintrust RAG Evaluation Pipeline

Save the following script as `scripts/evaluate_rag.py`. It runs the RAG query pipeline against a Braintrust evaluation dataset and scores retrieval quality:

```python
import braintrust
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone
import os

llm = OpenAI(
    model="gpt-4o",
    api_base="http://localhost:4000/v1",
    api_key="sk-rag-master-key",
    temperature=0,
)

embed_model = OpenAIEmbedding(
    model_name="text-embedding-3-small",
    api_base="http://localhost:4000/v1",
    api_key="sk-rag-master-key",
)

Settings.llm = llm
Settings.embed_model = embed_model

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
pinecone_index = pc.Index("knowledge-base")
vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index,
    namespace="product-docs",
)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine(similarity_top_k=5)


def rag_task(input_text):
    response = query_engine.query(input_text)
    return {
        "answer": str(response),
        "sources": [n.metadata.get("source", "") for n in response.source_nodes],
        "scores": [n.score for n in response.source_nodes],
    }


def faithfulness_scorer(output, expected):
    expected_lower = expected.lower()
    answer_lower = output["answer"].lower()
    key_phrases = [p.strip() for p in expected_lower.split(".") if p.strip()]
    matches = sum(1 for p in key_phrases if p in answer_lower)
    return matches / max(len(key_phrases), 1)


eval_result = braintrust.Eval(
    "rag-knowledge-system",
    data=lambda: [
        {
            "input": "What are the system requirements for deploying vLLM?",
            "expected": "vLLM requires Linux with NVIDIA GPU drivers and CUDA toolkit. "
                        "At least one GPU with 24GB+ VRAM is needed.",
        },
        {
            "input": "How does LiteLLM handle cost governance?",
            "expected": "LiteLLM generates virtual API keys for each team with "
                        "per-team budget caps, spend tracking, and usage analytics.",
        },
    ],
    task=lambda input: rag_task(input),
    scores=[faithfulness_scorer],
)

print("Evaluation complete. View results in the Braintrust dashboard.")
```

## Verification

The following end-to-end checks confirm that all components are installed, wired, and operational.

| Check | Command | Expected Result |
|---|---|---|
| LlamaIndex | `python -c "import llama_index.core; print('OK')"` | Prints "OK" |
| Pinecone | `python -c "from pinecone import Pinecone; print('OK')"` | Prints "OK" |
| LiteLLM proxy | `curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-rag-master-key"` | Returns JSON model list |
| LlamaParse | `python -c "from llama_parse import LlamaParse; print('OK')"` | Prints "OK" |
| Firecrawl | `python -c "from firecrawl import FirecrawlApp; print('OK')"` | Prints "OK" |
| Braintrust | `python -c "import braintrust; print('OK')"` | Prints "OK" |
| Document ingestion | Place test PDFs in `knowledge_docs/`, run `python scripts/ingest_documents.py` | Reports vectors stored per document |
| Web ingestion | Set `CRAWL_URL` in `scripts/ingest_web_content.py`, run `python scripts/ingest_web_content.py` | Reports vectors stored per crawled page |
| RAG query | `python scripts/rag_query.py` | Prints answer with retrieved source citations |
| Evaluation | `python scripts/evaluate_rag.py` | Prints evaluation scores and directs to Braintrust dashboard |

The RAG-First Knowledge System is operational once all ten checks pass. The architecture chapter provides the rationale behind each component selection, the dual-pipeline design, and the retrieval quality optimization principles governing how the layers interact.

## References

1. LlamaIndex Installation Guide, LlamaIndex Inc.
2. Pinecone Getting Started Guide, Pinecone Systems Inc.
3. LiteLLM Proxy Documentation, BerriAI.
4. LlamaParse Documentation, LlamaIndex Inc.
5. Firecrawl Documentation, Mendable Inc.
6. Braintrust Documentation, Braintrust Data Inc.
7. OpenAI Embeddings Guide, OpenAI.
