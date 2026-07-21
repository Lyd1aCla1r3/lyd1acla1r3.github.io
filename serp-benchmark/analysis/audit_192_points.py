"""
Definitive 196-Point Data Integrity Audit
==========================================
Validates all raw JSON responses against extracted results.
Implements the corrected 5-phase architecture from the adversarial audit.
"""
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "results" / "raw"
EXTRACTED_DIR = ROOT / "results" / "extracted"
PROVIDERS = ["searchapi", "serpapi", "serper", "dataforseo"]
PROVIDER_DISPLAY = {"searchapi": "SearchApi", "serpapi": "SerpApi", "serper": "Serper", "dataforseo": "DataForSEO"}

# Schema Sweep keywords (applied to JSON keys only)
SCHEMA_KEYWORDS = ["ai_overview", "ai overview", "aiOverview", "generative", "sge", "generated_text"]
# Separate handling for "answer" — only flag if NOT under answerBox/answer_box
ANSWER_KEYWORDS = ["answer"]

# Blob sweep config
BLOB_MIN_LENGTH = 500
BLOB_EXCLUDE_PREFIXES = ("http://", "https://")
BLOB_EXCLUDE_PARENT_KEYS = {"snippet", "description", "question", "title", "snippetHighlighted",
                             "status_message", "check_url", "google_url", "request_url",
                             "html_url", "json_url", "raw_html_file", "link", "url",
                             "displayed_link", "redirect_link", "source", "date",
                             "xpath", "cache_url", "related_page_url",
                             "pixel_position_endpoint", "json_endpoint"}


def recursive_key_scan(obj, path="", results=None):
    """Recursively scan all keys in a JSON object for AI-related substrings."""
    if results is None:
        results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_path = f"{path}.{k}" if path else k
            k_lower = k.lower()
            # Check schema keywords
            for kw in SCHEMA_KEYWORDS:
                if kw.lower() in k_lower:
                    results.append(("SCHEMA", full_path, k, type(v).__name__))
            # Check answer keywords — only flag if not under answerBox/answer_box
            for kw in ANSWER_KEYWORDS:
                if kw in k_lower and "answerBox" not in path and "answer_box" not in path:
                    results.append(("SCHEMA_ANSWER", full_path, k, type(v).__name__))
            recursive_key_scan(v, full_path, results)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            recursive_key_scan(item, f"{path}[{i}]", results)
    return results


def recursive_blob_scan(obj, path="", parent_key="", results=None):
    """Recursively find suspiciously long strings."""
    if results is None:
        results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_path = f"{path}.{k}" if path else k
            recursive_blob_scan(v, full_path, k, results)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            recursive_blob_scan(item, f"{path}[{i}]", parent_key, results)
    elif isinstance(obj, str):
        if len(obj) >= BLOB_MIN_LENGTH:
            if not any(obj.startswith(p) for p in BLOB_EXCLUDE_PREFIXES):
                if parent_key not in BLOB_EXCLUDE_PARENT_KEYS:
                    results.append(("BLOB", path, parent_key, len(obj), obj[:100]))
    return results


