# Repository Structure

**Legislation Library LexLink** - Multilingual Legal Translation Knowledge Graph

---

## 📁 Directory Organization

```
legislation-library-lexlink/
│
├── data/                                    # All data files (raw + processed)
│   ├── raw/                                 # Original source files (unmodified)
│   │   ├── tmx/                            # Translation Memory eXchange files
│   │   │   ├── Glossary_Dutch_Code_of_Civil_Procedure.tmx (570 KB)
│   │   │   ├── Dutch_Code_of_Civil_Procecudre_Book_1.tmx (5.5 MB)
│   │   │   ├── Dutch_Code_of_Civil_Procecudre_Book_2_and_3.tmx (539 KB)
│   │   │   └── Dutch_Code_of_Civil_Procecudre_Book_4.tmx (433 KB)
│   │   └── xml/                            # XML source documents (future)
│   │
│   ├── dictionaries/                        # Extracted term dictionaries
│   │   ├── nl-nl_de-de/                   # Dutch ↔ German
│   │   │   └── dictionary_nl-nl_de-de_tax-treaty.csv (202 terms)
│   │   ├── nl-nl_en-gb/                   # Dutch ↔ English
│   │   │   └── dictionary_nl-nl_en-gb_civil-procedure.csv (619 terms)
│   │   └── nl-nl_de-de_en-gb/             # Trilingual (future)
│   │       └── dictionary_nl-nl_de-de_en-gb_core-terms.csv
│   │
│   ├── examples/                           # Usage examples and sentence pairs
│   │   ├── examples_nl-nl_en-gb_civil-procedure_book-1.csv (2750 pairs)
│   │   ├── examples_nl-nl_en-gb_civil-procedure_book-2-3.csv (809 pairs)
│   │   ├── examples_nl-nl_en-gb_civil-procedure_book-4.csv (693 pairs)
│   │   └── examples_nl-nl_de-de_tax-treaty.csv (future)
│   │
│   └── registries/                         # Source document registries
│       └── registry_legal_sources.csv
│
├── legislation/                            # Official XML legislation files
│   └── netherlands/
│       ├── BWBR0001827_2025-01-01_0/      # Civil Procedure Code
│       │   └── BWBR0001827_2025-01-01_0.xml
│       └── BWBV0005862_2022-07-31_0/      # NL-DE Tax Treaty
│           └── BWBV0005862_2022-07-31_0.xml
│
├── scripts/                                # Python processing scripts
│   ├── parse_tmx_to_dictionary.py         # TMX → CSV converter
│   ├── clean_and_generate_ids.py          # Term cleaning & UUID generation
│   └── validate_extraction.py             # Data quality checks
│
├── docs/                                   # Documentation
│   ├── REPOSITORY_STRUCTURE.md            # This file
│   ├── NAMING_CONVENTIONS.md              # Naming standards
│   ├── LINKING_ARCHITECTURE_v2.md         # Data architecture
│   ├── MIGRATION_TO_V2.md                 # Migration guide
│   ├── ANALYSIS_NL_CIVIL_PROCEDURE.md     # Analysis of Civil Procedure
│   └── INTEGRATION_ROADMAP.md             # Integration plan
│
├── translation-dictionaries/               # Legacy folder (keeping for reference)
│   └── netherlands/
│       ├── nl-nl-to-de-de.csv             # Original NL-DE pairs
│       └── nl-nl-to-de-de.tsv
│
├── README.md                               # Project overview
├── requirements.txt                        # Python dependencies
├── .gitignore                              # Git exclusions
│
└── [deprecated files/]                     # Old schema files (see .gitignore)
    ├── schema_source_documents.csv
    ├── schema_term_occurrences.csv
    └── legislation_terms_cleaned.*
```

---

## 🗂️ File Naming Conventions

### ISO Language Codes (Strictly Followed)

All files and columns use **ISO 639-1 + ISO 3166-1** codes:

