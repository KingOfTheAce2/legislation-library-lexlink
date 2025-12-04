# Linking Architecture v2: Dictionary ↔ Tax Treaty XML
## Human-Readable Edition

> **Updated:** Using human-readable file and column names for multilingual, multi-jurisdictional project

---

## Document Classification

**Source Type:** `treaty` (NOT `legislation`)
**Source Subtype:** `tax_treaty`
**Source ID:** `nl-de-tax-treaty-2012`
**Official Title:** Netherlands-Germany Double Taxation Avoidance Agreement

---

## Three-Layer Architecture

```
┌──────────────────────────────────┐
│ Translation Dictionary           │  ← dictionary_nl_de_legal_terms.csv
│ (Dutch ↔ German legal terms)    │     - 202 verified term pairs
│                                  │     - Expert-reviewed translations
│                                  │     - UUID identifiers
└────────────┬─────────────────────┘
             │
             │ linked via: dictionary_term_id
             ↓
┌──────────────────────────────────┐
│ Term Usage Examples              │  ← examples_term_usage_in_sources.csv
│ (Links terms to legal texts)    │     - term_id + source_id
│                                  │     - XPath locations in XML
│                                  │     - Bilingual example sentences
│                                  │     - Article references
└────────────┬─────────────────────┘
             │
             │ references: legal_source_id
             ↓
┌──────────────────────────────────┐
│ Legal Sources Registry           │  ← registry_legal_sources.csv
│ (Treaty/legislation metadata)   │     - Human-readable source_id
│                                  │     - Multilingual titles
│                                  │     - File paths & URLs
│                                  │     - Jurisdiction info
└────────────┬─────────────────────┘
             │
             │ points to XML file
             ↓
┌──────────────────────────────────┐
│ XML Source File                  │  ← BWBV0005862_2022-07-31_0.xml
│ (Authoritative treaty text)     │     - Full bilingual treaty
│                                  │     - Official publication
│                                  │     - Article structure
└──────────────────────────────────┘
```

---

## File Structure

```
legislation-library-lexlink/
│
├── dictionary_nl_de_legal_terms.csv         # 202 NL↔DE term pairs
├── registry_legal_sources.csv               # Treaty metadata
├── examples_term_usage_in_sources.csv       # Term → Treaty links
│
├── legislation/
│   └── netherlands/
│       └── BWBV0005862_2022-07-31_0/
│           └── BWBV0005862_2022-07-31_0.xml
│
├── NAMING_CONVENTIONS.md                    # Naming standards
└── LINKING_ARCHITECTURE_v2.md              # This document
```

---

## Data Model with Human-Readable Names

### Layer 1: Translation Dictionary
**File:** `dictionary_nl_de_legal_terms.csv`

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `dictionary_term_id` | UUID | Unique identifier | `a7714aec-7e41-4852-a905-82443caa2dab` |
| `term_nl` | text | Dutch legal term | `Verdrag` |
| `language_nl` | code | Dutch language code | `nl-nl` |
| `term_de` | text | German translation | `Abkommen` |
| `language_de` | code | German language code | `de-de` |
| `translator_name` | text | Who created translation | `van Gassen` |
| `usage_license` | text | Usage rights | `All rights reserved` |
| `expert_reviewed` | yes/no | SME verified | `yes` |
| `premium_content` | yes/no | Requires paid access | `no` |
| `external_dictionary_reference` | text | Link to external dict | (empty) |
| `term_category` | category | Type of term | `tax_concept` |
| `legal_domain` | domain | Legal field | `tax_law` |

**Example Row:**
```csv
a7714aec-...,Verdrag,nl-nl,Abkommen,de-de,van Gassen,All rights reserved,yes,no,,treaty_terminology,international_law
```

**Key Points:**
- Standalone reference: Works without accessing XML
- Language-explicit: `term_nl` and `term_de` (not generic "source/target")
- Boolean clarity: `yes/no` (not TRUE/FALSE)
- Categorized: `term_category` and `legal_domain` for filtering

---