def main():
    report_lines = []
    def log(msg=""):
        print(msg)
        report_lines.append(msg)

    log("=" * 70)
    log("DEFINITIVE DATA INTEGRITY AUDIT REPORT")
    log("=" * 70)

    # ===== PHASE 0: CENSUS =====
    log("\n## PHASE 0: CENSUS\n")
    
    extracted_files = sorted([f for f in os.listdir(EXTRACTED_DIR) if f.endswith('.json')])
    log(f"Extracted result files: {len(extracted_files)}")
    
    raw_counts = {}
    for p in PROVIDERS:
        pdir = RAW_DIR / p
        raw_counts[p] = len([f for f in os.listdir(pdir) if f.endswith('.json')])
        log(f"Raw files ({PROVIDER_DISPLAY[p]}): {raw_counts[p]}")
    
    total_data_points = len(extracted_files) * len(PROVIDERS)
    log(f"Total data points: {len(extracted_files)} queries × {len(PROVIDERS)} providers = {total_data_points}")
    
    # Verify consistency
    for p in PROVIDERS:
        if raw_counts[p] != len(extracted_files):
            log(f"⚠️  WARNING: {PROVIDER_DISPLAY[p]} has {raw_counts[p]} raw files but {len(extracted_files)} extracted files")

    # ===== PHASE 1: ERROR RESPONSE FILTER =====
    log(f"\n## PHASE 1: ERROR RESPONSE FILTER\n")
    
    error_points = []  # (filename, provider, reason)
    
    for p in PROVIDERS:
        pdir = RAW_DIR / p
        for fname in sorted(os.listdir(pdir)):
            if not fname.endswith('.json'):
                continue
            fpath = pdir / fname
            fsize = fpath.stat().st_size
            with open(fpath) as f:
                data = json.load(f)
            
            reason = None
            if "error" in data:
                reason = f"Error key present: {str(data['error'])[:80]}"
            elif fsize < 500 and p != "serper":  # Serper files are legitimately smaller but not THIS small
                reason = f"Suspiciously small file ({fsize} bytes)"
            elif p == "dataforseo":
                try:
                    status = data.get("tasks", [{}])[0].get("status_code", 0)
                    if status != 20000:
                        reason = f"DataForSEO status_code={status}"
                except (IndexError, KeyError):
                    reason = "DataForSEO: could not parse task status"
            
            if reason:
                error_points.append((fname, PROVIDER_DISPLAY[p], reason))
    
    log(f"Error/inconclusive responses found: {len(error_points)}")
    for fname, pname, reason in error_points:
        log(f"  ⚠️  {pname:12s} | {fname:55s} | {reason}")
    
    error_set = set((fname, pname) for fname, pname, _ in error_points)

    # ===== PHASE 2 & 3: SCHEMA + BLOB SWEEPS (present==False only, excluding errors) =====
    log(f"\n## PHASE 2 & 3: SCHEMA + BLOB SWEEPS (present==False, non-error files)\n")
    
    # Build present==False set from extracted results
    false_negatives_to_check = []
    for efname in extracted_files:
        with open(EXTRACTED_DIR / efname) as f:
            edata = json.load(f)
        for pname, pdata in edata["scores"].items():
            if not pdata["extracted"].get("present", False):
                dir_name = pname.lower().replace("dataforseo", "dataforseo").replace("searchapi", "searchapi").replace("serpapi", "serpapi")
                # Map display name to directory name
                dir_map = {"SearchApi": "searchapi", "SerpApi": "serpapi", "Serper": "serper", "DataForSEO": "dataforseo"}
                false_negatives_to_check.append((efname, pname, dir_map[pname]))
    
    log(f"Data points with present==False: {len(false_negatives_to_check)}")
    
    # Separate errors from auditable points
    auditable = [(fname, pname, dname) for fname, pname, dname in false_negatives_to_check 
                 if (fname, pname) not in error_set]
    skipped_errors = [(fname, pname, dname) for fname, pname, dname in false_negatives_to_check 
                      if (fname, pname) in error_set]
    
    log(f"Skipped (error responses, already flagged): {len(skipped_errors)}")
    log(f"Auditable (valid responses with present==False): {len(auditable)}")
    
    schema_flags = []
    blob_flags = []
    
    for fname, pname, dname in auditable:
        raw_path = RAW_DIR / dname / fname
        if not raw_path.exists():
            log(f"  ❌ MISSING RAW FILE: {dname}/{fname}")
            continue
        
        with open(raw_path) as f:
            raw = json.load(f)
        
        # Schema Sweep
        s_results = recursive_key_scan(raw)
        for rtype, path, key, vtype in s_results:
            schema_flags.append((fname, pname, path, key, vtype))
        
        # Blob Sweep
        b_results = recursive_blob_scan(raw)
        for rtype, path, parent_key, length, preview in b_results:
            blob_flags.append((fname, pname, path, parent_key, length, preview))
    
    log(f"\nSchema Sweep flags: {len(schema_flags)}")
    for fname, pname, path, key, vtype in schema_flags:
        log(f"  🔍 {pname:12s} | {fname:55s} | key={key} at {path} (type={vtype})")
    
    log(f"\nBlob Sweep flags: {len(blob_flags)}")
    for fname, pname, path, parent_key, length, preview in blob_flags:
        log(f"  📄 {pname:12s} | {fname:55s} | {length} chars at {path} (parent_key={parent_key})")
        log(f"     Preview: {preview}...")

    # ===== PHASE 4: RICHNESS CHECK (present==True only) =====
    log(f"\n## PHASE 4: RICHNESS CHECK (present==True data points)\n")
    
    empty_present = []
    schema_violations = []
    total_present = 0
    
    for efname in extracted_files:
        with open(EXTRACTED_DIR / efname) as f:
            edata = json.load(f)
        for pname, pdata in edata["scores"].items():
            ext = pdata["extracted"]
            if ext.get("present", False):
                total_present += 1
                # Check richness
                has_summary = bool(ext.get("summary", "").strip())
                has_text_blocks = bool(ext.get("text_blocks", []))
                has_citations = bool(ext.get("citations", []))
                
                if not has_summary and not has_text_blocks:
                    empty_present.append((efname, pname, has_summary, has_text_blocks, has_citations))
                
                # Schema conformance
                required_keys = {"present", "summary", "text_blocks", "citations", "related_searches"}
                actual_keys = set(ext.keys())
                missing_keys = required_keys - actual_keys
                if missing_keys:
                    schema_violations.append((efname, pname, f"missing keys: {missing_keys}"))
                
                # Type checks
                if not isinstance(ext.get("present"), bool):
                    schema_violations.append((efname, pname, f"present is {type(ext['present']).__name__}, not bool"))
                if not isinstance(ext.get("text_blocks"), list):
                    schema_violations.append((efname, pname, f"text_blocks is {type(ext.get('text_blocks')).__name__}, not list"))
                if not isinstance(ext.get("citations"), list):
                    schema_violations.append((efname, pname, f"citations is {type(ext.get('citations')).__name__}, not list"))
    
    log(f"Total present==True data points: {total_present}")
    log(f"Present but empty (no summary AND no text_blocks): {len(empty_present)}")
    for fname, pname, has_s, has_tb, has_c in empty_present:
        log(f"  ⚠️  {pname:12s} | {fname:55s} | summary={has_s}, text_blocks={has_tb}, citations={has_c}")
    
    log(f"\nSchema violations: {len(schema_violations)}")
    for fname, pname, violation in schema_violations:
        log(f"  ❌ {pname:12s} | {fname:55s} | {violation}")

    # ===== PHASE 5: FINAL REPORT =====
    log(f"\n{'='*70}")
    log("PHASE 5: FINAL SUMMARY")
    log(f"{'='*70}")
    
    log(f"\nTotal data points audited: {total_data_points}")
    log(f"  ✅ Present (AI Overview detected):     {total_present}")
    log(f"  ❌ Proven Absent (valid, no AIO):       {len(auditable)}")
    log(f"  ⚠️  Inconclusive (error responses):     {len(error_points)}")
    log(f"  Sum check: {total_present} + {len(auditable)} + {len(error_points)} = {total_present + len(auditable) + len(error_points)} (expected {total_data_points})")
    
    log(f"\nPer-Provider Detection Yield:")
    for pname in ["SearchApi", "SerpApi", "Serper", "DataForSEO"]:
        present_count = 0
        error_count = 0
        absent_count = 0
        for efname in extracted_files:
            with open(EXTRACTED_DIR / efname) as f:
                edata = json.load(f)
            ext = edata["scores"][pname]["extracted"]
            if ext.get("present", False):
                present_count += 1
            elif (efname, pname) in error_set:
                error_count += 1
            else:
                absent_count += 1
        
        total = present_count + error_count + absent_count
        raw_yield = (present_count / total * 100) if total else 0
        adjusted_denom = present_count + absent_count
        adj_yield = (present_count / adjusted_denom * 100) if adjusted_denom else 0
        
        log(f"  {pname:12s}: {present_count:2d} present | {absent_count:2d} absent | {error_count:2d} errors | Raw Yield: {raw_yield:5.1f}% | Adjusted Yield: {adj_yield:5.1f}%")
    
    # Final verdict
    log(f"\n{'='*70}")
    total_flags = len(schema_flags) + len(blob_flags)
    if total_flags == 0 and len(empty_present) == 0 and len(schema_violations) == 0:
        log("✅ VERDICT: ALL DATA POINTS VERIFIED CLEAN")
        log("   - Zero false negatives detected in Schema or Blob sweeps")
        log("   - Zero empty-but-present anomalies") 
        log("   - Zero schema violations")
        log(f"   - {len(error_points)} error responses correctly classified as Inconclusive")
    else:
        log(f"⚠️  VERDICT: {total_flags} FLAGS REQUIRE MANUAL REVIEW")
        log(f"   - Schema flags: {len(schema_flags)}")
        log(f"   - Blob flags: {len(blob_flags)}")
        log(f"   - Empty-present: {len(empty_present)}")
        log(f"   - Schema violations: {len(schema_violations)}")
    log(f"{'='*70}")
    
    # Save report
    report_path = ROOT / "analysis" / "audit_report.txt"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    log(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
