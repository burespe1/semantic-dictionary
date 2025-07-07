# Semantic Dictionary 📚

A structured dictionary of concepts managed in Markdown, exported as Linked Open Data (LOD) using SKOS vocabulary. Includes human-readable previews, machine-readable RDF, and published releases via GitHub Pages.

## 📁 Structure

- `drafts/`: Individual Markdown entries (can include images and code)
- `preview/`: Automatically generated review files
- `release/`: Final published dictionary with approved entries
- `vocab/`: RDF files exported from release items
- `scripts/`: Python scripts for automation (preview + release)
- `images/`, `code/`: Optional supporting media

## 🚀 Workflows

- Run `scripts/generate_preview.py` to generate entry previews.
- Run `scripts/generate_release.py` to build release files and export RDF.
- GitHub Actions automate preview on draft updates and release on version tags.

## 🌍 Published Outputs

- **Combined dictionary:** [`release/dictionary.md`](release/dictionary.md)
- **RDF vocabularies:** [`vocab/`](vocab/)
- **Website:** [GitHub Pages](https://yourusername.github.io/semantic-dictionary) ← update URL!

## 🛠 Technologies

- Python 3 + `pyyaml`, `rdflib`
- SKOS (RDF vocabulary)
- GitHub Actions
- Markdown + YAML frontmatter

## 💬 License & Contributions

Open-source under the MIT License. Contributions are welcome—just submit a PR or open an issue.
