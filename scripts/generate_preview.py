import os
import yaml
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

DRAFT_ROOT = ROOT_DIR / "drafts"
PREVIEW_DIR = ROOT_DIR / "preview"
os.makedirs(PREVIEW_DIR, exist_ok=True)

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
    return meta, content

def format_entry(meta, content, heading_level=3):
    header = f"{'#' * heading_level} {meta.get('label', 'Untitled')}\n\n"
    definition = f"**Definition**: {meta.get('definition', '')}\n\n"
    return header + definition + content + "\n\n---\n"

def main():
    for dr_folder in DRAFT_ROOT.iterdir():
        if not dr_folder.is_dir():
            continue

        grouped_entries = defaultdict(list)  # {combined_heading: [(label, meta, content)]}

        for md_file in dr_folder.glob("*.md"):
            with open(md_file, "r", encoding="utf-8") as f:
                raw = f.read()

            meta, body = extract_content(raw)
            if not meta or meta.get("status") != "approved":
                print(f"⏩ Skipping {md_file.name} in {dr_folder.name}")
                continue

            category = meta.get("category", "Uncategorized").strip()
            subcategory = meta.get("subcategory", "").strip()
            label = meta.get("label", "").strip()

            heading = category
            if subcategory:
                heading += f" – {subcategory}"

            grouped_entries[heading].append((label.lower(), meta, body))

        if grouped_entries:
            combined = f"# Preview: {dr_folder.name}\n\n"

            for heading in sorted(grouped_entries.keys(), key=str.lower):
                combined += f"## {heading}\n\n"
                for _, meta, body in sorted(grouped_entries[heading], key=lambda x: x[0]):
                    combined += format_entry(meta, body, heading_level=3)

            out_path = PREVIEW_DIR / f"{dr_folder.name}.md"
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(combined)

            print(f"✅ Preview generated: {out_path.name}")
        else:
            print(f"⚠️ No approved items found in {dr_folder.name}")

if __name__ == "__main__":
    main()