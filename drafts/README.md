# 📄 Draft Dictionary Items
This folder contains draft entries for semantic dictionary concepts, written in Markdown format with metadata in front matter. Each file includes:

- YAML frontmatter for metadata (e.g. label, definition, language, status)
- Rich content like text, code, and image references

**Workflow**: Drafts are manually edited. Previews are auto-generated in each commit by `generate_preview.py`, and only approved entries are included in releases.

**Index of working definitions**: [list of definitions with their status](INDEX.md)
¨
## 🧱 File Structure

Each file must:
- Use .md extension
- Start with a YAML metadata block (between --- lines)
- Include a human-readable definition and optionally commentary, diagrams, or citations

### 🧾 Metadata Fields

| Field | Description | 
| - | - | 
| id | Unique lowercase identifier for the concept (also used as filename) | 
| label | Human-friendly title | 
| definition | Concise explanation of the concept's meaning | 
| category | Domain or grouping the concept belongs to | 
| language | Language code of the definition (e.g. en) | 
| status | Approval state (draft, review, approved, etc.) | 
| source | Citable source or reference (standard, report, etc.) | 
| subcategory | sub grouping the concept belongs to |

## 🧠 Example

Here’s an example draft file named: road-classification.md

```markdown
---
id: road-classification
label: road classification
definition: the minimum information required for distinguishing the links of a road network encompassing form of way, functional, or other concerns.
category: Types of data on infrastructure
language: en
status: in review
source: DR_EU_2022-670
---

**Road classification:**  
the minimum information required for distinguishing the links of a road network encompassing form of way, functional, or other concerns.

> According to ETSI TS 102 894-2 (DE=RoadType), road types are distinguished based on two parameters:  
> (a) urban versus non-urban roads and  
> (b) roads with versus without structural separation to opposite lanes.

> An extended **classification** is provided by the INSPIRE data specification on transport networks... *(truncated)*

![Figure 2](/Figures/RTTI_fig_2.png)
```
This structure allows automated parsing of metadata while retaining rich, readable content for users and editors alike.
