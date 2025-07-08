import os
import re
from pathlib import Path

# === CONFIG ===
SOURCE_FOLDER = "../source"
SOURCE_FILES = sorted(Path(SOURCE_FOLDER).glob("*.md"))
MAX_FILENAME_LENGTH = 128  # or 100 to be extra safe

# === PATTERNS ===
category_pattern = re.compile(r"^###\s+(.*)")
item_pattern = re.compile(r"\*\*(.+?)\*\*\s*:?\s*(.*)")
code_block_pattern = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)

# === NORMALIZATION FUNCTION ===
def normalize_item_metadata(label_raw):
    label_raw = label_raw.replace('–', '-').replace('—', '-').replace('/', '_').rstrip(':')
    if '-' in label_raw:
        subcategory, label_clean = label_raw.split('-', 1)
        subcategory = subcategory.strip()
        label_clean = label_clean.strip()
    else:
        subcategory = None
        label_clean = label_raw.strip()
    label_clean = re.sub(r'^[_*]+|[_*]+$', '', label_clean)
    combined = f"{subcategory}-{label_clean}" if subcategory else label_clean
    combined = re.sub(r'[^\w\s-]', '', combined)
    combined = re.sub(r'\s*-\s*', '-', combined)
    combined = re.sub(r'\s+', '-', combined).strip('-')
    item_id = re.sub(r'-+', '-', combined.lower())
    
    if len(item_id) > MAX_FILENAME_LENGTH:
        item_id = item_id[:MAX_FILENAME_LENGTH]
    
    return {
        "id": item_id,
        "label": label_clean,
        "subcategory": subcategory
    }

# === PROCESS BUFFER ===
def process_buffer(buffer, category, source_name, target_dir, code_dir):
    i = 0
    while i < len(buffer):
        line = buffer[i]
        item_match = item_pattern.match(line)
        if item_match:
            label_raw = item_match.group(1).strip()
            definition = item_match.group(2).strip()

            meta = normalize_item_metadata(label_raw)
            item_id = meta["id"]
            label_clean = meta["label"]
            subcategory = meta["subcategory"]

            body_lines = []
            skip_lines = {
                f"**{label_raw}**".strip(),
                definition.strip()
            }
            i += 1
            while i < len(buffer) and not item_pattern.match(buffer[i]) and not category_pattern.match(buffer[i]):
                line_clean = buffer[i].strip()
                if line_clean not in skip_lines:
                    body_lines.append(buffer[i])
                i += 1

            body = "\n".join(body_lines)

            code_md = ""
            code_blocks = code_block_pattern.findall(body)
            for j, (lang, code) in enumerate(code_blocks):
                lang = lang if lang else "txt"
                filename = f"{item_id}_snippet_{j+1}.{lang}"
                code_path = code_dir / filename
                with open(code_path, "w", encoding="utf-8") as cf:
                    cf.write(code.strip())
                code_md += f"\n[View Code Sample](../../code/{source_name}/{filename})\n"

            definition_clean = code_block_pattern.sub("", definition).strip()

            frontmatter = f"""---
id: {item_id}
label: {label_clean}
definition: {definition_clean}
category: {category}
language: en
status: approved
source: {source_name}"""
            if subcategory:
                frontmatter += f"\nsubcategory: {subcategory}"
            frontmatter += "\n---"

            draft_md = f"{frontmatter}\n\n{body}\n{code_md}"
            file_path = target_dir / f"{item_id}.md"
            with open(file_path, "w", encoding="utf-8") as out:
                out.write(draft_md)
            print(f"✅ Created: {source_name}/{item_id}.md")
        else:
            i += 1

# === MAIN LOOP ===
for source_file in SOURCE_FILES:
    source_name = source_file.stem.replace(" ", "_").replace("(", "").replace(")", "")
    target_dir = Path(f"../drafts/{source_name}")
    code_dir = Path(f"../code/{source_name}")
    os.makedirs(target_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)

    print(f"\n📄 Processing: {source_file.name}")
    current_category = "Uncategorized"
    buffer = []

    with open(source_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if category_pattern.match(line):
                if buffer:
                    process_buffer(buffer, current_category, source_name, target_dir, code_dir)
                    buffer = []
                current_category = category_pattern.match(line).group(1).strip()
            else:
                buffer.append(line)

    if buffer:
        process_buffer(buffer, current_category, source_name, target_dir, code_dir)