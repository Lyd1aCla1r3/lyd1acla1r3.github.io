# Agent Frameworks Compared

<!-- SUMMARY: A deep-dive comparison of LangChain, LlamaIndex, Microsoft Agent Framework, Pydantic AI, and DSPy, including tabbed profiles and feature matrices. -->

An agent is an application where a language model makes decisions and takes actions. At its simplest, this requires three components: a language model accessed via its API, tools exposed as MCP servers, and a host application that connects the two. The host acts as an MCP client: it sends the user's request to the model, the model decides which tool to call, the host forwards that call to the appropriate MCP server, and the result feeds back into the model. The coding agents in the previous post, such as Cursor, Copilot, and Claude Code, are agents built on this pattern. They connect a language model to development-specific tools like file reading, terminal commands, and web search, and provide a user interface for the developer to interact through.

An agent framework is a code library, such as a Python or JavaScript package, that provides pre-built components for the host application layer. For a simple agent that calls one or two tools, the host can be minimal: a short script that manages the model-call-tool-result loop. However, as applications grow more complex, the host needs internal processing stages that are not tool calls themselves. A retrieval-augmented pipeline needs to load documents, split them into chunks, compute embeddings, store them in a vector index, and retrieve the relevant chunks at query time. An extraction pipeline needs to validate the model's output against a schema and retry if it fails. A multi-turn assistant needs to maintain conversation state across interactions. Frameworks provide pre-built, composable implementations of these stages so that developers do not build each one from scratch. A framework has no UI and no standalone executable; the developer writes application code using the framework's components, and that code becomes the host application.

