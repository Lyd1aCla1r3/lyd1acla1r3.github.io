# Private and Airgapped Deployment: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Private and Airgapped Deployment stack, covering air-gap transfer procedures, LlamaIndex and LangGraph setup, LiteLLM gateway configuration for internal-only routing, vLLM and SGLang model serving, Qdrant vector database provisioning, Docling document parsing, Arize Phoenix observability, and Unsloth fine-tuning, with integration wiring and end-to-end verification steps. -->

The [Architecture and Configuration](private-and-airgapped-deployment-configuration.html) chapter explains the rationale behind each component selection, the sealed network boundary constraint, and the substitutions required to eliminate all external cloud dependencies. This setup guide provides the offline staging commands, installation steps, configuration files, and Python wiring scripts needed to bring that architecture to a working state on isolated infrastructure. Every installation command inside the enclave operates exclusively against pre-staged local wheel archives, binaries, and model checkpoints transferred across the physical air gap.

## Prerequisites

| Requirement | Details |
|---|---|
| Operating system | Linux host with `systemd` across all serving, storage, and agent nodes |
| Python runtime | Python 3.11 or later with `pip` and offline wheel directories pre-staged |
| Node.js runtime | Node.js 18 or later with local `node_modules` pre-staged for MCP servers |
| GPU hardware | Minimum one 24 GB NVIDIA GPU; four 48 GB GPUs for 70B BF16 serving |
| Network topology | Internal TCP access across enclave hosts with zero outbound internet routes |
| Staging media | Accredited physical transfer media scanned per organizational security policy |

### Air-Gap Transfer Procedure

Before entering the isolated network, run the following staging script on an internet-connected Linux workstation matching the target enclave architecture (CPU instruction set, glibc version, and CUDA runtime) to download all Python wheels, model checkpoints, Docling vision weights, and the Qdrant binary:

<details class="code-drop">
<summary><span class="code-drop__name">stage_airgap_artifacts.sh</span><span class="code-drop__meta">Bash · 27 lines</span></summary>

```bash
# 1. Core framework, gateway, parser, observability, and training wheels
pip download -d ./offline_packages \
  llama-index llama-index-core llama-index-vector-stores-qdrant \
  llama-index-llms-openai-like llama-index-embeddings-huggingface \
  langgraph langgraph-checkpoint-sqlite langgraph-checkpoint-postgres \
  "litellm[proxy]" qdrant-client docling \
  arize-phoenix arize-phoenix-otel openinference-instrumentation-llama-index \
  opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp \
  unsloth trl peft transformers datasets accelerate bitsandbytes \
  uvicorn fastapi mcp-server-git

# 2. Serving engines (separate folders to avoid FlashInfer version conflicts)
pip download -d ./offline_vllm vllm
pip download -d ./offline_sglang sglang

# 3. Gated Llama 3.1 checkpoints, BGE embeddings, and Docling vision models
hf download meta-llama/Llama-3.1-70B-Instruct --local-dir ./models/llama-70b
hf download meta-llama/Llama-3.1-8B-Instruct --local-dir ./models/llama-8b
hf download BAAI/bge-large-en-v1.5 --local-dir ./models/bge-large
docling-tools models download --output-dir ./models/docling

# 4. Qdrant single binary and MCP filesystem server
curl -L --create-dirs -o ./binaries/qdrant.tar.gz \
  https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-gnu.tar.gz
npm install --prefix ./mcp_servers @modelcontextprotocol/server-filesystem
```

</details>

Copy the six staged directories (`offline_packages/`, `offline_vllm/`, `offline_sglang/`, `models/`, `binaries/`, and `mcp_servers/`) onto accredited transfer media, complete cryptographic hash verification and malware scanning at the security boundary, and mount the verified directories on the target enclave hosts. Keeping the vLLM and SGLang wheel caches in separate folders prevents binary wheel collisions during offline installation.

## Step 1: LlamaIndex and LangGraph

LlamaIndex provides the retrieval-first agent framework, and LangGraph provides stateful multi-agent orchestration. Install both libraries and their Qdrant, local Hugging Face embedding, and OpenAI-compatible LLM adapters from the pre-staged wheel directory using `--no-index` and `--find-links`:

<details class="code-drop">
<summary><span class="code-drop__name">install-frameworks.sh</span><span class="code-drop__meta">Bash · 5 lines</span></summary>

