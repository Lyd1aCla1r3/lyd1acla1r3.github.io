import re

with open('architecture.html', 'r') as f:
    html = f.read()

with open('svgs.txt', 'r') as f:
    svgs_text = f.read()
svgs = re.split(r'=== SVG \d ===\n', svgs_text)[1:]
svg_ai = svgs[0].strip()
svg_conn = svgs[1].strip()
svg_phy = svgs[2].strip()

# We need to replace the entire CSS inside <style> for .arch-*
# And the entire <main> content.
# Since we have full control, let's just generate a fresh architecture.html from a template, parsing only the <nav> and header metadata.
# Actually, since we only change <main> and some <style>, we can regex replace carefully.

# First, remove the old arch-diagram, arch-intro, cv-hint, cv-text-stack, reset-btn, etc.
# We will just replace everything inside <div class="ks-container"> ... </div> inside <main>

container_start = html.find('<div class="ks-container">')
container_end = html.find('</main>')
if container_start == -1 or container_end == -1:
    print("Could not find <main> container")
    exit(1)

new_container = f"""<div class="ks-container">

      <header class="ks-page-header ks-reveal">
        <div class="ks-label" style="text-align: center;">Section 03 / Architecture</div>
        <h1 class="ks-page-header__title metallic-text" style="text-align: center; margin-bottom: 1.5rem;">How I see the role</h1>
      </header>

      <p class="arch-intro ks-reveal ks-reveal-delay-1">
        Two distinct domains define the modern engineering landscape. The computational workloads generating unprecedented bandwidth demand operate in tandem with the physical-layer standards validated by Keysight instrumentation. The solutions engineer operates precisely across this gap.
      </p>

      <section class="arch-layout ks-reveal ks-reveal-delay-2">
        
        <!-- Group 1: Workloads -->
        <div class="arch-group">
          <div class="arch-header-row">
            <div class="arch-card-bg arch-card-bg--ai">
              {svg_ai}
              <div class="arch-card-title arch-card-title--ai">Workloads</div>
            </div>
            <div class="cv-text-card cv-text-card--ai is-visible" style="opacity:1; transform:translateY(0); margin-bottom:0;">
              <p class="cv-text-card__body">My perspective centers on the structural bottlenecks created when algorithms distribute massive calculations across thousands of processors. Neural networks demand continuous memory access to evaluate context. This generates intense bandwidth demands. Training workloads force individual chips to synchronize their calculations and broadcast updated weights. This saturates network switches. Engineers must split massive models across multiple accelerators. This pushes the physical links between those units to their absolute limits.</p>
            </div>
          </div>
          <div class="arch-btn-row">
            <div class="arch-accordion arch-accordion--ai" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Context Retrieval (Attention)</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">Calculates focus weights across a sequence of data. Expanding context windows require massive, continuous data retrieval from local memory to sustain this operation.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--ai" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Gradient Synchronization</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">Distributed training processors must periodically pause, sum mathematical gradients, and broadcast updated weights. This collective operation generates instantaneous network traffic spikes.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--ai" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Pipeline Distribution</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">Slices a massive neural network into discrete layers across multiple processors. Extreme low-latency communication is mandatory to constantly exchange intermediate mathematical results.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--ai" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Expert Routing (MoE)</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">Conditionally activates only specific sub-networks per token calculation. This drastically increases compute efficiency but generates unpredictable, highly bursty memory access patterns.</div></div>
            </div>
          </div>
        </div>

        <!-- Group 2: Operational Impact -->
        <div class="arch-group">
          <div class="arch-header-row">
            <div class="arch-card-bg arch-card-bg--conn">
              {svg_conn}
              <div class="arch-card-title arch-card-title--conn">Operational Impact</div>
            </div>
            <div class="cv-text-card cv-text-card--conn is-visible" style="opacity:1; transform:translateY(0); margin-bottom:0;">
              <p class="cv-text-card__body">Strategic engineering requires understanding the foundational purpose behind technical specifications. A direct physical path exists between a computational software pattern and the electrical standard built to support it. Memory bandwidth deficits directly drive the adoption of new interconnect protocols. Network saturation necessitates higher capacity ethernet standards. Local memory limitations force the development of specialized communication links to bridge individual processors effectively.</p>
            </div>
          </div>
          <div class="arch-btn-row">
            <div class="arch-accordion arch-accordion--conn" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Memory Bandwidth</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">The volumetric rate at which a processor reads or stores data in local memory. Expensive processors sit idle waiting for data if a system lacks sufficient bandwidth.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--conn" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Network Saturation</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">Hardware queues or drops packets if the aggregate data traversing the network switches exceeds maximum routing capacity. Thousands of processors attempting simultaneous synchronization will instantly stall a poorly designed network.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--conn" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Direct Chip Links</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">Dedicated physical pathways connecting processors within a single server chassis. They bypass the slower host processor and network interface cards to facilitate low-latency exchanges.</div></div>
            </div>
          </div>
        </div>

        <!-- Group 3: PHY Standards -->
        <div class="arch-group">
          <div class="arch-header-row">
            <div class="arch-card-bg arch-card-bg--phy">
              {svg_phy}
              <div class="arch-card-title arch-card-title--phy">PHY Standards</div>
            </div>
            <div class="cv-text-card cv-text-card--phy is-visible" style="opacity:1; transform:translateY(0); margin-bottom:0;">
              <p class="cv-text-card__body">Fluency in electrical specifications is expected. Understanding the architectural drivers provides a distinct strategic advantage. Recognizing that coherent memory pooling necessitates CXL elevates the technical dialogue with customers. Understanding that distributed training requires high-speed Ethernet moves conversations beyond basic compliance. I map physical layer standards directly back to the software workloads that demand them.</p>
            </div>
          </div>
          <div class="arch-btn-row">
            <div class="arch-accordion arch-accordion--phy" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">CXL 3.0 / 3.1</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">An open standard allowing processors to share external memory pools dynamically. It provides a standardized physical layer to solve severe memory capacity constraints.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--phy" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">800G / 1.6T Ethernet</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">The latest generations of high-speed networking. Massive Ethernet architectures scale out networks across thousands of server racks to prevent saturation.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--phy" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">PCIe 6.0 / 7.0</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">The foundational electrical and protocol standard for peripheral communication. It dictates the base physical layer constraints for nearly all local system interconnects.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--phy" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">UALink</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">An open consortium specification governing direct chip-to-chip communication. It standardizes high-speed inter-accelerator links for distributed parallel computing.</div></div>
            </div>
            <div class="arch-accordion arch-accordion--phy" onclick="toggleAccordion(this)">
              <div class="arch-accordion__header">Linear Drive Optics (LPO)</div>
              <div class="arch-accordion__content"><div class="arch-accordion__inner">Removes digital signal processors from optical transceivers. This reduces power consumption and latency but places extreme analog equalization burdens directly on the host switch.</div></div>
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

html = html[:container_start] + new_container + "\n  " + html[container_end:]

# Now replace the <style> tag contents related to arch layout
# We will use regex to find the style tag block
# Alternatively, we can just replace everything between /* ── Layout ── */ and /* --- Reset Button --- */
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

    .arch-layout {
      display: flex;
      flex-direction: column;
      gap: 3rem;
      margin-bottom: var(--ks-space-xl);
    }
    .arch-group {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }
    .arch-header-row {
      display: grid;
      grid-template-columns: 1fr 2.5fr;
      gap: 1.5rem;
      align-items: stretch;
    }
    @media (max-width: 900px) {
      .arch-header-row {
        grid-template-columns: 1fr;
      }
    }
    .arch-card-bg {
      position: relative;
      border-radius: var(--ks-radius-lg);
      border: 1px solid var(--ks-border);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 140px;
    }
    .arch-card-bg--ai { background: var(--bg-ai-solid); border-color: rgba(192,136,104,0.3); }
    .arch-card-bg--conn { background: var(--bg-conn-solid); border-color: rgba(192,120,136,0.3); }
    .arch-card-bg--phy { background: var(--bg-phy-solid); border-color: rgba(183,110,121,0.3); }
    
    .arch-bg-graphic {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      opacity: 1.0;
      pointer-events: none;
    }

    .arch-card-title {
      z-index: 3;
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 20px;
      font-weight: 600;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      text-align: center;
      padding: 1rem;
    }
    .arch-card-title--ai { color: var(--color-peach); }
    .arch-card-title--conn { color: var(--color-blush); }
    .arch-card-title--phy { color: var(--color-dpink); }

    .cv-text-card {
      border-radius: 8px;
      border-left-width: 4px;
      border-left-style: solid;
      padding: 20px 24px;
      margin-bottom: 0 !important;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    
    .cv-text-card__title {
      font-family: 'JetBrains Mono', monospace;
      font-size: var(--ks-fs-section-label);
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 8px;
    }

    .cv-text-card__body {
      font-size: var(--ks-fs-small);
      color: var(--ks-text-secondary);
      line-height: 1.65;
      margin: 0;
    }
    
    .cv-text-card--ai { background: var(--grad-ai-solid); border-left-color: var(--color-peach); }
    .cv-text-card--ai .cv-text-card__title, .cv-text-card--ai .cv-text-card__body { color: var(--color-peach) !important; }
    
    .cv-text-card--conn { background: var(--grad-conn-solid); border-left-color: var(--color-blush); }
    .cv-text-card--conn .cv-text-card__title, .cv-text-card--conn .cv-text-card__body { color: var(--color-blush) !important; }
    
    .cv-text-card--phy { background: var(--grad-phy-solid); border-left-color: var(--color-dpink); }
    .cv-text-card--phy .cv-text-card__title, .cv-text-card--phy .cv-text-card__body { color: var(--color-dpink) !important; }

    .arch-btn-row {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 1rem;
    }
    @media (max-width: 900px) {
      .arch-btn-row {
        grid-template-columns: 1fr;
      }
    }

    /* Accordions */
    .arch-accordion {
      border: 1px solid;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.4s var(--ks-ease);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-self: start;
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
    }
    
    .arch-accordion--ai { background: var(--grad-ai-solid); border-color: rgba(192,136,104,0.4); color: var(--color-peach); }
    .arch-accordion--conn { background: var(--grad-conn-solid); border-color: rgba(192,120,136,0.4); color: var(--color-blush); }
    .arch-accordion--phy { background: var(--grad-phy-solid); border-color: rgba(166,93,108,0.4); color: var(--color-dpink); }
    
    .arch-accordion:hover {
      filter: brightness(1.05);
    }

    .arch-accordion__header {
      padding: 12px 16px;
      text-align: center;
      font-family: 'Outfit', sans-serif;
      font-size: 14px;
      font-weight: 500;
      letter-spacing: 0.02em;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 54px;
    }
    .arch-accordion__content {
      max-height: 0;
      opacity: 0;
      transition: max-height 0.4s var(--ks-ease), opacity 0.4s var(--ks-ease), padding 0.4s var(--ks-ease);
    }
    .arch-accordion.is-expanded .arch-accordion__content {
      max-height: 400px;
      opacity: 1;
      padding: 0 16px 16px 16px;
    }
    .arch-accordion__inner {
      font-size: 0.85rem;
      line-height: 1.5;
      border-top: 1px solid;
      padding-top: 12px;
    }
    .arch-accordion--ai .arch-accordion__inner { border-top-color: rgba(192,136,104,0.3); }
    .arch-accordion--conn .arch-accordion__inner { border-top-color: rgba(192,120,136,0.3); }
    .arch-accordion--phy .arch-accordion__inner { border-top-color: rgba(166,93,108,0.3); }

    """

html = html[:start_idx] + new_styles + html[end_idx:]

# Rewrite the JS script tag
js_start = html.find('<script>')
js_end = html.find('</script>', js_start) + len('</script>')
new_js = """<script>
    function toggleAccordion(element) {
      const isExpanded = element.classList.contains('is-expanded');
      
      // Optional: Collapse all other accordions in the same row
      // const row = element.parentElement;
      // const allAccordions = row.querySelectorAll('.arch-accordion');
      // allAccordions.forEach(acc => acc.classList.remove('is-expanded'));
      
      if (isExpanded) {
        element.classList.remove('is-expanded');
      } else {
        element.classList.add('is-expanded');
      }
    }
  </script>"""

html = html[:js_start] + new_js + html[js_end:]

with open('architecture.html', 'w') as f:
    f.write(html)
