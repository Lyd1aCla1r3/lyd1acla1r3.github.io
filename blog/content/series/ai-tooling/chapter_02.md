# Agent Frameworks Compared

<!-- SUMMARY: A deep-dive comparison of LangChain, LlamaIndex, Microsoft Agent Framework, Pydantic AI, and DSPy, including tabbed profiles and feature matrices. -->

An agent is an application where a language model makes decisions and takes actions. At its simplest, this architecture requires three components: a language model accessed via its API, tools exposed as local functions or MCP servers, and a host application that connects the two. Acting as an MCP client, the host sends the user's request to the model, forwards the model's selected tool invocation to the appropriate MCP server, and returns the execution result back to the model. The coding agents in [Coding Agents Compared](ai-tooling-chapter_01.html), such as Cursor, Copilot, and Claude Code, follow this pattern by connecting a language model to workspace tools and providing an interactive user interface.

An agent framework is a code library, such as a Python or TypeScript package, that provides pre-built abstractions for the host application layer. A simple agent that calls one or two tools requires only a minimal script to manage the request-tool-response loop. Production applications grow beyond simple tool loops and require internal host stages that execute alongside model calls:

- **Retrieval-Augmented Generation (`RAG`) Stages:** Ingestion pipelines load documents, split text into chunks, compute vector embeddings, store vectors in an index, and retrieve relevant context at query time.
- **Structured Extraction Stages:** Validation layers parse model outputs against strict data schemas and trigger automatic correction retries on malformed responses.
- **Conversation Memory Stages:** State management layers persist, summarize, and window multi-turn dialogue history across user sessions.

Frameworks provide composable implementations of these host stages so engineering teams do not rebuild infrastructure primitives from scratch. Unlike a coding agent, a framework has no user interface and no standalone binary; the developer imports the framework's components into application code to construct the host runtime.

The five frameworks below are selected for their adoption, architectural distinctiveness, and ecosystem influence: a general-purpose composition library (LangChain), a data-and-retrieval-first toolkit (LlamaIndex), a unified enterprise SDK (Microsoft Agent Framework), a type-safe minimalist validation layer (Pydantic AI), and a declarative prompt compiler (DSPy).

<style>
.fw-profile-panel {
    border: 1.5px solid rgba(183,110,121,0.18);
    border-radius: 10px;
    padding: 14px 22px 18px 22px;
    margin-bottom: 1.5rem;
    background: rgba(255,255,255,0.85);
    transition: border-color 0.3s ease, background 0.3s ease;
}
.fw-profile-panel .post-tab-content h3 {
    margin-top: 0 !important;
}
.fw-profile-panel .post-tab-content.active {
    padding-top: 0;
}
</style>

<script>
var _fwColors = {
    'langchain':   { border: 'rgba(183,110,121,0.35)', bg: 'rgba(251,243,244,0.6)' },
    'llamaindex':  { border: 'rgba(192,120,136,0.35)', bg: 'rgba(251,241,243,0.6)' },
    'maf':         { border: 'rgba(192,136,104,0.35)', bg: 'rgba(251,244,239,0.6)' },
    'pydantic':    { border: 'rgba(184,144,40,0.35)',  bg: 'rgba(252,247,236,0.6)' },
    'dspy':        { border: 'rgba(168,104,104,0.35)', bg: 'rgba(250,241,239,0.6)' }
};

document.addEventListener('DOMContentLoaded', function() {
    var panel = document.getElementById('fw-profile-panel');
    if (!panel) return;
    var btns = panel.parentElement.querySelectorAll('[data-tab]');
    btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var key = this.getAttribute('data-tab');
            var colors = _fwColors[key];
            if (colors && panel) {
                panel.style.borderColor = colors.border;
                panel.style.background = colors.bg;
            }
        });
    });
    var firstColors = _fwColors['langchain'];
    if (firstColors && panel) {
        panel.style.borderColor = firstColors.border;
        panel.style.background = firstColors.bg;
    }
});
</script>

