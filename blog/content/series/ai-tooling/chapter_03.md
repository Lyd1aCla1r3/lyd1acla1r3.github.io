# Agent Orchestrators Compared

<!-- SUMMARY: A deep-dive comparison of LangGraph, CrewAI, Microsoft Agent Framework, OpenAI Agents SDK, and Temporal, covering tabbed profiles, capability matrices, and guidance on which orchestrator fits which scenario. -->

A single agent, comprising one model connected to tools via a host application, can accomplish a wide range of tasks: answering questions, writing code, searching documents, and executing commands. Certain production workflows exceed what a single agent loop can handle reliably. A thorough code review requires one agent to analyze functional correctness, another to audit security vulnerabilities, and a third to synthesize a summary informed by the security findings. A long-running research pipeline needs to pause for human approval, survive a server restart, and resume from its saved state without repeating completed work. A customer support system needs to route a conversation from a triage agent to a billing specialist to a returns handler, each equipped with isolated tools and instructions.

An orchestrator manages these multi-agent or stateful single-agent workflows. It determines which agent runs next, what state each agent receives, how the system handles step failures, and how execution recovers from process crashes. The libraries in [Agent Frameworks Compared](ai-tooling-chapter_02.html) provide the building blocks for individual agents, including model connectors, tool interfaces, and retrieval pipelines, whereas orchestrators provide the coordination runtime that connects multiple agents into a reliable, stateful system.

The five orchestrators below represent distinct points on the complexity-to-control spectrum: a cyclic graph state machine (LangGraph), a role-based team abstraction (CrewAI), an actor-and-workflow enterprise platform (Microsoft Agent Framework), a lightweight handoff loop (OpenAI Agents SDK), and a durable event-sourcing execution engine (Temporal).

Microsoft Agent Framework appears in both this chapter and [Agent Frameworks Compared](ai-tooling-chapter_02.html) because its architecture spans both layers. Its framework layer (model connectors, plugins, and typed schemas) was covered in the frameworks chapter; this chapter focuses on its orchestration runtime (actor message queues, pub/sub routing, workflow graphs, and durable tasks). For orchestration capabilities embedded directly inside developer environments, such as sub-agent spawning and workspace sandboxing, see [Coding Agents Compared](ai-tooling-chapter_01.html).

<style>
.orch-profile-panel {
    border: 1.5px solid rgba(183,110,121,0.18);
    border-radius: 10px;
    padding: 14px 22px 18px 22px;
    margin-bottom: 1.5rem;
    background: rgba(255,255,255,0.85);
    transition: border-color 0.3s ease, background 0.3s ease;
}
.orch-profile-panel .post-tab-content h3 {
    margin-top: 0 !important;
}
.orch-profile-panel .post-tab-content.active {
    padding-top: 0;
}
</style>

<script>
var _orchColors = {
    'langgraph':  { border: 'rgba(183,110,121,0.35)', bg: 'rgba(251,243,244,0.6)' },
    'crewai':     { border: 'rgba(192,120,136,0.35)', bg: 'rgba(251,241,243,0.6)' },
    'maf':        { border: 'rgba(192,136,104,0.35)', bg: 'rgba(251,244,239,0.6)' },
    'openai':     { border: 'rgba(184,144,40,0.35)',  bg: 'rgba(252,247,236,0.6)' },
    'temporal':   { border: 'rgba(168,104,104,0.35)', bg: 'rgba(250,241,239,0.6)' }
};

document.addEventListener('DOMContentLoaded', function() {
    var panel = document.getElementById('orch-profile-panel');
    if (!panel) return;
    var btns = panel.parentElement.querySelectorAll('[data-tab]');
    btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var key = this.getAttribute('data-tab');
            var colors = _orchColors[key];
            if (colors && panel) {
                panel.style.borderColor = colors.border;
                panel.style.background = colors.bg;
            }
        });
    });
    var firstColors = _orchColors['langgraph'];
    if (firstColors && panel) {
        panel.style.borderColor = firstColors.border;
        panel.style.background = firstColors.bg;
    }
});
</script>