The five frameworks below are selected for their adoption, architectural distinctiveness, and ecosystem influence: a general-purpose composition library like LangChain, a data-and-retrieval-first toolkit like LlamaIndex, a unified enterprise platform like Microsoft Agent Framework, a type-safe minimalist layer like Pydantic AI, and a declarative prompt optimizer like DSPy.

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
    <p>Every component in LangChain's catalog, including model wrappers, prompt templates, output parsers, document loaders, retrievers, and vector store connectors, implements a single interface called the <strong>Runnable</strong>. Each Runnable exposes the same set of methods, such as invoke, stream, batch, and their async counterparts, and because every component shares this interface, they compose using the LangChain Expression Language (LCEL), a pipe-based syntax where stages chain with the <code>|</code> operator, such as <code>prompt | model | parser</code>. A pipeline built this way inherits streaming, concurrency, and retry behavior from the Runnable protocol, without the developer wiring those capabilities at each stage. All of these components are Python or JavaScript classes called directly in application code; MCP is not involved. MCP becomes relevant as an additional option: if external tools are exposed as MCP servers, LangChain can connect to them through an adapter package called <code>langchain-mcp-adapters</code>, but the core framework operates through Runnable.</p>
    <p>LangChain maintains the largest catalog of pre-built Runnables across any framework in this comparison: dedicated partner packages for every major model provider, hundreds of document loaders for ingesting PDFs and databases, text splitters for chunking, and connectors for dozens of vector stores. The trade-off for this breadth is abstraction depth; the layers of Runnables between the developer's code and the underlying API calls can make debugging difficult, which is part of why LangSmith, the companion observability platform, provides detailed traces through the chain. LangChain also anchors a broader ecosystem, such as LangGraph for graph-based orchestration, covered in the orchestrators post, and is natively implemented in both Python and JavaScript/TypeScript with near-feature parity, making it the only framework in this comparison with full support for both language ecosystems.</p>
  </div>

  <div class="post-tab-content" data-tab-content="llamaindex">
    <h3>LlamaIndex</h3>
    <p><strong>Maker:</strong> LlamaIndex, Inc.<br><strong>Architecture:</strong> Data-centric framework (load, index, query)</p>
    <p>Most agent frameworks treat data retrieval as one feature among many: they provide a basic retriever component, connect it to a vector store, and move on. However, for applications querying massive, complex document repositories, like legal contracts, medical records, or enterprise wikis, basic vector similarity search is often insufficient. A single query needs to be decomposed into sub-questions, each answered from different data sources. Complex documents with tables, charts, and multi-column layouts lose their structure entirely during standard text extraction.</p>
    <p>LlamaIndex is built around solving this data ingestion and retrieval problem. Its architecture follows a <strong>load, index, query</strong> pipeline. Data is ingested through connectors, with LlamaHub offering over 300, and parsed into <strong>nodes</strong>, which are objects that contain not just a chunk of text, but also metadata and explicit relationships to other chunks. This structure enables retrieval strategies that go well beyond basic vector search. For example, small chunks of text yield more precise search matches, but the model requires the broader context of the full section to synthesize a good answer. The <code>AutoMergingRetriever</code> splits large parent nodes into smaller child nodes and searches only against the children. If a specified threshold of child nodes from the same parent match the search query, the retriever infers the entire section is relevant. Instead of returning the isolated child nodes, it returns the complete parent node, or only the matching child nodes if the threshold is not met. Another strategy, the <code>PropertyGraphIndex</code>, extracts concrete entities, such as "Company A", and their relationships, such as "acquired by Company B", into a graph structure, allowing the application to query exact logical connections rather than just searching by general text similarity.</p>
    <p>LlamaIndex began as a pure retrieval library and evolved into a full agent framework. It provides pre-built base classes like <code>FunctionCallingAgent</code> or <code>AgentWorkflow</code> that developers use to instantiate an agent and manage its reasoning loop. The distinctive architectural trait is that LlamaIndex wraps its complex data engines into standard tools. These tools can be called by an agent instantiated via LlamaIndex, or they can be exported and called by a host application built on an entirely different framework, like LangChain or Microsoft Agent Framework. When an agent is handed a query engine as a single tool to answer "compare the Q3 revenue of Company A and Company B," the engine handles decomposing the query, searching the indices, and synthesizing the facts, returning a clean answer back to the agent's main reasoning loop.</p>
  </div>

  <div class="post-tab-content" data-tab-content="maf">
    <h3>Microsoft Agent Framework</h3>
    <p><strong>Maker:</strong> Microsoft<br><strong>Architecture:</strong> Unified agent SDK (merged from Semantic Kernel + AutoGen)</p>
    <p>Most agent frameworks are written in Python. This presents a specific challenge for large enterprises that have built their software in C# on Microsoft's .NET platform. A development team cannot easily plug a Python framework into an existing C# codebase without building complex bridges between the two languages. Furthermore, enterprises in regulated industries rely on their cloud hosting providers for security and compliance certifications like HIPAA. If a team uses a general-purpose framework, they must manually write the security code required to make their agents safely interact with corporate databases and identity systems.</p>
    <p>Microsoft Agent Framework (MAF) addresses this by treating C# and .NET as first-class citizens alongside Python. It allows enterprise teams to build agents using the same programming language and structural rules their existing software already uses. MAF unifies two previously separate Microsoft projects, Semantic Kernel and AutoGen, into a single toolkit. Like most frameworks in this space, it provides standard capabilities for giving models access to tools, managing memory, and orchestrating multiple agents to work together on a single task.</p>
    <p>The primary differentiator is MAF's built-in integration with Microsoft's enterprise infrastructure. Instead of requiring custom security code, MAF connects directly to Entra ID, Microsoft's corporate identity system. This allows an organization to issue autonomous agents their own corporate identities and restrict their access to sensitive data exactly as they would for human employees. The framework also connects directly to Azure AI Foundry, a Microsoft platform for hosting, testing, and monitoring AI models, and Azure AI Search for data retrieval. This combination of a native C# architecture and direct Azure integration makes MAF unique among major agent frameworks: it is the only one designed specifically to bridge the gap between AI agents and existing .NET enterprise codebases.</p>
  </div>

  <div class="post-tab-content" data-tab-content="pydantic">
    <h3>Pydantic AI</h3>
    <p><strong>Maker:</strong> Pydantic, led by Samuel Colvin and the team behind the Pydantic data validation library<br><strong>Architecture:</strong> Type-safe, minimal agent framework</p>
    <p>In most agent frameworks, giving an AI model access to a tool requires writing duplicate code. A developer must write the actual Python function, for example, code that fetches a customer record from a database, and then separately write a JSON schema that explains to the AI what that function does and what inputs it requires. The same duplication happens when asking the AI to return structured data. This creates a brittle system: if the Python code changes but the AI schema is not updated, the pipeline breaks. Furthermore, general-purpose AI frameworks often hide database connections or configuration data in global variables, which makes it difficult to test the system reliably without accidentally triggering real database changes or external API calls.</p>
    <p>Pydantic AI addresses these problems by building directly on top of Pydantic, a widely used data validation library in the Python ecosystem. Instead of forcing developers to write separate schemas for the AI, Pydantic AI inspects the standard type hints, like <code>customer_id: int</code>, that developers already use in their normal Python code. It automatically translates those Python types into the exact instructions and schemas the AI model needs. If the AI returns a response that does not match the expected Python structure, the framework automatically catches the validation error, feeds it back to the AI, and prompts it to correct the mistake.</p>
    <p>Pydantic AI enforces strict engineering practices because it is built for production backend systems. It requires developers to explicitly pass dependencies, like database connections or API clients, to the agent during execution, rather than relying on global state. This makes it trivial to swap in a fake database for deterministic unit testing. The framework is intentionally minimal: it does not include built-in integrations for vector databases or document parsing. Instead, it assumes developers will write their own standard Python functions using existing Python libraries, and then expose those functions to the AI as tools. This makes Pydantic AI the natural choice for engineering teams who already use Pydantic or FastAPI and want to add reliable, testable AI capabilities to their backend services without adopting a heavy orchestration framework.</p>
  </div>

  <div class="post-tab-content" data-tab-content="dspy">
    <h3>DSPy</h3>
    <p><strong>Maker:</strong> Stanford NLP, including Omar Khattab, now at MIT CSAIL<br><strong>Architecture:</strong> Declarative prompt optimization framework using signatures, modules, and optimizers</p>
    <p>Every other framework in this post treats prompts as something the developer writes manually. The developer crafts a system message, selects a few-shot example set by hand, adjusts the wording based on trial and error, and hopes the result generalizes. When the application switches from one model to another, such as from GPT-4o to Claude, or from a cloud model to a self-hosted Llama, prompts that worked well on the original model often degrade, requiring another round of manual tuning. As pipelines grow more complex, such as retrieval followed by reasoning followed by formatting followed by validation, prompt quality issues compound across stages. Manually optimizing prompts for a multi-stage pipeline across multiple models is not scalable.</p>
    <p>DSPy takes a different approach: it treats prompt construction as an optimization problem rather than a writing task. The developer defines the task structure by writing a <strong>Signature</strong>. A Signature is a simple declaration of what goes in and what comes out, for example, <code>"document -> summary"</code>, separating the goal of the task from the specific wording of the prompt. If the developer needs the output in a specific data format, they use a "typed" Signature to enforce those rules. Next, the developer selects a reasoning strategy, known as a <strong>Module</strong>, such as instructing the model to think step-by-step before answering, and writes an evaluation <strong>Metric</strong>, which is a Python function that scores output quality. An <strong>Optimizer</strong> then automatically searches for the best prompt configuration, including instructions, few-shot examples, and reasoning patterns, that maximizes the metric on a training set. The architecture is analogous to PyTorch: just as a PyTorch "layer definition" dictates the shape of data flowing through a network, a DSPy Signature dictates the inputs and outputs of a prompt. Just as a PyTorch <code>nn.Module</code> contains the computation logic and weights that get optimized, a DSPy Module contains the reasoning strategy and prompt wording that get optimized. Metrics correspond to loss functions, and Optimizers correspond to gradient descent.</p>
    <p>The practical benefit is model portability. A pipeline optimized for GPT-4o can be recompiled for a smaller, cheaper model, like Llama-3-8B, by running the optimizer again with the new model as the target. The optimizer adapts the prompt strategy to the target model's strengths and weaknesses automatically, without the developer rewriting any prompts. DSPy also supports distillation: training data generated by a large, capable model can be used to fine-tune a smaller, cheaper model, bridging the gap between proprietary cloud models and self-hosted open-source alternatives. Optimizers range from BootstrapFewShot, which automates the selection of examples, to MIPROv2, which searches mathematically for the best combination of instructions and examples, to GEPA, which automatically asks a larger AI model to critique and improve the prompts iteratively. For teams where prompt quality directly impacts business metrics and labeled evaluation data is available, DSPy provides a systematic, reproducible alternative to manual prompt engineering.</p>
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
| **Microsoft Agent Framework** | Kernel + plugins + graph-based Workflow API | C#/.NET, Python, Go (preview) | `pip install agent-framework` or NuGet `Microsoft.Agents.AI` |
| **Pydantic AI** | Type-safe agents with dependency injection and Pydantic validation | Python | `pip install pydantic-ai` |
| **DSPy** | Declarative signatures compiled by optimizers | Python | `pip install dspy` |

