import os
import yaml
from pathlib import Path

# Make paths relative to the script location
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

DRAFT_ROOT = ROOT_DIR / "drafts"
PREVIEW_ROOT = ROOT_DIR / "preview"

def escape_colons_in_yaml(yaml_text):
    lines = yaml_text.splitlines()
    fixed_lines = []
    for line in lines:
        if ':' in line and not line.strip().startswith('#') and not line.strip().startswith('"'):
            parts = line.split(":", 1)
            key = parts[0].strip()
            value = parts[1].strip()
            # Avoid quoting numeric or boolean values
            if value and not (value.startswith('"') or value.startswith("'") or value.lower() in ['true', 'false']) and not value.replace('.', '', 1).isdigit():
                value = f'"{value}"'
            fixed_lines.append(f"{key}: {value}")
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)
    
def extract_content(md_text):
    parts = md_text.split('---')
    if len(parts) < 3:
        return None, md_text
    raw_yaml = escape_colons_in_yaml(parts[1])
    meta = yaml.safe_load(raw_yaml)
    content = '---'.join(parts[2:]).strip()
    return meta, content


def format_preview(meta, content):
    header = f"# {meta.get('label', 'Untitled')}\n\n"
    definition = f"**Definition**: {meta.get('definition', '')}\n\n"
    return header + definition + content

def main():
    for draft_folder in DRAFT_ROOT.iterdir():
        if not draft_folder.is_dir():
            continue

        preview_folder = PREVIEW_ROOT / draft_folder.name
        os.makedirs(preview_folder, exist_ok=True)

        for md_file in draft_folder.glob("*.md"):
            with open(md_file, "r", encoding="utf-8") as f:
                raw = f.read()

            meta, body = extract_content(raw)
            if not meta:
                print(f"⚠️ Skipping {md_file.name}: Missing frontmatter")
                continue

            preview_content = format_preview(meta, body)
            out_path = preview_folder / md_file.name
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(preview_content)

            print(f"✅ Preview generated: {draft_folder.name}/{md_file.name}")

if __name__ == "__main__":
    main()