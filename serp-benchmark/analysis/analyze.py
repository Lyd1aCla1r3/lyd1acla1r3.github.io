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
    
    # Custom colors mapping from the portfolio CSS
    colors = {
        'yield': '#b76e79',       # --rose-gold
        'Citations': '#eab8bf',   # Lighter, more blush gold
        'Text Blocks': '#8b4f5a'  # --rose-gold-dark
    }
    
    def add_sheen(ax):
        import matplotlib.patches as patches
        for patch in ax.patches:
            if not isinstance(patch, patches.Rectangle): continue
            x, y = patch.get_xy()
            w, h = patch.get_width(), patch.get_height()
            if h <= 0 or w <= 0: continue
            
            # Left edge bright highlight (sheen)
            highlight1 = patches.Rectangle((x, y), w * 0.25, h, color='white', alpha=0.25, zorder=patch.get_zorder()+0.1)
            ax.add_patch(highlight1)
            # Second highlight step for smooth gradient feel
            highlight2 = patches.Rectangle((x + w * 0.25, y), w * 0.15, h, color='white', alpha=0.1, zorder=patch.get_zorder()+0.1)
            ax.add_patch(highlight2)
            
            # Right edge shadow (depth)
            shadow = patches.Rectangle((x + w * 0.85, y), w * 0.15, h, color='black', alpha=0.15, zorder=patch.get_zorder()+0.1)
            ax.add_patch(shadow)
            
            # Crisp white border for metallic polish
            patch.set_edgecolor('white')
            patch.set_linewidth(1.0)
            
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
        ax = sns.barplot(x=detection_rates.index, y=detection_rates.values, color=colors['yield'], width=0.5)
        
        plt.title('AI Overview Detection Yield', fontsize=16, pad=20)
        plt.ylabel('Extraction Rate (%)', fontsize=12)
        plt.xlabel('', fontsize=12)
        plt.ylim(0, 105)
        import numpy as np
        plt.yticks(np.arange(0, 101, 10))
        
        add_sheen(ax)
        
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
        ax = sns.barplot(
            data=melted_df, 
            x='provider', 
            y='Average Count', 
            hue='Metric',
            palette={'Citations': colors['Citations'], 'Text Blocks': colors['Text Blocks']},
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
        
        add_sheen(ax)
        
        # Direct Labeling on grouped bars
        for p in ax.patches:
            if p.get_height() > 0:
                ax.annotate(f"{p.get_height():.1f}", 
                            (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha='center', va='bottom', 
                            xytext=(0, 5), textcoords='offset points',
                            fontsize=10, fontweight='bold', color='#333333')
                
        # Style Legend
        plt.legend(title='', frameon=False, loc='upper right', fontsize=11)
            
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