### Layer 2: Legal Sources Registry
**File:** `registry_legal_sources.csv`

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `source_id` | text | Human-readable ID | `nl-de-tax-treaty-2012` |
| `source_type` | enum | treaty/legislation/case_law | `treaty` |
| `source_subtype` | enum | Specific type | `tax_treaty` |
| `country_nl` | text | Country name (Dutch) | `Nederland` |
| `country_de` | text | Country name (German) | `Deutschland` |
| `treaty_parties` | list | Participating countries | `Netherlands\|Germany` |
| `available_languages` | list | Available translations | `nl-nl\|de-de` |
| `effective_date` | date | When took effect | `2012-04-01` |
| `xml_file_path` | path | Relative path to XML | `legislation/.../BWBV...xml` |
| `official_url` | url | Official publication | `https://wetten.overheid.nl/...` |
| `legal_jurisdiction` | enum | Jurisdiction scope | `international` |
| `current_status` | enum | Legal status | `in_force` |
| `full_title_nl` | text | Complete Dutch title | `Verdrag tussen het Koninkrijk...` |
| `full_title_de` | text | Complete German title | `Abkommen zwischen dem Königreich...` |
| `short_title_nl` | text | Short Dutch reference | `NL-DE Belastingverdrag 2012` |
| `short_title_de` | text | Short German reference | `NL-DE Steuerabkommen 2012` |

**Example Row:**
```csv
nl-de-tax-treaty-2012,treaty,tax_treaty,Nederland,Deutschland,Netherlands|Germany,nl-nl|de-de,2012-04-01,...
```

**Key Points:**
- Human-readable ID: `nl-de-tax-treaty-2012` (not `bwbv0005862-2022-07-31`)
- Multilingual titles: Both `full_title_nl` and `full_title_de`
- Short references: Easy citation in both languages
- Explicit categorization: `source_type` + `source_subtype`

---

### Layer 3: Term Usage Examples
**File:** `examples_term_usage_in_sources.csv`

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `example_id` | text | Unique example ID | `example-001` |
| `dictionary_term_id` | UUID | → Links to dictionary | `a7714aec-...` |
| `legal_source_id` | text | → Links to registry | `nl-de-tax-treaty-2012` |
| `xml_location_xpath` | xpath | Where in XML | `//artikel[@id='artikel-5']` |
| `location_type` | enum | Context type | `article_text` |
| `article_number` | text | Article/section ref | `5` |
| `example_sentence_nl` | text | Dutch sentence | Full sentence in Dutch |
| `example_sentence_de` | text | German sentence | Full sentence in German |
| `term_appears_in_source_count` | number | Usage frequency | `35` |
| `is_legal_definition` | yes/no | Definitional usage? | `yes` |
| `usage_notes` | text | Context notes | `Core definition in Article 5` |
| `article_title_nl` | text | Article heading (NL) | `Vaste inrichting` |
| `article_title_de` | text | Article heading (DE) | `Betriebsstätte` |

**Example Row:**
```csv
example-003,c4f63b2f-...,nl-de-tax-treaty-2012,//artikel[@id='artikel-5']/lid[1],article_text,5,"Voor de toepassing...","Für die Zwecke...",35,yes,Core definition,Vaste inrichting,Betriebsstätte
```

**Key Points:**
- Links both ways: `dictionary_term_id` + `legal_source_id`
- Bilingual examples: Both `example_sentence_nl` and `example_sentence_de`
- Article context: Both number and title in both languages
- Definition marker: `is_legal_definition` flags key passages

---

## Example Query Workflows

### Query 1: Find All Tax Treaty Examples of "vaste inrichting"

**Human-readable SQL:**
```sql
-- Step 1: Find term in dictionary
SELECT dictionary_term_id, term_nl, term_de, term_category
FROM dictionary_nl_de_legal_terms
WHERE term_nl = 'vaste inrichting'

-- Returns:
-- dictionary_term_id = 'c4f63b2f-...'
-- term_de = 'Betriebsstätte'
-- term_category = 'tax_concept'

-- Step 2: Find examples in tax treaties
SELECT
    e.example_sentence_nl,
    e.example_sentence_de,
    e.article_title_nl,
    s.short_title_nl,
    s.official_url
FROM examples_term_usage_in_sources e
JOIN registry_legal_sources s
    ON e.legal_source_id = s.source_id
WHERE e.dictionary_term_id = 'c4f63b2f-...'
  AND s.source_type = 'treaty'
  AND s.source_subtype = 'tax_treaty'
  AND e.is_legal_definition = 'yes'

-- Returns bilingual definition with citation
```

### Query 2: List All Terms from Netherlands-Germany Tax Treaty

**Human-readable SQL:**
```sql
-- Get all unique terms used in this treaty
SELECT DISTINCT
    d.term_nl,
    d.term_de,
    d.term_category,
    e.term_appears_in_source_count,
    e.is_legal_definition
FROM examples_term_usage_in_sources e
JOIN dictionary_nl_de_legal_terms d
    ON e.dictionary_term_id = d.dictionary_term_id
WHERE e.legal_source_id = 'nl-de-tax-treaty-2012'
ORDER BY e.term_appears_in_source_count DESC
```

### Query 3: Find German Legislation Using Same Term

**Scenario:** Find German national tax law that uses "Betriebsstätte"

