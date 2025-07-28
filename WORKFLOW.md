# 🛠️ Definition Processing Workflow

A structured process for refining definitions with explanatory notes, status tracking, and assigned codes.

## 🔁 Example Status Lifecycle

| Status        | Description                           |
|---------------|---------------------------------------|
| `draft`       | Initial, unreviewed definition        |
| `in review`   | Undergoing peer or expert evaluation  |
| `finalised`   | Updated after feedback - no changes   |
| `modified`    | Updated after feedback - changes      |
| `approved`    | Final version, validated              |
| `deprecated`  | No longer in active use               |
| `unknown`     | status unknown                        |


## 1. Initial Capture

- Collect raw definitions from reliable sources.
- Assign preliminary status: `Draft`.
- Add basic metadata (source, category, id, definition, status, subcategory).

---

## 2. Semantic Enrichment

Enhance each definition for clarity and utility.

### 🔍 Refinement

- Clarify wording and correct inconsistencies.
- Align terminology to domain standards.

### 📝 Explanatory Notes

- Provide background context.
- Include usage examples and edge cases.
- Note any assumptions or limitations.
- provide code samples and explanatory images

## 3. Peer review Cycle

- Assign tag `in review`
- Submit enriched definition for peer or domain expert review.
- Reviewers may:
  - Suggest edits
  - Append comments
  - Approve or reject
- Track all revisions and feedback history.

- Once reviewed assign tag `finalised` if accepted as is, or `modified` if there are changes to the definitions.

## 4. Approval

- Once peer reviewed with statuses `finalised` or `modified` submit for the approval in regular cycles
- if accepted update status to `approved`.
- if not accepted update status to `draft` for more changes.

## 5. Publishing & Discovery

- Generate versioned release files of definitions to `release/DR_*.md`
- Generate semantic vocabulary to `vocab/<DR>/<item>.ttl`
- Upload files as a downloadable GitHub Actions artifact under a versioned release tag.

## 6. Change Management

- New updates initiate a fresh workflow cycle.
- Maintain changelog for each definition.
- if the concept is no longer needed of replaced by new concept update status to `deprecated`.
- Support rollback or restore previous versions.

---

