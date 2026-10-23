# Solo Developer Stack: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Solo Developer Stack, covering Claude Code setup, MCP server configuration, Ollama local inference, ChromaDB vector storage, and Docling document parsing, with end-to-end verification commands confirming the full system operates correctly. -->

The [Architecture and Configuration](solo-developer-stack-configuration.html) chapter explains the rationale behind each component selection and how the five local layers interconnect. This setup guide provides the installation commands, configuration files, Python wiring scripts, and verification checks needed to bring that architecture to a working state on a single development workstation. Each step installs one layer in isolation and verifies its readiness before the wiring section connects the five tools into a unified local workflow.

## Prerequisites

| Requirement | Details |
|---|---|
| Operating system | macOS, Linux, or Windows with WSL2 |
| Python runtime | Python 3.10 or later with `pip` and virtual environment support |
| Node.js runtime | Node.js 22 or later with `npm` and `npx` on the system path |
| Python tool runner | Astral `uv` package manager providing the `uvx` runner |
| Workstation hardware | Minimum 16 GB RAM; Apple Silicon or NVIDIA GPU recommended for local inference |
| Anthropic credentials | Active Claude subscription or `ANTHROPIC_API_KEY` for Claude Code sessions |
| Brave Search credentials | Free-tier `BRAVE_API_KEY` from the Brave Search API portal for live web queries |

## Step 1: Claude Code

Claude Code runs as a terminal-native coding agent that inspects files, executes shell commands, and coordinates local MCP tools directly from the project directory. Global installation through `npm` places the `claude` binary on the system path so any repository can launch an interactive session without adding agent dependencies to the project's own package manifest.

```bash
npm install -g \
  @anthropic-ai/claude-code
```

Navigate to the target repository root and start an interactive session once the global package installation finishes:

```bash
cd /path/to/project
claude
```

The initial launch opens a browser or terminal prompt to authenticate against a Claude subscription or an Anthropic API key. Subsequent launches reuse the stored credential token from the user profile directory, scan the working tree for project configuration files, and initialize the interactive prompt loop automatically. Running the agent from the repository root ensures that relative file paths, Git operations, and project-scoped MCP server definitions resolve against the intended workspace boundary.

**Verification**:

```bash
claude --version
```

The command prints the installed semantic version string and exits with status code zero, confirming that the binary is reachable on the shell path.

## Step 2: MCP Servers

Model Context Protocol servers grant Claude Code structured, schema-validated access to the project filesystem, Git repository history, and live web search results. Each server runs as a local `stdio` child process that Claude Code spawns automatically at session startup and terminates when the terminal session exits, avoiding persistent background daemons or open localhost ports.

Create `.mcp.json` in the root of the project directory so the tool definitions travel with the repository configuration:

<details class="code-drop">
<summary><span class="code-drop__name">.mcp.json</span><span class="code-drop__meta">JSON · 30 lines</span></summary>

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/project"
      ]
    },
    "git": {
      "command": "uvx",
      "args": [
        "mcp-server-git",
        "--repository",
        "/path/to/project"
      ]
    },
    "web-search": {
      "command": "npx",
      "args": [
        "-y",
        "@brave/brave-search-mcp-server"
      ],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key-here"
      }
    }
  }
}
```

</details>

Replace `/path/to/project` with the absolute path to the target repository on disk. The `filesystem` server restricts file reads, directory listings, and writes to that directory tree, preventing unintended modifications outside the workspace boundary. The `git` server launches on demand through `uvx` in an isolated ephemeral environment without polluting the project's Python virtual environment, exposing structured tools for commit log inspection, branch comparison, and working-tree diff retrieval. The `web-search` server authenticates outbound documentation and issue-tracker queries using `BRAVE_API_KEY`, keeping live search capabilities independent of the local codebase tools.

**Verification**:

Launch Claude Code inside the repository root and inspect the registered MCP server connections:

```bash
claude
# Run: /mcp
```

The `/mcp` status output lists `filesystem`, `git`, and `web-search` in the connected state alongside their discovered tool schemas and argument signatures.

## Step 3: Ollama

Ollama manages quantized open-weight language models on the workstation and exposes an OpenAI-compatible HTTP endpoint on localhost port 11434. Installing the runtime binary sets up automatic hardware detection for Apple Silicon Metal, NVIDIA CUDA, AMD ROCm, or CPU fallback execution without manual driver compilation.

On macOS, install the Ollama binary through Homebrew:

```bash
brew install ollama
```

On Linux or WSL2, run the official installation script or download the platform installer from `ollama.com`:

<details class="code-drop">
<summary><span class="code-drop__name">install-ollama-linux.sh</span><span class="code-drop__meta">Bash · 4 lines</span></summary>

```bash
curl -fsSL \
  https://ollama.com/install.sh \
  | sh
