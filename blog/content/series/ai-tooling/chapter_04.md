# Connectivity and Routing

<!-- SUMMARY: A detailed examination of the two protocol layers connecting AI applications to external services and model providers, covering the Model Context Protocol for standardized tool and data access, and AI gateways and routers for unified multi-provider traffic management. -->

The tools covered in previous posts do not operate in isolation. A coding agent needs connections to external data sources, and an orchestrator needs to route requests across multiple model providers. This post covers two protocol layers that solve these connectivity problems.

<style>
.eco-profile-panel {
    border: 1.5px solid rgba(183,110,121,0.18);
    border-radius: 10px;
    padding: 14px 22px 18px 22px;
    margin-bottom: 1.5rem;
    background: rgba(255,255,255,0.85);
    transition: border-color 0.3s ease, background 0.3s ease;
}
.eco-profile-panel .post-tab-content h3 {
    margin-top: 0 !important;
}
.eco-profile-panel .post-tab-content.active {
    padding-top: 0;
}
</style>

<script>
var _ecoGatewayColors = {
    'litellm':    { border: 'rgba(183,110,121,0.35)', bg: 'rgba(251,243,244,0.6)' },
    'portkey':    { border: 'rgba(192,120,136,0.35)', bg: 'rgba(251,241,243,0.6)' },
    'notdiamond': { border: 'rgba(192,136,104,0.35)', bg: 'rgba(251,244,239,0.6)' },
    'openrouter': { border: 'rgba(184,144,40,0.35)',  bg: 'rgba(252,247,236,0.6)' }
};

function _ecoBindPanel(panelId, colorMap) {
    var panel = document.getElementById(panelId);
    if (!panel) return;
    var btns = panel.parentElement.querySelectorAll('[data-tab]');
    btns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var key = this.getAttribute('data-tab');
            var colors = colorMap[key];
            if (colors && panel) {
                panel.style.borderColor = colors.border;
                panel.style.background = colors.bg;
            }
        });
    });
    var keys = Object.keys(colorMap);
    if (keys.length > 0) {
        var firstColors = colorMap[keys[0]];
        if (firstColors && panel) {
            panel.style.borderColor = firstColors.border;
            panel.style.background = firstColors.bg;
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    _ecoBindPanel('eco-gateway-panel', _ecoGatewayColors);
});
</script>

## Model Context Protocol (MCP)

Before MCP, connecting an AI tool to an external service required a custom integration for every client-service pair. Cursor needed its own GitHub integration, its own database connector, its own filesystem bridge. So did Copilot. So did Claude Code. So did every framework and orchestrator. If there were N AI clients and M external services, the ecosystem needed N×M custom integrations, each with its own authentication scheme, data format, and maintenance burden. Adding one new service meant writing N new integrations. Adding one new AI client meant writing M new integrations.

The Model Context Protocol, created by Anthropic and released as an open standard under the MIT License, solves this by defining a single interface between AI clients and external services. The analogy is USB: before USB, every device needed its own proprietary connector. USB standardized the plug, so any device works with any computer. MCP standardizes the protocol, so any MCP-compatible AI client can connect to any MCP-compatible server.

MCP defines three primitives. **Tools** are executable functions that a server exposes, such as creating a GitHub issue, running a database query, or writing a file. **Resources** provide structured or unstructured data that a server can serve on demand, such as the contents of a repository, a database schema, or a document. **Prompts** are reusable instruction templates that a server offers to guide specific workflows. The protocol uses JSON-RPC 2.0 for message framing, with two transport options. The first is local process communication over `stdio`: the "server" is simply a software script, like a Node.js or Python file, downloaded to the local machine, which the client application launches as a background subprocess. The second is remote communication over Streamable HTTP with Server-Sent Events, where the server software is hosted on a different machine across the network.

**Adoption** has been broad. On the client side, Claude Desktop, Claude Code, Cursor, GitHub Copilot, Windsurf, Cline, and Zed all implement MCP client runtimes. On the framework side, LangChain via `@langchain/mcp-adapters`, LlamaIndex, and LiteLLM consume MCP servers as modular tool providers. On the server side, the ecosystem includes reference implementations for common needs, including filesystem access, Git operations, web content fetching, and persistent memory via a knowledge graph, and vendor-maintained servers like the GitHub MCP server, which was the first major platform server to support remote deployment with OAuth 2.0 authentication.

