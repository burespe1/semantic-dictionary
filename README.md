# Semantic Dictionary 📚

![Version](https://img.shields.io/github/v/tag/burespe1/semantic-dictionary?label=version&style=flat-square)
![License](https://img.shields.io/github/license/burespe1/semantic-dictionary?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/burespe1/semantic-dictionary?style=flat-square)
![Issues](https://img.shields.io/github/issues/burespe1/semantic-dictionary?style=flat-square)
![Build](https://github.com/burespe1/semantic-dictionary/actions/workflows/release.yml/badge.svg)
![Build](https://github.com/burespe1/semantic-dictionary/actions/workflows/preview.yml/badge.svg)

A structured dictionary of **transport-related concepts** defined in delegated regulations of the [ITS Directive](https://eur-lex.europa.eu/eli/dir/2010/40/oj/eng), managed in Markdown. Includes human-readable previews, releases and machine-readable RDF.

## 📁 Structure

- `drafts/`: Individual Markdown entries grouped by delegated regulation
- `preview/`: Auto-generated browsable review files (one per DR)
- `release/`: Final published dictionary for each tagged version
- `vocab/`: RDF files (Turtle format) for each concept
- `scripts/`: Python automation for preview and release generation
- `images/`, `code/`: Optional media and supporting examples

## 🚀 Workflows

### Content Creation

The work on **transport-related concepts** aka **data types** is done in the `drafts/` folder in the subfolder per delegated regulation. Each data type is a separate markdown document (fragment), with predefined attributes and "free" content. 

See [`drafts/README.md`](drafts/README.md) for the detailed instructions.

### 🔄 Preview auto-generation

Triggered automatically on each push to:

- `drafts/**`
- `code/**`
- `scripts/generate_preview.py`

Generates:

- [`preview/INDEX.md`](preview/INDEX.md) – an index file with links to individual data type file fragments with their statuses.
- `preview/DR_*.md` – review file of data types definitions, one per delegated regulation
- Commits updated previews back to the repository
- Uploads preview files as GitHub Actions artifact

### 🏁 Release Workflow

Triggered automatically when a version tag is pushed (e.g. `v1.0.0`):

```bash
git tag v1.0.0
git push origin v1.0.0
```

Generates:

- `release/DR_*.md` – versioned release file of data types definitions, one per delegated regulation
- `vocab/<DR>/<item>.ttl` – SKOS-formatted RDF files from data types strict-definitions
- Uploads files as a downloadable GitHub Actions artifact

## 🌍 Published Outputs

- 📦 List of Preview Dictionary items:  [`preview/INDEX.md`](drafts/INDEX.md)
- 📦 Release Dictionaries:  [`release/README.md`](release/README.md)
- 🐢 RDF Vocabularies: [`vocab/`](vocab/)

## 🛠 Technologies

- Python 3.10+ with pyyaml, rdflib
- SKOS (RDF vocabulary)
- GitHub Actions automation
- Markdown + YAML frontmatter

## 💬 License & Contributions

Open-source under the MIT License. Contributions are welcome—just submit a PR or open an issue.