ollama --version
```

</details>

Start the local Ollama background server and pull the 8-billion-parameter Llama 3.1 checkpoint for supplementary local inference:

```bash
ollama serve &
ollama pull llama3.1:8b
```

The `llama3.1:8b` checkpoint requires roughly 4.9 GB of disk storage and fits comfortably inside 16 GB of unified memory alongside an active IDE, browser, and compiler toolchain. Workstations with 32 GB or more of memory can also pull `qwen2.5-coder:14b` or `llama3.1:70b` for heavier local code generation, commit classification, and batch log analysis. Ollama unloads idle models from memory automatically after a configurable inactivity window so local inference does not starve build processes.

To standardize local log scrubbing and summarization, save a custom `Modelfile` in the repository root that locks a low sampling temperature, an 8,192-token context window, and an explicit system prompt:

<details class="code-drop">
<summary><span class="code-drop__name">Modelfile</span><span class="code-drop__meta">Dockerfile · 7 lines</span></summary>

```dockerfile
FROM llama3.1:8b
PARAMETER temperature 0.1
PARAMETER num_ctx 8192
SYSTEM """
Redact secrets, API keys, and tokens from logs and summarize root causes concisely.
"""
```

</details>

Register the custom `local-scrub` persona in Ollama so shell scripts and Claude Code can invoke it by name without repeating system instructions on every call:

```bash
ollama create local-scrub \
  -f Modelfile
```

**Verification**:

Test direct model generation from the terminal first:

```bash
ollama run local-scrub \
  "Summarize Dockerfile."
```

Then confirm that the local OpenAI-compatible HTTP endpoint responds with the registered model catalog:

```bash
curl -s \
  localhost:11434/v1/models
```

The terminal command streams a concise two-sentence summary to standard output, and the HTTP request returns a JSON payload listing both `llama3.1:8b` and `local-scrub`.

## Step 4: ChromaDB

ChromaDB runs embedded inside the local Python environment and persists vector indices and metadata to a project directory on disk. Installing the `chromadb` package includes the default local sentence-transformer embedding model (`all-MiniLM-L6-v2` via ONNX Runtime), eliminating external embedding API calls and billing credentials during document indexing and semantic retrieval.

```bash
pip install chromadb
```

Save the following initialization script as `scripts/init_chromadb.py` to create the on-disk SQLite metadata database and cosine-similarity HNSW vector index at `./chroma_data`:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/init_chromadb.py</span><span class="code-drop__meta">Python · 11 lines</span></summary>

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(
    name="project_docs",
    metadata={"hnsw:space": "cosine"},
)

print(f"Collection '{collection.name}' ready.")
print(f"Document count: {collection.count()}")
```

</details>

Execute the initialization script from the repository root:

```bash
python \
  scripts/init_chromadb.py
```

Using `get_or_create_collection` makes the initialization script safe to run repeatedly; existing embeddings and metadata remain untouched if `./chroma_data` already exists on disk. Adding `./chroma_data/` to `.gitignore` keeps binary index files out of version control while allowing each developer machine to build its index from the tracked documentation directory.

