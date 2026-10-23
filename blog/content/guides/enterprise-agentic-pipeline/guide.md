# Enterprise Agentic Pipeline: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Enterprise Agentic Pipeline, covering LangChain and LangGraph setup, LiteLLM gateway deployment, Weaviate vector database provisioning, Unstructured document parsing, Langfuse observability, vLLM model serving, and HF TRL fine-tuning, with integration wiring and end-to-end verification steps. -->

The [Architecture and Configuration](enterprise-agentic-pipeline-configuration.html) chapter explains the rationale behind each component selection, the multi-agent orchestration model, and the governance requirements driving the nine-layer design. This setup guide provides the installation commands, container manifests, Python wiring scripts, and verification checks needed to deploy that architecture on enterprise infrastructure. Each step provisions and verifies one layer in isolation before the wiring section connects the services into a traced, multi-tenant, multi-agent pipeline.

## Prerequisites

| Requirement | Details |
|---|---|
| Operating system | Linux host with `systemd` or a container orchestration cluster |
| Python runtime | Python 3.11, 3.12, or 3.13 with `pip` and virtual environment support |
| Node.js runtime | Node.js 18 or later with `npx` available for MCP servers |
| Container engine | Docker Engine and `docker compose` v2 for LiteLLM, Weaviate, and Langfuse |
| GPU hardware | Minimum one NVIDIA GPU with 24 GB VRAM; four 48 GB GPUs for 70B models |
| Upstream credentials | Commercial provider API keys or Hugging Face `HF_TOKEN` for gated weights |
| Network topology | Internal TCP connectivity across ports 3000, 4000, 8000, 8080, and 50051 |

## Step 1: LangChain and LangGraph

LangChain supplies the specialist agent abstractions, prompt templates, and model wrappers, while LangGraph supplies the stateful graph orchestrator that coordinates multiple specialist agents across cyclic or branching workflows. Install the core packages and the OpenAI-compatible client integration from PyPI inside a dedicated Python virtual environment:

```bash
pip install langchain \
  langgraph langchain-core
```

LangGraph requires a checkpointer backend to serialize the workflow state dictionary after every node transition so interrupted runs can resume without repeating completed agent steps. Install the SQLite checkpointer for local staging and single-process verification:

<details class="code-drop">
<summary><span class="code-drop__name">install-sqlite-checkpointer.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
pip install langgraph-checkpoint-sqlite
```

</details>

Multi-worker production deployments should also install `langgraph-checkpoint-postgres` so concurrent orchestrator replicas share durable state in PostgreSQL with row-level locking and automatic connection pooling.

**Verification**:

Save or execute the following version check to confirm that both framework and orchestrator packages import cleanly:

<details class="code-drop">
<summary><span class="code-drop__name">verify_langchain.py</span><span class="code-drop__meta">Python · 5 lines</span></summary>

```python
from importlib.metadata import version
import langchain_core

print(f"LangChain Core: {langchain_core.__version__}")
print(f"LangGraph: {version('langgraph')}")
```

</details>

```bash
python verify_langchain.py
```

The script prints the installed semantic version strings for both packages without import errors.

## Step 2: LiteLLM Gateway

LiteLLM operates as the centralized model gateway between LangChain agents and upstream model endpoints, enforcing team budgets, translating provider APIs into a single OpenAI-compatible surface, and streaming telemetry spans to Langfuse.

### Gateway Configuration

Create `litellm_config.yaml` to map unified model aliases (`gpt-4o`, `claude-sonnet`, `self-hosted-llama`) to commercial APIs and the internal vLLM server while registering the Langfuse success callback:

<details class="code-drop">
<summary><span class="code-drop__name">litellm_config.yaml</span><span class="code-drop__meta">YAML · 25 lines</span></summary>

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

  - model_name: self-hosted-llama
    litellm_params:
      model: openai/meta-llama/Llama-3.1-70B-Instruct
      api_base: http://host.docker.internal:8000/v1
      api_key: token-placeholder

litellm_settings:
  success_callback: ["langfuse"]
  max_budget: 1000
  budget_duration: 30d

general_settings:
  master_key: sk-litellm-master-key
```

