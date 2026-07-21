import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import seaborn as sns

def generate_charts(df, charts_dir, blog_charts_dir):
    # Professional, publication-ready aesthetics
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.weight': 'medium',
        'axes.labelweight': 'bold',
        'axes.titleweight': 'bold',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.spines.left': False,
        'axes.grid': True,
        'grid.color': '#E0E0E0',
        'grid.linestyle': '--',
        'grid.linewidth': 0.8,
        'axes.axisbelow': True,
    })
    
    import matplotlib.colors as mcolors
    import matplotlib.patches as patches
    import numpy as np

    # Define Ombre Gradients (bottom_color, top_color)
    ombre_palettes = {
        'Peach/Gold': ('#e6a98d', '#fdf0df'),  # deeper peach to pale gold
        'Blush': ('#d99aab', '#fae4e8'),       # deeper rose to pale blush
        'Rose Gold': ('#a6606e', '#eab8bf')    # dark rose gold to light rose
    }

    def apply_ombre(ax, gradient_keys):
        """Applies an ombre gradient strictly to the bar containers."""
        from matplotlib.image import BboxImage
        from matplotlib.transforms import Bbox, TransformedBbox
        
        for group_idx, container in enumerate(ax.containers):
            if group_idx >= len(gradient_keys): break
            key = gradient_keys[group_idx]
            color_bottom, color_top = ombre_palettes[key]
            
            cmap = mcolors.LinearSegmentedColormap.from_list("grad", [color_bottom, color_top])
            gradient = np.linspace(0, 1, 256).reshape(256, 1)
            
            for patch in container:
                if patch.get_height() <= 0: continue
                x, y = patch.get_xy()
                w, h = patch.get_width(), patch.get_height()
                
                patch.set_visible(False)
                
                # Use BboxImage which safely bypasses categorical axis converters
                bbox = Bbox.from_bounds(x, y, w, h)
                bbox = TransformedBbox(bbox, ax.transData)
                bbox_image = BboxImage(bbox, cmap=cmap, origin='lower', zorder=2)
                bbox_image.set_data(gradient)
                ax.add_artist(bbox_image)
                
                # Subtle border
                rect = patches.Rectangle((x, y), w, h, linewidth=0.5, edgecolor='#cccccc', facecolor='none', zorder=3)
                ax.add_patch(rect)
            
    def save_dual(filename):
        plt.tight_layout()
        plt.savefig(charts_dir / filename, dpi=300, bbox_inches='tight')
        plt.savefig(blog_charts_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()

    # 1. Detection Yield (Bar Chart)
    if not df.empty:
        detection_rates = df.groupby('provider')['present'].mean() * 100
        detection_rates = detection_rates.sort_values(ascending=False)
        
        plt.figure(figsize=(9, 5.5))
        # Initial draw (color doesn't matter, we overwrite with ombre)
        ax = sns.barplot(x=detection_rates.index, y=detection_rates.values, color='#cccccc', width=0.5)
        
        plt.title('AI Overview Detection Yield', fontsize=16, pad=20)
        plt.ylabel('Extraction Rate (%)', fontsize=12)
        plt.xlabel('', fontsize=12)
        plt.ylim(0, 105)
        plt.yticks(np.arange(0, 101, 10))
        
        # Apply Peach/Gold ombre
        apply_ombre(ax, ['Peach/Gold'])
        
        # Direct Labeling
        for i, v in enumerate(detection_rates.values):
            ax.text(i, v + 2, f"{v:.1f}%", ha='center', va='bottom', fontsize=11, fontweight='bold', color='#333333')
            
        save_dual('detection_yield.png')

    # 2. Extraction Richness (Combined Grouped Bar Chart)
    present_df = df[df['present'] == True]
    if not present_df.empty:
        active_providers = present_df['provider'].unique()
        
        avg_citations = present_df.groupby('provider')['citations_count'].mean().reindex(active_providers)
        avg_blocks = present_df.groupby('provider')['text_blocks_count'].mean().reindex(active_providers)
        
        # Create a combined DataFrame for melting
        richness_df = pd.DataFrame({
            'provider': active_providers,
            'Citations': avg_citations.values,
            'Text Blocks': avg_blocks.values
        })
        
        # Sort by Citations descending for aesthetic flow
        richness_df = richness_df.sort_values(by='Citations', ascending=False)
        
        melted_df = richness_df.melt(id_vars='provider', var_name='Metric', value_name='Average Count')
        
        plt.figure(figsize=(9, 5.5))
        # Initial draw (colors overridden)
        ax = sns.barplot(
            data=melted_df, 
            x='provider', 
            y='Average Count', 
            hue='Metric',
            palette={'Citations': '#cccccc', 'Text Blocks': '#aaaaaa'},
            width=0.6
        )
        
        plt.title('Extraction Richness: Citations & Text Blocks', fontsize=16, pad=20)
        plt.ylabel('Average Count per AI Overview', fontsize=12)
        plt.xlabel('', fontsize=12)
        
        # Add granular ticks for the count
        max_val = melted_df['Average Count'].max()
        if max_val > 0:
            tick_step = 1 if max_val <= 10 else 2
            plt.yticks(np.arange(0, int(max_val) + 2, tick_step))
        
        # Apply Blush (Citations) and Rose Gold (Text Blocks) ombre
        apply_ombre(ax, ['Blush', 'Rose Gold'])
        
        # Direct Labeling on grouped bars
        for p in [patch for patch in ax.patches if isinstance(patch, patches.Rectangle) and patch.get_height() > 0 and patch.get_visible()]:
            ax.annotate(f"{p.get_height():.1f}", 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', 
                        xytext=(0, 5), textcoords='offset points',
                        fontsize=10, fontweight='bold', color='#333333')
                
        # Style Legend - Since we hid original patches, we need to create proxy artists for the legend
        import matplotlib.patches as mpatches
        patch1 = mpatches.Patch(color=ombre_palettes['Blush'][0], label='Citations')
        patch2 = mpatches.Patch(color=ombre_palettes['Rose Gold'][0], label='Text Blocks')
        plt.legend(handles=[patch1, patch2], title='', frameon=False, loc='upper right', fontsize=11)
            
        save_dual('richness_combined.png')

def main():
    root_dir = Path(__file__).parent.parent
    extracted_dir = root_dir / "results" / "extracted"
    charts_dir = root_dir / "analysis" / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)
    
    if not extracted_dir.exists():
        print("No extracted results found. Please run benchmark/run.py first.")
        return
        
    records = []
    
    for file in extracted_dir.glob("*.json"):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            query = data["query"]
            intent = data["intent"]
            
            for provider, p_data in data["scores"].items():
                extracted = p_data.get("extracted", {})
                
                records.append({
                    "query": query,
                    "intent": intent,
                    "provider": provider,
                    "present": extracted.get("present", False),
                    "citations_count": len(extracted.get("citations", [])),
                    "text_blocks_count": len(extracted.get("text_blocks", []))
                })
                
    df = pd.DataFrame(records)
    
    if df.empty:
        print("No valid records to analyze.")
        return
        
    print("Aggregate Benchmark Results:\n")
    
    # Detection Yield
    extraction = df.groupby('provider')['present'].mean() * 100
    print("--- Detection Yield (Higher is better) ---")
    for provider, rate in extraction.items():
        print(f"{provider:12s}: {rate:.1f}%")
        
    print("\n--- Extraction Richness (For extracted overviews) ---")
    present_df = df[df['present'] == True]
    all_providers = df['provider'].unique()
    if not present_df.empty:
        avg_citations = present_df.groupby('provider')['citations_count'].mean().reindex(all_providers, fill_value=0)
        avg_blocks = present_df.groupby('provider')['text_blocks_count'].mean().reindex(all_providers, fill_value=0)
        
        for provider in avg_citations.index:
            print(f"{provider:12s}: Mean Citations: {avg_citations[provider]:.1f} | Mean Text Blocks: {avg_blocks[provider]:.1f}")
    else:
        print("No providers successfully extracted any AI Overviews.")

    print("\nGenerating charts in analysis/charts/ and ../assets/images/blog/serp-benchmark/...")
    blog_charts_dir = root_dir.parent / "assets" / "images" / "blog" / "serp-benchmark"
    blog_charts_dir.mkdir(parents=True, exist_ok=True)
    generate_charts(df, charts_dir, blog_charts_dir)
    print("Done! Check the charts folder for visualizations.")

if __name__ == "__main__":
    main()
