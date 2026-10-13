# Evaluation-Driven Development Loop: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Evaluation-Driven Development Loop, covering Langfuse deployment for production trace capture, Braintrust setup for evaluation scoring and experiment management, Unsloth installation for memory-efficient fine-tuning, vLLM configuration for multi-model serving with LoRA adapter support, and LiteLLM weighted routing for A/B traffic distribution, with integration wiring scripts and end-to-end verification steps. -->

The Evaluation-Driven Development Loop architecture chapter explains the rationale behind each component selection, the continuous improvement cycle, and the principle that systematic quality measurement replaces intuition-based prompt iteration. This guide provides the concrete installation commands, configuration snippets, and wiring steps needed to bring that architecture to a working state.

## Prerequisites

- **Operating system**: Linux with NVIDIA GPU drivers for vLLM and Unsloth. macOS or Windows can run Langfuse, Braintrust, and LiteLLM components without GPU hardware.
- **Python**: Version 3.10 or later, with `pip` available
- **Docker**: Required for Langfuse self-hosted deployment
- **GPU hardware**: At least one NVIDIA GPU with 24GB+ VRAM for Unsloth fine-tuning and vLLM serving. Multi-GPU configurations enable larger models.
- **API keys**: The following service accounts are required before proceeding:
  - **Braintrust**: API key from the Braintrust console
  - **LLM provider**: At least one commercial model provider API key for baseline inference
  - **Hugging Face**: Access token (exported as `HF_TOKEN`) for an account with approved access to the gated `meta-llama/Llama-3.1-8B-Instruct` repository, which vLLM and Unsloth download in later steps
- **Existing application**: A running AI application built with LangChain or LlamaIndex that produces outputs to evaluate. Any configuration from prior chapters in this series can serve as the application under evaluation.

## Step 1: Langfuse

Langfuse provides production trace capture. The official Docker Compose deployment runs the full Langfuse v4 stack: the web and worker containers together with PostgreSQL, ClickHouse, Redis, and MinIO. Current releases of the Langfuse Python SDK and of the LiteLLM Langfuse callback require a Langfuse v3 or later server, and the curation script later in this guide uses the observations API introduced in Langfuse v4, so the legacy single-container v2 image does not work here.

Clone the Langfuse repository:

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

Replace the default secrets on every line marked `# CHANGEME` in `docker-compose.yml`, then start the stack:

```bash
docker compose up -d
```

The Langfuse dashboard becomes available at `http://localhost:3000` after startup. Create a project there and generate API keys.

Install the Langfuse Python SDK together with the LangChain packages that the Langfuse LangChain integration and the wiring scripts import:

```bash
pip install langfuse langchain langchain-openai
```

Set environment variables:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_BASE_URL="http://localhost:3000"
```

**Verification**:

```bash
curl http://localhost:3000/api/public/health
```

A successful deployment returns a health status indicating the server and database are operational.

## Step 2: Braintrust

Braintrust provides evaluation scoring, dataset versioning, and experiment comparison. Install the SDK:

```bash
pip install braintrust
```

Set the API key:

```bash
export BRAINTRUST_API_KEY="sk-..."
```

Create an evaluation project and an initial dataset:

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
    metadata={"category": "infrastructure", "difficulty": "standard"}
)

dataset.insert(
    input="Explain the difference between LoRA and full fine-tuning.",
    expected="LoRA trains low-rank adapter matrices that attach to frozen base model "
             "weights, requiring a fraction of the memory and compute. Full "
             "fine-tuning updates all model parameters, producing potentially "
             "higher quality at significantly greater resource cost.",
    metadata={"category": "ml-ops", "difficulty": "standard"}
)

summary = dataset.summarize()
print(f"Dataset '{dataset.name}' created with {summary.data_summary.total_records} records.")
```

**Verification**:

```python
import braintrust
print("Braintrust imported successfully.")
```

A successful installation prints the confirmation message. Full verification requires creating a project and inserting evaluation records through the SDK.

## Step 3: Unsloth

Unsloth provides memory-efficient fine-tuning with custom CUDA kernels. Installation requires a Linux system with NVIDIA GPU drivers and CUDA toolkit.

```bash
pip install unsloth
```

Install additional training dependencies:

```bash
pip install datasets transformers accelerate bitsandbytes
```

**Verification**:

```python
from unsloth import FastLanguageModel
print("Unsloth imported successfully.")
```

A successful installation prints the confirmation message without CUDA errors. Full verification requires loading a model and confirming GPU memory allocation.

## Step 4: vLLM

vLLM provides high-throughput model serving with LoRA adapter support. Installation requires a Linux system with NVIDIA GPU drivers and CUDA toolkit.

```bash
pip install vllm
```

Start vLLM with LoRA adapter support enabled. The `VLLM_ALLOW_RUNTIME_LORA_UPDATING` environment variable enables the runtime adapter loading endpoint used later in this guide:

```bash
export VLLM_ALLOW_RUNTIME_LORA_UPDATING=True

vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --enable-lora \
  --max-lora-rank 64 \
  --max-model-len 8192
```

