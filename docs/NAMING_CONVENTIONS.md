# Naming Conventions for Multilingual Legal Translation Project

## Design Philosophy

**Human-Readable First:** All file names, column names, and identifiers should be understandable by legal professionals, translators, and non-technical users who may work with multiple languages and jurisdictions.

**Self-Documenting:** Names should clearly indicate what data they contain without needing external documentation.

**Consistent Patterns:** Similar types of data use similar naming patterns across languages and sources.

---

## File Naming

### Core Data Files

| File Name | Purpose | Content |
|-----------|---------|---------|
| `dictionary_{source_lang}_{target_lang}_legal_terms.csv` | Bilingual terminology | Translation pairs with metadata |
| `registry_legal_sources.csv` | Document registry | Metadata for all treaties, legislation, cases |
| `examples_term_usage_in_sources.csv` | Usage examples | Links terms to actual usage in legal texts |

### Language-Specific Examples

```
dictionary_nl_de_legal_terms.csv        # Dutch ↔ German
dictionary_nl_en_legal_terms.csv        # Dutch ↔ English (future)
dictionary_de_fr_legal_terms.csv        # German ↔ French (future)
dictionary_nl_de_en_legal_terms.csv     # Trilingual (future)
```

### Source-Specific Organization

```
translation-dictionaries/
├── netherlands/
│   ├── nl-nl-to-de-de.csv              # Current structure
│   └── nl-nl-to-en-gb.csv              # Future
├── germany/
│   └── de-de-to-en-gb.csv              # Future
└── international/
    └── treaties/
        └── nl-de-tax-treaty-terms.csv  # Treaty-specific
```

---

## Column Naming

### General Principles

1. **Full words, not abbreviations**: `dictionary_term_id` not `term_id`
2. **Explicit language markers**: `term_nl`, `term_de` not `source`, `target`
3. **Action-oriented for booleans**: `expert_reviewed` not `sme_reviewed`
4. **Clear relationships**: `legal_source_id` references `source_id` in registry

### Dictionary File Columns

| Column Name | Old Name | Type | Description | Example |
|-------------|----------|------|-------------|---------|
| `dictionary_term_id` | `id` | UUID | Unique term identifier | `a7714aec-...` |
| `term_nl` | `source` | text | Dutch legal term | `Verdrag` |
| `language_nl` | `lang-source` | code | Dutch language code | `nl-nl` |
| `term_de` | `target` | text | German legal term | `Abkommen` |
| `language_de` | `lang-target` | code | German language code | `de-de` |
| `translator_name` | `author` | text | Who created this translation | `van Gassen` |
| `usage_license` | `license` | text | Usage rights | `All rights reserved` |
| `expert_reviewed` | `sme-reviewed` | yes/no | Subject matter expert verified | `yes` |
| `premium_content` | `premium` | yes/no | Requires paid access | `no` |
| `external_dictionary_reference` | `lang-target-dict` | text | Link to external dictionary | (empty) |
| `term_category` | (new) | category | Type of term | `tax_concept` |
| `legal_domain` | (new) | domain | Legal field | `tax_law` |

### Legal Sources Registry Columns

| Column Name | Old Name | Type | Description | Example |
|-------------|----------|------|-------------|---------|
| `source_id` | `doc_id` | text | Short, human-readable ID | `nl-de-tax-treaty-2012` |
| `source_type` | `doc_type` | enum | treaty/legislation/case_law | `treaty` |
| `source_subtype` | `doc_subtype` | enum | Specific category | `tax_treaty` |
| `country_nl` | (new) | text | Country name in Dutch | `Nederland` |
| `country_de` | (new) | text | Country name in German | `Deutschland` |
| `treaty_parties` | `parties` | list | Participating countries | `Netherlands\|Germany` |
| `available_languages` | `languages` | list | Available translations | `nl-nl\|de-de` |
| `effective_date` | `date` | date | When it took effect | `2012-04-01` |
| `xml_file_path` | `file_path` | path | Relative path to XML | `legislation/.../file.xml` |
| `official_url` | `url` | url | Official publication source | `https://wetten.overheid.nl/...` |
| `legal_jurisdiction` | `jurisdiction` | enum | international/national/eu | `international` |
| `current_status` | `status` | enum | in_force/superseded/draft | `in_force` |
| `full_title_nl` | (new) | text | Complete official title (Dutch) | `Verdrag tussen...` |
| `full_title_de` | (new) | text | Complete official title (German) | `Abkommen zwischen...` |
| `short_title_nl` | (new) | text | Short reference title (Dutch) | `NL-DE Belastingverdrag 2012` |
| `short_title_de` | (new) | text | Short reference title (German) | `NL-DE Steuerabkommen 2012` |