**Registries** address the discovery and installation problem. Developers publish their MCP servers to central public catalogs, like Smithery, Glama, or PulseMCP, so others can discover them. Configurations are not automatically provisioned for every server in the catalog. Instead, a user browses the registry, selects a specific server they need, for example, a PostgreSQL connector, and triggers an installation. A tool like Smithery automates this step: it downloads the selected server code and writes a configuration file telling the user's specific AI client, like Claude Desktop, exactly how and where to launch that server on the local machine.

MCP is not without limitations. It currently struggles with both halves of security: authentication by verifying who is connecting and authorization by restricting what they can do. On the authentication side, the challenge applies to remote servers. The client software must authenticate with the remote server, but standards are still evolving; clients handle OAuth logins and stateful sessions inconsistently when connecting over the internet. On the authorization side, the protocol lacks fine-grained Role-Based Access Control (RBAC). For remote servers, developers can often mitigate this flaw by scoping the underlying API tokens, for example, by supplying a GitHub token restricted to read-only access. For local servers, the challenge is acute. When a local AI client launches a local MCP server, the server runs as a background process that inherits all of the user's broad operating system permissions. There is no built-in way to restrict the AI client to a safer subset of those permissions. If the server exposes a "delete_file" tool, the AI client can use it, because the underlying server process has the OS permission to delete files. There is no standard way to configure the server to say "allow this client to read files, but deny delete requests," creating exposure to prompt injection attacks where untrusted data could instruct the model to invoke destructive tools. Furthermore, exposing many MCP tools simultaneously injects large JSON schema definitions into the model's context window, increasing token costs and potentially degrading reasoning accuracy. Most `stdio` implementations spawn direct subprocesses without default isolation or resource containment.

## AI Gateways and Routers

When an application uses a single model provider, only OpenAI, or only Anthropic, the integration is straightforward: import the SDK, pass an API key, make calls. However, production systems rarely stay on one provider. Different models excel at different tasks, such as smaller models for classification and larger models for reasoning. Providers experience outages and rate limits. Pricing varies by an order of magnitude. A team that hardcodes a single provider's SDK into its application creates a coupling that makes provider switching, fallback routing, and cost optimization difficult.

AI gateways and routers sit between the application and multiple model providers, abstracting away provider-specific differences. While often grouped together, the terms "gateway" and "router" describe distinct layers of routing.

A **gateway** operates at the infrastructure layer, performing *operational routing*. It acts as a reverse proxy that routes traffic between identical or equivalent endpoints to ensure uptime and manage infrastructure constraints. For example, if an OpenAI endpoint hits a rate limit, the gateway automatically routes the next request to an Azure OpenAI fallback endpoint. Gateways also provide *multi-tenancy* through virtual API keys. Merely sharing a single provider API key across a company is a security and budgeting nightmare. Instead, the company stores its real provider keys securely in the gateway. The gateway then generates unique "virtual" API keys for each internal application, or tenant. In software, a tenant is a logical boundary rather than a physical one. These applications can be distributed across different servers or cloud environments. When an application makes a request over the network using its virtual key, the gateway authenticates the tenant, logs their specific usage, enforces team-specific budget caps, and swaps the virtual key for the real provider key before forwarding the request. This allows fifty different distributed teams to share one corporate provider account while remaining strictly isolated from each other.

A **router** operates at the semantic layer, performing *intelligence routing*. Instead of rule-based dispatch for uptime, a router uses machine learning meta-models to inspect the text of the prompt and determine which model is best suited to answer it. A simple factual question gets routed to a fast, inexpensive model. A complex reasoning task gets routed to a larger, more capable model.

In production, these tools compose. An application sends a request to a gateway, which consults a router to pick the best model for the prompt, and then the gateway executes the call.

