import re

with open('architecture.html', 'r') as f:
    html = f.read()

# 1. Update CSS
css_updates = [
    (r"\.arch-card-content \{[\s\S]*?pointer-events: none; /\* Let clicks pass to bg \*/[\s\S]*?\}",
     lambda m: m.group(0).replace("pointer-events: none; /* Let clicks pass to bg */", "/* pointer-events removed */")),
    (r"\.arch-btn \{[\s\S]*?pointer-events: none;[\s\S]*?\}",
     lambda m: m.group(0).replace("pointer-events: none;", "cursor: pointer;")),
]
for p, r in css_updates:
    html = re.sub(p, r, html)

# Add CSS for callout
callout_css = """
    .arch-callout {
      margin-top: -1rem;
      margin-bottom: 0.5rem;
      padding: 1rem;
      border-radius: 8px;
      font-size: 0.9rem;
      line-height: 1.5;
      animation: fadeInDown 0.3s ease forwards;
    }
    @keyframes fadeInDown {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .arch-callout--ai {
      background: var(--grad-ai-solid);
      color: var(--color-peach);
      border: 1px solid rgba(192,136,104,0.3);
    }
    .arch-callout--conn {
      background: var(--grad-conn-solid);
      color: var(--color-blush);
      border: 1px solid rgba(192,120,136,0.3);
    }
    .arch-callout--phy {
      background: var(--grad-phy-solid);
      color: var(--color-dpink);
      border: 1px solid rgba(166,93,108,0.3);
    }
"""
html = html.replace("/* --- Reset Button --- */", callout_css + "\n    /* --- Reset Button --- */")

# 2. Update Column Titles
html = html.replace('<div class="arch-title-wrapper arch-title--ai arch-trigger" data-step="0">AI Compute</div>',
                    '<div class="arch-title-wrapper arch-title--ai">Workloads</div>')
html = html.replace('<div class="arch-title-wrapper arch-title--conn arch-trigger" data-step="1">The Connection</div>',
                    '<div class="arch-title-wrapper arch-title--conn">Bridges</div>')
html = html.replace('<div class="arch-title-wrapper arch-title--phy arch-trigger" data-step="2">Physical Layer</div>',
                    '<div class="arch-title-wrapper arch-title--phy">Physical Layer</div>')

# 3. Strip trigger classes from backgrounds
html = re.sub(r'class="arch-card-bg (arch-card-bg--\w+) arch-trigger" data-step="\d+" role="button" tabindex="0" aria-label="[^"]+"',
              r'class="arch-card-bg \1"', html)

# 4. Replace buttons content
ai_buttons = """
          <div class="arch-btn arch-btn--ai" data-desc="Calculates focus weights across a sequence of data. Expanding context windows require massive, continuous data retrieval from local memory to sustain this operation.">Context Retrieval (Attention)</div>
          <div class="arch-btn arch-btn--ai" data-desc="Distributed training processors must periodically pause, sum mathematical gradients, and broadcast updated weights. This collective operation generates instantaneous network traffic spikes.">Gradient Synchronization</div>
          <div class="arch-btn arch-btn--ai" data-desc="Slices a massive neural network into discrete layers across multiple processors. Extreme low-latency communication is mandatory to constantly exchange intermediate mathematical results.">Pipeline Distribution</div>
          <div class="arch-btn arch-btn--ai" data-desc="Conditionally activates only specific sub-networks per token calculation. This drastically increases compute efficiency but generates unpredictable, highly bursty memory access patterns.">Expert Routing (MoE)</div>
"""
conn_buttons = """
          <div class="arch-btn arch-btn--conn" data-desc="The volumetric rate at which a processor reads or stores data in local memory. Expensive processors sit idle waiting for data if a system lacks sufficient bandwidth.">Memory Bandwidth</div>
          <div class="arch-btn arch-btn--conn" data-desc="Hardware queues or drops packets if the aggregate data traversing the network switches exceeds maximum routing capacity. Thousands of processors attempting simultaneous synchronization will instantly stall a poorly designed network.">Network Saturation</div>
          <div class="arch-btn arch-btn--conn" data-desc="Dedicated physical pathways connecting processors within a single server chassis. They bypass the slower host processor and network interface cards to facilitate low-latency exchanges.">Direct Chip Links</div>
"""
phy_buttons = """
          <div class="arch-btn arch-btn--phy" data-desc="An open standard allowing processors to share external memory pools dynamically. It provides a standardized physical layer to solve severe memory capacity constraints.">CXL 3.0 / 3.1</div>
          <div class="arch-btn arch-btn--phy" data-desc="The latest generations of high-speed networking. Massive Ethernet architectures scale out networks across thousands of server racks to prevent saturation.">800G / 1.6T Ethernet</div>
          <div class="arch-btn arch-btn--phy" data-desc="The foundational electrical and protocol standard for peripheral communication. It dictates the base physical layer constraints for nearly all local system interconnects.">PCIe 6.0 / 7.0</div>
          <div class="arch-btn arch-btn--phy" data-desc="An open consortium specification governing direct chip-to-chip communication. It standardizes high-speed inter-accelerator links for distributed parallel computing.">UALink</div>
          <div class="arch-btn arch-btn--phy" data-desc="Removes digital signal processors from optical transceivers. This reduces power consumption and latency but places extreme analog equalization burdens directly on the host switch.">Linear Drive Optics (LPO)</div>
"""

