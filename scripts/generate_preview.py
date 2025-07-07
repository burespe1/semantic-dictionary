# scripts/generate_preview.py

import os
import yaml

DRAFT_DIR = "../drafts"
PREVIEW_DIR = "../preview"

def extract_content(md_text):
    parts = md_text.split('---')
    if len(parts) < 3:
        return None, md_text
    meta = yaml.safe_load(parts[1])
    content = '---'.join(parts[2:]).strip()
    return meta, content

def format_preview(meta, content):
    header = f"# {meta.get('label', 'Untitled')}\n\n"
    definition = f"**Definition**: {meta.get('definition', '')}\n\n"
    return header + definition + content

def main():
    os.makedirs(PREVIEW_DIR, exist_ok=True)

    for fname in os.listdir(DRAFT_DIR):
        if fname.endswith(".md"):
            path = os.path.join(DRAFT_DIR, fname)
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()

            meta, body = extract_content(raw)
            if not meta:
                print(f"Skipping {fname}: Missing frontmatter")
                continue

            preview_content = format_preview(meta, body)

            out_path = os.path.join(PREVIEW_DIR, fname)
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(preview_content)

            print(f"✅ Preview generated for: {fname}")

if __name__ == "__main__":
    main()