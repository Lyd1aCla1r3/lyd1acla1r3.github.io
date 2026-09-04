# Private and Airgapped Deployment: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Private and Airgapped Deployment stack, covering air-gap transfer procedures, LlamaIndex and LangGraph setup, LiteLLM gateway configuration for internal-only routing, vLLM and SGLang model serving, Qdrant vector database provisioning, Docling document parsing, Arize Phoenix observability, and Unsloth fine-tuning, with integration wiring and end-to-end verification steps. -->

The Private and Airgapped Deployment architecture chapter explains the rationale behind each component selection, the network boundary constraint, and the substitutions required to eliminate all external dependencies. This guide provides the concrete installation commands, configuration snippets, and wiring steps needed to bring that architecture to a working state on isolated infrastructure. All installation steps assume that dependencies have been pre-staged through the air-gap transfer process described in the prerequisites.

## Prerequisites

- **Operating system**: Linux with systemd or a container runtime. All components run on Linux; macOS and Windows are not supported for production airgapped deployments.
- **Python**: Version 3.10 or later, with `pip` available. All Python packages must be pre-downloaded as wheel files and transferred to the airgapped network.
- **Node.js**: Version 18 or later, with `npx` available. Required for MCP server execution.
- **GPU hardware**: At least one NVIDIA GPU with 24GB+ VRAM for vLLM and SGLang serving. Multi-GPU configurations enable serving larger models. A separate GPU or shared GPU time is needed for Unsloth fine-tuning.
- **Network**: Internal network access between all components. No outbound internet connectivity exists by design.
- **Pre-staged artifacts**: All model weights, Python packages, Docker images, and Node.js packages must be downloaded on an internet-connected system, transferred to approved physical media, scanned according to organizational security policy, and installed on the airgapped network before proceeding.

### Air-Gap Transfer Procedure

On an internet-connected staging machine, download all required artifacts:

```bash
# Python packages: download wheels for offline installation
pip download -d ./offline_packages \
  llama-index llama-index-core llama-index-vector-stores-qdrant \
  llama-index-llms-openai-like llama-index-embeddings-huggingface \
  langgraph langgraph-checkpoint-sqlite langgraph-checkpoint-postgres \
  litellm qdrant-client docling arize-phoenix \
  opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp \
  unsloth peft transformers datasets accelerate bitsandbytes \
  uvicorn fastapi

# Model weights: download from Hugging Face
huggingface-cli download meta-llama/Llama-3.1-70B-Instruct --local-dir ./models/llama-70b
huggingface-cli download meta-llama/Llama-3.1-8B-Instruct --local-dir ./models/llama-8b
huggingface-cli download BAAI/bge-large-en-v1.5 --local-dir ./models/bge-large

# Qdrant binary
curl -L -o ./binaries/qdrant.tar.gz \
  https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-gnu.tar.gz

# MCP server packages
npm pack @modelcontextprotocol/server-filesystem
npm pack @modelcontextprotocol/server-git
```

Transfer the `offline_packages/`, `models/`, `binaries/`, and MCP `.tgz` files to approved media and follow the organizational transfer and scanning procedures.

## Step 1: LlamaIndex and LangGraph

LlamaIndex provides the RAG-focused agent framework, and LangGraph provides the orchestration layer. Install from pre-staged wheel files:

```bash
pip install --no-index --find-links ./offline_packages \
  llama-index llama-index-core llama-index-vector-stores-qdrant \
  llama-index-llms-openai-like llama-index-embeddings-huggingface \
  langgraph langgraph-checkpoint-sqlite
```

Production deployments should add the PostgreSQL checkpointer for multi-process state access:

```bash
pip install --no-index --find-links ./offline_packages \
  langgraph-checkpoint-postgres
```

**Verification**:

```python
import llama_index.core
import langgraph
print(f"LlamaIndex Core: {llama_index.core.__version__}")
print(f"LangGraph: {langgraph.__version__}")
```

A successful installation prints both version numbers without import errors.

## Step 2: Qdrant

Qdrant provides the vector database as a single binary with no external dependencies. Extract the pre-staged binary:

```bash
mkdir -p /opt/qdrant
tar -xzf ./binaries/qdrant.tar.gz -C /opt/qdrant
```

Create a configuration file at `/opt/qdrant/config.yaml`:

```yaml
storage:
  storage_path: /opt/qdrant/storage
  on_disk_payload: true

service:
  grpc_port: 6334
  http_port: 6333

cluster:
  enabled: false
```

