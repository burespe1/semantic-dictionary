import os
import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import re

DR_TITLES = {
    "DR_EU_886-2013": "SRTI - Safety-Related Traffic Information",
    "DR_EU_2024-490": "MMTIS - Multimodal Travel Information Services",
    "DR_EU_2015-962": "RTTI - Real-Time Traffic Information",
    "DR_EU_2022-670": "RTTI - Real-Time Traffic Information",  
    "DR_EU_885-2013": "SSTP - Safe and Secure Truck Parking"
}

BASE_DIR = Path(__file__).resolve().parent.parent
DRAFT_ROOT = BASE_DIR / "drafts"
PREVIEW_DIR = BASE_DIR / "preview"
INDEX_FILE = DRAFT_ROOT / "INDEX.md"

BADGES = {
    "draft": "![Status](https://img.shields.io/badge/status-draft-ff9800)",         # Warm orange for a work-in-progress
    "in review": "![Status](https://img.shields.io/badge/status-in_review-ffc107)", # Amber/gold to indicate scrutiny
    "modified": "![Status](https://img.shields.io/badge/status-modified-673ab7)",   # Deep violet, bold for attention
    "finalised": "![Status](https://img.shields.io/badge/status-finalised-2196f3)", # Classic blue for trust & clarity
    "approved": "![Status](https://img.shields.io/badge/status-approved-4caf50)",   # Deep green for confirmation
    "deprecated": "![Status](https://img.shields.io/badge/status-deprecated-bdbdbd)",# Medium grey for obsolescence
    "unknown": "![Status](https://img.shields.io/badge/status-unknown-9e9e9e)"       # Neutral grey for ambiguity
}

index_entries= []

def escape_yaml_value(value):
    if not isinstance(value, str):
        return value
    risky_chars = ['<', '>', '[', ']', '(', ')', ':']
    if any(c in value for c in risky_chars) and not value.startswith('"'):
        value = value.replace('"', '\\"')
        return f'"{value}"'
    return value

def escape_yaml_block(yaml_text):
    lines = yaml_text.splitlines()
    fixed_lines = []
    for line in lines:
        if ':' in line and not line.strip().startswith('#'):
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if value and not value.lower() in ['true', 'false'] and not value.replace('.', '', 1).isdigit():
                value = escape_yaml_value(value)
            fixed_lines.append(f"{key}: {value}")
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)

def extract_content(md_text):

    def adjust_relative_links(text):
        # Replace "../../media/" with "../images/"
        text = re.sub(r'\(\.\./\.\./(images/.*?)\)', r'(../\1)', text)
        text = re.sub(r'\(\.\./\.\./(code/.*?)\)', r'(../\1)', text)
        return text

    parts = md_text.split('---')
    if len(parts) < 3:
        return None, md_text

    raw_yaml = escape_yaml_block(parts[1])
    try:
        meta = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as e:
        print(f"⚠️ YAML error: {e}")
        return None, md_text

    content = '---'.join(parts[2:]).strip()
    content = adjust_relative_links(content)

    return meta, content

def format_entry(meta, content, heading_level=3):
    # header = f"{'#' * heading_level} {meta.get('label', 'Untitled')} \n\n"
    header = f"{'#' * heading_level} {meta.get('label', 'Untitled')} {BADGES.get(meta.get('status', 'unknown').strip(), 'unknown')}\n\n"
    definition_text = meta.get("definition") or ""
    definition = f"**Definition**: {definition_text.strip()}"

    body = content.strip() if content and content.strip() else None

    if body:
        return f"{header}{definition}\n\n{body}\n\n---\n"
    else:
        return f"{header}{definition}\n\n---\n"


def process_dr_folder(dr_folder):
    preview_file = PREVIEW_DIR / f"{dr_folder.name}.md" 
    
    grouped_entries = defaultdict(list)  # {combined_heading: [(label, meta, content)]}

    for md_file in dr_folder.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            raw = f.read()

        meta, body = extract_content(raw)
        if not meta:
            print(f"⏩ Skipping {md_file.name} in {dr_folder.name} ... missing metadata")
            continue

        category = meta.get("category", "uncategorised").strip()
        raw_subcategory = meta.get("subcategory", [])
        subcategory = [str(item).strip() for item in raw_subcategory] if isinstance(raw_subcategory, list) else [str(raw_subcategory).strip()]
        label = meta.get("label", "").strip()
        
        heading = category
        if subcategory and any(subcategory):
            heading += " – " + " – ".join(subcategory)

        grouped_entries[heading].append((label.lower(), meta, body))

    if grouped_entries:
        title = DR_TITLES.get(dr_folder.name, dr_folder.name)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        combined = f"# Preview: {title} ({dr_folder.name})\n\n"
        combined += f"**Generated on:** {timestamp}\n\n"
        
        index_entries.append((dr_folder.name, f"\n## {title} ({dr_folder.name})\n"))
        
        for heading in sorted(grouped_entries.keys(), key=str.lower):
            combined += f"## {heading}\n\n"
            for _, meta, body in sorted(grouped_entries[heading], key=lambda x: x[0]):
                combined += format_entry(meta, body, heading_level=3)
                
                label = meta.get("label", "").strip()
                d_id = meta.get("id", "").strip()
                status = meta.get("status", "unknown").strip()
                badge = BADGES.get(status, status)
                relative_path = f"{dr_folder.name}/{d_id}.md" 
                link = f"[{label}]({relative_path})"
                index_entries.append((label.lower(), f"- [{badge}] {link}"))

        with open(preview_file, "w", encoding="utf-8") as out:
            out.write(combined)

        print(f"✅ Preview generated: {preview_file.name}")
    else:
        print(f"⚠️ No approved items found in {dr_folder.name}")
 
def main():
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    
    for dr_folder in DRAFT_ROOT.iterdir():
        if dr_folder.is_dir():
            process_dr_folder(dr_folder)
       
    header = "# 📚 Drafts Master Index\n"
    content = "\n".join([entry[1] for entry in index_entries])
    
    with open(INDEX_FILE, "w", encoding="utf-8") as out:
        out.write(header + content + "\n")

    print(f"✅ Master index created at: {INDEX_FILE}")        

    print("\n🎉 All DR vocabularies previews published!")   

if __name__ == "__main__":
    main()