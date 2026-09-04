# Enterprise Agentic Pipeline: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Enterprise Agentic Pipeline, covering LangChain and LangGraph setup, LiteLLM gateway deployment, Weaviate vector database provisioning, Unstructured document parsing, Langfuse observability, vLLM model serving, and HF TRL fine-tuning, with integration wiring and end-to-end verification steps. -->

The Enterprise Agentic Pipeline architecture chapter explains the rationale behind each component selection, the multi-agent orchestration model, and the governance requirements driving the design. This guide provides the concrete installation commands, configuration snippets, and wiring steps needed to bring that architecture to a working state on enterprise infrastructure.

## Prerequisites

- **Operating system**: Linux with systemd or a container orchestration platform
- **Python**: Version 3.10 or later, with `pip` available
- **Node.js**: Version 18 or later, with `npx` available
- **Docker**: Required for Weaviate, Langfuse, and LiteLLM proxy deployments
- **GPU hardware**: At least one NVIDIA GPU with 24GB+ VRAM for vLLM serving. Multi-GPU configurations enable serving larger models.
- **API keys**: At least one commercial model provider account for LiteLLM routing. Self-hosted-only deployments can omit this requirement.
- **Network**: Internal network access between all components. No public internet exposure is required for self-hosted components.

## Step 1: LangChain and LangGraph

LangChain provides the agent framework, and LangGraph provides the orchestration layer. Both install from PyPI.

```bash
pip install langchain langchain-core langchain-community langgraph
```

LangGraph requires a checkpointer backend for persistent state. The SQLite checkpointer provides a zero-configuration starting point:

```bash
pip install langgraph-checkpoint-sqlite
```

Production deployments should use the PostgreSQL checkpointer for reliability and multi-process access:

```bash
pip install langgraph-checkpoint-postgres
```

**Verification**:

```python
import langchain_core
import langgraph
print(f"LangChain Core: {langchain_core.__version__}")
print(f"LangGraph: {langgraph.__version__}")
```

A successful installation prints both version numbers without import errors.

## Step 2: LiteLLM Gateway

LiteLLM provides the unified gateway between agents and model providers. The proxy runs as a Docker container or a standalone Python process.

### Docker deployment

```bash
docker run -d \
  --name litellm-proxy \
  -p 4000:4000 \
  -v $(pwd)/litellm_config.yaml:/app/config.yaml \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml
```

### Configuration

Create `litellm_config.yaml` with model routing rules:

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

  - model_name: self-hosted-llama
    litellm_params:
      model: openai/meta-llama/Llama-3.1-70B-Instruct
      api_base: http://vllm-server:8000/v1
      api_key: token-placeholder

litellm_settings:
  success_callback: ["langfuse"]
  max_budget: 1000
  budget_duration: 30d

general_settings:
  master_key: sk-litellm-master-key
```

Set environment variables for API keys and Langfuse integration:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="http://langfuse-server:3000"
```

**Verification**:

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-litellm-master-key"
```

A successful deployment returns a JSON list of configured models.

### Virtual keys for team isolation

Generate virtual API keys for each team:

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

Each team uses its virtual key to authenticate with LiteLLM. The gateway tracks per-team usage against the configured budget cap.

## Step 3: Weaviate

Weaviate provides the multi-tenant vector database. A Docker Compose deployment provides the quickest path to a running instance.

Create `docker-compose-weaviate.yaml`:

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

```bash
docker compose -f docker-compose-weaviate.yaml up -d
```

Initialize a multi-tenant collection using the Weaviate Python client:

```bash
pip install weaviate-client
```

```python
import weaviate
from weaviate.classes.config import Configure, Property, DataType

client = weaviate.connect_to_local()

collection = client.collections.create(
    name="EnterpriseDocuments",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    multi_tenancy_config=Configure.multi_tenancy(
        enabled=True,
        auto_tenant_creation=True
    ),
    properties=[
        Property(name="content", data_type=DataType.TEXT),
        Property(name="source", data_type=DataType.TEXT),
        Property(name="doc_type", data_type=DataType.TEXT),
        Property(name="chunk_index", data_type=DataType.INT),
    ]
)

print(f"Collection '{collection.name}' created with multi-tenancy enabled.")
client.close()
```

**Verification**:

```bash
curl http://localhost:8080/v1/meta
```

A successful deployment returns Weaviate metadata including version and configured modules.

## Step 4: Unstructured

Unstructured handles enterprise document parsing. The open-source library processes documents locally.

```bash
pip install unstructured[all-docs]
```

The `[all-docs]` extra installs dependencies for PDF, DOCX, PPTX, HTML, and image-based OCR processing. The initial installation downloads several hundred megabytes of parsing models.

**Verification**:

```python
from unstructured.partition.auto import partition

