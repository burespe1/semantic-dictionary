import os
import yaml
from pathlib import Path
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import SKOS, RDF
from datetime import datetime

DR_TITLES = {
    "SRTI": "Safety-Related Traffic Information",
    "MMTIS": "Multimodal Travel Information Services",
    "RTTI": "Real-Time Traffic Information",
    "SSTP": "Safe and Secure Truck Parking"
}

ROOT = Path("../drafts")
RELEASE_DIR = Path("../release")
VOCAB_DIR = Path("../vocab")
EX = Namespace("http://example.org/dictionary#")

def extract_md_parts(md_text):
    parts = md_text.split('---')
    if len(parts) < 3:
        return None, ''
    meta = yaml.safe_load(parts[1])
    content = '---'.join(parts[2:]).strip()
    return meta, content

def generate_rdf(meta):
    g = Graph()
    term = EX[meta['id']]
    lang = meta.get('language', 'en')
    g.add((term, RDF.type, SKOS.Concept))
    g.add((term, SKOS.prefLabel, Literal(meta['label'], lang=lang)))
    g.add((term, SKOS.definition, Literal(meta['definition'], lang=lang)))
    if 'related' in meta:
        g.add((term, SKOS.related, EX[meta['related']]))
    return g

def process_dr_folder(dr_folder):
    release_file = RELEASE_DIR / f"{dr_folder}.md"
    vocab_path = VOCAB_DIR / dr_folder
    os.makedirs(vocab_path, exist_ok=True)

    title = DR_TITLES.get(dr_folder, dr_folder)
    combined_md = f"# {title} Vocabulary ({dr_folder})\n\n"

    draft_path = ROOT / dr_folder
    items = []

    for md_file in draft_path.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            raw = f.read()

        meta, body = extract_md_parts(raw)
        if not meta or meta.get("status") != "approved":
            print(f"⏩ Skipping {md_file.name} in {dr_folder}")
            continue

        items.append((meta['label'], meta, body))

    # Sort items by label
    items.sort(key=lambda x: x[0].lower())

    for label, meta, body in items:
        entry_md = f"## {meta['label']}\n\n**Definition**: {meta['definition']}\n\n{body}\n\n---\n"
        combined_md += entry_md

        rdf_graph = generate_rdf(meta)
        rdf_graph.serialize(destination=vocab_path / f"{meta['id']}.ttl", format="turtle")

        print(f"✅ Released {meta['id']} in {dr_folder}")

    timestamp = datetime.now().strftime("%Y-%m-%d")
    combined_md += f"\n_Last updated: {timestamp}_\n"

    with open(release_file, "w", encoding="utf-8") as out:
        out.write(combined_md)

    print(f"📦 Created release: {release_file.name}")

def main():
    os.makedirs(RELEASE_DIR, exist_ok=True)
    os.makedirs(VOCAB_DIR, exist_ok=True)

    for dr_folder in ROOT.iterdir():
        if dr_folder.is_dir():
            process_dr_folder(dr_folder.name)

    print("\n🎉 All DR vocabularies released!")

if __name__ == "__main__":
    main()