<div data-tab-group="frameworks">
  <div class="post-tabs">
    <button class="post-tab-btn active" data-tab="langchain">LangChain</button>
    <button class="post-tab-btn" data-tab="llamaindex">LlamaIndex</button>
    <button class="post-tab-btn" data-tab="maf">Microsoft Agent Framework</button>
    <button class="post-tab-btn" data-tab="pydantic">Pydantic AI</button>
    <button class="post-tab-btn" data-tab="dspy">DSPy</button>
  </div>

  <div class="fw-profile-panel" id="fw-profile-panel">

  <div class="post-tab-content active" data-tab-content="langchain">
    <h3>LangChain</h3>
    <p><strong>Maker:</strong> LangChain, Inc.<br><strong>Architecture:</strong> Composable chain library with LCEL (LangChain Expression Language)</p>
    <p>Every component in LangChain's catalog, including model wrappers, prompt templates, output parsers, document loaders, retrievers, and vector store connectors, implements a unified interface called the <strong>Runnable</strong>. Each Runnable exposes a standard execution contract (<code>invoke</code>, <code>stream</code>, <code>batch</code>, and their asynchronous counterparts). That shared contract allows components to compose via the LangChain Expression Language (<code>LCEL</code>), a declarative pipe syntax where stages chain with the <code>|</code> operator, such as <code>prompt | model | parser</code>.</p>
    <p>A pipeline constructed through <code>LCEL</code> automatically inherits streaming propagation, parallel batch execution, and configurable retry behavior from the Runnable protocol without custom plumbing at each stage. All of these components execute as native Python or TypeScript classes inside the host application. External tools exposed as MCP servers integrate into this Runnable pipeline through the <code>langchain-mcp-adapters</code> package.</p>
    <p>LangChain maintains the broadest catalog of pre-built integrations across any framework in this comparison, with dedicated partner packages for major model providers, document loaders, text splitters, and vector stores. The trade-off for this breadth is abstraction depth: multiple wrapper layers between application code and raw API calls can obscure runtime state, which motivates pairing the library with LangSmith for step-by-step trace inspection. LangChain also anchors a broader ecosystem that includes <a href="ai-tooling-chapter_03.html">LangGraph</a> for cyclic orchestration and maintains first-party SDKs in both Python and JavaScript/TypeScript.</p>
  </div>

  <div class="post-tab-content" data-tab-content="llamaindex">
    <h3>LlamaIndex</h3>
    <p><strong>Maker:</strong> LlamaIndex, Inc.<br><strong>Architecture:</strong> Data-centric framework (load, index, query)</p>
    <p>Most agent frameworks treat data retrieval as one feature among many: they provide a basic retriever component, connect it to a vector store, and move on. Applications querying complex enterprise repositories, such as legal contracts, medical records, or multi-modal technical manuals, quickly outgrow flat top-k vector similarity search. A single user request often requires decomposing the query into sub-questions routed across distinct indices, while documents containing tables, charts, and multi-column layouts lose their structural hierarchy during naive text splitting.</p>
    <p>LlamaIndex is architected specifically around this data ingestion and retrieval pipeline through a three-stage <strong>load, index, query</strong> model. Data is ingested through LlamaHub connectors and parsed into <strong>Nodes</strong>, which store text chunks alongside structural metadata and explicit parent-child and sibling relationships to surrounding chunks. This graph of relationships enables retrieval strategies that go well beyond flat vector similarity.</p>
    <p>Small text chunks yield high-precision embedding matches, whereas language models require broader section context to synthesize complete answers. The <code>AutoMergingRetriever</code> resolves this tension by indexing fine-grained child nodes linked to larger parent section nodes; whenever a sufficient ratio of child nodes under the same parent match a query, the retriever swaps in the full parent node to preserve surrounding context. A complementary strategy, the <code>PropertyGraphIndex</code>, extracts typed entities and relationships into a knowledge graph so queries can traverse explicit logical connections alongside vector similarity.</p>
    <p>LlamaIndex wraps these retrieval pipelines into standard query engine tools and event-driven <code>AgentWorkflow</code> orchestrators. A query engine tool can run inside a native LlamaIndex agent or be exported to a host application built on LangChain or Microsoft Agent Framework. Handed a complex multi-document question, the query engine decomposes the query, searches the underlying vector and graph indices, and synthesizes a grounded response before returning control to the outer agent loop.</p>
  </div>

  <div class="post-tab-content" data-tab-content="maf">
    <h3>Microsoft Agent Framework</h3>
    <p><strong>Maker:</strong> Microsoft<br><strong>Architecture:</strong> Unified agent SDK (merged from Semantic Kernel + AutoGen)</p>
    <p>Most agent frameworks are written in Python. That language boundary creates friction for large enterprises whose core backend services run in C# on Microsoft's .NET platform. Engineering teams cannot embed a Python-only library into an existing C# service without maintaining inter-process bridges or separate microservices. Enterprises in regulated industries also rely on their cloud provider's identity and compliance boundary; adopting a standalone open-source library often forces teams to hand-roll authentication and audit logging around every tool call.</p>
    <p>Microsoft Agent Framework (<code>MAF</code>) addresses this requirement by treating C#/.NET and Python as co-equal, first-class runtimes. It unifies Microsoft's enterprise plugin architecture (Semantic Kernel) and multi-agent orchestration patterns (AutoGen) into a single SDK. Developers define tools, memory stores, and typed middleware pipelines using native .NET dependency injection or standard Python idioms.</p>
    <p>The primary differentiator is native integration with enterprise identity and cloud governance infrastructure. Rather than requiring custom security wrappers, <code>MAF</code> integrates directly with Microsoft Entra ID so organizations can provision autonomous agents with dedicated service identities and enforce role-based access control (<code>RBAC</code>) on corporate data sources. Coupled with native connectors for Azure AI Foundry and Azure AI Search, <code>MAF</code> bridges AI agent workflows directly into existing .NET and Azure enterprise architectures.</p>
  </div>

  <div class="post-tab-content" data-tab-content="pydantic">
    <h3>Pydantic AI</h3>
    <p><strong>Maker:</strong> Pydantic, led by Samuel Colvin and the team behind the Pydantic data validation library<br><strong>Architecture:</strong> Type-safe, minimal agent framework</p>
    <p>In many agent frameworks, exposing a tool or enforcing structured output requires maintaining parallel definitions: a Python function for execution alongside a separate schema definition for the language model. That duplication introduces schema drift whenever application code changes without updating the corresponding prompt schema. Many general-purpose frameworks also store database connections or API clients in implicit global state, complicating deterministic unit testing without live network calls.</p>
    <p>Pydantic AI eliminates schema duplication by building directly on top of the Pydantic validation library. Rather than writing separate JSON schemas, developers annotate tool parameters and return types with standard Python type hints such as <code>customer_id: int</code> and Pydantic <code>BaseModel</code> classes. The framework introspects those type annotations to generate the JSON schema sent to the model and validates the returned payload against the same Python definition. Any response that fails validation triggers an automatic reflection retry that sends the structured Pydantic error trace back to the model for self-correction.</p>
    <p>Pydantic AI enforces production backend engineering patterns through explicit dependency injection. Database connections, HTTP clients, and user context objects are passed through a typed <code>RunContext</code> object at invocation time rather than stored in global state, allowing unit tests to substitute deterministic mock dependencies or use the built-in <code>TestModel</code> without live API calls. By intentionally omitting bundled document loaders or vector store wrappers, Pydantic AI provides a lightweight, type-safe agent layer for teams building on FastAPI and standard Python backend libraries.</p>
  </div>

  <div class="post-tab-content" data-tab-content="dspy">
    <h3>DSPy</h3>
    <p><strong>Maker:</strong> Stanford NLP, including Omar Khattab, now at MIT CSAIL<br><strong>Architecture:</strong> Declarative prompt optimization framework using signatures, modules, and optimizers</p>
    <p>Every other framework in this chapter treats prompts as hand-authored strings. Developers draft a system prompt, curate a few-shot example set by trial and error, and tune phrasing around a specific model family. Switching the underlying model from one proprietary frontier model to another, or migrating to a smaller open-weight model, frequently degrades output accuracy and forces another round of manual prompt editing. Multi-stage pipelines compound this fragility across sequential retrieval, reasoning, and formatting steps.</p>
    <p>DSPy replaces manual prompt editing with declarative program compilation. Developers specify task interfaces using a <strong>Signature</strong>, which declares typed inputs and outputs (such as <code>document -&gt; summary</code>) without hardcoding prompt prose. Next, developers compose those Signatures inside reasoning <strong>Modules</strong> (such as <code>ChainOfThought</code> or <code>ReAct</code>) and define a programmatic evaluation <strong>Metric</strong> that scores output quality against a validation dataset.</p>
    <p>A DSPy <strong>Optimizer</strong> (formerly called a teleprompter) then compiles the pipeline by searching over candidate instructions, synthesized few-shot demonstrations, and model weights to maximize the target metric. The programming model mirrors PyTorch: Signatures define the layer input/output contract, Modules encapsulate parameterized reasoning blocks, Metrics act as the objective function, and Optimizers (such as <code>BootstrapFewShot</code>, <code>MIPROv2</code>, and <code>GEPA</code>) automate parameter tuning.</p>
    <p>The primary engineering payoff is systematic model portability. A multi-stage pipeline compiled against a large frontier model can be recompiled for a smaller, lower-cost open-weight model by re-running the optimizer against the new target endpoint and evaluation metric. For teams with labeled evaluation datasets and quantitative accuracy targets, DSPy turns prompt engineering into a reproducible, metric-driven build step.</p>
  </div>

  </div>
