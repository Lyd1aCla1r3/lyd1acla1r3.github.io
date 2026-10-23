# Evaluation-Driven Development Loop: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Evaluation-Driven Development Loop, covering Langfuse deployment for production trace capture, Braintrust setup for evaluation scoring and experiment management, Unsloth installation for memory-efficient fine-tuning, vLLM configuration for multi-model serving with LoRA adapter support, and LiteLLM weighted routing for A/B traffic distribution, with integration wiring scripts and end-to-end verification steps. -->

The [Architecture and Configuration](evaluation-driven-development-loop-configuration.html) chapter explains the rationale behind each component selection, the continuous improvement cycle, and the principle that systematic quality measurement replaces intuition-based prompt iteration. This guide provides the concrete installation commands, configuration snippets, and wiring steps needed to bring that architecture to a working state.

## Prerequisites

| Requirement | Details |
|---|---|
| Operating system | Linux with NVIDIA GPU drivers and CUDA toolkit for vLLM and Unsloth; macOS or Windows can run the Langfuse, Braintrust, and LiteLLM services without GPU hardware |
| Python | Version 3.10 or later with `pip` and virtual environment support |
| Docker | Docker Engine and Docker Compose v2 for self-hosted Langfuse v4 deployment |
| GPU hardware | At least one NVIDIA GPU with 24GB or more VRAM for Unsloth 4-bit LoRA fine-tuning and vLLM multi-LoRA serving |
| Braintrust account | Active API key exported as `BRAINTRUST_API_KEY` from the Braintrust console |
| Judge LLM provider | Commercial provider key exported as `OPENAI_API_KEY` for LLM-as-judge evaluation scoring |
| Hugging Face access | Access token exported as `HF_TOKEN` for an account approved for the gated `Llama-3.1-8B-Instruct` repository |
| Existing application | A running AI application built with LangChain or LlamaIndex that emits inference requests to evaluate |

## Step 1: Langfuse

Langfuse provides asynchronous production trace capture and root observation indexing. The official Docker Compose deployment runs the complete Langfuse v4 stack, combining the web and background worker containers with PostgreSQL, ClickHouse, Redis, and MinIO. Current releases of the Langfuse Python SDK and the LiteLLM callback integration require a Langfuse v3 or later server, and the dataset curation script in this guide queries the observations API introduced in Langfuse v4, so the legacy single-container v2 image cannot support this workflow.

Clone the official Langfuse repository and enter the deployment directory:

<details class="code-drop">
<summary><span class="code-drop__name">Clone Langfuse repository</span><span class="code-drop__meta">bash · 2 lines</span></summary>

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

</details>

Replace the default placeholder credentials on every line marked `# CHANGEME` in `docker-compose.yml` before exposing the stack on a shared network, then start the containers in detached mode:

```bash
docker compose up -d
```

The Langfuse web interface listens on `http://localhost:3000` once PostgreSQL and ClickHouse complete their initial migrations. Open the browser dashboard, create an organization project, and generate a public and secret API key pair for the evaluation loop.

Install the Langfuse Python SDK alongside the LangChain client packages that the application trace wrapper and evaluation scripts import:

<details class="code-drop">
<summary><span class="code-drop__name">Install Langfuse and LangChain packages</span><span class="code-drop__meta">bash · 1 line</span></summary>

```bash
pip install langfuse langchain langchain-openai
```

</details>

Export the project credentials and local server address in the shell environment so both the application callback handler and the LiteLLM proxy can authenticate against Langfuse:

<details class="code-drop">
<summary><span class="code-drop__name">Export Langfuse environment variables</span><span class="code-drop__meta">bash · 3 lines</span></summary>

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_BASE_URL="http://localhost:3000"
```

</details>

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">Check Langfuse health endpoint</span><span class="code-drop__meta">bash · 1 line</span></summary>

```bash
curl http://localhost:3000/api/public/health
```

</details>

A healthy deployment returns a JSON payload confirming that the web server, PostgreSQL metadata store, and ClickHouse event database are operational.

## Step 2: Braintrust

Braintrust manages versioned evaluation datasets, programmatic scoring rubrics, and side-by-side experiment comparisons across model variants. Install the Braintrust Python SDK in the active environment:

```bash
pip install braintrust
```

Export the Braintrust API key generated from the account settings console so local evaluation and dataset curation scripts can push records to the platform:

<details class="code-drop">
<summary><span class="code-drop__name">Export Braintrust API key</span><span class="code-drop__meta">bash · 1 line</span></summary>

```bash
export BRAINTRUST_API_KEY="sk-..."
```

</details>

Initialize an evaluation project and seed a versioned baseline dataset with representative reference examples. Storing expected outputs alongside domain category tags establishes a cold-start benchmark before live production traces accumulate in Langfuse:

<details class="code-drop">
<summary><span class="code-drop__name">seed_baseline_dataset.py</span><span class="code-drop__meta">python · 28 lines</span></summary>

```python
import braintrust

dataset = braintrust.init_dataset(
    project="eval-loop-demo",
    name="baseline-eval-v1",
    description="Baseline evaluation dataset for quality measurement",
)

dataset.insert(
    input="Summarize the key benefits of container orchestration.",
    expected="Container orchestration automates deployment, scaling, and management "
             "of containerized applications. It handles load balancing, service "
             "discovery, and self-healing across cluster nodes.",
    metadata={"category": "infrastructure", "difficulty": "standard"},
)

dataset.insert(
    input="Explain the difference between LoRA and full fine-tuning.",
    expected="LoRA trains low-rank adapter matrices that attach to frozen base model "
             "weights, requiring a fraction of the memory and compute. Full "
             "fine-tuning updates all model parameters, producing potentially "
             "higher quality at significantly greater resource cost.",
    metadata={"category": "ml-ops", "difficulty": "standard"},
)

summary = dataset.summarize()
print(f"Dataset '{dataset.name}' created with {summary.data_summary.total_records} records.")
```

</details>

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">Verify Braintrust SDK import</span><span class="code-drop__meta">python · 2 lines</span></summary>

```python
import braintrust
print("Braintrust imported successfully.")
```

</details>

Running the verification snippet confirms that the SDK is installed cleanly, and executing the seeding script verifies outbound API authentication by creating the initial dataset snapshot in the Braintrust dashboard.

## Step 3: Unsloth

Unsloth accelerates low-rank adapter training and cuts GPU VRAM consumption through custom Triton kernels. Installing Unsloth requires a Linux workstation or server equipped with NVIDIA GPU drivers and a compatible CUDA runtime:

```bash
pip install unsloth
```

Install the companion Hugging Face training libraries that provide dataset loading, 4-bit quantization through `bitsandbytes`, and the supervised fine-tuning trainer loop:

<details class="code-drop">
<summary><span class="code-drop__name">Install Hugging Face training dependencies</span><span class="code-drop__meta">bash · 1 line</span></summary>

```bash
pip install datasets transformers accelerate bitsandbytes trl
```

</details>

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">Verify Unsloth CUDA kernel initialization</span><span class="code-drop__meta">python · 2 lines</span></summary>

```python
from unsloth import FastLanguageModel
print("Unsloth imported successfully.")
```

</details>

A clean import confirms that Unsloth discovered the local CUDA device and compiled its custom attention and RoPE kernels without driver mismatches.

## Step 4: vLLM

vLLM serves the frozen base model alongside dynamically loaded LoRA adapters over an OpenAI-compatible HTTP interface. Install the vLLM serving package on the GPU host:

```bash
pip install vllm
```

Launch the vLLM server with dynamic LoRA support enabled. Exporting the runtime LoRA updating flag activates the `/v1/load_lora_adapter` control endpoint so newly trained Unsloth adapters can attach to the running process without interrupting active baseline requests:

<details class="code-drop">
<summary><span class="code-drop__name">Start vLLM with runtime LoRA updating</span><span class="code-drop__meta">bash · 8 lines</span></summary>

```bash
export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True

vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --enable-lora \
  --max-lora-rank 64 \
  --max-model-len 8192
```

</details>

The `--enable-lora` flag reserves shared adapter memory slots in the paged attention engine, while `--max-lora-rank 64` sets an upper bound that accommodates the rank-16 adapters produced by the Unsloth training script as well as higher-rank future experiments.

Register the trained domain adapter checkpoint at runtime by sending a `POST` request to the local vLLM control endpoint after Unsloth completes its training run:

<details class="code-drop">
<summary><span class="code-drop__name">Hot-load LoRA adapter into running vLLM server</span><span class="code-drop__meta">bash · 7 lines</span></summary>

```bash
curl -X POST http://localhost:8000/v1/load_lora_adapter \
  -H "Content-Type: application/json" \
  -d '{
    "lora_name": "finetuned-v1",
    "lora_path": "./eval-finetuned-adapter"
  }'
```

</details>

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">Query vLLM model registry</span><span class="code-drop__meta">bash · 1 line</span></summary>

```bash
curl http://localhost:8000/v1/models
```

</details>

The `/v1/models` endpoint returns a JSON list containing `Llama-3.1-8B-Instruct` immediately after startup, and appends `finetuned-v1` as a second callable model identifier as soon as the runtime LoRA load request succeeds.

## Step 5: LiteLLM Gateway with Weighted Routing

LiteLLM sits in front of vLLM to split live application traffic across model variants according to configurable percentage weights while forwarding variant attribution to Langfuse. Install the LiteLLM proxy package:

<details class="code-drop">
<summary><span class="code-drop__name">Install LiteLLM proxy package</span><span class="code-drop__meta">bash · 1 line</span></summary>

```bash
pip install 'litellm[proxy]'
```

</details>

Create `litellm_config.yaml` to define the `app-model` routing group across the base model and the fine-tuned LoRA adapter alongside the `gpt-4o-judge` evaluation target:

<details class="code-drop">
<summary><span class="code-drop__name">litellm_config.yaml</span><span class="code-drop__meta">yaml · 30 lines</span></summary>

```yaml
model_list:
  - model_name: app-model
    litellm_params:
      model: openai/meta-llama/Llama-3.1-8B-Instruct
      api_base: http://localhost:8000/v1
      api_key: token-placeholder
      weight: 90
    model_info:
      id: base-model

  - model_name: app-model
    litellm_params:
      model: openai/finetuned-v1
      api_base: http://localhost:8000/v1
      api_key: token-placeholder
      weight: 10
    model_info:
      id: finetuned-v1

  - model_name: gpt-4o-judge
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  success_callback: ["langfuse"]

general_settings:
  master_key: sk-eval-master-key
```

</details>

Declaring two entries under `model_name: app-model` instructs LiteLLM to form a weighted load-balancing group that dispatches 90% of incoming requests to the frozen base model and 10% to the `finetuned-v1` adapter. LiteLLM embeds each target's `model_info.id` string as `model_id` inside the `hidden_params` dictionary of every Langfuse generation event, allowing downstream curation scripts to partition evaluation scores by model variant. Before the first LoRA adapter is trained and loaded into vLLM, set the `finetuned-v1` entry's `weight` to zero so baseline traffic never hits an unregistered model name.

Export the OpenAI judge API key and Langfuse telemetry credentials in the shell where the LiteLLM proxy will run:

<details class="code-drop">
<summary><span class="code-drop__name">Export gateway environment variables</span><span class="code-drop__meta">bash · 4 lines</span></summary>

```bash
export OPENAI_API_KEY="sk-..."
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_BASE_URL="http://localhost:3000"
```

</details>

Launch the LiteLLM proxy server on port 4000:

<details class="code-drop">
<summary><span class="code-drop__name">Start LiteLLM proxy server</span><span class="code-drop__meta">bash · 1 line</span></summary>

```bash
litellm --config litellm_config.yaml --host 0.0.0.0 --port 4000
```

</details>

**Verification**:

<details class="code-drop">
<summary><span class="code-drop__name">Verify LiteLLM proxy model list</span><span class="code-drop__meta">bash · 2 lines</span></summary>

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-eval-master-key"
```

