# Migration Guide: v1 → v2 (Human-Readable Names)

## Summary of Changes

**Goal:** Make all file and column names human-readable and self-documenting for a multilingual, multi-jurisdictional legal translation project.

---

## File Name Changes

| Old File Name | New File Name | Purpose |
|---------------|---------------|---------|
| `legislation_terms_cleaned.csv` | `dictionary_nl_de_legal_terms.csv` | Dutch-German legal term pairs |
| `schema_source_documents.csv` | `registry_legal_sources.csv` | Legal document metadata |
| `schema_term_occurrences.csv` | `examples_term_usage_in_sources.csv` | Term usage examples |

---

## Column Name Changes

### Dictionary File

| Old Column | New Column | Notes |
|------------|------------|-------|
| `id` | `dictionary_term_id` | More descriptive |
| `source` | `term_nl` | Explicitly Dutch |
| `lang-source` | `language_nl` | Clear naming |
| `target` | `term_de` | Explicitly German |
| `lang-target` | `language_de` | Clear naming |
| `author` | `translator_name` | Role clarity |
| `license` | `usage_license` | Purpose clarity |
| `sme-reviewed` | `expert_reviewed` | Less jargon |
| `premium` | `premium_content` | More descriptive |
| `lang-target-dict` | `external_dictionary_reference` | Self-documenting |
| (new) | `term_category` | Added for filtering |
| (new) | `legal_domain` | Added for filtering |

### Legal Sources Registry

| Old Column | New Column | Notes |
|------------|------------|-------|
| `doc_id` | `source_id` | Clearer purpose |
| `doc_type` | `source_type` | Consistent naming |
| `doc_subtype` | `source_subtype` | Consistent naming |
| `parties` | `treaty_parties` | More specific |
| `languages` | `available_languages` | More descriptive |
| `date` | `effective_date` | Specify which date |
| `file_path` | `xml_file_path` | Specify format |
| `url` | `official_url` | Specify type |
| `jurisdiction` | `legal_jurisdiction` | Domain clarity |
| `status` | `current_status` | Temporal clarity |
| (new) | `country_nl` | Added for multilingual |
| (new) | `country_de` | Added for multilingual |
| (new) | `full_title_nl` | Complete Dutch title |
| (new) | `full_title_de` | Complete German title |
| (new) | `short_title_nl` | Short Dutch reference |
| (new) | `short_title_de` | Short German reference |

### Term Usage Examples

| Old Column | New Column | Notes |
|------------|------------|-------|
| `occurrence_id` | `example_id` | More intuitive |
| `term_id` | `dictionary_term_id` | Shows relationship |
| `doc_id` | `legal_source_id` | Shows relationship |
| `xpath` | `xml_location_xpath` | Specify format |
| `element_type` | `location_type` | Clearer meaning |
| `article_id` | `article_number` | More accurate |
| `context_nl` | `example_sentence_nl` | More descriptive |
| `context_de` | `example_sentence_de` | More descriptive |
| `term_frequency_in_doc` | `term_appears_in_source_count` | Self-documenting |
| `is_definition` | `is_legal_definition` | Domain-specific |
| `notes` | `usage_notes` | Purpose clarity |
| (new) | `article_title_nl` | Added article context |
| (new) | `article_title_de` | Added article context |

---

## Value Format Changes

### Boolean Values
**Old:** `TRUE` / `FALSE`
**New:** `yes` / `no`

**Rationale:** More natural language, clearer to non-technical users

**Example:**
```csv
# Old
sme-reviewed,premium
TRUE,FALSE

# New
expert_reviewed,premium_content
yes,no
```

### IDs
**Old:** Technical IDs like `bwbv0005862-2022-07-31`
**New:** Human-readable like `nl-de-tax-treaty-2012`

**Example:**
```csv
# Old
doc_id
bwbv0005862-2022-07-31

# New
source_id
nl-de-tax-treaty-2012
```

---

## Migration Script

### Quick Rename (Bash)

```bash
# Rename files
mv legislation_terms_cleaned.csv dictionary_nl_de_legal_terms.csv
mv legislation_terms_cleaned.tsv dictionary_nl_de_legal_terms.tsv
mv schema_source_documents.csv registry_legal_sources.csv
mv schema_term_occurrences.csv examples_term_usage_in_sources.csv

# Update column headers in CSV files
# (Manual edit or use sed/awk)
```

### Python Migration Script