Start the Qdrant server:

```bash
/opt/qdrant/qdrant --config-path /opt/qdrant/config.yaml
```

For production deployments, create a systemd service:

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

Initialize a collection using the Python client:

```bash
pip install --no-index --find-links ./offline_packages qdrant-client
```

```python
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

client = QdrantClient(host="localhost", port=6333)

client.create_collection(
    collection_name="internal_documents",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE
    )
)

info = client.get_collection("internal_documents")
print(f"Collection 'internal_documents' created: {info.points_count} points.")
```

The `size=1024` parameter matches the embedding dimension of the BGE-Large model used in this configuration. Adjust if using a different embedding model.

**Verification**:

```bash
curl http://localhost:6333/collections
```

A successful deployment returns a JSON response listing the created collection.

## Step 3: vLLM

vLLM provides high-throughput inference for general-purpose model requests. Install from pre-staged packages:

```bash
pip install --no-index --find-links ./offline_packages vllm
```

Start the vLLM server using the pre-staged model weights:

```bash
vllm serve /path/to/models/llama-70b \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 4 \
  --max-model-len 8192 \
  --enable-prefix-caching \
  --served-model-name llama-70b-instruct
```

The `--served-model-name` flag sets the model name that appears in the API response, which LiteLLM references in its routing table. Using a local path instead of a Hugging Face model ID bypasses any network download attempt.

**Verification**:

```bash
curl http://localhost:8000/v1/models
```

A successful deployment returns a JSON list containing `llama-70b-instruct`.

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-70b-instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 50
  }'
```

A successful test returns a chat completion response.

## Step 4: SGLang

SGLang provides structured output generation for tasks requiring constrained decoding. Install from pre-staged packages:

```bash
pip install --no-index --find-links ./offline_packages sglang
```

Start the SGLang server using the pre-staged model weights:

```bash
python -m sglang.launch_server \
  --model-path /path/to/models/llama-8b \
  --host 0.0.0.0 \
  --port 8001 \
  --served-model-name llama-8b-structured
```

The SGLang server runs on a separate port from vLLM, allowing both engines to operate concurrently. A smaller model is typical for the SGLang deployment, because structured output tasks involve shorter sequences and benefit from lower latency rather than maximum model capability.

**Verification**:

```bash
curl http://localhost:8001/v1/models
```

A successful deployment returns a JSON list containing `llama-8b-structured`.

## Step 5: LiteLLM Gateway

LiteLLM provides the unified gateway between LlamaIndex agents and the local serving engines. Install from pre-staged packages:

```bash
pip install --no-index --find-links ./offline_packages litellm uvicorn
```

Create `litellm_config.yaml` with internal-only routing:

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
      model: openai/BAAI/bge-large-en-v1.5
      api_base: http://vllm-server:8000/v1
      api_key: token-not-used

litellm_settings:
  success_callback: ["arize_phoenix"]

general_settings:
  master_key: sk-internal-master-key
```

Replace `vllm-server` and `sglang-server` with the actual hostnames or IP addresses of the serving machines. Every `api_base` entry points to an internal address; no external URLs appear in the configuration.

Start the LiteLLM proxy:

```bash
litellm --config litellm_config.yaml --host 0.0.0.0 --port 4000
```

**Verification**:

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-internal-master-key"
```

A successful deployment returns a JSON list of the three configured models.

## Step 6: Docling

Docling provides local document parsing. Install from pre-staged packages:

```bash
pip install --no-index --find-links ./offline_packages docling
```

Docling's compact vision models must be pre-staged along with the Python packages. On the internet-connected staging machine, run Docling once on a test document to trigger the model download, then copy the cached models from `~/.cache/docling/` to the airgapped system's equivalent path.

**Verification**:

```python
from docling.document_converter import DocumentConverter
print("Docling imported successfully.")
```

A successful installation prints the confirmation message. Full verification requires converting a test document:

```python
converter = DocumentConverter()
result = converter.convert("test_document.pdf")
print(f"Extracted {len(result.document.texts)} text elements.")
```

## Step 7: Arize Phoenix

Arize Phoenix provides self-hosted observability and tracing. Install from pre-staged packages:

```bash
pip install --no-index --find-links ./offline_packages \
  arize-phoenix opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

Start the Phoenix server:

```bash
phoenix serve --host 0.0.0.0 --port 6006
```