| Code | Language | Region | Example Usage |
|------|----------|--------|---------------|
| `nl-nl` | Dutch | Netherlands | `dictionary_nl-nl_en-gb_civil-procedure.csv` |
| `nl-be` | Flemish | Belgium | `dictionary_nl-be_fr-be_...` (future) |
| `de-de` | German | Germany | `term_de_de` column |
| `de-at` | German | Austria | (future support) |
| `en-gb` | English | UK | `sentence_en_gb` column |
| `en-us` | English | USA | (future support) |
| `fr-fr` | French | France | (future support) |

### Dictionary Files

**Pattern:** `dictionary_{source-code}_{target-code}_{domain}.csv`

**Examples:**
- `dictionary_nl-nl_de-de_tax-treaty.csv`
- `dictionary_nl-nl_en-gb_civil-procedure.csv`
- `dictionary_nl-nl_de-de_en-gb_core-terms.csv` (trilingual)

### Example/Sentence Files

**Pattern:** `examples_{source-code}_{target-code}_{domain}_{identifier}.csv`

**Examples:**
- `examples_nl-nl_en-gb_civil-procedure_book-1.csv`
- `examples_nl-nl_de-de_tax-treaty_articles-1-10.csv`

### Column Naming

Columns use ISO codes directly:

```csv
# Instead of generic "source" / "target":
term_nl_nl,language_source,term_en_gb,language_target

# Instead of generic "context_nl" / "context_de":
sentence_nl_nl,sentence_en_gb,article_title_de_de
```

---

## 📊 Current Data Inventory

### Dictionaries

| File | Language Pair | Terms | Domain | Status |
|------|---------------|-------|--------|--------|
| `dictionary_nl-nl_de-de_tax-treaty.csv` | NL → DE | 202 | Tax law | ✅ Complete |
| `dictionary_nl-nl_en-gb_civil-procedure.csv` | NL → EN | 619 | Civil procedure | ✅ Complete |
| Total | | **821** | Multi-domain | |

### Examples

| File | Language Pair | Sentences | Source | Status |
|------|---------------|-----------|--------|--------|
| `examples_nl-nl_en-gb_civil-procedure_book-1.csv` | NL → EN | 2750 | Book 1 | ✅ Complete |
| `examples_nl-nl_en-gb_civil-procedure_book-2-3.csv` | NL → EN | 809 | Books 2-3 | ✅ Complete |
| `examples_nl-nl_en-gb_civil-procedure_book-4.csv` | NL → EN | 693 | Book 4 | ✅ Complete |
| Total | | **4252** | Professional translations | |

### Grand Total

**5,073 translation units** (821 terms + 4,252 sentence pairs)

---

## 🔄 Data Flow

```
┌─────────────┐
│ Raw Sources │
└──────┬──────┘
       │
       ├─── TMX Files (data/raw/tmx/)
       │    ↓
       │    Python Parser (scripts/parse_tmx_to_dictionary.py)
       │    ↓
       ├──→ Dictionaries (data/dictionaries/{lang-pair}/)
       │    └─ ISO-coded term pairs with UUIDs
       │
       └─── XML Files (legislation/)
            ↓
            Python Parser (future: article_matcher.py)
            ↓
            Examples (data/examples/)
            └─ Sentence pairs linked to articles
```

---

## 🎯 Directory Purpose

### `/data` - All Data Files

**Purpose:** Centralized data storage, separated by processing stage

**Subfolders:**
- **`raw/`** - Untouched source files (TMX, XML)
- **`dictionaries/`** - Processed term pairs by language
- **`examples/`** - Usage examples and sentence translations
- **`registries/`** - Metadata about legal sources

### `/legislation` - Official XML Sources

**Purpose:** Authoritative legal text in structured XML format

**Organization:** `{country}/{document-id}_{effective-date}_{version}/`

**Examples:**
- `netherlands/BWBR0001827_2025-01-01_0/` - Civil Procedure Code
- `netherlands/BWBV0005862_2022-07-31_0/` - NL-DE Tax Treaty

