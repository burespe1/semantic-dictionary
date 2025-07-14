# Scripts Folder ⚙️

Python scripts for generating previews and releases.

- 🧪 `generate_preview.py`: scans all Markdown files in drafts/, reads their frontmatter, and outputs cleaned versions to preview.
- 🚀 `generate_release.py`: Extracts approved drafts, merges them into a single dictionary.md in release/, and outputs RDF to vocab/.

Dependencies:
```bash
pip install pyyaml rdflib
```