html = re.sub(r'<div class="arch-card-content arch-card-content--ai arch-trigger" data-step="0">[\s\S]*?</div>',
              f'<div class="arch-card-content arch-card-content--ai">\n{ai_buttons}        </div>', html)
html = re.sub(r'<div class="arch-card-content arch-card-content--conn arch-trigger" data-step="1">[\s\S]*?</div>',
              f'<div class="arch-card-content arch-card-content--conn">\n{conn_buttons}        </div>', html)
html = re.sub(r'<div class="arch-card-content arch-card-content--phy arch-trigger" data-step="2">[\s\S]*?</div>',
              f'<div class="arch-card-content arch-card-content--phy">\n{phy_buttons}        </div>', html)

# 5. Static CV Text Stack replacement
static_cv = """
      <div class="cv-text-stack" id="archTextStack">
        <div class="cv-text-card cv-text-card--ai is-visible" style="opacity:1; transform:translateY(0);">
          <div class="cv-text-card__title">Workloads</div>
          <p class="cv-text-card__body">My perspective centers on the structural bottlenecks created when algorithms distribute massive calculations across thousands of processors. Neural networks demand continuous memory access to evaluate context. This generates intense bandwidth demands. Training workloads force individual chips to synchronize their calculations and broadcast updated weights. This saturates network switches. Engineers must split massive models across multiple accelerators. This pushes the physical links between those units to their absolute limits.</p>
        </div>
        <div class="cv-text-card cv-text-card--conn is-visible" style="opacity:1; transform:translateY(0);">
          <div class="cv-text-card__title">Bridges</div>
          <p class="cv-text-card__body">Strategic engineering requires understanding the foundational purpose behind technical specifications. A direct physical path exists between a computational software pattern and the electrical standard built to support it. Memory bandwidth deficits directly drive the adoption of new interconnect protocols. Network saturation necessitates higher capacity ethernet standards. Local memory limitations force the development of specialized communication links to bridge individual processors effectively.</p>
        </div>
        <div class="cv-text-card cv-text-card--phy is-visible" style="opacity:1; transform:translateY(0);">
          <div class="cv-text-card__title">Physical Layer</div>
          <p class="cv-text-card__body">Fluency in electrical specifications is expected. Understanding the architectural drivers provides a distinct strategic advantage. Recognizing that coherent memory pooling necessitates CXL elevates the technical dialogue with customers. Understanding that distributed training requires high-speed Ethernet moves conversations beyond basic compliance. I map physical layer standards directly back to the software workloads that demand them.</p>
        </div>
      </div>
"""
html = re.sub(r'<p class="cv-hint ks-reveal ks-reveal-delay-2" id="archHint">Click each section to reveal the sequence</p>[\s\S]*?<div class="cv-text-stack" id="archTextStack" aria-live="polite"></div>',
              static_cv, html)

# Make Reset button always visible initially? "Insert a new button ... beneath the grid to clear all active callouts"
# We can make it visible and rely on JS to show/hide it based on active callouts, or just leave it.
# Let's just make it hidden initially. Wait, if it resets callouts, it should be visible when a callout is active.
html = re.sub(r'<button id="reset-btn" class="ks-translate-btn ks-reveal" style="opacity: 0; pointer-events: none;">',
              r'<button id="reset-btn" class="ks-translate-btn" style="opacity: 0; pointer-events: none;">', html)

# 6. Rewrite JavaScript logic
new_script = """
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const resetBtn = document.getElementById('reset-btn');
      const allButtons = document.querySelectorAll('.arch-btn');
      let activeCallout = null;

      function clearCallouts() {
        if (activeCallout) {
          activeCallout.remove();
          activeCallout = null;
        }
        resetBtn.style.opacity = '0';
        resetBtn.style.pointerEvents = 'none';
      }

      allButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          const desc = btn.getAttribute('data-desc');
          if (!desc) return;
          
          const isSameBtn = activeCallout && activeCallout.previousElementSibling === btn;
          
          clearCallouts();

          if (!isSameBtn) {
            const callout = document.createElement('div');
            callout.className = 'arch-callout';
            if (btn.classList.contains('arch-btn--ai')) callout.classList.add('arch-callout--ai');
            if (btn.classList.contains('arch-btn--conn')) callout.classList.add('arch-callout--conn');
            if (btn.classList.contains('arch-btn--phy')) callout.classList.add('arch-callout--phy');
            
            callout.textContent = desc;
            
            btn.parentNode.insertBefore(callout, btn.nextSibling);
            activeCallout = callout;
            
            resetBtn.style.opacity = '1';
            resetBtn.style.pointerEvents = 'auto';
          }
        });
      });

      if (resetBtn) {
        resetBtn.addEventListener('click', clearCallouts);
      }
    });
  </script>
"""
html = re.sub(r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{[\s\S]*?</script>', new_script, html)

# Fix removing ks-reveal classes correctly if we don't need them, but they are fine.

with open('architecture.html', 'w') as f:
    f.write(html)
