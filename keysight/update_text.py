import re
html_path = "/Users/lydia/Desktop/personal/career/resumes/portfolio/keysight/architecture.html"
with open(html_path, "r") as f:
    content = f.read()

ai_old = "Transformer architecture generates specific, predictable interconnect demands. The attention mechanism inherently drives memory bandwidth requirements, while collective communications saturate switch fabrics during distributed training. Model parallelism pushes inter-accelerator links to their physical limits."
ai_new = "Artificial intelligence algorithms distribute massive calculations across thousands of processors, creating distinct structural bottlenecks. Neural networks require continuous memory access to evaluate context, generating intense bandwidth demands. Training workloads force individual chips to synchronize their calculations, saturating network switches. Massive models must be split directly across multiple accelerators, pushing the physical links between those units to their absolute limits."

conn_old = "Comprehending the foundational reasons behind a specification fundamentally alters the approach to positioning solutions. Each logical bridge connection traces a direct causal path from a computational software pattern to the electrical standard engineered to support it."
conn_new = "Strategic engineering requires understanding the foundational purpose behind technical specifications. A direct physical path exists between a computational software pattern and the electrical standard built to support it. Memory bandwidth deficits drive the adoption of new interconnect protocols. Switch fabric saturation necessitates higher capacity ethernet standards. Accelerator memory limitations force the development of specialized communication links to bridge individual processors."

phy_old = "Fluency in electrical specifications is standard, but understanding the architectural drivers provides a strategic advantage. The recognition that coherent memory pooling necessitates low-latency interconnects transforms a component discussion into a data center architecture consultation."
phy_new = "Fluency in electrical specifications is an industry standard, but understanding the underlying architectural drivers provides a distinct strategic advantage. Recognizing that memory pooling requires ultra-fast interconnects elevates a basic component discussion into a comprehensive architecture consultation. Physical layer standards exist specifically to resolve the bottlenecks created by software workloads, allowing individual servers to operate as a singular cohesive computing engine."

content = content.replace(ai_old, ai_new)
content = content.replace(conn_old, conn_new)
content = content.replace(phy_old, phy_new)

with open(html_path, "w") as f:
    f.write(content)
