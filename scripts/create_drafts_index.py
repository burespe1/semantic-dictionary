import yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DRAFT_ROOT = PROJECT_ROOT / "drafts"
INDEX_PATH = DRAFT_ROOT / "index.md"

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
    
def extract_frontmatter(md_file):
    with md_file.open("r", encoding="utf-8") as f:
        md_text = f.read()   
        
    parts = md_text.split('---')
    if len(parts) < 3:
        return None

    raw_yaml = escape_yaml_block(parts[1])
    try:
        meta = yaml.safe_load(raw_yaml)
    except yaml.YAMLError as e:
        print(f"⚠️ YAML error: {e}")
        return None

    return meta

def build_index():
    entries = []

    for md_file in DRAFT_ROOT.rglob("*.md"):
        if md_file.name == "index.md":
            continue  # Skip self

        meta = extract_frontmatter(md_file)
        if not meta:
            continue

        label = meta.get("label", md_file.stem).strip()
        status = meta.get("status", "unknown").strip()
        relative_path = md_file.relative_to(DRAFT_ROOT).as_posix()
        link = f"[{label}]({relative_path})"
        entries.append((label.lower(), f"- {link} — **{status}**"))

    if entries:
        header = "# 📚 Drafts Master Index\n\n"
        content = "\n".join(sorted([entry[1] for entry in entries]))
        INDEX_PATH.write_text(header + content + "\n", encoding="utf-8")
        print(f"✅ Master index created at: {INDEX_PATH}")
    else:
        print("⚠️ No valid draft entries found.")

if __name__ == "__main__":
    build_index()