</div>

## Comparison Tables

Selecting an agent framework depends on the application's core requirements: whether the primary challenge is integration breadth, data retrieval depth, enterprise platform compliance, production type safety, or systematic prompt optimization. The tables below compare the five frameworks across five dimensions. Each table is followed by a brief synthesis of the key takeaway.

### Architecture and Runtime Requirements

A framework's architecture determines how developers structure their applications and what languages they can use. The **Core Paradigm** column describes the fundamental approach for building agents. The **Primary Languages** column lists languages with first-party, actively maintained SDKs.

| Framework | Core Paradigm | Primary Languages | Installation |
|-----------|-------------------|-------------------|-------------|
| **LangChain** | Chain composition (connecting steps sequentially) and Runnable protocol | Python, JavaScript/TypeScript | `pip install langchain` or `npm install langchain` |
| **LlamaIndex** | Data-centric pipeline (load, index, query) with event-driven Workflows | Python, TypeScript | `pip install llama-index` or `npm install llamaindex` |
| **Microsoft Agent Framework** | Kernel + plugins + graph-based Workflow API | C#/.NET, Python | `pip install agent-framework` or NuGet `Microsoft.Agents.AI` |
| **Pydantic AI** | Type-safe agents with dependency injection and Pydantic validation | Python | `pip install pydantic-ai` |
| **DSPy** | Declarative signatures compiled by optimizers | Python | `pip install dspy` |