Set the environment variables that instrumented components use to export traces:

```bash
export PHOENIX_COLLECTOR_ENDPOINT="http://phoenix-server:6006"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://phoenix-server:6006"
```

Replace `phoenix-server` with the actual hostname or IP address.

**Verification**:

```bash
curl http://localhost:6006/healthz
```

A successful deployment returns a health status response. Access the Phoenix dashboard at `http://phoenix-server:6006` from any machine within the internal network.

## Step 8: Unsloth

Unsloth provides memory-efficient fine-tuning. Install from pre-staged packages:

```bash
pip install --no-index --find-links ./offline_packages \
  unsloth peft transformers datasets accelerate bitsandbytes
```

A minimal supervised fine-tuning script for the airgapped environment. Save as `scripts/finetune_airgapped.py`:

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

MODEL_PATH = "/path/to/models/llama-8b"
OUTPUT_DIR = "./fine-tuned-airgapped"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_PATH,
    max_seq_length=2048,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0,
    bias="none",
)

dataset = load_dataset(
    "json",
    data_files="/path/to/training_data.jsonl",
    split="train"
)

training_config = SFTConfig(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=10,
    save_steps=100,
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_config,
    tokenizer=tokenizer,
)

trainer.train()
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"Fine-tuned model saved to {OUTPUT_DIR}")
```

The training data file `training_data.jsonl` contains instruction-response pairs curated from Arize Phoenix production traces:

```json
{"text": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nSummarize the findings from document SEC-2024-0847.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nThe document identifies three compliance gaps in the Q3 audit...<|eot_id|>"}
```

After training, deploy the fine-tuned model to vLLM:

```bash
vllm serve /path/to/fine-tuned-airgapped \
  --host 0.0.0.0 \
  --port 8002 \
  --served-model-name llama-8b-finetuned
```

Add the fine-tuned model to the LiteLLM configuration:

```yaml
- model_name: llama-8b-finetuned
  litellm_params:
    model: openai/llama-8b-finetuned
    api_base: http://vllm-server:8002/v1
    api_key: token-not-used
```

**Verification**:

```python
import unsloth
import peft
print(f"Unsloth: {unsloth.__version__}")
print(f"PEFT: {peft.__version__}")
```

A successful installation prints both version numbers. Full fine-tuning verification requires running the training script with a sample dataset and confirming that the output directory contains adapter weights and tokenizer files.

## Wiring the Components

With all components installed individually, the final step connects them into the integrated pipeline described in the architecture chapter.

### LlamaIndex Agent with LiteLLM and Qdrant

Save the following script as `scripts/airgapped_agent.py`. It configures a LlamaIndex agent to perform retrieval-augmented generation over the local Qdrant collection, routing all inference through LiteLLM:

```python
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient

llm = OpenAILike(
    model="llama-70b",
    api_base="http://localhost:4000/v1",
    api_key="sk-internal-master-key",
    is_chat_model=True,
    temperature=0,
)

embed_model = HuggingFaceEmbedding(
    model_name="/path/to/models/bge-large",
    trust_remote_code=False,
)

Settings.llm = llm
Settings.embed_model = embed_model

qdrant_client = QdrantClient(host="localhost", port=6333)
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="internal_documents",
)

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine(similarity_top_k=5)

response = query_engine.query(
    "What are the key findings from the latest security audit?"
)

print("Response:")
print(response)
print(f"\nSources: {len(response.source_nodes)} chunks retrieved.")
```

### LangGraph Orchestrated Analysis Workflow

Save the following script as `scripts/airgapped_workflow.py`. It defines a LangGraph workflow with two LlamaIndex agents coordinating a multi-step analysis:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient
from typing import TypedDict

llm = OpenAILike(
    model="llama-70b",
    api_base="http://localhost:4000/v1",
    api_key="sk-internal-master-key",
    is_chat_model=True,
)

embed_model = HuggingFaceEmbedding(
    model_name="/path/to/models/bge-large",
    trust_remote_code=False,
)

Settings.llm = llm
Settings.embed_model = embed_model

qdrant_client = QdrantClient(host="localhost", port=6333)
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="internal_documents",
)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

class AnalysisState(TypedDict):
    query: str
    retrieved_context: str
    analysis_result: str

def research_agent(state: AnalysisState) -> AnalysisState:
    query_engine = index.as_query_engine(similarity_top_k=10)
    response = query_engine.query(state["query"])
    context = "\n\n".join([n.text for n in response.source_nodes])
    return {"retrieved_context": context}

def analysis_agent(state: AnalysisState) -> AnalysisState:
    query_engine = index.as_query_engine(similarity_top_k=3)
    prompt = f"Based on the following context, provide a detailed analysis:\n\n{state['retrieved_context']}\n\nQuestion: {state['query']}"
    response = query_engine.query(prompt)
    return {"analysis_result": str(response)}

graph = StateGraph(AnalysisState)
graph.add_node("research", research_agent)
graph.add_node("analysis", analysis_agent)
graph.add_edge(START, "research")
graph.add_edge("research", "analysis")
graph.add_edge("analysis", END)

checkpointer = SqliteSaver.from_conn_string("airgapped_workflow.db")
app = graph.compile(checkpointer=checkpointer)

result = app.invoke(
    {"query": "Identify compliance gaps from recent audit documents"},
    config={"configurable": {"thread_id": "analysis-001"}}
)

print("Analysis result:")
print(result["analysis_result"])
```