LangChain and LlamaIndex offer the broadest language accessibility with both Python and JavaScript/TypeScript SDKs. Microsoft Agent Framework is the only option with first-class C#/.NET support, making it the natural choice for enterprise .NET shops. Pydantic AI and DSPy are Python-only, which limits their reach but allows them to leverage Python-specific features (type hints, decorators, Pydantic schemas) more deeply.

### Core Capabilities

Beyond basic model interaction, frameworks differ in how they handle retrieval, memory, and output validation. **Built-in RAG Pipeline** indicates whether the framework ships with integrated document loaders, text splitters, and vector store connectors as part of its core offering (not requiring external libraries). **Structured Output** describes how the framework ensures model responses conform to a defined schema. **Built-in Testing Mode** indicates whether the framework provides a purpose-built mechanism for running agent tests without making real API calls.

| Capability | LangChain | LlamaIndex | Microsoft Agent Framework | Pydantic AI | DSPy |
|------------|-----------|------------|---------------------------|-------------|------|
| Tool/function calling | Yes | Yes | Yes | Yes | Yes |
| Structured output | Yes | Yes | Yes | Yes | Yes |
| Built-in RAG pipeline | Yes | Yes | Yes | No | Yes |
| Memory | Yes | Yes | Yes | No | No |
| Streaming | Yes | Yes | Yes | Yes | Yes |
| Built-in testing mode | No | No | No | Yes | No |
| Prompt optimization | No | No | No | No | Yes |