</details>

A successful response returns a JSON object listing both the `app-model` routing group and the `gpt-4o-judge` endpoint.

## Wiring the Components

With all five services running, the four Python wiring scripts below connect live application inference, dataset curation, multi-metric scoring, and LoRA fine-tuning into a closed loop.

### Langfuse Trace Capture Integration

Save the following script as `traced_application.py` in `scripts/`. It routes a LangChain chat request through LiteLLM's `app-model` alias while attaching the Langfuse `CallbackHandler` so the full prompt, completion, latency, and selected model variant flush to the telemetry server. Calling `langfuse.flush()` at the end of short-lived CLI scripts ensures the background telemetry thread transmits all pending spans before the Python interpreter exits:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/traced_application.py</span><span class="code-drop__meta">python · 32 lines</span></summary>

```python
import os
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    base_url=os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000"),
)
langfuse_handler = CallbackHandler()

llm = ChatOpenAI(
    model="app-model",
    base_url="http://localhost:4000/v1",
    api_key="sk-eval-master-key",
    temperature=0,
)

messages = [
    SystemMessage(content="Provide concise, factual responses."),
    HumanMessage(content="Explain the difference between LoRA and full fine-tuning."),
]

response = llm.invoke(messages, config={"callbacks": [langfuse_handler]})
langfuse.flush()

print("Response:", response.content)
print("Trace exported to Langfuse.")
```

</details>

### Langfuse-to-Braintrust Dataset Curation

Save the following script as `curate_dataset.py` in `scripts/`. It queries Langfuse's v4 observations API for root traces, extracts the normalized prompt, completion, and `model_id` tag injected by LiteLLM, and uploads those records into a versioned Braintrust dataset. Setting `expand_metadata` to `"hidden_params"` in the observation query retrieves the nested LiteLLM routing dictionary so each benchmark record preserves the identifier of the model variant that generated it:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/curate_dataset.py</span><span class="code-drop__meta">python · 40 lines</span></summary>

```python
import json
import os
import braintrust
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    base_url=os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000"),
)
traces = langfuse.api.observations.get_many(
    is_root_observation=True, fields="core,io,metadata",
    expand_metadata="hidden_params", limit=100,
).data
dataset = braintrust.init_dataset(project="eval-loop-demo", name="production-traces-v1")

def as_text(val):
    if isinstance(val, str):
        try: val = json.loads(val)
        except json.JSONDecodeError: return val
    return str(val.get("content", val)) if isinstance(val, dict) else str(val)

def get_model_id(meta):
    hp = meta.get("hidden_params") if isinstance(meta, dict) else None
    if isinstance(hp, str):
        try: hp = json.loads(hp)
        except json.JSONDecodeError: hp = None
    return hp.get("model_id", "unknown") if isinstance(hp, dict) else "unknown"

count = 0
for t in traces:
    if t.input and t.output:
        dataset.insert(
            input=as_text(t.input), expected=as_text(t.output),
            metadata={"trace_id": t.trace_id, "model_id": get_model_id(t.metadata)},
        )
        count += 1
print(f"Curated {count} traces into dataset '{dataset.name}'.")
```

</details>

### Braintrust Evaluation Pipeline

Save the following script as `evaluate_models.py` in `scripts/`. It runs the `app-model` endpoint against reference evaluation records and grades every completion with both a deterministic key-phrase faithfulness function and an LLM-as-judge accuracy rubric powered by `gpt-4o-judge`. Combining deterministic phrase matching with a semantic judge catches both missing domain terminology and broader factual hallucinations in a single experiment pass:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/evaluate_models.py</span><span class="code-drop__meta">python · 40 lines</span></summary>

