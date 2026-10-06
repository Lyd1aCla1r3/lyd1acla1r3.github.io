import re

with open('architecture.html', 'r') as f:
    html = f.read()

# Load SVGs
with open('svgs.txt', 'r') as f:
    svgs_text = f.read()
svg_blocks = re.split(r'=== SVG \d ===\n', svgs_text)[1:]
svg_ai = svg_blocks[0].strip()
svg_conn = svg_blocks[1].strip()
svg_phy = svg_blocks[2].strip()

new_container = f"""<div class="ks-container">

      <header class="ks-page-header ks-reveal">
        <div class="ks-label" style="text-align: center;">Section 03 / Architecture</div>
        <h1 class="ks-page-header__title metallic-text" style="text-align: center; margin-bottom: 1.5rem;">How I see the role</h1>
      </header>

      <p class="arch-intro ks-reveal ks-reveal-delay-1">
        Two distinct domains define the modern engineering landscape. The computational workloads generating unprecedented bandwidth demand operate in tandem with the physical-layer standards validated by Keysight instrumentation. The solutions engineer operates precisely across this gap.
      </p>

      <section class="arch-layout ks-reveal ks-reveal-delay-2">
        
        <!-- Group 1: Workloads (Pink) -->
        <div class="arch-super-group ks-color--pink">
          <div class="arch-top-row">
            <div class="arch-image-card">
              {svg_ai}
              <div class="arch-card-title">Workloads</div>
            </div>
            <div class="arch-cv-card">
              <p class="cv-text-card__body">My perspective centers on the structural bottlenecks created when algorithms distribute massive calculations across thousands of processors. Neural networks demand continuous memory access to evaluate context. This generates intense bandwidth demands. Training workloads force individual chips to synchronize their calculations and broadcast updated weights. This saturates network switches. Engineers must split massive models across multiple accelerators. This pushes the physical links between those units to their absolute limits.</p>
            </div>
          </div>
          
          <div class="arch-tab-container">
            <div class="arch-tab-row">
              <button class="arch-tab ks-color--gold is-active" onclick="selectTab(this, 'Context Retrieval (Attention)', 'Calculates focus weights across a sequence of data. Expanding context windows require massive, continuous data retrieval from local memory to sustain this operation.')">
                <span class="tab-text">Context Retrieval</span><span class="tab-num">01</span>
              </button>
              <button class="arch-tab ks-color--peach" onclick="selectTab(this, 'Gradient Synchronization', 'Distributed training processors must periodically pause, sum mathematical gradients, and broadcast updated weights. This collective operation generates instantaneous network traffic spikes.')">
                <span class="tab-text">Gradient Sync</span><span class="tab-num">02</span>
              </button>
              <button class="arch-tab ks-color--blush" onclick="selectTab(this, 'Pipeline Distribution', 'Slices a massive neural network into discrete layers across multiple processors. Extreme low-latency communication is mandatory to constantly exchange intermediate mathematical results.')">
                <span class="tab-text">Pipeline Dist</span><span class="tab-num">03</span>
              </button>
              <button class="arch-tab ks-color--rose" onclick="selectTab(this, 'Expert Routing (MoE)', 'Conditionally activates only specific sub-networks per token calculation. This drastically increases compute efficiency but generates unpredictable, highly bursty memory access patterns.')">
                <span class="tab-text">Expert Routing</span><span class="tab-num">04</span>
              </button>
            </div>
            <div class="arch-tab-content ks-color--gold">
              <h3 class="arch-tab-content__title">Context Retrieval (Attention)</h3>
              <p class="arch-tab-content__desc">Calculates focus weights across a sequence of data. Expanding context windows require massive, continuous data retrieval from local memory to sustain this operation.</p>
            </div>
          </div>
        </div>

        <!-- Group 2: Operational Impact (Rose) -->
        <div class="arch-super-group ks-color--rose">
          <div class="arch-top-row">
            <div class="arch-image-card">
              {svg_conn}
              <div class="arch-card-title">Operational Impact</div>
            </div>
            <div class="arch-cv-card">
              <p class="cv-text-card__body">Strategic engineering requires understanding the foundational purpose behind technical specifications. A direct physical path exists between a computational software pattern and the electrical standard built to support it. Memory bandwidth deficits directly drive the adoption of new interconnect protocols. Network saturation necessitates higher capacity ethernet standards. Local memory limitations force the development of specialized communication links to bridge individual processors effectively.</p>
            </div>
          </div>
          
          <div class="arch-tab-container">
            <div class="arch-tab-row">
              <button class="arch-tab ks-color--dpink is-active" onclick="selectTab(this, 'Memory Bandwidth', 'The volumetric rate at which a processor reads or stores data in local memory. Expensive processors sit idle waiting for data if a system lacks sufficient bandwidth.')">
                <span class="tab-text">Memory Bandwidth</span><span class="tab-num">01</span>
              </button>
              <button class="arch-tab ks-color--pink" onclick="selectTab(this, 'Network Saturation', 'Hardware queues or drops packets if the aggregate data traversing the network switches exceeds maximum routing capacity. Thousands of processors attempting simultaneous synchronization will instantly stall a poorly designed network.')">
                <span class="tab-text">Network Saturation</span><span class="tab-num">02</span>
              </button>
              <button class="arch-tab ks-color--gold" onclick="selectTab(this, 'Direct Chip Links', 'Dedicated physical pathways connecting processors within a single server chassis. They bypass the slower host processor and network interface cards to facilitate low-latency exchanges.')">
                <span class="tab-text">Direct Chip Links</span><span class="tab-num">03</span>
              </button>
            </div>
            <div class="arch-tab-content ks-color--dpink">
              <h3 class="arch-tab-content__title">Memory Bandwidth</h3>
              <p class="arch-tab-content__desc">The volumetric rate at which a processor reads or stores data in local memory. Expensive processors sit idle waiting for data if a system lacks sufficient bandwidth.</p>
            </div>
          </div>
        </div>

        <!-- Group 3: PHY Standards (Dark Pink) -->
        <div class="arch-super-group ks-color--dpink">
          <div class="arch-top-row">
            <div class="arch-image-card">
              {svg_phy}
              <div class="arch-card-title">PHY Standards</div>
            </div>
            <div class="arch-cv-card">
              <p class="cv-text-card__body">Fluency in electrical specifications is expected. Understanding the architectural drivers provides a distinct strategic advantage. Recognizing that coherent memory pooling necessitates CXL elevates the technical dialogue with customers. Understanding that distributed training requires high-speed Ethernet moves conversations beyond basic compliance. I map physical layer standards directly back to the software workloads that demand them.</p>
            </div>
          </div>
          
          <div class="arch-tab-container">
            <div class="arch-tab-row">
              <button class="arch-tab ks-color--peach is-active" onclick="selectTab(this, 'CXL 3.0 / 3.1', 'An open standard allowing processors to share external memory pools dynamically. It provides a standardized physical layer to solve severe memory capacity constraints.')">
                <span class="tab-text">CXL 3.0 / 3.1</span><span class="tab-num">01</span>
              </button>
              <button class="arch-tab ks-color--blush" onclick="selectTab(this, '800G / 1.6T Ethernet', 'The latest generations of high-speed networking. Massive Ethernet architectures scale out networks across thousands of server racks to prevent saturation.')">
                <span class="tab-text">800G / 1.6T</span><span class="tab-num">02</span>
              </button>
              <button class="arch-tab ks-color--pink" onclick="selectTab(this, 'PCIe 6.0 / 7.0', 'The foundational electrical and protocol standard for peripheral communication. It dictates the base physical layer constraints for nearly all local system interconnects.')">
                <span class="tab-text">PCIe 6.0 / 7.0</span><span class="tab-num">03</span>
              </button>
              <button class="arch-tab ks-color--rose" onclick="selectTab(this, 'UALink', 'An open consortium specification governing direct chip-to-chip communication. It standardizes high-speed inter-accelerator links for distributed parallel computing.')">
                <span class="tab-text">UALink</span><span class="tab-num">04</span>
              </button>
              <button class="arch-tab ks-color--gold" onclick="selectTab(this, 'Linear Drive Optics (LPO)', 'Removes digital signal processors from optical transceivers. This reduces power consumption and latency but places extreme analog equalization burdens directly on the host switch.')">
                <span class="tab-text">LPO</span><span class="tab-num">05</span>
              </button>
            </div>
            <div class="arch-tab-content ks-color--peach">
              <h3 class="arch-tab-content__title">CXL 3.0 / 3.1</h3>
              <p class="arch-tab-content__desc">An open standard allowing processors to share external memory pools dynamically. It provides a standardized physical layer to solve severe memory capacity constraints.</p>
            </div>
          </div>
        </div>

      </section>

      <div style="text-align: center; margin: 4rem 0 2rem; display: flex; justify-content: center; gap: 1rem;">
        <a href="standards.html" target="_blank" class="ks-translate-btn ks-reveal" style="text-decoration: none;"><span class="metallic-text">View Standards Grid &#8599;</span></a>
      </div>

      <!-- Bottom Navigation -->
      <nav class="ks-bottom-nav ks-reveal ks-reveal-delay-3" aria-label="Section navigation">
        <a href="customer.html" class="ks-bottom-nav__link metallic-text">&larr; I Have Been the Customer</a>
        <a href="translation.html" class="ks-bottom-nav__link metallic-text">Translation &rarr;</a>
      </nav>

    </div>
"""