The `--enable-lora` flag activates LoRA adapter support, and the environment variable above permits hot-loading adapters into the running server. The `--max-lora-rank` parameter sets the maximum rank for loaded adapters, which must match or exceed the rank used during Unsloth training.

To load a fine-tuned LoRA adapter after training:

```bash
curl -X POST http://localhost:8000/v1/load_lora_adapter \
  -H "Content-Type: application/json" \
  -d '{
    "lora_name": "finetuned-v1",
    "lora_path": "/path/to/unsloth-output/lora-adapter"
  }'
```

**Verification**:

```bash
curl http://localhost:8000/v1/models
```

A successful deployment returns a JSON list containing the base model. The list includes both the base model and the adapter variant once a LoRA adapter is loaded.

## Step 5: LiteLLM Gateway with Weighted Routing

LiteLLM provides unified routing with weighted traffic distribution for A/B comparison between model variants.

```bash
pip install 'litellm[proxy]'
```

Create `litellm_config.yaml` with weighted routing between base and fine-tuned models:

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

The two entries with `model_name: app-model` create a weighted routing group. LiteLLM reads `weight` from `litellm_params` and routes 90% of requests to the base model and 10% to the fine-tuned variant. LiteLLM records the `model_info.id` value as `model_id` inside the `hidden_params` metadata of each Langfuse generation, enabling Braintrust evaluations to separate results by model variant. The `finetuned-v1` deployment returns errors until the fine-tuning step loads that adapter into vLLM, so set its `weight` to `0` until then.

Set environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_BASE_URL="http://localhost:3000"
```

Start the LiteLLM proxy:

```bash
litellm --config litellm_config.yaml --host 0.0.0.0 --port 4000
```

**Verification**:

```bash
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-eval-master-key"
```

A successful deployment returns a JSON list of the configured models including the weighted routing group.

## Wiring the Components

With all components installed individually, the final step connects them into the continuous improvement cycle described in the architecture chapter.

### Langfuse Trace Capture Integration

Save the following script as `scripts/traced_application.py`. It demonstrates Langfuse trace capture for a LangChain application:

```python
import os
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    base_url=os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000"),
)
langfuse_handler = CallbackHandler()

# --- LangChain application example ---
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

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

### Langfuse-to-Braintrust Dataset Curation

Save the following script as `scripts/curate_dataset.py`. It queries Langfuse for production traces (the root observation of each trace) and creates a Braintrust evaluation dataset:

```python
import json
import os
from langfuse import Langfuse
import braintrust

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    base_url=os.environ.get("LANGFUSE_BASE_URL", "http://localhost:3000"),
)

traces = langfuse.api.observations.get_many(
    is_root_observation=True,
    fields="core,io,metadata",
    expand_metadata="hidden_params",
    limit=100,
).data
print(f"Fetched {len(traces)} traces from Langfuse.")

dataset = braintrust.init_dataset(
    project="eval-loop-demo",
    name="production-traces-v1",
    description="Evaluation dataset curated from production traces",
)


def as_text(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return value
    if isinstance(value, dict):
        return str(value.get("content", value))
    return str(value)


def lookup_model_id(metadata):
    hidden = metadata.get("hidden_params") if isinstance(metadata, dict) else None
    if isinstance(hidden, str):
        try:
            hidden = json.loads(hidden)
        except json.JSONDecodeError:
            hidden = None
    return hidden.get("model_id", "unknown") if isinstance(hidden, dict) else "unknown"


curated_count = 0
for trace in traces:
    if not trace.input or not trace.output:
        continue

    dataset.insert(
        input=as_text(trace.input),
        expected=as_text(trace.output),
        metadata={
            "trace_id": trace.trace_id,
            "model_id": lookup_model_id(trace.metadata),
            "timestamp": str(trace.start_time),
        }
    )
    curated_count += 1

print(f"Curated {curated_count} traces into dataset '{dataset.name}'.")
```

### Braintrust Evaluation Pipeline

Save the following script as `scripts/evaluate_models.py`. It runs the production application against a Braintrust dataset and scores outputs on multiple quality dimensions:

```python
import os
import braintrust
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(
    model="app-model",
    base_url="http://localhost:4000/v1",
    api_key="sk-eval-master-key",
    temperature=0,
)

judge_llm = ChatOpenAI(
    model="gpt-4o-judge",
    base_url="http://localhost:4000/v1",
    api_key="sk-eval-master-key",
    temperature=0,
)


def app_task(input_text):
    messages = [
        SystemMessage(content="Provide concise, factual responses."),
        HumanMessage(content=input_text),
    ]
    response = llm.invoke(messages)
    return {"answer": response.content}


def faithfulness_scorer(output, expected):
    expected_lower = expected.lower()
    answer_lower = output["answer"].lower()
    key_phrases = [p.strip() for p in expected_lower.split(".") if p.strip()]
    matches = sum(1 for p in key_phrases if p in answer_lower)
    return matches / max(len(key_phrases), 1)


def llm_judge_scorer(output, expected):
    judge_prompt = (
        f"Rate the following response on a scale of 0.0 to 1.0 for accuracy "
        f"and completeness compared to the expected answer.\n\n"
        f"Expected: {expected}\n\n"
        f"Actual: {output['answer']}\n\n"
        f"Respond with only a decimal number between 0.0 and 1.0."
    )
    messages = [HumanMessage(content=judge_prompt)]
    response = judge_llm.invoke(messages)
    try:
        return float(response.content.strip())
    except ValueError:
        return 0.0


eval_result = braintrust.Eval(
    "eval-loop-demo",
    data=lambda: [
        {
            "input": "Summarize the key benefits of container orchestration.",
            "expected": "Container orchestration automates deployment, scaling, "
                        "and management of containerized applications. It handles "
                        "load balancing, service discovery, and self-healing "
                        "across cluster nodes.",
        },
        {
            "input": "Explain the difference between LoRA and full fine-tuning.",
            "expected": "LoRA trains low-rank adapter matrices that attach to "
                        "frozen base model weights, requiring a fraction of the "
                        "memory and compute. Full fine-tuning updates all model "
                        "parameters, producing potentially higher quality at "
                        "significantly greater resource cost.",
        },
    ],
    task=lambda input: app_task(input),
    scores=[faithfulness_scorer, llm_judge_scorer],
)

print("Evaluation complete. View results in the Braintrust dashboard.")
```

### Unsloth Fine-Tuning from Evaluation Data

Save the following script as `scripts/finetune_from_eval.py`. It trains a LoRA adapter using high-quality examples from the evaluation pipeline:

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
OUTPUT_DIR = "./eval-finetuned-adapter"
MAX_SEQ_LEN = 2048

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=MODEL_NAME,
    max_seq_length=MAX_SEQ_LEN,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_dropout=0,
    bias="none",
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
    max_seq_length=MAX_SEQ_LEN,
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
print(f"LoRA adapter saved to {OUTPUT_DIR}")
print(f"Load into vLLM with: curl -X POST http://localhost:8000/v1/load_lora_adapter \\")
print(f"  -H 'Content-Type: application/json' \\")
print(f"  -d '{{\"lora_name\": \"finetuned-v1\", \"lora_path\": \"{OUTPUT_DIR}\"}}'")
```

The `training_data.jsonl` file should contain one JSON object per line with instruction-response pairs derived from high-scoring Braintrust evaluation records:

```json
{"text": "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nSummarize the key benefits of container orchestration.<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\nContainer orchestration automates deployment, scaling, and management of containerized applications...<|eot_id|>"}
```

### A/B Routing Weight Adjustment

Adjust LiteLLM's routing weights in `litellm_config.yaml` once evaluation results confirm the fine-tuned model's quality. Only the two `weight` values change, and the judge model, callback, and master key settings remain as configured in Step 5:

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

Restart the LiteLLM proxy to apply the new weights. The traffic split shifts from 90/10 to 50/50, increasing the fine-tuned model's production exposure for further evaluation.

## Verification

The following end-to-end checks confirm that all components are installed, wired, and operational.

| Check | Command | Expected Result |
|---|---|---|
| Langfuse server | `curl http://localhost:3000/api/public/health` | Returns health status |
| Langfuse SDK | `python -c "import langfuse; print('OK')"` | Prints "OK" |
| Braintrust | `python -c "import braintrust; print('OK')"` | Prints "OK" |
| Unsloth | `python -c "from unsloth import FastLanguageModel; print('OK')"` | Prints "OK" |
| vLLM | `curl http://localhost:8000/v1/models` | Returns loaded model list |
| LiteLLM proxy | `curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-eval-master-key"` | Returns JSON model list with weighted routing group |
| Traced application | `python scripts/traced_application.py` | Prints response and Langfuse trace confirmation |
| Dataset curation | `python scripts/curate_dataset.py` | Reports curated trace count and dataset name |
| Model evaluation | `python scripts/evaluate_models.py` | Prints evaluation scores and directs to Braintrust dashboard |
| Fine-tuning | `python scripts/finetune_from_eval.py` with sample `training_data.jsonl` | Saves LoRA adapter to output directory |

The Evaluation-Driven Development Loop is operational once all ten checks pass. The architecture chapter provides the rationale behind each component selection, the continuous improvement cycle design, and the evaluation principles governing how production traces convert into measurable quality gains.

## References

1. Langfuse Self-Hosting Documentation, Langfuse GmbH.
2. Langfuse Python SDK Documentation, Langfuse GmbH.
3. Braintrust Documentation, Braintrust Data Inc.
4. Unsloth Documentation, Unsloth AI.
5. vLLM Documentation, vLLM Project.
6. vLLM LoRA Adapter Documentation, vLLM Project.
7. LiteLLM Proxy Documentation, BerriAI.
8. Hugging Face TRL Documentation, Hugging Face.