LangChain and LlamaIndex offer the broadest language accessibility with both Python and JavaScript/TypeScript SDKs. Microsoft Agent Framework is the only option with first-class C#/.NET support, making it the natural choice for enterprise .NET shops. Pydantic AI and DSPy are Python-only, which narrows their runtime scope but allows them to exploit Python-specific language primitives (type annotations, decorators, and Pydantic validation schemas) directly.

### Core Capabilities

Beyond basic model interaction, all five frameworks support tool calling and streaming responses as baseline capabilities, while diverging in how they handle structured validation, retrieval, memory, and testing. **Built-In RAG & Indexing** indicates whether the framework ships with integrated document loaders, node parsers, and vector store adapters as part of its core architecture. **Deterministic Test Mode** indicates whether the framework provides a first-party mock model runtime for executing unit tests without network calls.

| Framework | Structured Output | Built-In RAG & Memory | Deterministic Testing | Prompt Compilation |
|-----------|-------------------|-----------------------|-----------------------|--------------------|
| **LangChain** | Schema parsers (`LCEL`) | Loaders, splitters, `Runnable` history | Via mock Runnables | No |
| **LlamaIndex** | Pydantic output parsers | Hierarchical nodes, graph indices, memory buffers | Via mock LLMs | No |
| **Microsoft Agent Framework** | Typed response schemas | Connectors, Azure AI Search, thread stores | Via .NET/Python mocks | No |
| **Pydantic AI** | Native Pydantic reflection + retry | Delegated to Python tools; message injection | Yes (`TestModel`, `FunctionModel`) | No |
| **DSPy** | Typed `Signature` fields | Retriever modules (stateless by default) | Via custom LM mocks | Yes (Optimizers) |

All five frameworks support tool calling, structured output, and streaming. The primary differentiations emerge in retrieval depth, testing infrastructure, and the prompt authoring paradigm. LlamaIndex provides the most sophisticated built-in retrieval, with hierarchical node relationships and knowledge graph indices that go beyond flat vector search. Pydantic AI is the only framework with a dedicated `TestModel` and dependency injection container designed for deterministic backend unit testing. DSPy is the only framework that treats prompt construction as a metric-driven compilation pass rather than a manual authoring task.

### Pricing and LLM Support

All five frameworks are open source under the MIT License and support multiple LLM providers through a bring-your-own-key (BYOK) approach. The differences lie in the commercial services each framework's parent company offers alongside the open-source library.

| Framework | Commercial Add-ons | Core LLM Providers |
|-----------|--------------------|--------------------|
| **LangChain** | LangSmith (observability), LangGraph Platform (hosting) | OpenAI, Anthropic, Google, Bedrock, Azure, Mistral, Groq, Cohere, Ollama |
| **LlamaIndex** | LlamaParse (parsing), LlamaCloud (managed RAG) | OpenAI, Anthropic, Google, Bedrock, Azure, Mistral, Groq, Cohere, Ollama |
| **Microsoft Agent Framework** | Azure AI Foundry, Azure AI Search, Cosmos DB | Azure, OpenAI, Anthropic, Gemini, Mistral, Bedrock, Ollama, ONNX |
| **Pydantic AI** | Logfire (observability), Pydantic AI Gateway (routing) | OpenAI, Anthropic, Google, Groq, Mistral, Bedrock, Azure, Cohere, Ollama |
| **DSPy** | None | OpenAI, Anthropic, Gemini, Mistral, Groq, Ollama, Databricks, Together, vLLM |