```sql
-- Step 1: Get German term from dictionary
SELECT dictionary_term_id, term_de
FROM dictionary_nl_de_legal_terms
WHERE term_nl = 'vaste inrichting'
-- Returns: term_de = 'Betriebsstätte'

-- Step 2: Find in German legislation
SELECT
    s.short_title_de,
    s.source_type,
    e.article_number,
    e.example_sentence_de
FROM examples_term_usage_in_sources e
JOIN registry_legal_sources s
    ON e.legal_source_id = s.source_id
WHERE e.dictionary_term_id = 'c4f63b2f-...'
  AND s.source_type = 'legislation'
  AND s.country_de = 'Deutschland'
```

---

## Naming Benefits for Multilingual Project

### ✅ Language Clarity
**Old:** `source`, `target` (which language?)
**New:** `term_nl`, `term_de` (explicit)

**Scales to:**
```
dictionary_nl_en_legal_terms.csv → term_nl, term_en
dictionary_de_fr_legal_terms.csv → term_de, term_fr
dictionary_nl_de_en_legal_terms.csv → term_nl, term_de, term_en
```

### ✅ Non-Technical Accessibility
**Old:** `doc_id: bwbv0005862-2022-07-31` (what is this?)
**New:** `source_id: nl-de-tax-treaty-2012` (immediately clear)

### ✅ Self-Documenting
**Old:** `context_nl`, `context_de` (context of what?)
**New:** `example_sentence_nl`, `example_sentence_de` (clear purpose)

### ✅ Boolean Clarity
**Old:** `TRUE`, `FALSE` (programming convention)
**New:** `yes`, `no` (natural language)

### ✅ Future-Proof
Easy to add:
- More languages: `term_fr`, `language_fr`
- More jurisdictions: `country_fr`, `full_title_fr`
- More source types: `eu_directive`, `supreme_court_ruling`

---

## File Naming Pattern for Growth

### Current Structure
```
dictionary_nl_de_legal_terms.csv
registry_legal_sources.csv
examples_term_usage_in_sources.csv
```

### Adding English
```
dictionary_nl_en_legal_terms.csv
dictionary_de_en_legal_terms.csv
dictionary_nl_de_en_legal_terms.csv  # Trilingual
```

### Adding Jurisdictions
```
registry_legal_sources.csv  # All sources in one file

With rows:
nl-de-tax-treaty-2012       # Treaty
nl-vpb-1969                 # Dutch Corporate Income Tax Act
de-estg-2023                # German Income Tax Act
eu-directive-2018-822       # EU DAC6 Directive
ecj-case-c-123-2020         # European Court case
```

### Domain-Specific Dictionaries
```
dictionary_nl_de_tax_law.csv          # Tax-specific terms
dictionary_nl_de_corporate_law.csv    # Corporate law terms
dictionary_nl_de_civil_procedure.csv  # Procedural terms
```

---

## Implementation Checklist

### ✅ Completed
- [x] Human-readable file names
- [x] Explicit language column names
- [x] Human-readable source IDs
- [x] Boolean values as `yes/no`
- [x] Multi-language support in schema
- [x] Comprehensive documentation

### 🔄 Ready to Implement
- [ ] Populate full 202-term dictionary with categories
- [ ] Extract article references from XML
- [ ] Generate all term usage examples
- [ ] Add article titles to examples
- [ ] Cross-reference analysis

### 📋 Future Enhancements
- [ ] Add English translations
- [ ] Link to German national tax law
- [ ] Include case law references
- [ ] Add term usage statistics
- [ ] Create trilingual dictionary

---

## Quick Reference

### File Naming
| Type | Pattern | Example |
|------|---------|---------|
| Dictionary | `dictionary_{lang1}_{lang2}_legal_terms.csv` | `dictionary_nl_de_legal_terms.csv` |
| Registry | `registry_legal_sources.csv` | Single file for all sources |
| Examples | `examples_term_usage_in_sources.csv` | Single file, links via IDs |

### ID Patterns
| Entity | Pattern | Example |
|--------|---------|---------|
| Dictionary term | UUID v4 | `a7714aec-7e41-4852-a905-82443caa2dab` |
| Legal source | `{country}-{type}-{year}` | `nl-de-tax-treaty-2012` |
| Usage example | `example-{number}` | `example-001` |

### Column Naming
- **Language-specific:** `term_nl`, `term_de`, `term_en`
- **Descriptive:** `expert_reviewed` (not `sme_reviewed`)
- **Explicit:** `legal_source_id` (not `doc_id`)
- **Bilingual titles:** `full_title_nl` + `full_title_de`

---

**Documentation:** See `NAMING_CONVENTIONS.md` for complete naming standards.
