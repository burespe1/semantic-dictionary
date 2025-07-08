import os
import yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

DRAFT_ROOT = ROOT_DIR / "drafts"
PREVIEW_DIR = ROOT_DIR / "preview"
os.makedirs(PREVIEW_DIR, exist_ok=True)

def extract_content(md_text):
    parts = md_text.split('---')
    if len(parts) < 3:
        return None, md_text
    raw_yaml = parts[1]
    try:
        meta = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as e:
        print(f"⚠️ YAML error: {e}")
        return None, md_text
    content = '---'.join(parts[2:]).strip()
    return meta, content

def format_entry(meta, content):
    header = f"## {meta.get('label', 'Untitled')}\n\n"
    definition = f"**Definition**: {meta.get('definition', '')}\n\n"
    return header + definition + content + "\n\n---\n"

def main():
    for dr_folder in DRAFT_ROOT.iterdir():
        if not dr_folder.is_dir():
            continue

        entries = []
        for md_file in dr_folder.glob("*.md"):
            with open(md_file, "r", encoding="utf-8") as f:
                raw = f.read()

            meta, body = extract_content(raw)
            if not meta or meta.get("status") != "approved":
                print(f"⏩ Skipping {md_file.name} in {dr_folder.name}")
                continue

            entry = format_entry(meta, body)
            entries.append((meta.get("label", ""), entry))

        if entries:
            entries.sort(key=lambda x: x[0].lower())
            combined = f"# Preview: {dr_folder.name}\n\n"
            combined += "\n".join(entry for _, entry in entries)

            out_path = PREVIEW_DIR / f"{dr_folder.name}.md"
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(combined)

            print(f"✅ Preview generated: {out_path.name}")
        else:
            print(f"⚠️ No approved items found in {dr_folder.name}")

if __name__ == "__main__":
    main()