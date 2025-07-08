import os
import yaml
from pathlib import Path
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import SKOS, RDF
from datetime import datetime
import shutil

ROOT = Path("../drafts")
VOCAB_DIR = Path("../vocab")
EX = Namespace("http://example.org/dictionary#")

def extract_metadata(md_text):
    parts = md_text.split('---')
    if len(parts) < 3:
        return None
    try:
        meta = yaml.safe_load(parts[1])
        return meta
    except yaml.YAMLError as e:
        print(f"⚠️ YAML error: {e}")
        return None

def generate_rdf(meta):
    g = Graph()
    term = EX[meta["id"]]
    lang = meta.get("language", "en")
    g.add((term, RDF.type, SKOS.Concept))
    g.add((term, SKOS.prefLabel, Literal(meta["label"], lang=lang)))
    g.add((term, SKOS.definition, Literal(meta["definition"], lang=lang)))
    if "related" in meta:
        g.add((term, SKOS.related, EX[meta["related"]]))
    return g

def process_folder(dr_folder):
    vocab_path = VOCAB_DIR / dr_folder
    draft_path = ROOT / dr_folder
    os.makedirs(vocab_path, exist_ok=True)

    for md_file in draft_path.glob("*.md"):
        with open(md_file, "r", encoding="utf-8") as f:
            raw = f.read()

        meta = extract_metadata(raw)
        if not meta or meta.get("status") != "approved":
            print(f"⏩ Skipping {md_file.name} in {dr_folder}")
            continue

        rdf_graph = generate_rdf(meta)
        rdf_graph.serialize(destination=vocab_path / f"{meta['id']}.ttl", format="turtle")
        print(f"✅ Serialized {meta['id']} → {vocab_path.name}/")

    # ⬇️ Also copy preview .md to release folder
    preview_file = Path("../preview") / f"{dr_folder}.md"
    if preview_file.exists():
        release_file = Path("../release") / f"{dr_folder}.md"
        shutil.copy2(preview_file, release_file)
        print(f"📄 Copied preview → release: {release_file.name}")
    else:
        print(f"⚠️ Preview not found for {dr_folder}")

def main():
    os.makedirs(VOCAB_DIR, exist_ok=True)

    for dr_folder in ROOT.iterdir():
        if dr_folder.is_dir():
            process_folder(dr_folder.name)

    print("\n🎉 All RDF vocabularies released!")

if __name__ == "__main__":
    main()