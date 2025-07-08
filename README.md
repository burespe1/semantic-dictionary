# Semantic Dictionary 📚

A structured dictionary of transport-related concepts managed in Markdown, exported as Linked Open Data (LOD) using SKOS vocabulary. Includes human-readable previews, machine-readable RDF, and published releases via GitHub Pages.

## 📁 Structure

- `drafts/`: Individual Markdown entries grouped by delegated regulation
- `preview/`: Auto-generated browsable review files (one per DR)
- `release/`: Final published dictionary for each tagged version
- `vocab/`: RDF files (Turtle format) for each concept
- `scripts/`: Python automation for preview and release generation
- `images/`, `code/`: Optional media and supporting examples

## 🚀 Workflows

### 🔄 Content Creation

The work on data types is done in the `drafts/` folder in the subfolder per delegated regulation. Each data type is a separate markdown document, with predefined attributes and "free" content. 

### 🔄 Preview auto-generation

Triggered automatically on each push to:

- `drafts/**`
- `code/**`
- `scripts/generate_preview.py`

Generates:

- `preview/DR_*.md` – one review file per delegated regulation
- Commits updated previews back to the repository
- Uploads preview files as GitHub Actions artifact

### 🏁 Release Workflow

Triggered automatically when a version tag is pushed (e.g. `v1.0.0`):

```bash
git tag v1.0.0
git push origin v1.0.0
```

This executes:
- scripts/generate_release.py to compile approved entries and RDF vocabularies
- Generates release/dictionary.md – consolidated Markdown export
- Creates vocab/<DR>/<item>.ttl – SKOS-formatted RDF files
- Uploads files as a downloadable GitHub Actions artifact

## 🌍 Published Outputs
- 📦 Preview Dictionaries:  [`drafts/readme.md`](drafts/readme.md)
- 📦 Release Dictionaries:  [`release/index.md`](release/index.md)
- 🐢 RDF Vocabularies: [`vocab/`](vocab/)
- 🌐 Live Site via GitHub Pages: https://yourusername.github.io/semantic-dictionary

## 🛠 Technologies
- Python 3.10+ with pyyaml, rdflib
- SKOS (RDF vocabulary)
- GitHub Actions automation
- Markdown + YAML frontmatter

## 💬 License & Contributions

Open-source under the MIT License. Contributions are welcome—just submit a PR or open an issue.
