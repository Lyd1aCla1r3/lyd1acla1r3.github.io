import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

import seaborn as sns

def generate_charts(df, charts_dir, blog_charts_dir):
    sns.set_theme(style="whitegrid")
    # Custom colors mapping from the portfolio CSS
    colors = {
        'yield': '#b76e79',       # --rose-gold
        'citations': '#c9a96e',   # --gold
        'blocks': '#8b4f5a'       # --rose-gold-dark
    }
    
    def save_dual(filename):
        plt.tight_layout()
        plt.savefig(charts_dir / filename, dpi=300, bbox_inches='tight')
        plt.savefig(blog_charts_dir / filename, dpi=300, bbox_inches='tight')
        plt.close()

    # 1. Detection Yield (Bar Chart)
    if not df.empty:
        detection_rates = df.groupby('provider')['present'].mean() * 100
        detection_rates = detection_rates.sort_values(ascending=False)
        
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(x=detection_rates.index, y=detection_rates.values, color=colors['yield'])
        
        # Styling
        sns.despine(top=True, right=True)
        plt.title('AI Overview Detection Yield', fontsize=16, pad=20, fontfamily='sans-serif', fontweight='bold')
        plt.ylabel('Extraction Rate (%)', fontsize=12)
        plt.xlabel('', fontsize=12)
        plt.ylim(0, 110)
        
        # Direct Labeling
        for i, v in enumerate(detection_rates.values):
            ax.text(i, v + 2, f"{v:.1f}%", ha='center', va='bottom', fontsize=11, fontweight='bold')
            
        save_dual('detection_yield.png')

    # 2. Extraction Richness (Citations and Text Blocks)
    present_df = df[df['present'] == True]
    all_providers = df['provider'].unique()
    if not present_df.empty:
        # Average Citations
        avg_citations = present_df.groupby('provider')['citations_count'].mean().reindex(all_providers, fill_value=0)
        avg_citations = avg_citations.sort_values(ascending=False)
        
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(x=avg_citations.index, y=avg_citations.values, color=colors['citations'])
        sns.despine(top=True, right=True)
        plt.title('Extraction Richness: Citations Preserved', fontsize=16, pad=20, fontfamily='sans-serif', fontweight='bold')
        plt.ylabel('Average Citations per AI Overview', fontsize=12)
        plt.xlabel('', fontsize=12)
        
        for i, v in enumerate(avg_citations.values):
            ax.text(i, v + 0.2, f"{v:.1f}", ha='center', va='bottom', fontsize=11, fontweight='bold')
            
        save_dual('richness_citations.png')

        # Average Text Blocks
        avg_blocks = present_df.groupby('provider')['text_blocks_count'].mean().reindex(all_providers, fill_value=0)
        avg_blocks = avg_blocks.sort_values(ascending=False)
        
        plt.figure(figsize=(8, 5))
        ax = sns.barplot(x=avg_blocks.index, y=avg_blocks.values, color=colors['blocks'])
        sns.despine(top=True, right=True)
        plt.title('Extraction Richness: Text Blocks Preserved', fontsize=16, pad=20, fontfamily='sans-serif', fontweight='bold')
        plt.ylabel('Average Text Blocks per AI Overview', fontsize=12)
        plt.xlabel('', fontsize=12)
        
        for i, v in enumerate(avg_blocks.values):
            ax.text(i, v + 0.2, f"{v:.1f}", ha='center', va='bottom', fontsize=11, fontweight='bold')
            
        save_dual('richness_text_blocks.png')

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