</details>

Export the upstream provider credentials, the PostgreSQL connection string used for virtual key and budget storage, and the Langfuse project keys before starting the proxy container. Storing upstream provider keys only in the gateway environment prevents individual agent repositories from handling raw OpenAI or Anthropic credentials:

<details class="code-drop">
<summary><span class="code-drop__name">litellm_env.sh</span><span class="code-drop__meta">Bash · 6 lines</span></summary>

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DATABASE_URL="postgresql://user:pass@localhost:5432/litellm"
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="http://host.docker.internal:3000"
```

</details>

### Container Deployment

Launch the LiteLLM proxy container on port 4000 with the configuration file mounted and the environment variables passed through:

<details class="code-drop">
<summary><span class="code-drop__name">run-litellm.sh</span><span class="code-drop__meta">Bash · 11 lines</span></summary>

```bash
docker run -d \
  --name litellm-proxy \
  -p 4000:4000 \
  --add-host=host.docker.internal:host-gateway \
  -v ./litellm_config.yaml:/app/config.yaml \
  -e OPENAI_API_KEY -e ANTHROPIC_API_KEY \
  -e LANGFUSE_PUBLIC_KEY -e LANGFUSE_SECRET_KEY \
  -e LANGFUSE_HOST -e DATABASE_URL \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml
```

</details>

The `host.docker.internal` mapping resolves services running on the Docker host; replace it with internal DNS hostnames in multi-node Kubernetes or virtual machine deployments.

### Team Virtual Keys

Generate scoped virtual API keys so each engineering team authenticates against LiteLLM with an isolated monthly spend ceiling tracked in PostgreSQL:

<details class="code-drop">
<summary><span class="code-drop__name">create-virtual-key.sh</span><span class="code-drop__meta">Bash · 9 lines</span></summary>

```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-litellm-master-key" \
  -H "Content-Type: application/json" \
  -d '{
    "team_id": "research-team",
    "max_budget": 200,
    "budget_duration": "30d"
  }'
```

</details>

Distribute the returned `key` token (`sk-litellm-team-key`) to the team's LangChain agents instead of sharing raw provider credentials. LiteLLM increments the team's spend counter after every completion and returns an HTTP 429 budget-exceeded error if cumulative usage reaches the $200 thirty-day limit.

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">verify-litellm.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
curl -s http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-litellm-master-key"
```

</details>

The gateway returns a JSON object listing `gpt-4o`, `claude-sonnet`, and `self-hosted-llama`.

## Step 3: Weaviate

Weaviate provides self-hosted vector storage with storage-level multi-tenancy and hybrid BM25-plus-dense retrieval. Deploying Weaviate via Docker Compose exposes both the REST interface on port 8080 and the high-throughput gRPC interface on port 50051 required by the v4 Python client.

Create `docker-compose-weaviate.yaml` with persistent volume storage and the `text2vec-openai` vectorizer module enabled:

<details class="code-drop">
<summary><span class="code-drop__name">docker-compose-weaviate.yaml</span><span class="code-drop__meta">YAML · 20 lines</span></summary>

```yaml
services:
  weaviate:
    image: cr.weaviate.io/semitechnologies/weaviate:latest
    ports:
      - "8080:8080"
      - "50051:50051"
    volumes:
      - weaviate_data:/var/lib/weaviate
    environment:
      QUERY_DEFAULTS_LIMIT: 25
      AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED: "true"
      PERSISTENCE_DATA_PATH: "/var/lib/weaviate"
      ENABLE_MODULES: "text2vec-openai"
      DEFAULT_VECTORIZER_MODULE: "text2vec-openai"
      OPENAI_APIKEY: ${OPENAI_API_KEY}
      CLUSTER_HOSTNAME: "node1"

volumes:
  weaviate_data:
```