```bash
pip install --no-index --find-links ./offline_packages \
  llama-index llama-index-core llama-index-vector-stores-qdrant \
  llama-index-llms-openai-like llama-index-embeddings-huggingface \
  langgraph langgraph-checkpoint-sqlite langgraph-checkpoint-postgres
```

</details>

The `--no-index` flag prevents pip from attempting any connection to the public Python Package Index, which would time out or trigger intrusion-detection alerts inside a sealed subnet. Including both the SQLite and PostgreSQL checkpointer wheels allows developers to test workflows locally against a single file before switching the connection string to an internal PostgreSQL cluster.

**Verification**:

Save and run `verify_frameworks.py` to confirm that both LlamaIndex and LangGraph load cleanly from the offline environment:

<details class="code-drop">
<summary><span class="code-drop__name">verify_frameworks.py</span><span class="code-drop__meta">Python · 5 lines</span></summary>

```python
from importlib.metadata import version
import llama_index.core

print(f"LlamaIndex Core: {llama_index.core.__version__}")
print(f"LangGraph: {version('langgraph')}")
```

</details>

```bash
python verify_frameworks.py
```

The script prints both semantic version strings and exits with status code zero.

## Step 2: Qdrant

Qdrant runs as a single compiled Rust binary with zero container or external database dependencies, simplifying security accreditation on locked-down Linux servers. Extract the pre-staged archive into `/opt/qdrant`:

```bash
mkdir -p /opt/qdrant
tar -xzf qdrant.tgz \
  -C /opt/qdrant
```

Create `/opt/qdrant/config.yaml` to store vector payloads on disk, bind HTTP port 6333 and gRPC port 6334, and disable outbound telemetry:

<details class="code-drop">
<summary><span class="code-drop__name">/opt/qdrant/config.yaml</span><span class="code-drop__meta">YAML · 12 lines</span></summary>

```yaml
storage:
  storage_path: /opt/qdrant/storage
  on_disk_payload: true

service:
  grpc_port: 6334
  http_port: 6333

cluster:
  enabled: false

telemetry_disabled: true
```

</details>

For production operation, register `qdrant.service` under `/etc/systemd/system/` so the service manager supervises the binary and restarts it automatically across host reboots:

<details class="code-drop">
<summary><span class="code-drop__name">/etc/systemd/system/qdrant.service</span><span class="code-drop__meta">INI · 13 lines</span></summary>

```ini
[Unit]
Description=Qdrant Vector Database
After=network.target

[Service]
Type=simple
ExecStart=/opt/qdrant/qdrant --config-path /opt/qdrant/config.yaml
Restart=always
User=qdrant

[Install]
WantedBy=multi-user.target
```

</details>

Install the offline `qdrant-client` wheel and run `scripts/init_qdrant.py` to create the `internal_documents` collection configured for 1,024-dimensional BGE-Large vectors and cosine similarity scoring:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/init_qdrant.py</span><span class="code-drop__meta">Python · 13 lines</span></summary>

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)
client.recreate_collection(
    collection_name="internal_documents",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)
info = client.get_collection("internal_documents")
print(f"Collection ready: {info.points_count} points.")
```

</details>

```bash
python \
  scripts/init_qdrant.py
```

Matching the collection vector dimension (1,024) to the locally staged BGE-Large checkpoint prevents dimension-mismatch exceptions when LlamaIndex and the batch ingestion pipeline write points into Qdrant.

**Verification**:

```bash
curl -s \
  localhost:6333/readyz
```

The HTTP response confirms that the Qdrant storage engine is ready to accept collection queries.

## Step 3: vLLM

vLLM handles high-concurrency chat generation and pooled BGE embedding inference against local safetensors weights. Install `vllm` inside a dedicated virtual environment from `./offline_vllm`:

<details class="code-drop">
<summary><span class="code-drop__name">install-vllm-airgapped.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
pip install --no-index \
  --find-links ./offline_vllm vllm
```

</details>

Launch the primary 70B reasoning server on port 8000 across four GPUs and a second pooled embedding server on port 8003 pointed directly at the local filesystem paths:

<details class="code-drop">
<summary><span class="code-drop__name">start-vllm-airgapped.sh</span><span class="code-drop__meta">Bash · 15 lines</span></summary>