The open-source cores are functionally equivalent in terms of licensing. The commercial differences reflect each company's monetization strategy: LangChain monetizes through observability and hosted deployment, LlamaIndex through document parsing and managed RAG infrastructure, Microsoft through Azure cloud services, and Pydantic through observability and LLM gateway routing. DSPy has no associated commercial services; its development is supported by academic funding and Databricks engineering collaboration.

### Integration Points

All five frameworks support the Model Context Protocol (MCP), meaning any of them can connect to MCP-compatible tool servers. The differences lie in what each framework provides beyond MCP: native protocol support, ecosystem breadth, and observability platform integration.

| Framework | Built-in Integration Ecosystem | Native Observability |
|-----------|--------------------------------|----------------------|
| **LangChain** | Largest: hundreds of partner and community packages | LangSmith |
| **LlamaIndex** | Hundreds of data connectors (LlamaHub) and vector store adapters | OpenTelemetry / partner integrations |
| **Microsoft Agent Framework** | Azure ecosystem, A2A protocol | Azure Monitor |
| **Pydantic AI** | Minimal by design (relies on standard Python libraries) | Logfire |
| **DSPy** | Minimal (basic vector DB adapters) | None (Third-party) |

Shared MCP support allows all five frameworks to access the same external MCP tool servers using standard client adapters. The differentiator is what ships natively. Microsoft Agent Framework is the only one with built-in Agent-to-Agent (`A2A`) protocol support, enabling cross-platform agent communication without custom integration work. LangChain has the largest number of pre-built integration packages, and LlamaIndex provides the deepest catalog of document and data-source connectors. Pydantic AI intentionally ships with minimal integrations, relying on MCP and standard Python libraries for external connectivity.

### Strongest Use Cases and Known Limitations

Each framework is optimized for a specific development scenario and carries trade-offs that make it less suitable for others.

| Framework | Strongest Use Case | Known Limitation |
|-----------|--------------------|------------------|
| **LangChain** | Rapid prototyping with maximum integration breadth; teams needing a single framework that connects to every provider, loader, and vector store | Abstraction overhead: multiple wrapper layers can obscure simple operations, making debugging difficult without LangSmith tracing |
| **LlamaIndex** | Data-intensive retrieval applications (enterprise document search, multi-source knowledge bases, complex PDF ingestion) | Advanced document parsing (LlamaParse) and managed infrastructure (LlamaCloud) are paid services; general agent orchestration is less mature than its retrieval capabilities |
| **Microsoft Agent Framework** | Enterprise teams on Azure and .NET requiring platform-grade compliance, identity management, and C# as a primary language | Tightest integration is with the Azure ecosystem; teams not on Azure lose the platform advantages that distinguish it from other frameworks |
| **Pydantic AI** | Production backend services requiring strict type safety, dependency injection, deterministic testing, and minimal framework overhead | No built-in document loaders, vector store connectors, or memory abstractions; Python-only (no JavaScript/TypeScript SDK) |
| **DSPy** | Systematic prompt optimization when labeled evaluation data is available and prompt quality directly impacts measurable business metrics | Requires training data and well-defined metrics; optimization runs consume significant tokens; the paradigm shift from manual prompting has a steep learning curve |

Production systems frequently combine multiple frameworks across architectural layers rather than treating them as mutually exclusive. A common pattern pairs LlamaIndex for hierarchical document ingestion and query engines, Pydantic AI or LangChain for the typed tool-calling host layer, and DSPy to compile and optimize the prompt signatures executing inside those agents.

## References

1. LangChain Documentation and API Reference.
2. LlamaIndex Documentation and LlamaHub Integration Registry.
3. Microsoft Agent Framework Documentation on Microsoft Learn.
4. Pydantic AI Documentation and GitHub Repository.
5. DSPy: Compiling Declarative Language Model Calls into State-of-the-Art Pipelines (Khattab et al., Stanford NLP).
6. Model Context Protocol Specification, Linux Foundation Agentic AI.
7. Agent-to-Agent (A2A) Protocol Specification, Google.