</details>

Start the Weaviate container in detached mode and install the v4 Python client library:

<details class="code-drop">
<summary><span class="code-drop__name">start-weaviate.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
docker compose -f docker-compose-weaviate.yaml up -d
```

</details>

```bash
pip install weaviate-client
```

Save and run `scripts/init_weaviate.py` to create the `EnterpriseDocuments` collection with storage-level multi-tenancy and automatic tenant provisioning enabled. Defining explicit text and integer properties ensures that each tenant shard enforces consistent schema types across ingested document chunks:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/init_weaviate.py</span><span class="code-drop__meta">Python · 21 lines</span></summary>

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_local()
collection = client.collections.create(
    name="EnterpriseDocuments",
    vector_config=Configure.Vectors.text2vec_openai(),
    multi_tenancy_config=Configure.multi_tenancy(
        enabled=True,
        auto_tenant_creation=True,
    ),
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="doc_type", data_type=DataType.TEXT),
        Property(name="chunk_index", data_type=DataType.INT),
    ],
)
print(f"Collection '{collection.name}' ready with multi-tenancy.")
client.close()
```

</details>

```bash
python \
  scripts/init_weaviate.py
```

**Verification**:

```bash
curl -s \
  localhost:8080/v1/meta
```

The endpoint returns a JSON document containing the Weaviate server version and active vectorizer modules.

## Step 4: Unstructured

Unstructured partitions heterogeneous enterprise files (PDFs, PowerPoint decks, Word documents, HTML archives, and scanned images) into typed structural elements before chunking so tables and section headers stay intact.

```bash
pip install \
  "unstructured[all-docs]"
```

The `[all-docs]` extra installs Python bindings for layout detection, table extraction, and optical character recognition. On Linux hosts, install the companion system packages (`poppler-utils`, `tesseract-ocr`, and `libmagic`) through the distribution package manager so PDF rendering, image OCR, and MIME-type inspection succeed without runtime fallback errors.

**Verification**:

Save and run `verify_unstructured.py` against a sample PDF to confirm that element partitioning operates locally:

<details class="code-drop">
<summary><span class="code-drop__name">verify_unstructured.py</span><span class="code-drop__meta">Python · 6 lines</span></summary>

```python
from unstructured.partition.auto import partition

elements = partition(filename="test_document.pdf")
print(f"Extracted {len(elements)} elements.")
for el in elements[:3]:
    print(f"  {el.category}: {str(el)[:80]}")
```

</details>

The script prints the extracted element count and labels each structural block (`Title`, `NarrativeText`, `Table`).

## Step 5: Langfuse

Langfuse captures full-stack execution traces, calculates per-team token spend, and exports curated datasets for fine-tuning. The official Docker Compose stack deploys the Langfuse web server, asynchronous ingestion workers, PostgreSQL, ClickHouse, Redis, and MinIO blob storage. Current Langfuse Python SDK releases and the LiteLLM callback integration require Langfuse server v3 rather than the deprecated v2 single-container image.

Clone the Langfuse repository and start the multi-container stack:

<details class="code-drop">
<summary><span class="code-drop__name">deploy-langfuse.sh</span><span class="code-drop__meta">Bash · 4 lines</span></summary>

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d
```

</details>

Replace every default credential marked `# CHANGEME` in `docker-compose.yml` before exposing the stack on an internal network. The web container takes two to three minutes to initialize its database migrations and log `Ready` on port 3000; open `http://localhost:3000` in a browser, create an initial organization project, and copy the generated `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` into the LiteLLM and agent environments.

Install the Langfuse Python SDK for LangChain and LangGraph callback instrumentation:

```bash
pip install langfuse
```

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">verify-langfuse.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
curl -s http://localhost:3000/api/public/health
```

</details>

The health endpoint returns a JSON status payload confirming that the Langfuse web tier and backing stores are reachable.

## Step 6: vLLM

vLLM serves self-hosted open-weight checkpoints and fine-tuned LoRA adapters with PagedAttention memory management and continuous batching. Install `vllm` on a Linux GPU node with NVIDIA drivers and CUDA configured:

```bash
pip install vllm
```

Authenticate with Hugging Face (`hf auth login` or `export HF_TOKEN=...`) after accepting the Llama 3.1 community license, then launch the OpenAI-compatible serving endpoint on port 8000:

<details class="code-drop">
<summary><span class="code-drop__name">start-vllm.sh</span><span class="code-drop__meta">Bash · 7 lines</span></summary>

```bash
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 4 \
  --max-model-len 8192 \
  --enable-prefix-caching
```

</details>

Setting `--tensor-parallel-size 4` shards the 140 GB BF16 checkpoint across four 48 GB GPUs; single-GPU 24 GB staging hosts can substitute `meta-llama/Llama-3.1-8B-Instruct` with `--tensor-parallel-size 1`. The `--enable-prefix-caching` flag caches shared system prompt KV blocks across concurrent specialist agent turns, reducing time-to-first-token when multiple LangChain agents share standardized role instructions.

**Verification**:

```bash
curl -s \
  localhost:8000/v1/models
```

Test chat completion generation against the running vLLM server to confirm that tensor-parallel worker processes respond cleanly:

<details class="code-drop">
<summary><span class="code-drop__name">verify-vllm-chat.sh</span><span class="code-drop__meta">Bash · 8 lines</span></summary>

```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-70B-Instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 50
  }'
```

</details>

## Step 7: HF TRL

Hugging Face TRL and PEFT train compact LoRA adapters from curated Langfuse production traces so domain-specific tasks can shift from expensive frontier APIs to self-hosted models. Install the training and quantization libraries:

```bash
pip install trl peft \
  transformers datasets \
  accelerate bitsandbytes
```

Save the following supervised fine-tuning script as `scripts/finetune.py`:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/finetune.py</span><span class="code-drop__meta">Python · 36 lines</span></summary>

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
OUTPUT_DIR = "./fine-tuned-model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=BitsAndBytesConfig(load_in_4bit=True),
    device_map="auto",
)
lora_cfg = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"], bias="none", task_type="CAUSAL_LM",
)
dataset = load_dataset("json", data_files="training_data.jsonl", split="train")
sft_cfg = SFTConfig(
    output_dir=OUTPUT_DIR, num_train_epochs=3,
    per_device_train_batch_size=4, gradient_accumulation_steps=4,
    learning_rate=2e-4, logging_steps=10, save_steps=100,
)
trainer = SFTTrainer(
    model=model, train_dataset=dataset, peft_config=lora_cfg,
    args=sft_cfg, processing_class=tokenizer,
)
trainer.train()
trainer.save_model(OUTPUT_DIR)
print(f"Saved adapter weights to {OUTPUT_DIR}")
```

</details>

Format `training_data.jsonl` with one instruction-response record per line exported from annotated Langfuse production traces:

<details class="code-drop">
<summary><span class="code-drop__name">training_data.jsonl</span><span class="code-drop__meta">JSONL · 1 line</span></summary>

```json
{"text": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nSummarize the Q3 revenue report.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nQ3 revenue increased 12% year-over-year.<|eot_id|>"}
```

</details>

**Verification**:

```bash
python -c "import trl"
```

The command verifies that `trl`, `peft`, and their CUDA quantization dependencies resolve without import errors.

## Wiring the Components

With all infrastructure layers running, three integration scripts connect LangChain, LangGraph, LiteLLM, Langfuse, Unstructured, and Weaviate into an end-to-end enterprise pipeline.

### LangChain Agent with LiteLLM and Langfuse