<div data-tab-group="orchestrators">
  <div class="post-tabs">
    <button class="post-tab-btn active" data-tab="langgraph">LangGraph</button>
    <button class="post-tab-btn" data-tab="crewai">CrewAI</button>
    <button class="post-tab-btn" data-tab="maf">Microsoft Agent Framework</button>
    <button class="post-tab-btn" data-tab="openai">OpenAI Agents SDK</button>
    <button class="post-tab-btn" data-tab="temporal">Temporal</button>
  </div>

  <div class="orch-profile-panel" id="orch-profile-panel">

  <div class="post-tab-content active" data-tab-content="langgraph">
    <h3>LangGraph</h3>
    <p><strong>Maker:</strong> LangChain, Inc.<br><strong>Architecture:</strong> Graph-based cyclic state machine (Pregel BSP model)</p>
    <p>Workflows that require iterative refinement, where an agent generates a candidate solution, evaluates the result, and branches back to retry on failure, cannot be represented as a linear directed acyclic graph (<code>DAG</code>). Cyclic control flow requires a state machine: nodes represent computation steps, edges represent transitions, and conditional edges branch or loop based on runtime state. LangGraph models orchestration directly as a cyclic state graph initialized with a typed schema (<code>TypedDict</code>, Pydantic <code>BaseModel</code>, or dataclass).</p>
    <p>Every node is a standard Python or TypeScript function that reads the current state, performs work, and returns a state update dictionary. Parallel nodes executing within the same step merge their outputs through configurable reducer functions, such as appending new messages to an existing list rather than overwriting the key. This execution model draws from Google's Pregel Bulk Synchronous Parallel (<code>BSP</code>) architecture: computation advances through discrete supersteps where active nodes run concurrently in isolation and commit their state updates at the superstep barrier.</p>
    <p>LangGraph's core durability mechanism is its superstep checkpointer and time-travel API. At the end of every superstep, the runtime persists a snapshot of the graph state to a backing store such as PostgreSQL, SQLite, or Redis. Process crashes recover directly from the latest persisted superstep. Developers can also inspect historical checkpoints, fork execution from an earlier superstep to test alternative branches, or call <code>interrupt()</code> to pause execution mid-node for human approval before resuming with <code>Command(resume=...)</code>. Compiled sub-graphs can be embedded as nodes inside a parent graph to form hierarchical supervisor architectures.</p>
  </div>

  <div class="post-tab-content" data-tab-content="crewai">
    <h3>CrewAI</h3>
    <p><strong>Maker:</strong> CrewAI, Inc. (founded by Jo&#227;o Moura)<br><strong>Architecture:</strong> Role-based multi-agent crew with sequential, hierarchical, and event-driven process types</p>
    <p>Not every multi-agent application requires explicit state schemas and reducer functions. Many workflows, such as research synthesis, report generation, and multi-stage content review, map naturally to a team of specialists collaborating toward a shared objective. CrewAI models orchestration around two primitives: <strong>Agents</strong> (defined with a <code>role</code>, <code>goal</code>, and persona <code>backstory</code>) and <strong>Tasks</strong> (defined with a description, expected output contract, and assigned agent). A <strong>Crew</strong> groups these agents and tasks under a sequential or manager-led hierarchical execution process.</p>
    <p>Adopting a role-based team metaphor trades low-level transition wiring for rapid declarative setup. Inside a Crew, tasks either advance in a fixed sequence or rely on a manager LLM to delegate subtasks dynamically, which abstracts away deterministic per-step branching. CrewAI compensates with an integrated multi-tier memory subsystem that shares context across tasks automatically, combining vector-backed short-term memory, cross-session long-term storage, and entity memory that tracks named subjects and relationships across turns.</p>
    <p>Applications that require deterministic branching above the agent team layer use <strong>CrewAI Flows</strong>, a decorator-driven Python state machine. Using <code>@start()</code>, <code>@router(target)</code>, and <code>@listen(target)</code> decorators, developers wrap one or more Crews inside an outer programmatic pipeline that executes deterministic Python checks and routes data conditionally between specialist Crews. CrewAI also operates as a native MCP client (<code>MCPServerStdio</code>, <code>MCPServerHTTP</code>, and <code>MCPServerSSE</code>) and ships as a Python-first framework.</p>
  </div>

  <div class="post-tab-content" data-tab-content="maf">
    <h3>Microsoft Agent Framework</h3>
    <p><strong>Maker:</strong> Microsoft<br><strong>Architecture:</strong> Actor model runtime with event-driven pub/sub and workflow graph engine</p>
    <p><a href="ai-tooling-chapter_02.html">Agent Frameworks Compared</a> examined Microsoft Agent Framework's single-agent primitives: model connectors, Semantic Kernel plugins, typed schemas, and middleware pipelines. Sitting above those primitives is a distributed orchestration runtime derived from Microsoft's AutoGen architecture. Rather than coordinating agents through a single shared state dictionary, Microsoft Agent Framework (<code>MAF</code>) models each agent as an independent, decentralized <strong>Actor</strong> with a private state store and an asynchronous message queue.</p>
    <p>Strict asynchronous message passing without shared in-process memory makes the runtime inherently location-transparent. An agent actor can execute inside a local process during development and move to a remote worker node in production without modifying agent code. Alongside point-to-point actor messaging, the runtime provides a topic-based pub/sub event bus and a deterministic graph engine (<code>WorkflowBuilder</code>) with built-in patterns including <code>SequentialBuilder</code>, <code>ConcurrentBuilder</code>, <code>SelectorGroupChat</code>, and ledger-driven Magentic-One orchestration.</p>
    <p>Long-running enterprise workflows gain crash recovery and state persistence through integration with the Azure Durable Task framework. Cross-framework interoperability is handled through native support for the Agent-to-Agent (<code>A2A</code>) protocol: whereas internal orchestrator state is normally locked inside a single library, <code>A2A</code> exposes a standardized discovery and task-delegation contract over HTTP so a .NET or Python <code>MAF</code> agent can delegate work to external agents built on other frameworks.</p>
  </div>

  <div class="post-tab-content" data-tab-content="openai">
    <h3>OpenAI Agents SDK</h3>
    <p><strong>Maker:</strong> OpenAI<br><strong>Architecture:</strong> Lightweight handoff-driven agent loop with built-in guardrails</p>
    <p>State graphs, role-based crews, and distributed actor runtimes introduce significant architectural surface area. Applications whose coordination requirements center on conversational triage, specialist delegation, and input/output validation often benefit from a smaller primitive set. The OpenAI Agents SDK (the production successor to the experimental Swarm library) models orchestration around four primitives: <strong>Agents</strong>, <strong>Handoffs</strong>, <strong>Guardrails</strong>, and a <strong>Runner</strong> loop.</p>
    <p>An Agent encapsulates instructions, a target model, tools, and allowed handoff targets. A Handoff is a first-class delegation primitive exposed to the model as a typed tool call (such as <code>transfer_to_billing_agent</code>) that transfers active control and conversation history to another specialist agent. The Runner executes the message loop until the active agent returns a terminal response or invokes a handoff.</p>
    <p>The SDK's key architectural additions are parallel <strong>Guardrails</strong> and managed tool execution. Input, output, and tool guardrails run concurrently alongside the primary agent call; any validation failure triggers an immediate tripwire exception that halts execution before side effects occur or unsafe tokens reach the caller. The SDK connects to external MCP tool servers over stdio and HTTP transports, ships in both Python and TypeScript, and supports OpenAI's hosted tool runtime alongside third-party model routing via LiteLLM adapters.</p>
  </div>

  <div class="post-tab-content" data-tab-content="temporal">
    <h3>Temporal</h3>
    <p><strong>Maker:</strong> Temporal Technologies (founded by Maxim Fateev and Samar Abbas, creators of Uber's Cadence and contributors to AWS Simple Workflow Service)<br><strong>Architecture:</strong> Durable execution engine using event sourcing and deterministic replay</p>
    <p>The four preceding orchestrators are AI-native libraries designed specifically around language model loops. Temporal is a general-purpose durable execution engine originally engineered for distributed transactions, payment settlement, and infrastructure provisioning where multi-step workflows must run to completion across process crashes, network partitions, and multi-day human approval waits. Those same distributed systems guarantees map directly onto long-running agentic pipelines that invoke unreliable external APIs and expensive model inference calls.</p>
    <p>Temporal enforces a strict separation between deterministic <strong>Workflows</strong> (control flow, branching, timers, and signal handling) and non-deterministic <strong>Activities</strong> (LLM API calls, tool executions, and database writes). Rather than periodically saving mutable state snapshots, Temporal uses <strong>Event Sourcing</strong>: the Temporal cluster records every scheduling decision, Activity output, timer, and external Signal as an append-only event log.</p>
    <p>Crash recovery operates through deterministic replay. A replacement worker restarts the Workflow function from its first line of code, and whenever execution reaches a previously completed Activity, the Temporal SDK intercepts the call and injects the recorded return value from the event log without re-executing the external operation. Execution fast-forwards in milliseconds to the interrupted step and resumes forward progress, preventing duplicate execution of completed LLM calls or side-effecting tools. Available across Go, Java, Python, TypeScript, .NET, and PHP, Temporal frequently serves as the durable infrastructure substrate underneath AI-native orchestrators by wrapping LangGraph nodes, CrewAI tasks, or OpenAI agent steps inside Temporal Activities.</p>
  </div>

  </div>
</div>

## Comparison Tables

Selecting an orchestrator depends on the system's core requirements: whether the primary challenge is fine-grained workflow control, rapid team-based prototyping, enterprise infrastructure integration, minimal-overhead agent routing, or mission-critical durability guarantees. The tables below compare the five orchestrators across five dimensions. Each table is followed by a brief synthesis of the key takeaway.

### Architecture and Runtime Requirements

An orchestrator's architecture determines how developers define workflows and what deployment environments are available. The **Core Paradigm** column describes the fundamental execution model. The **Primary Languages** column lists languages with first-party, actively maintained SDKs.

| Orchestrator | Core Paradigm | Primary Languages | Deployment Options |
|---|---|---|---|
| **LangGraph** | Cyclic state machine | Python, TypeScript | Self-hosted, SaaS, VPC, Air-gapped |
| **CrewAI** | Role-based crew | Python | Self-hosted, SaaS, VPC |
| **Microsoft Agent Framework** | Actor model + graphs | C#/.NET, Python | Self-hosted, Azure managed |
| **OpenAI Agents SDK** | Handoff loop | Python, TypeScript | Self-hosted, Serverless |
| **Temporal** | Durable execution | Go, Java, Python, TS, .NET, PHP | Self-hosted, SaaS |

LangGraph and OpenAI Agents SDK offer both Python and TypeScript. Microsoft Agent Framework is the only option with first-class C#/.NET support. CrewAI is Python-only. Temporal provides the broadest language coverage with six official SDKs, reflecting its origins as general-purpose infrastructure rather than an AI-specific tool. On the deployment spectrum, all five can run self-hosted, but the managed hosting options differ significantly: LangGraph Platform offers cloud, hybrid, and fully air-gapped enterprise tiers; CrewAI AMP provides managed cloud with visual workflow editing; Microsoft Agent Framework integrates with Azure's managed services; OpenAI Agents SDK requires no special hosting (it runs in any standard Python or Node.js environment); and Temporal Cloud provides a fully managed cluster with consumption-based pricing.

### Core Capabilities

Beyond basic multi-agent coordination, orchestrators differ in how they handle state persistence, failure recovery, human interaction, and workflow topology. **Durable Execution** indicates whether the orchestrator can survive process crashes and resume from the last recorded state boundary. **HITL Depth** describes the architectural support for human-in-the-loop pause, inspection, and state mutation. **Workflow Topology** indicates what shapes of execution flow the orchestrator supports natively.

| Orchestrator | Durable Execution | HITL Depth | Workflow Topology | Built-In Memory | Streaming Modes |
|---|---|---|---|---|---|
| **LangGraph** | Superstep checkpointing | Advanced (`interrupt` + time-travel) | Arbitrary cyclic graphs | Checkpointer + Store | Multi-mode (tokens, state, node updates, events) |
| **CrewAI** | Flow-level state persistence | Moderate (before/after task hooks) | Role crews + decorator Flows | Multi-tier (short, long, entity) | Task + token streaming |
| **Microsoft Agent Framework** | Azure Durable Task integration | Advanced (actor events + approval gates) | Actor pub/sub + workflow graphs | Pluggable thread/state stores | Event + token streaming |
| **OpenAI Agents SDK** | Stateless loop (external persistence) | Basic (tool approval guardrails) | Handoff chains | Session history injection | Token + run-item events |
| **Temporal** | Deterministic event-sourcing replay | Advanced (durable `Signals` + `Updates`) | Arbitrary imperative code | Reconstructed workflow variables | Indirect (via external pub/sub or heartbeats) |

All five orchestrators support multi-agent coordination, but their underlying state machines differ structurally. LangGraph provides cyclic graph topologies with dynamic fan-out and superstep reducers. CrewAI trades low-level graph wiring for role-based crews composed inside decorator Flows. Microsoft Agent Framework combines decentralized actor messaging with deterministic workflow graphs. OpenAI Agents SDK focuses on lightweight handoff chains with parallel guardrail tripwires, whereas Temporal supports any control flow expressible in imperative code at the distributed systems layer.

Streaming and durability requirements quickly narrow the field. Most frameworks stream output tokens, whereas multi-mode event streaming allows frontends to render live state transitions, tool calls, and handoffs. For long-running pipelines that must survive server restarts without repeating expensive inference calls, LangGraph, Microsoft Agent Framework, and Temporal provide built-in state recovery, whereas CrewAI and OpenAI Agents SDK require external persistence wrappers.

### Pricing and LLM Support

All five orchestrators are open source under the MIT License and support a bring-your-own-key (BYOK) approach for model access. The differences lie in managed service pricing and the depth of multi-provider support.

| Orchestrator | Managed Service Pricing | LLM Provider Support |
|---|---|---|
| **LangGraph** | Free tier, developer usage tier, Enterprise | Model-agnostic |
| **CrewAI** | Free tier, Enterprise | Model-agnostic |
| **Microsoft Agent Framework** | Azure consumption-based | Model-agnostic |
| **OpenAI Agents SDK** | API usage costs | OpenAI native, others via LiteLLM adapter |
| **Temporal** | Cloud consumption-based | N/A (Infrastructure) |

LangGraph, CrewAI, and Microsoft Agent Framework are fully model-agnostic, supporting all major providers with comparable depth. OpenAI Agents SDK is optimized around OpenAI's Responses and tool-calling APIs; third-party models connect through a LiteLLM adapter layer, where schema translation differences can surface on provider-specific hosted tools. Temporal does not interact with models directly, since it operates as an infrastructure layer, so any model accessible from the programming language's SDK can be called inside a Temporal Activity. The pricing models reflect different monetization strategies: LangGraph and CrewAI charge for managed hosting and enterprise features, Microsoft charges through Azure consumption, OpenAI charges for API and hosted tool usage, and Temporal charges for managed cluster operations and action volume.

### Integration Points

All five orchestrators support the Model Context Protocol (MCP), enabling any of them to connect to MCP-compatible tool servers. The differentiators lie in how natively they support MCP, additional protocol support, and observability options.

| Orchestrator | MCP Integration | Additional Protocol Support | Native Observability |
|---|---|---|---|
| **LangGraph** | Yes (adapters) | None | LangSmith |
| **CrewAI** | Yes (native) | None | CrewAI AMP |
| **Microsoft Agent Framework** | Yes (native) | Agent-to-Agent (A2A) | Azure App Insights |
| **OpenAI Agents SDK** | Yes (hosted/native) | None | Built-in visualizer |
| **Temporal** | Indirect | None | Temporal Web UI |

Shared MCP support spans all five orchestrators, though their integration layers differ. CrewAI, Microsoft Agent Framework, and OpenAI Agents SDK provide built-in client classes to consume MCP servers directly. LangGraph connects through the `langchain-mcp-adapters` package. Temporal supports MCP indirectly: because it orchestrates infrastructure rather than AI primitives, developers instantiate standard MCP clients inside Temporal Activities. Beyond MCP, Microsoft Agent Framework is the only orchestrator with native Agent-to-Agent (`A2A`) protocol support for cross-framework agent discovery and delegation. On the observability side, each orchestrator pairs with a native trace UI alongside OpenTelemetry-compatible exporters that forward spans to third-party platforms such as Langfuse, Arize Phoenix, Datadog, or Jaeger.

### Strongest Use Cases and Known Limitations

Each orchestrator is optimized for a specific coordination pattern and carries trade-offs that make it less suitable for others.

| Orchestrator | Strongest Use Case | Known Limitation |
|---|---|---|
| **LangGraph** | Complex stateful workflows requiring cyclic execution, time-travel debugging, and fine-grained control | Steep learning curve: the Pregel BSP model and superstep semantics require a paradigm shift |
| **CrewAI** | Rapid prototyping of multi-agent teams where coordination maps to roles and delegation | High token consumption; risk of delegation loops; lacks granular execution control |
| **Microsoft Agent Framework** | Enterprise systems requiring multi-language support (C# and Python), Azure integration, and durable long-running workflows | Architectural learning curve (actor model); fragmented documentation across AutoGen and Semantic Kernel; Azure lock-in risks |
| **OpenAI Agents SDK** | Lightweight agent routing with built-in safety guardrails | Limited to handoff topologies; optimized primarily for OpenAI endpoints; no built-in durable execution |
| **Temporal** | Mission-critical workflows that must survive crashes, handle unreliable APIs, and provide audit trails | Operational overhead; strict determinism constraints on Workflow code |

Selecting an orchestrator comes down to two architectural axes: topology control and crash durability. Lightweight handoff loops (OpenAI Agents SDK) and role-based crews (CrewAI) minimize boilerplate for conversational routing and specialist delegation, whereas cyclic state graphs (LangGraph) and distributed actor runtimes (Microsoft Agent Framework) provide fine-grained state control and enterprise interoperability. These layers compose cleanly in production: teams frequently execute LangGraph state machines, CrewAI flows, or OpenAI agent loops inside Temporal Activities to pair AI-native reasoning patterns with infrastructure-grade event-sourcing durability.

## References

1. LangGraph Documentation, LangChain Inc.
2. CrewAI Documentation and GitHub Repository.
3. Microsoft Agent Framework Documentation on Microsoft Learn.
4. OpenAI Agents SDK Documentation and GitHub Repository.
5. Temporal Documentation, Temporal Technologies.
6. Model Context Protocol Specification, Linux Foundation Agentic AI.
7. Agent-to-Agent (A2A) Protocol Specification, Google.