```bash
vllm serve /path/to/models/llama-70b \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 4 \
  --max-model-len 8192 \
  --enable-prefix-caching \
  --served-model-name llama-70b-instruct &

vllm serve /path/to/models/bge-large \
  --host 0.0.0.0 \
  --port 8003 \
  --runner pooling \
  --served-model-name bge-large-en-v1.5 &
```

</details>

Passing a local directory path (`/path/to/models/llama-70b`) instead of a Hugging Face Hub repository identifier instructs vLLM to load weights, tokenizer vocabularies, and generation configs directly from disk without attempting outbound Hub metadata calls. The `--served-model-name` flag assigns a clean alias that LiteLLM references in its routing table.

**Verification**:

```bash
curl -s \
  localhost:8000/v1/models
```

Test a chat completion turn against the local vLLM endpoint to confirm that all tensor-parallel GPU workers respond:

<details class="code-drop">
<summary><span class="code-drop__name">verify-vllm-airgapped.sh</span><span class="code-drop__meta">Bash · 8 lines</span></summary>

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-70b-instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 50
  }'
```

</details>

## Step 4: SGLang

SGLang serves the 8-billion-parameter model on port 8001 for low-latency structured JSON decoding and branching agent prompts. SGLang and vLLM pin different CUDA and FlashInfer package versions, so install SGLang in a separate Python virtual environment from `./offline_sglang` and launch the server against the pre-staged `/path/to/models/llama-8b` directory:

<details class="code-drop">
<summary><span class="code-drop__name">start-sglang-airgapped.sh</span><span class="code-drop__meta">Bash · 8 lines</span></summary>

```bash
pip install --no-index --find-links ./offline_sglang sglang

python -m sglang.launch_server \
  --model-path /path/to/models/llama-8b \
  --host 0.0.0.0 \
  --port 8001 \
  --served-model-name llama-8b-structured
```

</details>

Binding port 8001 lets SGLang run alongside vLLM without port collisions while LiteLLM routes requests between the two engines transparently. Routing schema-constrained extraction tasks to this smaller 8B model keeps the 70B vLLM cluster free for deep multi-document synthesis.

**Verification**:

```bash
curl -s \
  localhost:8001/v1/models
```

The endpoint returns a JSON catalog listing `llama-8b-structured`.

## Step 5: LiteLLM Gateway

LiteLLM unifies the internal vLLM and SGLang servers behind a single OpenAI-compatible gateway on port 4000 so agent code never hardcodes GPU hostnames or engine ports. Create `litellm_config.yaml` with internal-only `api_base` endpoints and the `arize_phoenix` telemetry callback:

<details class="code-drop">
<summary><span class="code-drop__name">litellm_config.yaml</span><span class="code-drop__meta">YAML · 25 lines</span></summary>

```yaml
model_list:
  - model_name: llama-70b
    litellm_params:
      model: openai/llama-70b-instruct
      api_base: http://vllm-server:8000/v1
      api_key: token-not-used

  - model_name: llama-8b-structured
    litellm_params:
      model: openai/llama-8b-structured
      api_base: http://sglang-server:8001/v1
      api_key: token-not-used

  - model_name: bge-large-embedding
    litellm_params:
      model: openai/bge-large-en-v1.5
      api_base: http://vllm-server:8003/v1
      api_key: token-not-used

litellm_settings:
  callbacks: ["arize_phoenix"]

general_settings:
  master_key: sk-internal-master-key
```

</details>

Install the proxy package from `./offline_packages`, replace `vllm-server` and `sglang-server` with the internal IP addresses or enclave DNS hostnames of the GPU nodes, and start the proxy on port 4000:

<details class="code-drop">
<summary><span class="code-drop__name">start-litellm-airgapped.sh</span><span class="code-drop__meta">Bash · 6 lines</span></summary>

```bash
pip install --no-index --find-links ./offline_packages "litellm[proxy]" uvicorn

litellm \
  --config litellm_config.yaml \
  --host 0.0.0.0 \
  --port 4000
```

</details>

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">verify-litellm-airgapped.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
curl -s http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-internal-master-key"
```

</details>

The proxy returns a JSON model list containing `llama-70b`, `llama-8b-structured`, and `bge-large-embedding`.

## Step 6: Docling

Docling converts PDFs and DOCX specifications into structured Markdown using pre-staged local vision models. Install `docling` from `./offline_packages` and point `DOCLING_ARTIFACTS_PATH` at the transferred model weights directory:

<details class="code-drop">
<summary><span class="code-drop__name">docling_env.sh</span><span class="code-drop__meta">Bash · 3 lines</span></summary>

```bash
pip install --no-index --find-links ./offline_packages docling
export DOCLING_ARTIFACTS_PATH="/path/to/models/docling"
export HF_HUB_OFFLINE=1
```

</details>

Setting `DOCLING_ARTIFACTS_PATH` and `HF_HUB_OFFLINE=1` ensures that `DocumentConverter` loads layout detection and TableFormer weights strictly from local storage without querying Hugging Face on first execution.

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">verify_docling.py</span><span class="code-drop__meta">Python · 5 lines</span></summary>

```python
from docling.document_converter import DocumentConverter

conv = DocumentConverter()
res = conv.convert("test_document.pdf")
print(f"Extracted {len(res.document.texts)} text elements.")
```

</details>

```bash
python verify_docling.py
```

The script parses the test PDF against the offline vision artifacts and prints the extracted text element count.

## Step 7: Arize Phoenix

Arize Phoenix provides self-hosted OpenTelemetry trace storage, retrieval span inspection, and embedding drift diagnostics on port 6006. Install Phoenix and the OpenInference LlamaIndex instrumentor from `./offline_packages`:

<details class="code-drop">
<summary><span class="code-drop__name">install-phoenix.sh</span><span class="code-drop__meta">Bash · 4 lines</span></summary>

```bash
pip install --no-index --find-links ./offline_packages \
  arize-phoenix arize-phoenix-otel \
  openinference-instrumentation-llama-index \
  opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

</details>

Launch the Phoenix server and export the collector endpoint variables in the shell environments running LiteLLM and the agent scripts:

<details class="code-drop">
<summary><span class="code-drop__name">start-phoenix.sh</span><span class="code-drop__meta">Bash · 4 lines</span></summary>

```bash
phoenix serve --host 0.0.0.0 --port 6006 &
export PHOENIX_COLLECTOR_ENDPOINT="http://phoenix-server:6006/v1/traces"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://phoenix-server:6006"
```

</details>

**Verification**:

```bash
curl -s \
  localhost:6006/healthz
```

The health check returns an HTTP 200 status response, and the web UI is reachable inside the enclave at `http://phoenix-server:6006`.

## Step 8: Unsloth

Unsloth fine-tunes QLoRA adapters on single-GPU hardware using curated Phoenix trace exports so base open-weight models learn internal domain terminology and report formats. Install Unsloth and its training dependencies from `./offline_packages`:

<details class="code-drop">
<summary><span class="code-drop__name">install-unsloth.sh</span><span class="code-drop__meta">Bash · 3 lines</span></summary>

```bash
pip install --no-index --find-links ./offline_packages \
  unsloth trl peft transformers datasets accelerate bitsandbytes
```

</details>

Save `finetune_airgapped.py` in `scripts/` to train a rank-16 LoRA adapter against the locally staged `/path/to/models/llama-8b` checkpoint:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/finetune_airgapped.py</span><span class="code-drop__meta">Python · 34 lines</span></summary>

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

MODEL_PATH = "/path/to/models/llama-8b"
OUTPUT_DIR = "./fine-tuned-airgapped"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_PATH, max_seq_length=2048, load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32, lora_dropout=0,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"], bias="none",
)
dataset = load_dataset("json", data_files="/path/to/training_data.jsonl", split="train")
sft_cfg = SFTConfig(
    output_dir=OUTPUT_DIR, num_train_epochs=3,
    per_device_train_batch_size=4, gradient_accumulation_steps=4,
    learning_rate=2e-4, logging_steps=10, save_steps=100,
)
trainer = SFTTrainer(
    model=model, train_dataset=dataset,
    args=sft_cfg, processing_class=tokenizer,
)
trainer.train()
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"Saved airgapped LoRA adapter to {OUTPUT_DIR}")
```

</details>

Serve the resulting LoRA adapter through vLLM on port 8002 and register `llama-8b-finetuned` in `litellm_config.yaml`:

<details class="code-drop">
<summary><span class="code-drop__name">serve-lora-airgapped.sh</span><span class="code-drop__meta">Bash · 6 lines</span></summary>

```bash
vllm serve /path/to/models/llama-8b \
  --host 0.0.0.0 \
  --port 8002 \
  --enable-lora \
  --lora-modules llama-8b-finetuned=./fine-tuned-airgapped