Save `scripts/enterprise_agent.py` to route specialist agent calls through the LiteLLM gateway using a team virtual key while streaming execution spans to Langfuse:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/enterprise_agent.py</span><span class="code-drop__meta">Python · 26 lines</span></summary>

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler as LangfuseHandler

litellm_model = ChatOpenAI(
    model="gpt-4o",
    base_url="http://localhost:4000/v1",
    api_key="sk-litellm-team-key",
    temperature=0,
)
Langfuse(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    base_url="http://localhost:3000",
)
handler = LangfuseHandler()
messages = [
    SystemMessage(content="Provide concise, factual responses."),
    HumanMessage(content="Summarize multi-agent orchestration benefits."),
]
res = litellm_model.invoke(messages, config={"callbacks": [handler]})
print(res.content)
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-enterprise-agent.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
python scripts/enterprise_agent.py
```

</details>

The agent authenticates against LiteLLM on port 4000 with `sk-litellm-team-key` rather than an upstream OpenAI key, and both the LangChain callback handler and LiteLLM's proxy callback record trace spans in Langfuse on port 3000.

### LangGraph Multi-Agent Workflow

Save `scripts/multi_agent_workflow.py` to orchestrate a research node and a writing node with SQLite state checkpointing and unified Langfuse trace propagation:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/multi_agent_workflow.py</span><span class="code-drop__meta">Python · 39 lines</span></summary>

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler as LangfuseHandler

class WorkflowState(TypedDict):
    task: str
    research_result: str
    final_output: str

llm = ChatOpenAI(model="gpt-4o", base_url="http://localhost:4000/v1", api_key="sk-litellm-team-key")
Langfuse(public_key="pk-lf-...", secret_key="sk-lf-...", base_url="http://localhost:3000")
handler = LangfuseHandler()

def research_agent(state: WorkflowState) -> dict:
    msgs = [SystemMessage(content="Gather key facts."), HumanMessage(content=state["task"])]
    return {"research_result": llm.invoke(msgs, config={"callbacks": [handler]}).content}

def writing_agent(state: WorkflowState) -> dict:
    msgs = [SystemMessage(content="Write a concise summary."), HumanMessage(content=state["research_result"])]
    return {"final_output": llm.invoke(msgs, config={"callbacks": [handler]}).content}

graph = StateGraph(WorkflowState)
graph.add_node("research", research_agent)
graph.add_node("writing", writing_agent)
graph.add_edge(START, "research")
graph.add_edge("research", "writing")
graph.add_edge("writing", END)

with SqliteSaver.from_conn_string("enterprise_workflow.db") as saver:
    app = graph.compile(checkpointer=saver)
    out = app.invoke({"task": "Compare self-hosted vs commercial LLM serving"}, config={"configurable": {"thread_id": "demo-001"}})
    print(out["final_output"])
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-multi-agent-workflow.sh</span><span class="code-drop__meta">Bash · 1 line</span></summary>

```bash
python scripts/multi_agent_workflow.py
```

</details>

Passing a deterministic `thread_id` (`demo-001`) instructs `SqliteSaver` to persist the intermediate `research_result` dictionary to `enterprise_workflow.db` before `writing_agent` executes, allowing interrupted runs to resume from the last completed node.

### Unstructured-to-Weaviate Ingestion Pipeline

Save `scripts/ingest_enterprise_docs.py` to partition enterprise documents, chunk them along section titles, and insert the resulting chunks into a tenant-isolated Weaviate partition:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/ingest_enterprise_docs.py</span><span class="code-drop__meta">Python · 31 lines</span></summary>

```python
import os
import weaviate
from weaviate.classes.tenants import Tenant
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title

DOCS_DIR, TENANT = "./enterprise_docs", "engineering-team"
EXTS = (".pdf", ".docx", ".pptx", ".html", ".md")

client = weaviate.connect_to_local()
coll = client.collections.get("EnterpriseDocuments")
coll.tenants.create([Tenant(name=TENANT)])
tenant_coll = coll.with_tenant(TENANT)