elements = partition(filename="test_document.pdf")
print(f"Extracted {len(elements)} elements.")
for el in elements[:3]:
    print(f"  {el.category}: {str(el)[:80]}")
```

A successful installation partitions the test document and prints element categories such as `Title`, `NarrativeText`, and `Table`.

## Step 5: Langfuse

Langfuse provides production observability. A Docker Compose deployment runs the full Langfuse stack.

Create `docker-compose-langfuse.yaml`:

```yaml
services:
  langfuse-server:
    image: langfuse/langfuse:2
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://langfuse:langfuse@langfuse-db:5432/langfuse
      NEXTAUTH_SECRET: a-random-secret-string
      NEXTAUTH_URL: http://localhost:3000
      SALT: a-random-salt-string
    depends_on:
      - langfuse-db

  langfuse-db:
    image: postgres:16
    environment:
      POSTGRES_USER: langfuse
      POSTGRES_PASSWORD: langfuse
      POSTGRES_DB: langfuse
    volumes:
      - langfuse_pgdata:/var/lib/postgresql/data

volumes:
  langfuse_pgdata:
```

```bash
docker compose -f docker-compose-langfuse.yaml up -d
```

After startup, access the Langfuse dashboard at `http://localhost:3000`, create a project, and generate API keys for the `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` environment variables referenced in the LiteLLM configuration.

Install the Langfuse Python SDK for direct LangChain integration:

```bash
pip install langfuse
```

**Verification**:

```bash
curl http://localhost:3000/api/public/health
```

A successful deployment returns a health status indicating the server and database are operational.

## Step 6: vLLM

vLLM provides high-throughput serving for self-hosted models. Installation requires a Linux system with NVIDIA GPU drivers and CUDA toolkit.

```bash
pip install vllm
```

Start the vLLM server with a model:

```bash
vllm serve meta-llama/Llama-3.1-70B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 4 \
  --max-model-len 8192 \
  --enable-prefix-caching
```

The `--tensor-parallel-size 4` flag distributes inference across 4 GPUs. Adjust based on available hardware. The `--enable-prefix-caching` flag activates KV cache reuse for shared system prompts, which is common in enterprise agent deployments.

**Verification**:

```bash
curl http://localhost:8000/v1/models
```

A successful deployment returns a JSON list containing the loaded model. Test inference:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-70B-Instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 50
  }'
```

A successful test returns a chat completion response.

## Step 7: HF TRL

HF TRL and PEFT provide the fine-tuning pipeline. Installation uses pip.

```bash
pip install trl peft transformers datasets accelerate bitsandbytes
```

A minimal supervised fine-tuning script demonstrates the pipeline. Save as `scripts/finetune.py`:

```python
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
OUTPUT_DIR = "./fine-tuned-model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    load_in_4bit=True,
    device_map="auto"
)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

