import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.colors as mcolors
import glob

def enhance_blue_pink(img_path):
    print(f"Processing {img_path}")
    img = Image.open(img_path).convert('RGB')
    
    # Global enhance
    img = ImageEnhance.Color(img).enhance(1.4)
    img = ImageEnhance.Contrast(img).enhance(1.3)
    
    # Convert to HSV to target blue and pink
    hsv = mcolors.rgb_to_hsv(np.array(img) / 255.0)
    
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    
    # Blue: ~0.55 to 0.75
    # Pink: ~0.75 to 0.95
    mask_blue = (h > 0.50) & (h < 0.75)
    mask_pink = (h > 0.75) & (h < 0.95)
    
    s[mask_blue] = np.clip(s[mask_blue] * 1.3, 0, 1)
    v[mask_blue] = np.clip(v[mask_blue] * 1.15, 0, 1)
    
    s[mask_pink] = np.clip(s[mask_pink] * 1.4, 0, 1)
    v[mask_pink] = np.clip(v[mask_pink] * 1.25, 0, 1)
    
    hsv[:, :, 1] = s
    hsv[:, :, 2] = v
    
    rgb = mcolors.hsv_to_rgb(hsv)
    out = Image.fromarray((rgb * 255).astype(np.uint8))
    
    # Save back
    out.save(img_path)

images = glob.glob("assets/images/si_part[1-6]*.jpg") + ["assets/images/signal_integrity_cover.jpg"]
# Exclude the backups and any copies like ' 2.jpg' if not needed, but we'll just process the main ones
main_images = [
    "assets/images/signal_integrity_cover.jpg",
    "assets/images/si_part1_electromagnetic.jpg",
    "assets/images/si_part2_measurement.jpg",
    "assets/images/si_part3_jitter.jpg",
    "assets/images/si_part4_equalization.jpg",
    "assets/images/si_part5_serdes.jpg",
    "assets/images/si_part6_coherent_optics.jpg"
]
for img in main_images:
    enhance_blue_pink(img)
