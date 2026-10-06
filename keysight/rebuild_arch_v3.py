import re

# Read original
with open('architecture.html', 'r') as f:
    html = f.read()

# Load SVGs
with open('svgs.txt', 'r') as f:
    svgs_text = f.read()
svg_blocks = re.split(r'=== SVG \d ===\n', svgs_text)[1:]
svg_ai = svg_blocks[0].strip()
svg_conn = svg_blocks[1].strip()
svg_phy = svg_blocks[2].strip()

# New Main Container
new_container = f"""<div class="ks-container">

      <header class="ks-page-header ks-reveal">
        <div class="ks-label" style="text-align: center;">Section 03 / Architecture</div>
        <h1 class="ks-page-header__title metallic-text" style="text-align: center; margin-bottom: 1.5rem;">How I see the role</h1>
      </header>

      <p class="arch-intro ks-reveal ks-reveal-delay-1">
        Two distinct domains define the modern engineering landscape. The computational workloads generating unprecedented bandwidth demand operate in tandem with the physical-layer standards validated by Keysight instrumentation. The solutions engineer operates precisely across this gap.
      </p>

      <section class="arch-layout ks-reveal ks-reveal-delay-2">
        
        <!-- Group 1: Workloads (Color Pair: Pink) -->
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
          
          <div class="arch-button-row">
            <button class="arch-btn ks-color--gold" data-desc="Calculates focus weights across a sequence of data. Expanding context windows require massive, continuous data retrieval from local memory to sustain this operation." onclick="selectButton(this, 'Context Retrieval (Attention)', 'WORKLOADS')">Context Retrieval (Attention)</button>
            <button class="arch-btn ks-color--peach" data-desc="Distributed training processors must periodically pause, sum mathematical gradients, and broadcast updated weights. This collective operation generates instantaneous network traffic spikes." onclick="selectButton(this, 'Gradient Synchronization', 'WORKLOADS')">Gradient Synchronization</button>
            <button class="arch-btn ks-color--blush" data-desc="Slices a massive neural network into discrete layers across multiple processors. Extreme low-latency communication is mandatory to constantly exchange intermediate mathematical results." onclick="selectButton(this, 'Pipeline Distribution', 'WORKLOADS')">Pipeline Distribution</button>
            <button class="arch-btn ks-color--rose" data-desc="Conditionally activates only specific sub-networks per token calculation. This drastically increases compute efficiency but generates unpredictable, highly bursty memory access patterns." onclick="selectButton(this, 'Expert Routing (MoE)', 'WORKLOADS')">Expert Routing (MoE)</button>
          </div>
          
          <div class="arch-full-card" style="display: none;">
            <h3 class="arch-full-card__title"></h3>
            <div class="arch-full-card__subtitle"></div>
            <p class="arch-full-card__desc"></p>
          </div>
        </div>

        <!-- Group 2: Operational Impact (Color Pair: Rose) -->
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
          
          <div class="arch-button-row">
            <button class="arch-btn ks-color--dpink" data-desc="The volumetric rate at which a processor reads or stores data in local memory. Expensive processors sit idle waiting for data if a system lacks sufficient bandwidth." onclick="selectButton(this, 'Memory Bandwidth', 'OPERATIONAL IMPACT')">Memory Bandwidth</button>
            <button class="arch-btn ks-color--pink" data-desc="Hardware queues or drops packets if the aggregate data traversing the network switches exceeds maximum routing capacity. Thousands of processors attempting simultaneous synchronization will instantly stall a poorly designed network." onclick="selectButton(this, 'Network Saturation', 'OPERATIONAL IMPACT')">Network Saturation</button>
            <button class="arch-btn ks-color--gold" data-desc="Dedicated physical pathways connecting processors within a single server chassis. They bypass the slower host processor and network interface cards to facilitate low-latency exchanges." onclick="selectButton(this, 'Direct Chip Links', 'OPERATIONAL IMPACT')">Direct Chip Links</button>
          </div>
          
          <div class="arch-full-card" style="display: none;">
            <h3 class="arch-full-card__title"></h3>
            <div class="arch-full-card__subtitle"></div>
            <p class="arch-full-card__desc"></p>
          </div>
        </div>

        <!-- Group 3: PHY Standards (Color Pair: Dark Pink) -->
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
          
          <div class="arch-button-row">
            <button class="arch-btn ks-color--peach" data-desc="An open standard allowing processors to share external memory pools dynamically. It provides a standardized physical layer to solve severe memory capacity constraints." onclick="selectButton(this, 'CXL 3.0 / 3.1', 'PHY STANDARDS')">CXL 3.0 / 3.1</button>
            <button class="arch-btn ks-color--blush" data-desc="The latest generations of high-speed networking. Massive Ethernet architectures scale out networks across thousands of server racks to prevent saturation." onclick="selectButton(this, '800G / 1.6T Ethernet', 'PHY STANDARDS')">800G / 1.6T Ethernet</button>
            <button class="arch-btn ks-color--pink" data-desc="The foundational electrical and protocol standard for peripheral communication. It dictates the base physical layer constraints for nearly all local system interconnects." onclick="selectButton(this, 'PCIe 6.0 / 7.0', 'PHY STANDARDS')">PCIe 6.0 / 7.0</button>
            <button class="arch-btn ks-color--rose" data-desc="An open consortium specification governing direct chip-to-chip communication. It standardizes high-speed inter-accelerator links for distributed parallel computing." onclick="selectButton(this, 'UALink', 'PHY STANDARDS')">UALink</button>
            <button class="arch-btn ks-color--gold" data-desc="Removes digital signal processors from optical transceivers. This reduces power consumption and latency but places extreme analog equalization burdens directly on the host switch." onclick="selectButton(this, 'Linear Drive Optics (LPO)', 'PHY STANDARDS')">Linear Drive Optics (LPO)</button>
          </div>
          
          <div class="arch-full-card" style="display: none;">
            <h3 class="arch-full-card__title"></h3>
            <div class="arch-full-card__subtitle"></div>
            <p class="arch-full-card__desc"></p>
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

# Extract the body parts
container_start = html.find('<div class="ks-container">')
container_end = html.find('</main>')
if container_start == -1 or container_end == -1:
    print("Could not find <main> container")
    exit(1)

html = html[:container_start] + new_container + "\n  " + html[container_end:]

# CSS Updates
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

    /* Color Classes */
    .ks-color--gold {
      --c-light: linear-gradient(rgba(184,144,40,0.06), rgba(184,144,40,0.06)), rgba(255,255,255,0.55);
      --c-dark: #f8ecd0;
      --c-text: #9c7820;
      --c-border: rgba(184,144,40,0.35);
    }
    .ks-color--peach {
      --c-light: linear-gradient(rgba(192,136,104,0.06), rgba(192,136,104,0.06)), rgba(255,255,255,0.55);
      --c-dark: #f6e4d8;
      --c-text: #a66d4b;
      --c-border: rgba(192,136,104,0.35);
    }
    .ks-color--blush {
      --c-light: linear-gradient(rgba(184,122,128,0.06), rgba(184,122,128,0.06)), rgba(255,255,255,0.55);
      --c-dark: #f5e1e3;
      --c-text: #b87a80;
      --c-border: rgba(184,122,128,0.35);
    }
    .ks-color--pink {
      --c-light: linear-gradient(rgba(192,120,136,0.06), rgba(192,120,136,0.06)), rgba(255,255,255,0.55);
      --c-dark: #f6dde2;
      --c-text: #c07888;
      --c-border: rgba(192,120,136,0.35);
    }
    .ks-color--rose {
      --c-light: linear-gradient(rgba(183,110,121,0.06), rgba(183,110,121,0.06)), rgba(255,255,255,0.55);
      --c-dark: #f4e0e3;
      --c-text: #b76e79;
      --c-border: rgba(183,110,121,0.35);
    }
    .ks-color--dpink {
      --c-light: linear-gradient(rgba(166,93,108,0.06), rgba(166,93,108,0.06)), rgba(255,255,255,0.55);
      --c-dark: #f2d1d6;
      --c-text: #a65d6c;
      --c-border: rgba(166,93,108,0.35);
    }

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
      margin-bottom: 1.5rem;
      align-items: stretch;
    }

    @media (max-width: 900px) {
      .arch-top-row {
        grid-template-columns: 1fr;
      }
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
      background: linear-gradient(135deg, rgba(242,209,214,0.4), rgba(248,236,208,0.4), rgba(244,224,227,0.4), rgba(246,228,216,0.4), rgba(246,221,226,0.4), rgba(245,225,227,0.4));
      border: 1px solid rgba(183,110,121,0.2);
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

    .arch-button-row {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
    }

    .arch-btn {
      background: var(--c-light);
      border: 1px solid var(--c-border);
      color: var(--c-text);
      padding: 12px 20px;
      border-radius: 8px;
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.3s var(--ks-ease);
    }

    .arch-btn:hover {
      background: var(--c-dark);
    }

    .arch-btn.is-selected {
      background: var(--c-dark);
      font-weight: 600;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.03);
    }

    .arch-full-card {
      background: var(--c-light);
      border: 1px solid var(--c-border);
      border-radius: 12px;
      padding: 1.5rem 2rem;
      margin-top: 1rem;
      animation: slideDown 0.4s var(--ks-ease) forwards;
    }

    @keyframes slideDown {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .arch-full-card__title {
      color: var(--c-text);
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 0.25rem;
    }

    .arch-full-card__subtitle {
      color: var(--c-text);
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      margin-bottom: 1rem;
      opacity: 0.85;
    }

    .arch-full-card__desc {
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
    function selectButton(btn, title, subtitle) {
      const superGroup = btn.closest('.arch-super-group');
      const allButtons = superGroup.querySelectorAll('.arch-btn');
      const fullCard = superGroup.querySelector('.arch-full-card');
      const desc = btn.getAttribute('data-desc');
      
      const isAlreadySelected = btn.classList.contains('is-selected');
      
      // Deselect all
      allButtons.forEach(b => b.classList.remove('is-selected'));
      
      if (isAlreadySelected) {
        // Toggle off
        fullCard.style.display = 'none';
        return;
      }
      
      // Select clicked
      btn.classList.add('is-selected');
      
      // Update full card content
      superGroup.querySelector('.arch-full-card__title').textContent = title;
      superGroup.querySelector('.arch-full-card__subtitle').textContent = subtitle + ' ZONE';
      superGroup.querySelector('.arch-full-card__desc').textContent = desc;
      
      // Find the color class of the button to apply to the card
      const colorClass = Array.from(btn.classList).find(c => c.startsWith('ks-color--'));
      
      // Remove any existing color class from fullCard
      fullCard.className = 'arch-full-card';
      if (colorClass) {
        fullCard.classList.add(colorClass);
      }
      
      // Show card
      fullCard.style.display = 'block';
    }
  </script>"""

html = html[:js_start] + new_js + html[js_end:]

with open('architecture.html', 'w') as f:
    f.write(html)