**Verification**:

The script prints `Collection 'project_docs' ready.` followed by a document count of zero, confirming that ChromaDB created the persistent storage directory at `./chroma_data`.

## Step 5: Docling

Docling converts PDFs, Word documents, and Markdown specifications into structured Markdown using local layout analysis and table reconstruction models. Installing the library through `pip` pulls the core document converter, PDF rendering bindings, and local vision model integration.

```bash
pip install docling
```

The first document conversion downloads Docling's compact layout detector and TableFormer checkpoints into the local user cache directory. Subsequent runs execute offline against those cached weights without outbound network requests, preserving full local custody over proprietary architecture specifications and reference manuals.

**Verification**:

```bash
python -c "import docling"
```

The command imports the `docling` package cleanly and prints `OK` to the terminal.

## Wiring the Components

With all five tools installed and verified individually, three project files connect Docling, ChromaDB, Ollama, and Claude Code into an integrated local development workflow.

### Docling-to-ChromaDB Ingestion Pipeline

Save the following script as `scripts/ingest_docs.py`. The script walks the `docs/` directory, converts each PDF, DOCX, or Markdown file through Docling, splits the resulting Markdown along paragraph boundaries so tables and headings stay intact, and upserts the chunks into ChromaDB:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/ingest_docs.py</span><span class="code-drop__meta">Python · 36 lines</span></summary>

```python
import os
import chromadb
from docling.document_converter import DocumentConverter

DOCS_DIR, CHROMA_PATH, COLL = "./docs", "./chroma_data", "project_docs"

def chunk_markdown(text, max_chars=800):
    blocks, chunks, cur = text.split("\n\n"), [], ""
    for block in blocks:
        if len(cur) + len(block) > max_chars and cur:
            chunks.append(cur.strip())
            cur = ""
        cur = f"{cur}\n\n{block}" if cur else block
    if cur.strip():
        chunks.append(cur.strip())
    return chunks

def main():
    conv = DocumentConverter()
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    coll = client.get_or_create_collection(COLL, metadata={"hnsw:space": "cosine"})
    for root, _, files in os.walk(DOCS_DIR):
        for name in files:
            if not name.endswith((".pdf", ".docx", ".md")):
                continue
            path = os.path.join(root, name)
            md = conv.convert(path).document.export_to_markdown()
            chunks = chunk_markdown(md)
            if not chunks:
                continue
            rel = os.path.relpath(path, DOCS_DIR)
            ids = [f"{rel}_c{i}" for i in range(len(chunks))]
            metas = [{"source": rel, "chunk": i} for i in range(len(chunks))]
            coll.upsert(documents=chunks, ids=ids, metadatas=metas)
            print(f"Indexed {rel}: {len(chunks)} chunks (total: {coll.count()})")

if __name__ == "__main__":
    main()
```

</details>

Create the `docs/` directory, place reference PDFs or design specifications inside it, and run the ingestion pipeline:

```bash
mkdir -p docs
python \
  scripts/ingest_docs.py
```

Each run is idempotent because chunk identifiers derive deterministically from the relative file path and chunk index, updating modified sections in place through `coll.upsert`. Splitting on double newlines (`\n\n`) rather than naive period characters keeps Docling's reconstructed Markdown tables and fenced code blocks together inside single retrieval units.

### ChromaDB Retrieval Function

Save the following script as `scripts/query_docs.py` to query the embedded ChromaDB collection from the command line or from inside a Claude Code session:

<details class="code-drop">
<summary><span class="code-drop__name">scripts/query_docs.py</span><span class="code-drop__meta">Python · 21 lines</span></summary>