### Term Usage Examples Columns

| Column Name | Old Name | Type | Description | Example |
|-------------|----------|------|-------------|---------|
| `example_id` | `occurrence_id` | text | Unique example identifier | `example-001` |
| `dictionary_term_id` | `term_id` | UUID | → Links to dictionary | `a7714aec-...` |
| `legal_source_id` | `doc_id` | text | → Links to registry | `nl-de-tax-treaty-2012` |
| `xml_location_xpath` | `xpath` | xpath | Where to find in XML | `//artikel[@id='artikel-5']` |
| `location_type` | `element_type` | enum | document_title/article_text/definition | `article_text` |
| `article_number` | `article_id` | text | Article/section number | `5` or `artikel-5` |
| `example_sentence_nl` | `context_nl` | text | Dutch sentence with term | Full sentence in Dutch |
| `example_sentence_de` | `context_de` | text | German sentence with term | Full sentence in German |
| `term_appears_in_source_count` | `term_frequency_in_doc` | number | How many times term appears | `35` |
| `is_legal_definition` | `is_definition` | yes/no | Is this a definitional usage? | `yes` |
| `usage_notes` | `notes` | text | Context notes | `Core definition in Article 5` |
| `article_title_nl` | (new) | text | Article heading (Dutch) | `Vaste inrichting` |
| `article_title_de` | (new) | text | Article heading (German) | `Betriebsstätte` |

---

## Identifiers (IDs)

### Human-Readable IDs for Legal Sources

**Format:** `{country1}-{country2}-{type}-{year}`

**Examples:**
```
nl-de-tax-treaty-2012           # Netherlands-Germany Tax Treaty
nl-vennootschapsbelasting-1969  # Dutch Corporate Income Tax Act
de-estg-2023                    # German Income Tax Act (EStG)
eu-directive-2018-822           # EU DAC6 Directive
ecj-case-c-123-2020             # European Court case
```

**Rationale:** Immediately recognizable without looking up UUID

### UUIDs for Dictionary Terms

**Format:** UUID v4 (e.g., `a7714aec-7e41-4852-a905-82443caa2dab`)

**Rationale:**
- Truly unique across all language pairs
- No conflicts when merging dictionaries
- Stable identifier for citations/references

### Sequential IDs for Examples

**Format:** `example-{number}` (e.g., `example-001`, `example-002`)

**Rationale:**
- Human-readable in spreadsheets
- Easy to reference in discussions
- Can be regenerated if needed

---

## Boolean Values

**Use:** `yes` / `no` (not `TRUE` / `FALSE` or `1` / `0`)

**Rationale:** Clear to non-technical users in any language

**Examples:**
```csv
expert_reviewed,premium_content,is_legal_definition
yes,no,yes
```

---

## Language Codes

**Format:** ISO 639-1 + ISO 3166-1 (e.g., `nl-nl`, `de-de`, `en-gb`, `fr-fr`)

**Always use lowercase** for consistency

**Include region** even for single-country languages:
- `nl-nl` not `nl` (distinguishes from `nl-be` Belgian Dutch)
- `de-de` not `de` (distinguishes from `de-at` Austrian German)
- `en-gb` or `en-us` (distinguishes variants)

---

## Enumerations (Controlled Vocabularies)

### source_type (Legal Source Types)

```
treaty               # International agreements
legislation          # National law (acts, codes)
regulation           # Administrative rules, decrees
case_law            # Court decisions
directive           # EU directives
commentary          # Legal commentary, doctrine
guidance            # Official guidance, circulars
```

### source_subtype (Specific Categories)

```
# Under treaty:
tax_treaty, trade_agreement, extradition_treaty, human_rights_convention

# Under legislation:
tax_act, corporate_law_act, civil_code, criminal_code

# Under case_law:
supreme_court, court_of_appeal, tax_court, ecj_ruling
```

