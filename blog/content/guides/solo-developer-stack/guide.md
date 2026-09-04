# Solo Developer Stack: Setup Guide

<!-- SUMMARY: A step-by-step installation and configuration guide for assembling the Solo Developer Stack, covering Claude Code setup, MCP server configuration, Ollama local inference, ChromaDB vector storage, and Docling document parsing, with end-to-end verification commands confirming the full system operates correctly. -->

The Solo Developer Stack architecture chapter explains the rationale behind each component selection and how the pieces interconnect. This guide provides the concrete installation commands, configuration snippets, and wiring steps needed to bring that architecture to a working state on a single development machine.

## Prerequisites

- **Operating system**: macOS, Linux, or Windows with WSL2
- **Python**: Version 3.10 or later, with `pip` available
- **Node.js**: Version 18 or later, with `npx` available
- **Hardware**: At least 16GB of RAM for running local models alongside development tools. A GPU is beneficial for Ollama inference speed but not strictly required; Apple Silicon and CPU-only configurations are supported.
- **Anthropic account**: An active Claude subscription or API key for Claude Code access

## Step 1: Claude Code

Claude Code is Anthropic's terminal-native agentic coding assistant. Installation uses npm.

```bash
npm install -g @anthropic-ai/claude-code
```

After installation, launch Claude Code from any project directory:

```bash
cd /path/to/project
claude
```

The first launch prompts for Anthropic API authentication. Once authenticated, Claude Code operates directly in the terminal, reading and writing files, running shell commands, and reasoning about the project structure.

**Verification**:

```bash
claude --version
```

A successful installation prints the installed version number.

## Step 2: MCP Servers

MCP servers give Claude Code structured access to the filesystem, Git history, and web search results. Each server runs as a local `stdio` process that Claude Code launches automatically.

Create or edit the project-level MCP configuration file at `.mcp.json` in the project root:

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
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "--repository",
        "/path/to/project"
      ]
    },
    "web-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-web-search"
      ],
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key-here"
      }
    }
  }
}
```

Replace `/path/to/project` with the actual project directory path. The web search server requires a Brave Search API key, which is available at no cost for limited usage through the Brave Search API portal.

**Verification**:

Launch Claude Code in the project directory and ask it to list the available MCP tools:

```bash
claude
# Then type: "List all available MCP tools"
```

Claude Code should report tools from the filesystem, git, and web-search servers.

## Step 3: Ollama

Ollama provides local model inference with automatic hardware detection. Installation varies by operating system.

**macOS**:

```bash
brew install ollama
```

**Linux**:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows**: Download the installer from `https://ollama.com/download/windows`.

After installation, start the Ollama service and pull a model:

```bash
ollama serve &
ollama pull llama3.1:8b
```

The `llama3.1:8b` model requires approximately 4.7GB of disk space and runs on machines with 8GB or more of RAM. Developers with more capable hardware can pull larger models like `llama3.1:70b` for higher-quality local inference.

**Verification**:

```bash
ollama run llama3.1:8b "Explain what a Dockerfile does in two sentences."
```

A successful setup produces a coherent natural-language response directly in the terminal.

To verify the API endpoint is accessible:

```bash
curl http://localhost:11434/v1/models
```

This returns a JSON list of available models, confirming the OpenAI-compatible API is operational.

## Step 4: ChromaDB

ChromaDB runs embedded inside a Python process with local disk persistence. Installation uses pip.

```bash
pip install chromadb
```

Create a persistent ChromaDB collection by running the following Python script, saved as `scripts/init_chromadb.py` in the project:

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(
    name="project_docs",
    metadata={"hnsw:space": "cosine"}
)

print(f"Collection '{collection.name}' ready.")
print(f"Document count: {collection.count()}")
```

```bash
python scripts/init_chromadb.py
```

**Verification**:

The script should print the collection name and a document count of 0, confirming that ChromaDB initialized successfully with local persistence at `./chroma_data`.

## Step 5: Docling

Docling parses PDFs, DOCX files, and other document formats into clean structured text. Installation uses pip.

```bash
pip install docling
```

The first run downloads Docling's compact vision models, approximately 800MB total. Subsequent runs use the cached models.

**Verification**:

```bash
python -c "from docling.document_converter import DocumentConverter; print('Docling imported successfully.')"
```

A successful installation prints the confirmation message without errors.

## Wiring the Components

With all components installed individually, the final step connects them into the integrated knowledge pipeline described in the architecture chapter.

### Docling-to-ChromaDB Ingestion Pipeline

Save the following script as `scripts/ingest_docs.py`. It walks a documentation directory, parses each file with Docling, chunks the output, and stores the embeddings in ChromaDB:

```python
import os
import chromadb
from docling.document_converter import DocumentConverter

DOCS_DIR = "./docs"
CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "project_docs"
CHUNK_SIZE = 500

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
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

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

        ids = [f"{os.path.basename(filepath)}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filepath, "chunk_index": i} for i in range(len(chunks))]

        collection.upsert(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        print(f"  Stored {len(chunks)} chunks.")

    print(f"\nTotal documents in collection: {collection.count()}")

if __name__ == "__main__":
    main()
```

Run the pipeline:

```bash
mkdir -p docs
# Place PDF, DOCX, or Markdown files in the docs/ directory
python scripts/ingest_docs.py
```

### ChromaDB Retrieval Function

Save the following script as `scripts/query_docs.py` for testing semantic retrieval:

```python
import sys
import chromadb

CHROMA_PATH = "./chroma_data"
COLLECTION_NAME = "project_docs"

def query(question, n_results=3):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    for i, doc in enumerate(results["documents"][0]):
        source = results["metadatas"][0][i]["source"]
        print(f"\n--- Result {i+1} (source: {source}) ---")
        print(doc[:300])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/query_docs.py 'search query'")
        sys.exit(1)
    query(" ".join(sys.argv[1:]))
```

```bash
python scripts/query_docs.py "authentication flow for the API"
```

The script queries ChromaDB with the provided natural-language question and prints the top three matching document chunks with their source file paths.

## Verification

The following end-to-end checks confirm that all components are installed, wired, and operational.

| Check | Command | Expected Result |
|---|---|---|
| Claude Code | `claude --version` | Prints version number |
| MCP servers | Launch Claude Code, ask it to read a file via MCP | Agent reads the file without error |
| Ollama | `curl http://localhost:11434/v1/models` | Returns JSON list of pulled models |
| ChromaDB | `python scripts/init_chromadb.py` | Prints collection name and document count |
| Docling | `python -c "from docling.document_converter import DocumentConverter; print('OK')"` | Prints "OK" |
| Full pipeline | Place a test PDF in `docs/`, run `python scripts/ingest_docs.py`, then `python scripts/query_docs.py "test query"` | Returns relevant chunks from the ingested document |

The Solo Developer Stack is operational once all six checks pass. The architecture chapter provides the rationale behind each component selection and the design decisions governing how the layers interact.

## References

1. Claude Code Installation Guide, Anthropic.
2. MCP Server Reference Implementations, Model Context Protocol.
3. Ollama Installation Documentation, Ollama Inc.
4. ChromaDB Getting Started Guide, Chroma Inc.
5. Docling Installation Guide, IBM Research and LF AI and Data Foundation.
6. Brave Search API, Brave Software.
