DR_TITLES = {
    "SRTI": "Safety-Related Traffic Information",
    "MMTIS": "Multimodal Travel Information Services",
    "RTTI": "Real-Time Traffic Information",
    "SSTP": "Safe and Secure Truck Parking"
}

import os
import yaml
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import SKOS, RDF
from datetime import datetime

ROOT = "../drafts"
RELEASE_DIR = "../release"
VOCAB_DIR = "../vocab"
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
    g.add((term, RDF.type, SKOS.Concept))
    g.add((term, SKOS.prefLabel, Literal(meta['label'], lang=meta['language'])))
    g.add((term, SKOS.definition, Literal(meta['definition'], lang=meta['language'])))
    if 'related' in meta:
        g.add((term, SKOS.related, EX[meta['related']]))
    return g

def process_dr_folder(dr_folder):
    release_file = os.path.join(RELEASE_DIR, f"{dr_folder}.md")
    vocab_path = os.path.join(VOCAB_DIR, dr_folder)
    os.makedirs(vocab_path, exist_ok=True)

    combined_md = f"# {DR_TITLES.get(dr_folder, dr_folder)} Vocabulary ({dr_folder})\n\n"

    draft_path = os.path.join(ROOT, dr_folder)
    for fname in os.listdir(draft_path):
        if not fname.endswith(".md"):
            continue

        file_path = os.path.join(draft_path, fname)
        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read()

        meta, body = extract_md_parts(raw)
        if not meta or meta.get("status") != "approved":
            print(f"⏩ Skipping {fname} in {dr_folder}")
            continue

        # Add to Markdown
        entry_md = f"## {meta['label']}\n\n**Definition**: {meta['definition']}\n\n{body}\n\n---\n"
        combined_md += entry_md

        # Generate RDF
        rdf_graph = generate_rdf(meta)
        rdf_graph.serialize(destination=os.path.join(vocab_path, f"{meta['id']}.ttl"), format="turtle")

        print(f"✅ Released {meta['id']} in {dr_folder}")

        timestamp = datetime.now().strftime("%Y-%m-%d")
        combined_md += f"\n_Last updated: {timestamp}_\n"

        with open(release_file, "w", encoding="utf-8") as out:
            out.write(combined_md)
        print(f"📦 Created release: {release_file}")


def main():
    os.makedirs(RELEASE_DIR, exist_ok=True)
    os.makedirs(VOCAB_DIR, exist_ok=True)

    for dr_folder in os.listdir(ROOT):
        if os.path.isdir(os.path.join(ROOT, dr_folder)):
            process_dr_folder(dr_folder)

    print("\n🎉 All DR vocabularies released!")

if __name__ == "__main__":
    main()