```python
import pandas as pd

# Migrate Dictionary
df_dict = pd.read_csv('legislation_terms_cleaned.csv')
df_dict.rename(columns={
    'id': 'dictionary_term_id',
    'source': 'term_nl',
    'lang-source': 'language_nl',
    'target': 'term_de',
    'lang-target': 'language_de',
    'author': 'translator_name',
    'license': 'usage_license',
    'sme-reviewed': 'expert_reviewed',
    'premium': 'premium_content',
    'lang-target-dict': 'external_dictionary_reference'
}, inplace=True)

# Convert booleans
df_dict['expert_reviewed'] = df_dict['expert_reviewed'].map({True: 'yes', 'TRUE': 'yes', False: 'no', 'FALSE': 'no'})
df_dict['premium_content'] = df_dict['premium_content'].map({True: 'yes', 'TRUE': 'yes', False: 'no', 'FALSE': 'no'})

# Add new columns
df_dict['term_category'] = ''
df_dict['legal_domain'] = ''

df_dict.to_csv('dictionary_nl_de_legal_terms.csv', index=False)

# Migrate Registry
df_reg = pd.read_csv('schema_source_documents.csv')
df_reg.rename(columns={
    'doc_id': 'source_id',
    'doc_type': 'source_type',
    'doc_subtype': 'source_subtype',
    'parties': 'treaty_parties',
    'languages': 'available_languages',
    'date': 'effective_date',
    'file_path': 'xml_file_path',
    'url': 'official_url',
    'jurisdiction': 'legal_jurisdiction',
    'status': 'current_status'
}, inplace=True)

# Add new columns
df_reg['country_nl'] = ''
df_reg['country_de'] = ''
df_reg['full_title_nl'] = ''
df_reg['full_title_de'] = ''
df_reg['short_title_nl'] = ''
df_reg['short_title_de'] = ''

df_reg.to_csv('registry_legal_sources.csv', index=False)

# Migrate Examples
df_ex = pd.read_csv('schema_term_occurrences.csv', sep='\t')  # if TSV
df_ex.rename(columns={
    'occurrence_id': 'example_id',
    'term_id': 'dictionary_term_id',
    'doc_id': 'legal_source_id',
    'xpath': 'xml_location_xpath',
    'element_type': 'location_type',
    'article_id': 'article_number',
    'context_nl': 'example_sentence_nl',
    'context_de': 'example_sentence_de',
    'term_frequency_in_doc': 'term_appears_in_source_count',
    'is_definition': 'is_legal_definition',
    'notes': 'usage_notes'
}, inplace=True)

# Convert booleans
df_ex['is_legal_definition'] = df_ex['is_legal_definition'].map({True: 'yes', 'TRUE': 'yes', False: 'no', 'FALSE': 'no'})

# Add new columns
df_ex['article_title_nl'] = ''
df_ex['article_title_de'] = ''

df_ex.to_csv('examples_term_usage_in_sources.csv', index=False)
```

---

## Verification Checklist

After migration, verify:

- [ ] All file names use new convention
- [ ] All column names updated
- [ ] Boolean values are `yes/no` (not `TRUE/FALSE`)
- [ ] Source IDs are human-readable
- [ ] New columns added with empty values
- [ ] All data preserved (row count unchanged)
- [ ] CSV files properly formatted
- [ ] No data corruption

---

## Backward Compatibility

### If You Need Old Format

Keep old files as backup:
```bash
cp legislation_terms_cleaned.csv legislation_terms_cleaned.csv.backup
```

Create conversion script for legacy systems:
```python
def convert_to_v1(v2_file):
    """Convert v2 format back to v1 if needed."""
    df = pd.read_csv(v2_file)

    # Reverse column renaming
    old_columns = {
        'dictionary_term_id': 'id',
        'term_nl': 'source',
        # ... etc
    }

    df.rename(columns=old_columns, inplace=True)
    df['sme-reviewed'] = df['expert_reviewed'].map({'yes': 'TRUE', 'no': 'FALSE'})

    return df
```

---

## Benefits After Migration

✅ **Clarity:** Column names self-document their purpose
✅ **Multilingual Ready:** Pattern extends to any language
✅ **Non-Technical Friendly:** Legal professionals can understand structure
✅ **Scalable:** Easy to add jurisdictions, languages, source types
✅ **Maintainable:** Changes are obvious in version control
✅ **Professional:** Ready for production use

---

## Questions?

See:
- `NAMING_CONVENTIONS.md` - Complete naming standards
- `LINKING_ARCHITECTURE_v2.md` - Updated architecture with new names
- `example_linking_structure.json` - JSON examples with new format