```

</details>

**Verification**:

```bash
python -c "import unsloth"
```

The command verifies that Unsloth's custom Triton kernels and PEFT bindings load cleanly without outbound network checks.

## Wiring the Components

Three integration scripts connect Docling, Qdrant, LlamaIndex, LangGraph, LiteLLM, and Arize Phoenix into a completely offline retrieval and analysis pipeline.

### LlamaIndex Agent with LiteLLM, Qdrant, and Phoenix

Save `airgapped_agent.py` in `scripts/` to register OpenInference telemetry with the local Phoenix collector, load local BGE embeddings, query Qdrant, and synthesize answers through LiteLLM:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/airgapped_agent.py</span><span class="code-drop__meta">Python · 30 lines</span></summary>

```python
from phoenix.otel import register
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient

tracer_provider = register(endpoint="http://localhost:6006/v1/traces")
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)

Settings.llm = OpenAILike(
    model="llama-70b", api_base="http://localhost:4000/v1",
    api_key="sk-internal-master-key", is_chat_model=True, temperature=0,
)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="/path/to/models/bge-large", trust_remote_code=False,
)
qdrant = QdrantClient(host="localhost", port=6333)
store = QdrantVectorStore(client=qdrant, collection_name="internal_documents")
engine = VectorStoreIndex.from_vector_store(store).as_query_engine(similarity_top_k=5)

res = engine.query("What are the key findings from the latest security audit?")
print(res)
print(f"Retrieved {len(res.source_nodes)} source chunks.")
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-airgapped-agent.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
python scripts/airgapped_agent.py
```

</details>

Calling `register` and `LlamaIndexInstrumentor` before executing the query guarantees that both the Qdrant vector lookup and the LiteLLM chat completion appear as linked child spans inside the local Arize Phoenix UI.

### LangGraph Orchestrated Analysis Workflow

Save `airgapped_workflow.py` in `scripts/` to coordinate a LlamaIndex retrieval node and a synthesis node inside a checkpointed LangGraph state machine:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/airgapped_workflow.py</span><span class="code-drop__meta">Python · 39 lines</span></summary>

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient

llm = OpenAILike(model="llama-70b", api_base="http://localhost:4000/v1", api_key="sk-internal-master-key", is_chat_model=True)
Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(model_name="/path/to/models/bge-large", trust_remote_code=False)

store = QdrantVectorStore(client=QdrantClient(host="localhost", port=6333), collection_name="internal_documents")
index = VectorStoreIndex.from_vector_store(vector_store=store)

class AnalysisState(TypedDict):
    query: str
    retrieved_context: str
    analysis_result: str

def research_agent(state: AnalysisState) -> dict:
    res = index.as_query_engine(similarity_top_k=10).query(state["query"])
    return {"retrieved_context": "\n\n".join(n.text for n in res.source_nodes)}

def analysis_agent(state: AnalysisState) -> dict:
    prompt = f"Context:\n{state['retrieved_context']}\n\nAnalyze: {state['query']}"
    return {"analysis_result": str(llm.complete(prompt))}

graph = StateGraph(AnalysisState)
graph.add_node("research", research_agent)
graph.add_node("analysis", analysis_agent)
graph.add_edge(START, "research")
graph.add_edge("research", "analysis")
graph.add_edge("analysis", END)

with SqliteSaver.from_conn_string("airgapped_workflow.db") as saver:
    out = graph.compile(checkpointer=saver).invoke({"query": "Identify compliance gaps"}, config={"configurable": {"thread_id": "analysis-001"}})
    print(out["analysis_result"])
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-airgapped-workflow.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
python scripts/airgapped_workflow.py
```

</details>

The `research_agent` node queries Qdrant for the top ten relevant chunks and persists them into the `retrieved_context` key of `AnalysisState`, and `analysis_agent` invokes `llm.complete(prompt)` directly over that persisted context rather than re-querying the vector index.

### Docling-to-Qdrant Ingestion Pipeline

Save `ingest_airgapped_docs.py` in `scripts/` to convert accredited documents through Docling, chunk the Markdown along paragraph boundaries, compute local BGE embeddings, and upsert deterministic point IDs into Qdrant:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/ingest_airgapped_docs.py</span><span class="code-drop__meta">Python · 38 lines</span></summary>