dataset = load_dataset("json", data_files="training_data.jsonl", split="train")

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
    peft_config=lora_config,
    args=training_config,
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model(OUTPUT_DIR)
print(f"Fine-tuned model saved to {OUTPUT_DIR}")
```

The training data file `training_data.jsonl` should contain one JSON object per line with instruction-response pairs exported from Langfuse production traces:

```json
{"text": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nSummarize the Q3 revenue report.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nQ3 revenue increased 12% year-over-year...<|eot_id|>"}
```

**Verification**:

```python
import trl
import peft
print(f"TRL: {trl.__version__}")
print(f"PEFT: {peft.__version__}")
```

A successful installation prints both version numbers. Full fine-tuning verification requires running the training script with a sample dataset and confirming that the output directory contains adapter weights.

## Wiring the Components

With all components installed individually, the final step connects them into the integrated pipeline described in the architecture chapter.

### LangChain Agent with LiteLLM and Langfuse

Save the following script as `scripts/enterprise_agent.py`. It configures a LangChain agent to route model calls through LiteLLM and export traces to Langfuse:

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse.callback import CallbackHandler as LangfuseHandler

litellm_model = ChatOpenAI(
    model="gpt-4o",
    base_url="http://localhost:4000/v1",
    api_key="sk-litellm-team-key",
    temperature=0
)

langfuse_handler = LangfuseHandler(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="http://localhost:3000"
)

messages = [
    SystemMessage(content="Provide concise, factual responses."),
    HumanMessage(content="Summarize the key benefits of multi-agent orchestration.")
]

response = litellm_model.invoke(
    messages,
    config={"callbacks": [langfuse_handler]}
)

print(response.content)
print("Trace exported to Langfuse.")
```

### LangGraph Multi-Agent Workflow

Save the following script as `scripts/multi_agent_workflow.py`. It defines a minimal LangGraph workflow with two specialized agents:

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langfuse.callback import CallbackHandler as LangfuseHandler
from typing import TypedDict

class WorkflowState(TypedDict):
    task: str
    research_result: str
    final_output: str

llm = ChatOpenAI(
    model="gpt-4o",
    base_url="http://localhost:4000/v1",
    api_key="sk-litellm-team-key"
)

langfuse_handler = LangfuseHandler(
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="http://localhost:3000"
)

def research_agent(state: WorkflowState) -> WorkflowState:
    messages = [
        SystemMessage(content="Gather key facts about the given topic."),
        HumanMessage(content=state["task"])
    ]
    response = llm.invoke(messages, config={"callbacks": [langfuse_handler]})
    return {"research_result": response.content}

def writing_agent(state: WorkflowState) -> WorkflowState:
    messages = [
        SystemMessage(content="Write a concise summary from the research."),
        HumanMessage(content=state["research_result"])
    ]
    response = llm.invoke(messages, config={"callbacks": [langfuse_handler]})
    return {"final_output": response.content}

graph = StateGraph(WorkflowState)
graph.add_node("research", research_agent)
graph.add_node("writing", writing_agent)
graph.add_edge(START, "research")
graph.add_edge("research", "writing")
graph.add_edge("writing", END)

checkpointer = SqliteSaver.from_conn_string("enterprise_workflow.db")
app = graph.compile(checkpointer=checkpointer)

result = app.invoke(
    {"task": "Analyze the tradeoffs of self-hosted vs commercial LLM serving"},
    config={"configurable": {"thread_id": "demo-001"}}
)

print("Final output:")
print(result["final_output"])
```

### Unstructured-to-Weaviate Ingestion Pipeline

Save the following script as `scripts/ingest_enterprise_docs.py`:

```python
import os
import weaviate
from weaviate.classes.tenants import Tenant
from unstructured.partition.auto import partition
from unstructured.chunking.title import chunk_by_title

DOCS_DIR = "./enterprise_docs"
TENANT_NAME = "engineering-team"

client = weaviate.connect_to_local()
collection = client.collections.get("EnterpriseDocuments")

collection.tenants.create([Tenant(name=TENANT_NAME)])
tenant_collection = collection.with_tenant(TENANT_NAME)

doc_files = []
for root, dirs, files in os.walk(DOCS_DIR):
    for f in files:
        if f.endswith((".pdf", ".docx", ".pptx", ".html", ".md")):
            doc_files.append(os.path.join(root, f))

print(f"Found {len(doc_files)} documents to process.")

for filepath in doc_files:
    print(f"Processing: {filepath}")
    elements = partition(filename=filepath)
    chunks = chunk_by_title(elements, max_characters=500)

    for i, chunk in enumerate(chunks):
        tenant_collection.data.insert({
            "content": str(chunk),
            "source": filepath,
            "doc_type": os.path.splitext(filepath)[1],
            "chunk_index": i
        })

    print(f"  Stored {len(chunks)} chunks for tenant '{TENANT_NAME}'.")

total = tenant_collection.aggregate.over_all(total_count=True)
print(f"\nTotal documents in tenant '{TENANT_NAME}': {total.total_count}")
client.close()
```

## Verification

The following end-to-end checks confirm that all components are installed, wired, and operational.

| Check | Command | Expected Result |
|---|---|---|
| LangChain/LangGraph | `python -c "import langchain_core, langgraph; print('OK')"` | Prints "OK" |
| LiteLLM proxy | `curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-litellm-master-key"` | Returns JSON model list |
| Weaviate | `curl http://localhost:8080/v1/meta` | Returns Weaviate metadata |
| Unstructured | `python -c "from unstructured.partition.auto import partition; print('OK')"` | Prints "OK" |
| Langfuse | `curl http://localhost:3000/api/public/health` | Returns health status |
| vLLM | `curl http://localhost:8000/v1/models` | Returns loaded model list |
| HF TRL | `python -c "import trl, peft; print('OK')"` | Prints "OK" |
| Agent through LiteLLM | `python scripts/enterprise_agent.py` | Prints response and Langfuse trace confirmation |
| Multi-agent workflow | `python scripts/multi_agent_workflow.py` | Prints final output from two-agent pipeline |
| Document ingestion | Place test documents in `enterprise_docs/`, run `python scripts/ingest_enterprise_docs.py` | Reports chunks stored per document |

The Enterprise Agentic Pipeline is operational once all ten checks pass. The architecture chapter provides the rationale behind each component selection and the governance, observability, and fine-tuning design decisions governing how the layers interact.

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