### `/scripts` - Processing Tools

**Purpose:** Python scripts for data extraction and transformation

**Key Scripts:**
- `parse_tmx_to_dictionary.py` - TMX → CSV converter
- `clean_and_generate_ids.py` - UUID generation & deduplication
- `validate_extraction.py` - Data quality validation

### `/docs` - Documentation

**Purpose:** Architecture, conventions, and guides

**Key Documents:**
- `REPOSITORY_STRUCTURE.md` - This file
- `NAMING_CONVENTIONS.md` - Naming standards (ISO codes, etc.)
- `LINKING_ARCHITECTURE_v2.md` - How data layers connect

---

## 🚀 Quick Start

### Extract Translations from TMX

```bash
# Install dependencies
pip install chardet

# Run parser
cd scripts
python parse_tmx_to_dictionary.py

# Output:
# - data/dictionaries/nl-nl_en-gb/dictionary_nl-nl_en-gb_civil-procedure.csv
# - data/examples/examples_nl-nl_en-gb_civil-procedure_book-*.csv
```

### Validate Data Quality

```bash
cd scripts
python validate_extraction.py
```

### Generate UUIDs & Clean

```bash
cd scripts
python clean_and_generate_ids.py
```

---

## 📏 Storage Estimates

| Category | Current | Future Estimate |
|----------|---------|-----------------|
| **TMX Files** | 7 MB | 10-15 MB |
| **Dictionaries** | 183 KB | 500 KB - 1 MB |
| **Examples** | 1.4 MB | 5-10 MB |
| **XML Legislation** | 15 MB | 100-200 MB |
| **Total** | ~23 MB | 120-230 MB |

**Note:** Highly compressible text data, efficient for version control.

---

## 🔐 Version Control (.gitignore)

### Ignored Files
- `npm-cache/` - Build artifacts
- `.claude` - AI assistant cache
- `*.backup`, `*.bak`, `*_old.*` - Backup files
- `schema_*.csv` - Deprecated v1 schema files
- `legislation_terms_cleaned.*` - Legacy cleaned files

### Tracked Files
- All `/data` folders (CSV files)
- All `/scripts` (Python code)
- All `/docs` (Documentation)
- `/legislation` XML files
- Configuration files (requirements.txt, .gitignore, README.md)

---

## 🌍 Multilingual Expansion Path

### Current Languages
- ✅ Dutch (nl-nl)
- ✅ German (de-de)
- ✅ English (en-gb)

### Future Languages
```
data/dictionaries/
├── nl-nl_de-de/           ✅ Complete
├── nl-nl_en-gb/           ✅ Complete
├── nl-nl_fr-fr/           🔜 Next: French
├── nl-nl_es-es/           📋 Planned: Spanish
├── de-de_en-gb/           📋 Planned: DE-EN direct
└── nl-nl_de-de_en-gb/     🔜 Next: Trilingual core terms
```

### Future Domains
```
data/dictionaries/
└── {lang-pair}/
    ├── dictionary_{lang}_tax-law.csv           ✅ Complete (NL-DE)
    ├── dictionary_{lang}_civil-procedure.csv   ✅ Complete (NL-EN)
    ├── dictionary_{lang}_civil-code.csv        📋 Planned
    ├── dictionary_{lang}_criminal-law.csv      📋 Planned
    └── dictionary_{lang}_corporate-law.csv     📋 Planned
```

---

## 📚 Related Documentation

- **Architecture:** `docs/LINKING_ARCHITECTURE_v2.md`
- **Naming Standards:** `docs/NAMING_CONVENTIONS.md`
- **Integration Plan:** `docs/INTEGRATION_ROADMAP.md`
- **Analysis:** `docs/ANALYSIS_NL_CIVIL_PROCEDURE.md`

---

**Last Updated:** 2025-11-24
**Repository Version:** 2.0 (Structured & ISO-Compliant)