```python
import os
import uuid
from docling.document_converter import DocumentConverter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

DOCS_DIR, COLL = "./classified_docs", "internal_documents"
EXTS = (".pdf", ".docx", ".md", ".txt")
embed_model = HuggingFaceEmbedding(model_name="/path/to/models/bge-large", trust_remote_code=False)

def chunk_md(text, max_chars=600):
    chunks, cur = [], ""
    for block in text.split("\n\n"):
        if len(cur) + len(block) > max_chars and cur:
            chunks.append(cur.strip())
            cur = ""
        cur = f"{cur}\n\n{block}" if cur else block
    return chunks + ([cur.strip()] if cur.strip() else [])

def main():
    conv, client = DocumentConverter(), QdrantClient(host="localhost", port=6333)
    for root, _, files in os.walk(DOCS_DIR):
        for name in [f for f in files if f.endswith(EXTS)]:
            path = os.path.join(root, name)
            chunks = chunk_md(conv.convert(path).document.export_to_markdown())
            points = [
                PointStruct(
                    id=str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{path}_{i}")),
                    vector=embed_model.get_text_embedding(c),
                    payload={"text": c, "source": path, "chunk_index": i},
                )
                for i, c in enumerate(chunks)
            ]
            if points:
                client.upsert(collection_name=COLL, points=points)
                print(f"Indexed {path}: {len(points)} chunks.")

if __name__ == "__main__":
    main()
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-airgapped-ingest.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
mkdir -p classified_docs
python scripts/ingest_airgapped_docs.py
```

</details>

Generating point identifiers with `uuid.uuid5` from the document path and chunk index ensures that re-running the ingestion script after a physical media drop overwrites updated chunks in place instead of creating duplicate vectors.

## Verification

| Check | Command | Expected Result |
|---|---|---|
| Agent frameworks | `python verify_frameworks.py` | Prints installed framework and orchestrator versions |
| Qdrant binary | `curl -s localhost:6333/readyz` | Confirms Qdrant storage engine is ready |
| vLLM server | `curl -s localhost:8000/v1/models` | Lists 70B reasoning model alias |
| SGLang server | `curl -s localhost:8001/v1/models` | Lists 8B structured model alias |
| LiteLLM proxy | `curl -s localhost:4000/v1/models` | Lists all three internal model routes |
| Docling parser | `python verify_docling.py` | Extracts text elements without outbound network calls |
| Phoenix collector | `curl -s localhost:6006/healthz` | Returns healthy HTTP status |
| Unsloth kernels | `python -c "import unsloth"` | Exits with code zero and no import errors |
| Traced RAG agent | `bash run-airgapped-agent.sh` | Prints grounded answer and records span in Phoenix |
| Agent workflow | `bash run-airgapped-workflow.sh` | Runs two-node analysis and saves SQLite state |
| Batch ingestion | `bash run-airgapped-ingest.sh` | Upserts deterministic BGE vectors into Qdrant |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `pip install` hangs on external connection | Pass `--no-index` and `--find-links` on every offline install command |
| Docling downloads weights at runtime | Export `DOCLING_ARTIFACTS_PATH` and `HF_HUB_OFFLINE=1` before running |
| vLLM and SGLang conflict on CUDA wheels | Install `vllm` and `sglang` inside separate virtual environments |
| Spans do not appear in Arize Phoenix | Call `phoenix.otel.register` and instrument LlamaIndex at startup |
| Embedding loader queries Hugging Face Hub | Pass the local `./models/bge-large` path and `trust_remote_code=False` |

The [Private and Airgapped Deployment](private-and-airgapped-deployment-configuration.html) stack is operational once all eleven verification checks pass. That companion architecture chapter details the sealed perimeter design, component tradeoffs, and layer substitution options.

## References

1. LlamaIndex Installation Guide, LlamaIndex Inc.
2. LangGraph Getting Started Guide, LangChain Inc.
3. Qdrant Quick Start Guide, Qdrant Solutions GmbH.
4. vLLM Installation Guide, vLLM Project.
5. SGLang Installation Guide, SGLang Project.
6. LiteLLM Proxy Documentation, BerriAI.
7. Docling Installation Guide, IBM Research and LF AI and Data Foundation.
8. Arize Phoenix Documentation, Arize AI.
9. Unsloth Installation Guide, Unsloth AI.
10. Hugging Face CLI Documentation, Hugging Face.
