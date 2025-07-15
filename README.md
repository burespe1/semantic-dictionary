# Semantic Dictionary 📚

![Version](https://img.shields.io/github/v/tag/burespe1/semantic-dictionary?label=version&style=flat-square)
![License](https://img.shields.io/github/license/burespe1/semantic-dictionary?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/burespe1/semantic-dictionary?style=flat-square)
![Issues](https://img.shields.io/github/issues/burespe1/semantic-dictionary?style=flat-square)
![Build](https://github.com/burespe1/semantic-dictionary/actions/workflows/release.yml/badge.svg)
![Build](https://github.com/burespe1/semantic-dictionary/actions/workflows/preview.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.13-blue?style=flat-square)


![Stars](https://img.shields.io/github/stars/burespe1/semantic-dictionary?style=social)
![Forks](https://img.shields.io/github/forks/burespe1/semantic-dictionary?style=social)
![Watchers](https://img.shields.io/github/watchers/burespe1/semantic-dictionary?style=social)

A structured dictionary of transport-related concepts defined in delegated regulations of the ITS Directive, managed in Markdown, exported as Linked Open Data (LOD) using SKOS vocabulary. Includes human-readable previews, machine-readable RDF, and published releases via GitHub Pages.

## 📁 Structure

- `drafts/`: Individual Markdown entries grouped by delegated regulation
- `preview/`: Auto-generated browsable review files (one per DR)
- `release/`: Final published dictionary for each tagged version
- `vocab/`: RDF files (Turtle format) for each concept
- `scripts/`: Python automation for preview and release generation
- `images/`, `code/`: Optional media and supporting examples

## 🚀 Workflows

### Content Creation

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

- 📦 Preview Dictionaries:  [`drafts/README.md`](drafts/README.md)
- 📦 Release Dictionaries:  [`release/INDEX.md`](release/INDEX.md)
- 🐢 RDF Vocabularies: [`vocab/`](vocab/)
- 🌐 Live Site via GitHub Pages: https://yourusername.github.io/semantic-dictionary

## 🛠 Technologies

- Python 3.10+ with pyyaml, rdflib
- SKOS (RDF vocabulary)
- GitHub Actions automation
- Markdown + YAML frontmatter

## 💬 License & Contributions

Open-source under the MIT License. Contributions are welcome—just submit a PR or open an issue.