<div data-tab-group="gateways">
  <div class="post-tabs">
    <button class="post-tab-btn active" data-tab="litellm">LiteLLM</button>
    <button class="post-tab-btn" data-tab="portkey">Portkey</button>
    <button class="post-tab-btn" data-tab="notdiamond">Not Diamond</button>
    <button class="post-tab-btn" data-tab="openrouter">OpenRouter</button>
  </div>

  <div class="eco-profile-panel" id="eco-gateway-panel">

  <div class="post-tab-content active" data-tab-content="litellm">
    <h3>LiteLLM</h3>
    <p><strong>Maker:</strong> BerriAI<br><strong>Type:</strong> Open-source gateway and proxy (MIT License)</p>
    <p>LiteLLM is the most widely adopted open-source AI gateway. It provides a unified OpenAI-compatible interface that translates requests to 100+ provider APIs, including OpenAI, Anthropic, AWS Bedrock, Google Vertex AI, Azure OpenAI, Ollama, Groq, Mistral, and others, with minimal latency overhead of around 8ms P95. The proxy handles operational traffic management, such as round-robin load balancing, automated retries, and fallback routing during outages, spend tracking with programmatic budget caps at the user, team, or virtual API key level, and input/output guardrail integration. Observability traces export to Langfuse, OpenTelemetry, Datadog, Prometheus, and other backends. LiteLLM integrates with LangChain, LlamaIndex, CrewAI, AutoGen, and Instructor as a drop-in model provider.</p>
    <p><em>Pricing: The core proxy and Python SDK are free and open-source. An enterprise tier offers advanced governance features with custom pricing.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="portkey">
    <h3>Portkey</h3>
    <p><strong>Maker:</strong> Portkey AI<br><strong>Type:</strong> Open-source gateway with control plane (MIT License core)</p>
    <p>Portkey bundles the operational proxy capabilities of a gateway with tooling that approaches an observability platform. Beyond standard load balancing, fallback routing, and retry logic, it adds a semantic caching engine that stores responses for vector-similar prompts, reducing redundant inference costs and latency when the same type of question recurs. In-path guardrails and privacy filters handle PII redaction and safety policy enforcement before requests reach the model provider. Portkey supports 1,600+ models across 30+ providers and centralized virtual API key management for credential isolation. It also provides real-time distributed request tracing. While standard tracing tracks how long a function takes to run inside a single application, distributed request tracing tracks a request as it crosses network boundaries, stitching together the timeline from the user's application, through the gateway, to the external provider, and back.</p>
    <p><em>Pricing: The open-source core is free to self-host. The managed cloud offers a free tier, transitioning to flat-rate monthly subscriptions for production and enterprise deployments.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="notdiamond">
    <h3>Not Diamond</h3>
    <p><strong>Maker:</strong> Not Diamond Inc.<br><strong>Type:</strong> Intelligent model router (proprietary)</p>
    <p>Not Diamond occupies a different architectural layer from LiteLLM and Portkey. Rather than proxying and normalizing API traffic for infrastructure reasons, it analyzes the semantic content and complexity of each prompt using predictive meta-models and dispatches the query to whichever model is predicted to perform best for that specific input. Users configure the router by defining explicit trade-offs between response quality, latency, and token cost. Organizations can also train custom routing models on their own evaluation data, teaching the router how to optimize dispatch for their specific domain. Not Diamond provides specialized routing for multi-step agent trajectories and coding workflows. SDKs are available in Python and TypeScript, with integrations for LangChain and LlamaIndex.</p>
    <p><em>Pricing: Uses consumption-based billing per million tokens routed, along with a free tier for initial testing.</em></p>
  </div>

  <div class="post-tab-content" data-tab-content="openrouter">
    <h3>OpenRouter</h3>
    <p><strong>Maker:</strong> OpenRouter Inc., acquired by Stripe in August 2026<br><strong>Type:</strong> Model marketplace and API aggregator (proprietary)</p>
    <p>OpenRouter is a managed marketplace. It provides access to 500+ models from 60+ providers through a single API key and billing account, eliminating the need to maintain individual vendor contracts, credit minimums, and separate billing for each provider. For open-weight models hosted by multiple providers, such as Llama or Mistral, OpenRouter performs automatic provider-level arbitrage, routing requests to whichever host offers the lowest price at that moment. The API is OpenAI-compatible and supports structured outputs, such as JSON schema, tool/function calling, and multimodal inputs. A free model catalog provides rate-limited access to select open-source models for testing. OpenRouter integrates with Cursor, Continue.dev, Aider, LangChain, LlamaIndex, and any OpenAI SDK client via <code>base_url</code> reconfiguration.</p>
    <p><em>Pricing: Users pay the underlying provider's consumption rate plus a percentage-based transaction fee on credit purchases.</em></p>
  </div>

  </div>
</div>

The next post covers data infrastructure. It examines vector databases for storing and retrieving semantic context alongside knowledge management pipelines for preparing raw documents.

## References

1. Model Context Protocol Specification, Anthropic.
2. GitHub MCP Server, GitHub.
3. Smithery MCP Registry, Smithery AI.
4. LiteLLM Documentation, BerriAI.
5. Portkey Documentation, Portkey AI.
6. Not Diamond Documentation, Not Diamond Inc.
7. OpenRouter Documentation, OpenRouter Inc.
