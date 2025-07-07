# Drafts Folder 📝

This folder contains individual dictionary entries in Markdown format. Each file includes:

- YAML frontmatter for metadata (e.g. label, definition, language, status)
- Rich content like text, code, and image references

**Workflow**: Drafts are manually edited. Previews are auto-generated via `generate_preview.py`, and only approved entries are included in releases.

Use `status: approved` in frontmatter when ready for publishing.

Example:

```yaml
---
id: apple
label: Apple
definition: A sweet fruit that grows on trees.
language: en
status: approved
---