### Docling-to-Qdrant Ingestion Pipeline

Save the following script as `scripts/ingest_airgapped_docs.py`:

```python
import os
from docling.document_converter import DocumentConverter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import uuid

DOCS_DIR = "./classified_docs"
COLLECTION_NAME = "internal_documents"
CHUNK_SIZE = 500

embed_model = HuggingFaceEmbedding(
    model_name="/path/to/models/bge-large",
    trust_remote_code=False,
)

def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into chunks at sentence boundaries."""
    sentences = text.replace("\n", " ").split(". ")
    chunks = []
    current = []
    current_len = 0
    for sentence in sentences:
        if current_len + len(sentence) > chunk_size and current:
            chunks.append(". ".join(current) + ".")
            current = []
            current_len = 0
        current.append(sentence)
        current_len += len(sentence)
    if current:
        chunks.append(". ".join(current))
    return chunks

def main():
    converter = DocumentConverter()
    client = QdrantClient(host="localhost", port=6333)

    doc_files = []
    for root, dirs, files in os.walk(DOCS_DIR):
        for f in files:
            if f.endswith((".pdf", ".docx", ".md", ".txt")):
                doc_files.append(os.path.join(root, f))

    print(f"Found {len(doc_files)} documents to process.")

    for filepath in doc_files:
        print(f"Processing: {filepath}")
        result = converter.convert(filepath)
        text = result.document.export_to_markdown()
        chunks = chunk_text(text)

        points = []
        for i, chunk in enumerate(chunks):
            embedding = embed_model.get_text_embedding(chunk)
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "content": chunk,
                    "source": filepath,
                    "doc_type": os.path.splitext(filepath)[1],
                    "chunk_index": i,
                }
            ))

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )
        print(f"  Stored {len(chunks)} chunks.")

    info = client.get_collection(COLLECTION_NAME)
    print(f"\nTotal points in collection: {info.points_count}")

if __name__ == "__main__":
    main()
```

## Verification

The following end-to-end checks confirm that all components are installed, wired, and operational.

| Check | Command | Expected Result |
|---|---|---|
| LlamaIndex/LangGraph | `python -c "import llama_index.core, langgraph; print('OK')"` | Prints "OK" |
| Qdrant | `curl http://localhost:6333/collections` | Returns collection list |
| vLLM | `curl http://localhost:8000/v1/models` | Returns loaded model list |
| SGLang | `curl http://localhost:8001/v1/models` | Returns loaded model list |
| LiteLLM proxy | `curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-internal-master-key"` | Returns JSON model list |
| Docling | `python -c "from docling.document_converter import DocumentConverter; print('OK')"` | Prints "OK" |
| Arize Phoenix | `curl http://localhost:6006/healthz` | Returns health status |
| Unsloth | `python -c "import unsloth, peft; print('OK')"` | Prints "OK" |
| RAG agent | `python scripts/airgapped_agent.py` | Prints response with retrieved sources |
| Orchestrated workflow | `python scripts/airgapped_workflow.py` | Prints analysis result from two-agent pipeline |
| Document ingestion | Place test documents in `classified_docs/`, run `python scripts/ingest_airgapped_docs.py` | Reports chunks stored per document |

The Private and Airgapped Deployment stack is operational once all eleven checks pass. The architecture chapter provides the rationale behind each component selection, the network boundary constraint, and the design decisions governing how the layers interact within a sealed perimeter.

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