```python
import braintrust
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="app-model", base_url="http://localhost:4000/v1", api_key="sk-eval-master-key", temperature=0)
judge = ChatOpenAI(model="gpt-4o-judge", base_url="http://localhost:4000/v1", api_key="sk-eval-master-key", temperature=0)

def app_task(prompt):
    msgs = [SystemMessage(content="Provide concise, factual responses."), HumanMessage(content=prompt)]
    return {"answer": llm.invoke(msgs).content}

def faithfulness_scorer(output, expected):
    phrases = [p.strip() for p in expected.lower().split(".") if p.strip()]
    matches = sum(1 for p in phrases if p in output["answer"].lower())
    return matches / max(len(phrases), 1)

def llm_judge_scorer(output, expected):
    prompt = (
        f"Rate accuracy and completeness from 0.0 to 1.0.\n"
        f"Expected: {expected}\nActual: {output['answer']}\n"
        f"Respond with only a decimal number between 0.0 and 1.0."
    )
    try: return float(judge.invoke([HumanMessage(content=prompt)]).content.strip())
    except ValueError: return 0.0

braintrust.Eval(
    "eval-loop-demo",
    data=lambda: [
        {"input": "Summarize the key benefits of container orchestration.",
         "expected": "Container orchestration automates deployment, scaling, and management. It handles load balancing, service discovery, and self-healing."},
        {"input": "Explain the difference between LoRA and full fine-tuning.",
         "expected": "LoRA trains low-rank adapter matrices on frozen weights. Full fine-tuning updates all model parameters at greater resource cost."},
    ],
    task=app_task,
    scores=[faithfulness_scorer, llm_judge_scorer],
)
```

</details>

### Unsloth Fine-Tuning from Evaluation Data