### legal_jurisdiction

```
international       # Treaties, international law
national           # Single country legislation
eu                 # European Union law
regional           # Regional/provincial
bilateral          # Two-country agreement
```

### current_status

```
in_force           # Currently applicable
superseded         # Replaced by newer version
repealed           # No longer in effect
draft              # Proposed, not yet effective
consolidated       # Official consolidated version
```

### term_category

```
tax_concept        # General tax concepts
legal_entity       # Types of legal persons
procedural_term    # Procedural law terms
treaty_terminology # Treaty-specific language
proper_noun        # Names, places
residency_status   # Tax residency terms
location_type      # Geographic/location terms
```

---

## Multi-Value Fields

**Separator:** Pipe `|` (not comma, to avoid CSV conflicts)

**Examples:**
```
treaty_parties: Netherlands|Germany
available_languages: nl-nl|de-de|en-gb
related_terms: vaste inrichting|permanent establishment|Betriebsstätte
```

---

## Date Formats

**Format:** ISO 8601 `YYYY-MM-DD`

**Examples:**
```
2012-04-01          # Effective date
2022-07-31          # Last amended date
```

**Rationale:** Unambiguous, sortable, international standard

---

## File Paths

**Use:** Relative paths from project root

**Format:** Forward slashes `/` (cross-platform)

**Examples:**
```
legislation/netherlands/BWBV0005862_2022-07-31_0/BWBV0005862_2022-07-31_0.xml
case-law/netherlands/supreme-court/2023/HR-2023-145.xml
```

---

## Examples in Practice

### Adding a New Language Pair (Dutch-English)

**Dictionary file:**
```
dictionary_nl_en_legal_terms.csv

Columns:
dictionary_term_id, term_nl, language_nl, term_en, language_en, translator_name, ...
```

### Adding German Legislation

**Registry entry:**
```csv
source_id: de-estg-2023
source_type: legislation
source_subtype: tax_act
country_de: Deutschland
available_languages: de-de
full_title_de: Einkommensteuergesetz
short_title_de: EStG 2023
```

### Cross-Language Term Linking

When `Verdrag` (nl) = `Abkommen` (de) = `Treaty` (en):

Create separate dictionary files:
- `dictionary_nl_de_legal_terms.csv` with Dutch-German pair
- `dictionary_nl_en_legal_terms.csv` with Dutch-English pair
- `dictionary_de_en_legal_terms.csv` with German-English pair

Use **same UUID** if they represent the same concept, or different UUIDs if nuance differs.

---

## Migration Guide

### From Old to New Names

```bash
# Old → New file names
legislation_terms_cleaned.csv → dictionary_nl_de_legal_terms.csv
schema_source_documents.csv → registry_legal_sources.csv
schema_term_occurrences.csv → examples_term_usage_in_sources.csv

# Old → New column names
id → dictionary_term_id
source → term_nl
target → term_de
lang-source → language_nl
lang-target → language_de
sme-reviewed → expert_reviewed
TRUE/FALSE → yes/no
```

---

## Benefits of This System

✅ **Non-Technical Users:** Lawyers and translators can understand structure
✅ **Multi-Language Ready:** Pattern extends to any language pair
✅ **Self-Documenting:** Column names explain themselves
✅ **Scalable:** Easy to add jurisdictions, languages, source types
✅ **Version Control Friendly:** Clear diffs when data changes
✅ **International:** Language codes, date formats, paths are universal

---

## Quick Reference

| Concept | Format | Example |
|---------|--------|---------|
| Term ID | UUID v4 | `a7714aec-7e41-4852-a905-82443caa2dab` |
| Source ID | `country-type-year` | `nl-de-tax-treaty-2012` |
| Example ID | `example-NNN` | `example-001` |
| Language | `lang-region` | `nl-nl`, `de-de`, `en-gb` |
| Date | `YYYY-MM-DD` | `2012-04-01` |
| Boolean | `yes` / `no` | `yes` |
| Multi-value | `value\|value` | `Netherlands\|Germany` |
| File path | Relative, `/` separator | `legislation/.../file.xml` |
