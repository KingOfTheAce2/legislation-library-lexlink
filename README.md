# LexLink - Legal Translation Library

**Multilingual legal terminology database linking translations to authoritative sources: treaties, legislation, and case law.**

---

## Current Status

| Metric | Count |
|--------|-------|
| **Total Terms** | 4,244 |
| **Languages** | NL, DE, EN, FR, ES |
| **Dictionaries** | 9 |
| **Treaties** | 2 |
| **Jurisdictions** | Netherlands, France |

### Dictionaries

| Language Pair | Terms | Type |
|---------------|-------|------|
| NL → EN | 2,985 | Translation |
| FR | 495 | Monolingual (definitions) |
| NL | 289 | Monolingual (definitions) |
| NL → DE | 424 | Translation |
| NL → DE + FR | 17 | Combined (trilingual) |
| NL → FR | 17 | Translation |
| NL → ES | 17 | Translation |

### Treaties

| ID | Parties | Type |
|----|---------|------|
| BWBV0005862 | Netherlands - Germany | Tax Treaty (2012) |
| BWBV0004110 | Netherlands - ? | Treaty (2005) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB INTERFACE                            │
│  legislationlibrary.com/dictionary/nl-nl-en-gb/{term}          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Dictionaries │    │   Examples    │    │Legal Sources  │
│  (terms)      │    │  (sentences)  │    │  (treaties)   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
                    ┌───────────────┐
                    │   XML Files   │
                    │ (authoritative│
                    │    source)    │
                    └───────────────┘
```

---

## File Structure

```
legislation-library-lexlink/
│
├── data/
│   ├── dictionaries/
│   │   ├── nl-nl/                    ← Dutch monolingual (289 definitions)
│   │   ├── fr-fr/                    ← French monolingual (495 definitions)
│   │   ├── nl-nl_de-de/              ← Dutch → German (424 terms)
│   │   ├── nl-nl_en-gb/              ← Dutch → English (2,985 terms)
│   │   ├── nl-nl_fr-fr/              ← Dutch → French (17 terms)
│   │   ├── nl-nl_es-es/              ← Dutch → Spanish (17 terms)
│   │   └── nl-nl_de-de_fr-fr/        ← Dutch → German + French (17 terms)
│   │
│   ├── examples/                     ← Example sentences from sources
│   └── raw/                          ← Original TMX files
│
├── treaty/
│   └── netherlands/
│       ├── BWBV0005862_2022-07-31_0/ ← NL-DE Tax Treaty
│       └── BWBV0004110_2005-07-24_0/ ← Treaty
│
├── legislation/
│   └── netherlands/
│       └── BWBR0001827_2025-01-01_0/ ← Dutch legislation
│
├── import/                           ← Drop files here for processing
│   ├── dictionaries/                 ← Monolingual dictionaries
│   ├── translation-dictionaries/     ← Bilingual term pairs
│   ├── treaties/                     ← Treaty documents
│   ├── excel/                        ← Excel files
│   └── glossaries/                   ← TMX, TBX, CSV files
│
├── scripts/
│   ├── parse_tmx_to_dictionary.py
│   ├── validate_extraction.py
│   └── clean_and_generate_ids.py
│
└── docs/
    ├── LINKING_ARCHITECTURE.md
    ├── NAMING_CONVENTIONS.md
    └── REPOSITORY_STRUCTURE.md
```

---

## Extraction Rules

### Treaty Extractions (van Gassen)

Terms and sentences extracted from treaties have specific attribution:

| Field | Value |
|-------|-------|
| `author` | van Gassen |
| `license` | All rights reserved |
| `premium` | TRUE (for sentences) |
| `sme-reviewed` | TRUE |

**Applies to:**
- BWBV0005862 (NL-DE Tax Treaty)
- BWBV0004110 (Treaty 2005)

### Other Sources

| Source | Author | License |
|--------|--------|---------|
| Rijksoverheid glossaries | Rijksoverheid | CC0 |
| Dutch Ministry of Finance | Dutch Ministry of Finance | CC0 |
| Rechtspraak definitions | Rechtspraak | CC0 |
| French Ministry of Justice | Ministère de la Justice (France) | Licence Ouverte 2.0 |

---

## Data Schema

### Dictionary Files

**Translation dictionaries** (`nl-nl_de-de`, etc.):
```csv
id,source,lang-source,target,lang-target,author,license,sme-reviewed,premium
uuid,Verdrag,nl-nl,Abkommen,de-de,van Gassen,All rights reserved,TRUE,FALSE
```

**Monolingual dictionaries** (`nl-nl`, `fr-fr`):
```csv
id,source,lang-source,author,license,sme-reviewed,premium,lang-source-dict
uuid,Aanhangig maken,nl-nl,Rechtspraak,CC0,TRUE,FALSE,"Het starten van..."
```

### Example Sentences

```csv
id,term-id,source-id,sentence-source,lang-source,sentence-target,lang-target,author,sme-reviewed,premium
uuid,term-uuid,bwbv0005862,...,nl-nl,...,de-de,van Gassen,TRUE,TRUE
```

---

## URL Structure

```
legislationlibrary.com/
├── dictionary/
│   ├── nl-nl-de-de/{term}           ← Dutch→German lookup
│   ├── nl-nl-en-gb/{term}           ← Dutch→English lookup
│   ├── nl-nl-fr-fr/{term}           ← Dutch→French lookup
│   └── nl-nl-de-de-fr-fr/{term}     ← Dutch→German+French (trilingual)
│
├── netherlands/
│   ├── legislation/{doc-id}
│   └── treaty/{doc-id}
│
├── france/
│   └── legislation/{doc-id}
│
└── germany/
    └── legislation/{doc-id}
```

---

## Quick Start

### Import New Data

1. Drop files in `import/` folder
2. Run processing (or ask Claude)
3. Files moved to correct locations

### Query Terms

```python
import pandas as pd

# Load Dutch→English dictionary
df = pd.read_csv('data/dictionaries/nl-nl_en-gb/dictionary_nl-nl_en-gb.csv')

# Find term
term = df[df['source'] == 'deurwaarder']
print(f"{term['source'].values[0]} → {term['target'].values[0]}")
```

---

## Language Codes

| Code | Language |
|------|----------|
| `nl-nl` | Dutch (Netherlands) |
| `de-de` | German (Germany) |
| `en-gb` | English (British) |
| `fr-fr` | French (France) |
| `es-es` | Spanish (Spain) |

---

## License

| Content | License |
|---------|---------|
| Treaty extractions (van Gassen) | All rights reserved |
| Government glossaries | CC0 / Licence Ouverte |
| Code & structure | MIT |

---

**Last Updated:** 2025-11-29