Save the following script as `finetune_from_eval.py` in `scripts/`. It loads `Llama-3.1-8B-Instruct` in 4-bit precision, attaches rank-16 LoRA adapters across all attention and MLP projections, and runs supervised fine-tuning via `SFTTrainer` with `processing_class` set to `tokenizer`. Saving both the adapter weights and the tokenizer configuration to `./eval-finetuned-adapter` produces a self-contained directory that vLLM can hot-load directly:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/finetune_from_eval.py</span><span class="code-drop__meta">python · 36 lines</span></summary>

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
OUTPUT_DIR = "./eval-finetuned-adapter"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME, max_seq_length=2048, load_in_4bit=True,
)
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0, bias="none",
)
dataset = load_dataset("json", data_files="training_data.jsonl", split="train")

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    processing_class=tokenizer,
    args=SFTConfig(
        output_dir=OUTPUT_DIR, num_train_epochs=3, per_device_train_batch_size=4,
        gradient_accumulation_steps=4, learning_rate=2e-4, max_seq_length=2048,
    ),
)
trainer.train()
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"LoRA adapter saved to {OUTPUT_DIR}")
```

</details>

Create `training_data.jsonl` in the working directory before running the fine-tuning script, formatting validated high-scoring Braintrust evaluation pairs into Llama 3.1 chat template records:

<details class="code-drop">
<summary><span class="code-drop__name">training_data.jsonl</span><span class="code-drop__meta">json · 2 lines</span></summary>

```json
{"text": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nSummarize the key benefits of container orchestration.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nContainer orchestration automates deployment, scaling, and management of containerized applications. It handles load balancing, service discovery, and self-healing across cluster nodes.<|eot_id|>"}
{"text": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nExplain the difference between LoRA and full fine-tuning.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nLoRA trains low-rank adapter matrices that attach to frozen base model weights, requiring a fraction of the memory and compute. Full fine-tuning updates all model parameters at greater resource cost.<|eot_id|>"}
```

</details>

### A/B Routing Weight Adjustment

Update the two `weight` fields in `litellm_config.yaml` after Unsloth saves `./eval-finetuned-adapter` and the Step 4 `curl` command loads `finetuned-v1` into vLLM, shifting from the initial 90/10 canary split to a 50/50 comparison while keeping the judge endpoint and callback settings unchanged:

<details class="code-drop">
<summary><span class="code-drop__name">litellm_config.yaml (50/50 weight update)</span><span class="code-drop__meta">yaml · 19 lines</span></summary>

```yaml
model_list:
  - model_name: app-model
    litellm_params:
      model: openai/meta-llama/Llama-3.1-8B-Instruct
      api_base: http://localhost:8000/v1
      api_key: token-placeholder
      weight: 50
    model_info:
      id: base-model

  - model_name: app-model
    litellm_params:
      model: openai/finetuned-v1
      api_base: http://localhost:8000/v1
      api_key: token-placeholder
      weight: 50
    model_info:
      id: finetuned-v1
```

</details>

Restart the LiteLLM proxy process so the 50/50 traffic split takes effect immediately across live requests.

## Verification

Run the ten checks below in sequence to confirm that every layer of the Evaluation-Driven Development Loop is healthy and connected:

| Check | Command | Expected Result |
|---|---|---|
| Langfuse server | `curl -s localhost:3000/api` | Confirms web server and ClickHouse storage health |
| Langfuse SDK | `python -c "import langfuse"` | Exits with code zero and no import errors |
| Braintrust SDK | `python -c "import braintrust"` | Validates SDK installation in virtual environment |
| Unsloth kernels | `python -c "import unsloth"` | Initializes CUDA extensions without error |
| vLLM registry | `curl -s localhost:8000/v1/models` | Returns JSON list of base model and loaded adapters |
| LiteLLM gateway | `curl -s localhost:4000/v1/models` | Returns JSON list of routed application and judge models |
| Traced inference | `python scripts/traced_application.py` | Prints completion and flushes root trace to Langfuse |
| Dataset curation | `python scripts/curate_dataset.py` | Uploads root traces into versioned Braintrust dataset |
| Offline scoring | `python scripts/evaluate_models.py` | Runs faithfulness and judge scorers and prints summary |
| LoRA fine-tuning | `python scripts/finetune_from_eval.py` | Trains 4-bit LoRA adapter and writes checkpoint files |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `observations.get_many` raises 404 or attribute error | Deploy Langfuse from the v4 `docker-compose.yml` stack and upgrade the SDK via `pip install -U langfuse` |
| vLLM returns 404 on `/v1/load_lora_adapter` | Export the runtime LoRA updating flag in the shell before starting the server with `--enable-lora` |
| LiteLLM returns 500 error on 10% of `app-model` requests | Set the adapter weight to zero in `litellm_config.yaml` until `finetuned-v1` is registered in vLLM |
| Curation script records `model_id` as `unknown` | Confirm the Langfuse success callback is active in `litellm_config.yaml` and each model defines `model_info.id` |
| `SFTTrainer` raises unexpected keyword `tokenizer` | Pass `processing_class` instead of the deprecated `tokenizer` argument when running TRL 0.12 or newer |

The Evaluation-Driven Development Loop is operational once all ten verification checks pass. Return to the [Architecture and Configuration](evaluation-driven-development-loop-configuration.html) chapter to review the architectural tradeoffs, layer substitution options, and multi-iteration governance principles that guide long-term quality improvement.

## References

1. Langfuse Self-Hosting Documentation, Langfuse GmbH.
2. Langfuse Python SDK Documentation, Langfuse GmbH.
3. Braintrust Documentation, Braintrust Data Inc.
4. Unsloth Documentation, Unsloth AI.
5. vLLM Documentation, vLLM Project.
6. vLLM LoRA Adapter Documentation, vLLM Project.
7. LiteLLM Proxy Documentation, BerriAI.
8. Hugging Face TRL Documentation, Hugging Face.