```python
import sys
import chromadb

CHROMA_PATH, COLL = "./chroma_data", "project_docs"

def query_docs(question, n_results=3):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    coll = client.get_collection(name=COLL)
    res = coll.query(query_texts=[question], n_results=n_results)
    for idx, doc in enumerate(res["documents"][0]):
        meta = res["metadatas"][0][idx]
        print(f"\n--- Result {idx + 1} ({meta['source']}#{meta['chunk']}) ---")
        print(doc[:400])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python scripts/query_docs.py '<question>'")
    query_docs(" ".join(sys.argv[1:]))
```

</details>

Run a semantic query against the indexed documentation corpus:

```bash
python \
  scripts/query_docs.py \
  "authentication flow"
```

The script embeds the question using ChromaDB's local sentence-transformer model and prints the top three matching specification chunks alongside their relative source paths and chunk numbers. Returning both the relative document path and the chunk index lets the developer or the coding agent open the corresponding source specification file when deeper surrounding context is required.

### Claude Code Project Instructions

Create a `CLAUDE.md` file in the repository root so Claude Code knows how to invoke the local ChromaDB retrieval script and the Ollama `local-scrub` persona during interactive coding sessions:

<details class="code-drop">
<summary><span class="code-drop__name">CLAUDE.md</span><span class="code-drop__meta">Markdown · 12 lines</span></summary>

```markdown
# Project Tooling Instructions

- Use the `filesystem`, `git`, and `web-search` MCP servers for repository and web inspection.
- Search project PDFs and specifications in `./chroma_data` by running:
  `python scripts/query_docs.py "<natural language question>"`
- Re-index updated files in `./docs` by running:
  `python scripts/ingest_docs.py`
- Scrub sensitive logs or summarize large test outputs locally via Ollama:
  `ollama run local-scrub < build.log`
```

</details>

Storing these operational rules in `CLAUDE.md` connects the interactive terminal path and the local knowledge retrieval path without requiring manual prompt reminders at the start of every session. Claude Code reads `CLAUDE.md` automatically on startup and invokes `scripts/query_docs.py` or `ollama run local-scrub` through its bash tool whenever a task involves project specifications or sensitive log output.

## Verification

| Check | Command | Expected Result |
|---|---|---|
| Claude Code CLI | `claude --version` | Prints installed CLI version string |
| MCP server status | `/mcp` inside Claude Code | Lists filesystem, git, and web-search as connected |
| Ollama HTTP API | `curl -s localhost:11434/v1/models` | Returns JSON list containing pulled local models |
| ChromaDB store | `python scripts/init_chromadb.py` | Prints collection ready status and chunk count |
| Docling import | `python -c "import docling"` | Exits with code zero and no import errors |
| End-to-end RAG | `python scripts/query_docs.py "test"` | Prints top three chunks with source file metadata |

## Troubleshooting

| Symptom | Fix |
|---|---|
| MCP `git` server fails to start | Confirm `uvx --version` succeeds and that `.mcp.json` points to a valid Git repository root |
| MCP `web-search` returns authentication error | Verify `BRAVE_API_KEY` in `.mcp.json` holds an active token from the Brave Search portal |
| Localhost port 11434 connection refused | Start the background daemon with `ollama serve &` or launch the desktop Ollama application |
| ChromaDB raises SQLite version error on Linux | Upgrade to Python 3.10+ with recent SQLite or install `pysqlite3-binary` in the virtual environment |
| First `ingest_docs.py` run hangs for several minutes | Allow Docling and ChromaDB to finish downloading initial layout and embedding weights into `~/.cache` |

The [Solo Developer Stack](solo-developer-stack-configuration.html) is operational once all six verification checks pass. That companion architecture chapter details the component tradeoffs, layer omissions, and scaling paths when a project outgrows a single workstation.

## References

1. Claude Code Installation Guide, Anthropic.
2. MCP Server Reference Implementations, Model Context Protocol.
3. Ollama Installation Documentation, Ollama Inc.
4. ChromaDB Getting Started Guide, Chroma Inc.
5. Docling Installation Guide, IBM Research and LF AI and Data Foundation.
6. Brave Search API Documentation, Brave Software.