for root, _, files in os.walk(DOCS_DIR):
    for name in [f for f in files if f.endswith(EXTS)]:
        path = os.path.join(root, name)
        chunks = chunk_by_title(partition(filename=path), max_characters=500)
        for idx, chunk in enumerate(chunks):
            tenant_coll.data.insert({
                "content": str(chunk),
                "source": path,
                "doc_type": os.path.splitext(path)[1],
                "chunk_index": idx,
            })
        print(f"Stored {len(chunks)} chunks from {path} in tenant '{TENANT}'.")

total = tenant_coll.aggregate.over_all(total_count=True).total_count
print(f"Total objects in tenant '{TENANT}': {total}")
client.close()
```

</details>

<details class="code-drop">
<summary><span class="code-drop__name">run-enterprise-ingest.sh</span><span class="code-drop__meta">Bash · 2 lines</span></summary>

```bash
mkdir -p enterprise_docs
python scripts/ingest_enterprise_docs.py
```

</details>

Scoping insertions via `coll.with_tenant(TENANT)` guarantees that engineering documents reside in a separate storage shard from legal or finance documents indexed under other tenant names.

## Verification

| Check | Command | Expected Result |
|---|---|---|
| Agent frameworks | `python verify_langchain.py` | Prints installed framework and orchestrator versions |
| LiteLLM gateway | `curl -s localhost:4000/v1/models` | Returns JSON catalog of routed models |
| Weaviate cluster | `curl -s localhost:8080/v1/meta` | Returns server metadata and active modules |
| Unstructured | `python verify_unstructured.py` | Prints extracted structural element categories |
| Langfuse server | `bash verify-langfuse.sh` | Returns healthy status JSON payload |
| vLLM engine | `curl -s localhost:8000/v1/models` | Lists loaded open-weight checkpoint |
| HF TRL stack | `python -c "import trl, peft"` | Exits with code zero and no import errors |
| Single agent | `bash run-enterprise-agent.sh` | Prints completion and records span in Langfuse |
| Agent workflow | `bash run-multi-agent-workflow.sh` | Executes two-node graph and persists SQLite state |
| Doc ingestion | `bash run-enterprise-ingest.sh` | Populates engineering tenant shard in Weaviate |

## Troubleshooting

| Symptom | Fix |
|---|---|
| LiteLLM container cannot reach local vLLM or Langfuse | Pass `--add-host` with `host.docker.internal` to `docker run` on Linux hosts |
| Virtual key generation fails with database error | Verify `DATABASE_URL` points to an initialized PostgreSQL database reachable from the container |
| Weaviate client raises gRPC connection error | Expose port 50051 alongside port 8080 in the Weaviate Compose manifest |
| Unstructured fails on PDF or image files | Install `poppler-utils` and `tesseract-ocr` plus the system magic library on the host |
| vLLM exits with CUDA out-of-memory error | Increase `--tensor-parallel-size` or lower `--max-model-len` to fit available GPU VRAM |

The [Enterprise Agentic Pipeline](enterprise-agentic-pipeline-configuration.html) is operational once all ten verification checks pass. That companion architecture chapter details the governance model, layer tradeoffs, and component substitution options across all nine layers.

## References

1. LangChain Installation Guide, LangChain Inc.
2. LangGraph Getting Started Guide, LangChain Inc.
3. LiteLLM Proxy Documentation, BerriAI.
4. Weaviate Docker Installation Guide, Weaviate B.V.
5. Unstructured Installation Guide, Unstructured Technologies.
6. Langfuse Self-Hosting Documentation, Langfuse GmbH.
7. vLLM Installation Guide, vLLM Project.
8. Hugging Face TRL Documentation, Hugging Face.
9. Hugging Face PEFT Documentation, Hugging Face.
10. Weaviate Python Client Documentation, Weaviate B.V.