container_start = html.find('<div class="ks-container">')
container_end = html.find('</main>')
html = html[:container_start] + new_container + "\n  " + html[container_end:]

# Update CSS
style_start_marker = "/* ── Layout ── */"
style_end_marker = "/* --- Reset Button --- */"
start_idx = html.find(style_start_marker)
end_idx = html.find(style_end_marker)

new_styles = """/* ── Layout ── */
    .arch-intro {
      max-width: 800px;
      margin: 0 auto var(--ks-space-xl);
      text-align: center;
      font-size: var(--ks-fs-small);
      color: var(--ks-text-secondary);
    }

    /* Solid colors for clean tab UI */
    .ks-color--gold { --c-light: #fbf7ef; --c-dark: #f8ecd0; --c-text: #9c7820; --c-border: rgba(184,144,40,0.35); }
    .ks-color--peach { --c-light: #fcf6f2; --c-dark: #f6e4d8; --c-text: #a66d4b; --c-border: rgba(192,136,104,0.35); }
    .ks-color--blush { --c-light: #fbf4f5; --c-dark: #f5e1e3; --c-text: #b87a80; --c-border: rgba(184,122,128,0.35); }
    .ks-color--pink { --c-light: #fcf4f6; --c-dark: #f6dde2; --c-text: #c07888; --c-border: rgba(192,120,136,0.35); }
    .ks-color--rose { --c-light: #faeef0; --c-dark: #f4e0e3; --c-text: #b76e79; --c-border: rgba(183,110,121,0.35); }
    .ks-color--dpink { --c-light: #f7e8ea; --c-dark: #f2d1d6; --c-text: #a65d6c; --c-border: rgba(166,93,108,0.35); }

    .arch-layout {
      display: flex;
      flex-direction: column;
      gap: 3rem;
      margin-bottom: var(--ks-space-xl);
    }

    .arch-super-group {
      background: var(--c-dark);
      border-radius: 16px;
      padding: 1.5rem;
      transition: all 0.3s ease;
    }

    .arch-top-row {
      display: grid;
      grid-template-columns: 1fr 2.5fr;
      gap: 1.5rem;
      margin-bottom: 2.5rem;
      align-items: stretch;
    }

    @media (max-width: 900px) {
      .arch-top-row { grid-template-columns: 1fr; }
    }

    .arch-image-card {
      background: var(--c-light);
      border: 1px solid var(--c-border);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
      min-height: 160px;
    }

    .arch-bg-graphic {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      opacity: 0.8;
      pointer-events: none;
    }

    .arch-card-title {
      z-index: 2;
      position: relative;
      color: var(--c-text);
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      text-align: center;
    }

    .arch-cv-card {
      background: linear-gradient(135deg, rgba(242,209,214,0.6), rgba(248,236,208,0.6), rgba(244,224,227,0.6), rgba(246,228,216,0.6), rgba(246,221,226,0.6), rgba(245,225,227,0.6));
      border: 1px solid rgba(183,110,121,0.25);
      border-radius: 12px;
      padding: 1.5rem 2rem;
      display: flex;
      align-items: center;
    }

    .cv-text-card__body {
      font-size: var(--ks-fs-small);
      color: var(--ks-text-primary);
      line-height: 1.65;
      margin: 0;
    }

    /* Folder Tabs */
    .arch-tab-container {
      position: relative;
    }

    .arch-tab-row {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 0.5rem;
      margin-bottom: -1px; /* overlap border */
      position: relative;
      z-index: 2;
    }

    @media (max-width: 900px) {
      .arch-tab-row { grid-template-columns: 1fr; margin-bottom: 0; gap: 0.5rem; }
      .arch-tab { border-radius: 8px !important; margin-bottom: 0 !important; }
      .arch-tab.is-active { border-bottom-color: var(--c-border) !important; padding-bottom: 12px !important; }
    }

    .arch-tab {
      background: var(--c-light);
      border: 1px solid var(--c-border);
      border-radius: 12px 12px 0 0;
      padding: 12px 16px;
      cursor: pointer;
      
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 16px;
      font-weight: 500;
      color: var(--c-text);
      
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      
      transition: background 0.2s, font-weight 0.2s, color 0.2s;
    }

    .arch-tab:not(.is-active):hover {
      background: var(--c-dark);
    }

    .arch-tab.is-active {
      background: var(--c-light);
      border-bottom-color: var(--c-light);
      font-weight: 700;
      z-index: 3;
      padding-bottom: 13px; /* 12px padding + 1px border override */
    }

    .tab-text {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .tab-num {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 500;
      opacity: 0.8;
      flex-shrink: 0;
    }

    .arch-tab-content {
      background: var(--c-light);
      border: 1px solid var(--c-border);
      border-radius: 12px;
      padding: 2rem;
      position: relative;
      z-index: 1;
      
      /* Subtle inset shadow to emphasize depth */
      box-shadow: inset 0 2px 10px rgba(0,0,0,0.015);
    }

    .arch-tab-content__title {
      color: var(--c-text);
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 0.75rem;
    }

    .arch-tab-content__desc {
      color: var(--ks-text-primary);
      font-size: 17px;
      line-height: 1.6;
      margin: 0;
    }

    """

html = html[:start_idx] + new_styles + html[end_idx:]

# JS
js_start = html.find('<script>')
js_end = html.find('</script>', js_start) + len('</script>')

new_js = """<script>
    function selectTab(btn, title, desc) {
      const container = btn.closest('.arch-tab-container');
      const allTabs = container.querySelectorAll('.arch-tab');
      const contentBox = container.querySelector('.arch-tab-content');
      
      // If clicking the active tab, do nothing (tabs don't collapse fully)
      if (btn.classList.contains('is-active')) return;
      
      // Remove active state
      allTabs.forEach(t => t.classList.remove('is-active'));
      
      // Set active
      btn.classList.add('is-active');
      
      // Update content
      contentBox.querySelector('.arch-tab-content__title').textContent = title;
      contentBox.querySelector('.arch-tab-content__desc').textContent = desc;
      
      // Update content box color
      const colorClass = Array.from(btn.classList).find(c => c.startsWith('ks-color--'));
      contentBox.className = 'arch-tab-content';
      if (colorClass) {
        contentBox.classList.add(colorClass);
      }
    }
  </script>"""

html = html[:js_start] + new_js + html[js_end:]

with open('architecture.html', 'w') as f:
    f.write(html)