All five frameworks support tool calling, structured output, and streaming. The primary differentiations emerge in retrieval depth, testing infrastructure, and the prompt authoring paradigm. LlamaIndex provides the most sophisticated built-in retrieval, with strategies that combine multiple search techniques and understand document structure better than basic vector search. Pydantic AI is the only framework with a dedicated testing mode that eliminates the need for mocking. DSPy is the only framework that treats prompt construction as an optimization problem rather than a manual authoring task.

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
| **LlamaIndex** | 300+ data connectors, 40+ vector stores | None (Third-party) |
| **Microsoft Agent Framework** | Azure ecosystem, A2A protocol | Azure Monitor |
| **Pydantic AI** | Minimal by design (relies on standard Python libraries) | Logfire |
| **DSPy** | Minimal (basic vector DB adapters) | None (Third-party) |

Since all five frameworks support MCP, any of them can access the same set of MCP tool servers with the same configuration. The differentiator is what ships natively. Microsoft Agent Framework is the only one with built-in A2A protocol support, enabling cross-platform agent communication without custom integration work. LangChain has the largest number of pre-built integration packages. LlamaIndex has the largest collection of data-specific connectors. Pydantic AI intentionally ships with minimal integrations, relying on MCP and standard Python libraries for external connectivity.

### Strongest Use Cases and Known Limitations

Each framework is optimized for a specific development scenario and carries trade-offs that make it less suitable for others.

| Framework | Strongest Use Case | Known Limitation |
|-----------|--------------------|------------------|
| **LangChain** | Rapid prototyping with maximum integration breadth; teams needing a single framework that connects to every provider, loader, and vector store | Abstraction overhead: multiple wrapper layers can obscure simple operations, making debugging difficult without LangSmith tracing |
| **LlamaIndex** | Data-intensive retrieval applications (enterprise document search, multi-source knowledge bases, complex PDF ingestion) | Advanced document parsing (LlamaParse) and managed infrastructure (LlamaCloud) are paid services; general agent orchestration is less mature than its retrieval capabilities |
| **Microsoft Agent Framework** | Enterprise teams on Azure and .NET requiring platform-grade compliance, identity management, and C# as a primary language | Tightest integration is with the Azure ecosystem; teams not on Azure lose the platform advantages that distinguish it from other frameworks |
| **Pydantic AI** | Production backend services requiring strict type safety, dependency injection, deterministic testing, and minimal framework overhead | No built-in document loaders, vector store connectors, or memory abstractions; Python-only (no JavaScript/TypeScript SDK) |
| **DSPy** | Systematic prompt optimization when labeled evaluation data is available and prompt quality directly impacts measurable business metrics | Requires training data and well-defined metrics; optimization runs consume significant tokens; the paradigm shift from manual prompting has a steep learning curve |

Teams building their first LLM-powered application and needing broad integration support often start with LangChain. Teams whose primary challenge is retrieving the right context from complex data sources lean toward LlamaIndex. Enterprise organizations on Azure and .NET gravitate toward Microsoft Agent Framework for its platform integration and compliance inheritance. Backend developers who prioritize type safety, testability, and minimal abstraction prefer Pydantic AI. Teams with evaluation datasets and quantitative quality targets benefit from DSPy's optimization-driven approach. Many production systems combine multiple frameworks: using LlamaIndex for retrieval, LangChain or Pydantic AI for the agent layer, and DSPy for optimizing the prompts within that agent.

## References

1. LangChain Documentation and API Reference.
2. LlamaIndex Documentation and LlamaHub Integration Registry.
3. Microsoft Agent Framework Documentation on Microsoft Learn.
4. Pydantic AI Documentation and GitHub Repository.
5. DSPy: Compiling Declarative Language Model Calls into State-of-the-Art Pipelines (Khattab et al., Stanford NLP).
6. Model Context Protocol Specification, Linux Foundation Agentic AI.
7. Agent-to-Agent (A2A) Protocol Specification, Google.
