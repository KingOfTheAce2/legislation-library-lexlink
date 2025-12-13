# Linking Architecture: Dictionary ↔ Tax Treaty XML

## Correct Categorization

**Document Type:** `treaty` (specifically `tax_treaty`)
**NOT:** `legislation` (which implies national law)

**Source:** Netherlands-Germany Double Taxation Treaty (BWBV0005862)

---

## Three-Layer Architecture

```
┌─────────────────────────┐
│ Translation Dictionary  │  ← legislation_terms_cleaned.csv
│ (202 term pairs)        │     - UUIDs
│                         │     - NL ↔ DE translations
└───────────┬─────────────┘
            │
            │ linked via term_id
            ↓
┌─────────────────────────┐
│  Term Occurrences       │  ← schema_term_occurrences.csv
│  (linking table)        │     - term_id + doc_id
│                         │     - XPath locations
│                         │     - Bilingual context
└───────────┬─────────────┘
            │
            │ references doc_id
            ↓
┌─────────────────────────┐
│  Source Documents       │  ← schema_source_documents.csv
│  (treaty metadata)      │     - doc_type = "treaty"
│                         │     - File paths, URLs
└─────────────────────────┘     - Jurisdiction info
            │
            │ points to actual XML
            ↓
┌─────────────────────────┐
│  XML File               │  ← BWBV0005862_2022-07-31_0.xml
│  (authoritative source) │     - Full treaty text
│                         │     - Bilingual structure
└─────────────────────────┘
```

---

## File Structure

```
legislation-library-lexlink/
│
├── legislation_terms_cleaned.csv          # 202 NL↔DE term pairs with UUIDs
├── schema_source_documents.csv            # Treaty/document metadata
├── schema_term_occurrences.csv            # Links terms to treaty locations
│
├── legislation/
│   └── netherlands/
│       └── BWBV0005862_2022-07-31_0/
│           └── BWBV0005862_2022-07-31_0.xml
│
└── example_linking_structure.json         # Architecture documentation
```

---

## Data Model

### 1. Translation Dictionary
**File:** `legislation_terms_cleaned.csv`

| Column | Example | Purpose |
|--------|---------|---------|
| id | `a7714aec-...` | Unique term UUID |
| source | `Verdrag` | Dutch term |
| lang_source | `nl-nl` | Source language |
| target | `Abkommen` | German translation |
| lang_target | `de-de` | Target language |
| author | `van Gassen` | Translator/SME |
| sme_reviewed | `TRUE` | Quality marker |

**Independence:** This file stands alone — can be queried without XML

---

### 2. Source Documents Registry
**File:** `schema_source_documents.csv`

| Column | Example | Purpose |
|--------|---------|---------|
| doc_id | `bwbv0005862-2022-07-31` | Unique document ID |
| doc_type | `treaty` | **Not** legislation! |
| doc_subtype | `tax_treaty` | Specific category |
| title_nl | `Verdrag tussen...` | Dutch title |
| title_de | `Abkommen zwischen...` | German title |
| parties | `Netherlands\|Germany` | Treaty signatories |
| languages | `nl-nl\|de-de` | Available languages |
| file_path | `legislation/.../BWBV...xml` | Relative path to XML |
| url | `https://wetten.overheid.nl/...` | Official source |
| jurisdiction | `international` | Legal scope |
| status | `in_force` | Current validity |

---

### 3. Term Occurrences (Linking Table)
**File:** `schema_term_occurrences.csv`

| Column | Example | Purpose |
|--------|---------|---------|
| occurrence_id | `occ-001` | Unique occurrence |
| **term_id** | `a7714aec-...` | → Links to dictionary |
| **doc_id** | `bwbv0005862-...` | → Links to document |
| xpath | `//meta-data/titel...` | XML location |
| element_type | `title` / `article` | Context type |
| article_id | `artikel-5` | Specific article |
| context_nl | `"Verdrag tussen..."` | Dutch sentence |
| context_de | `"Abkommen zwischen..."` | German sentence |
| term_frequency | `47` | Usage count |
| is_definition | `TRUE` / `FALSE` | Definitional usage? |

**Key Insight:** This is where the magic happens — connects abstract terms to concrete treaty text

---

## Example Query Workflow

### Query: "Show me treaty examples of 'vaste inrichting' (permanent establishment)"

```sql
-- 1. Find term in dictionary
SELECT id, source, target
FROM translation_terms
WHERE source = 'vaste inrichting'
-- Returns: id = 'c4f63b2f-...', target = 'Betriebsstätte'

-- 2. Find all treaty occurrences
SELECT o.context_nl, o.context_de, d.title_nl, d.url
FROM term_occurrences o
JOIN source_documents d ON o.doc_id = d.doc_id
WHERE o.term_id = 'c4f63b2f-...'
  AND d.doc_type = 'treaty'
  AND o.is_definition = TRUE
-- Returns bilingual definition from Article 5

-- 3. (Optional) Parse XML for full article text
-- Use xpath from term_occurrences to extract complete article
```

---

## Why This Architecture?

### ✅ Advantages

1. **No Data Duplication**
   - XML stays authoritative source
   - Dictionary doesn't embed context
   - Context extracted dynamically via XPath

2. **Modular & Scalable**
   - Add new treaties → new row in `source_documents`
   - Add new languages → new columns or translation pairs
   - Add case law → same linking mechanism

3. **Queryable Without XML**
   - Dictionary works standalone for quick lookups
   - Metadata available without parsing XML
   - Full context available on demand

4. **Multilingual Native**
   - Treaty already has NL + DE in same XML
   - Easy to add EN, FR later
   - Language codes in every layer

5. **Future-Proof**
   - Can link same term to multiple treaties
   - Can link to case law citing treaties
   - Can add usage notes, definitions, see-also links

---

## Document Type Taxonomy

```
legal_sources/
│
├── treaty/                    ← International agreements
│   ├── tax_treaty            ← Double taxation (current)
│   ├── trade_agreement
│   ├── extradition_treaty
│   └── human_rights
│
├── legislation/               ← National law
│   ├── act                   ← Primary legislation
│   ├── code                  ← Codified law
│   └── decree                ← Secondary legislation
│
├── regulation/                ← Administrative rules
│   ├── eu_regulation
│   └── ministerial_decree
│
└── case_law/                  ← Judicial decisions
    ├── supreme_court
    ├── court_of_appeal
    └── ecj                   ← European Court of Justice
```

**Current Status:** Working with `treaty/tax_treaty`
**Next Steps:** Can expand to national legislation, EU regulations, case law

---

## Implementation Notes

### For Tax Treaties Specifically

Tax treaties have special characteristics:
- **Always bilateral** (two parties)
- **Highly standardized** (OECD Model Convention)
- **Technical terminology** (withholding tax, permanent establishment, etc.)
- **Article structure** (numbered articles with definitions)
- **Both languages equally authoritative**

The linking architecture preserves all these features:
- `parties` field tracks bilateral nature
- `article_id` preserves structure
- Bilingual `context_nl` + `context_de` shows both authoritative texts
- `is_definition` flags definitional articles

### Extending to National Legislation

When you add Dutch or German national tax law:
```csv
doc_id,doc_type,doc_subtype,title_nl,jurisdiction,...
vpb-1969,legislation,tax_act,"Wet op de vennootschapsbelasting 1969",national,...
```

Same linking mechanism, different `doc_type` and `jurisdiction`.

---

## Web URL Structure

The website follows clean, SEO-friendly URL patterns similar to established dictionaries:

### Reference Examples
- Linguee: `https://www.linguee.nl/nederlands-engels/vertaling/deurwaarder.html`
- Cambridge: `https://dictionary.cambridge.org/nl/woordenboek/engels/bailiff`

### LexLink URL Patterns

```
legislationlibrary.com/
│
├── dictionary/                                    ← Dictionary home
│   ├── nl-nl-de-de/                               ← Language pair (NL→DE)
│   │   └── {term}
│   │       Example: /dictionary/nl-nl-de-de/vaste-inrichting
│   │
│   └── nl-nl-en-gb/                               ← Language pair (NL→EN-GB)
│       └── {term}
│           Example: /dictionary/nl-nl-en-gb/deurwaarder
│
├── netherlands/                                   ← Jurisdiction
│   ├── legislation/                               ← National legislation
│   │   └── {doc-id}/
│   │       Example: /netherlands/legislation/bwbr0001827
│   │
│   └── treaty/                                    ← Treaties (NL party)
│       └── {doc-id}/
│           Example: /netherlands/treaty/bwbv0005862
│
├── germany/                                       ← Jurisdiction
│   ├── legislation/
│   │   └── {doc-id}/
│   │       Example: /germany/legislation/estg
│   │
│   └── treaty/
│       └── {doc-id}/
│
├── eu/                                            ← EU jurisdiction
│   ├── regulation/
│   │   └── {doc-id}/
│   │       Example: /eu/regulation/2016-679
│   │
│   └── directive/
│       └── {doc-id}/
│
└── term/                                          ← Term detail (all sources)
    └── {term-id}/
        Example: /term/a7714aec-1234-5678-9abc-def012345678
```

### URL Conventions

| Element | Format | Example |
|---------|--------|---------|
| Terms | lowercase, hyphenated | `vaste-inrichting` |
| Language codes | BCP 47 locale pairs | `nl-nl-de-de`, `nl-nl-en-gb` |
| Jurisdictions | lowercase country/region | `netherlands`, `germany`, `eu` |
| Document IDs | lowercase, original | `bwbv0005862`, `bwbr0001827` |
| UUIDs | full UUID | `a7714aec-...` |

### Supported Language Variants

| Code | Language |
|------|----------|
| `nl-nl` | Dutch (Netherlands) |
| `de-de` | German (Germany) |
| `en-gb` | English (British) |
| `en-us` | English (American) |
| `fr-fr` | French (France) |

### Homepage Statistics Counter

The homepage displays live statistics from the database:

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│   TERMS              EXAMPLES            LEGAL SOURCES     │
│   ─────              ────────            ─────────────     │
│   1,247 total        8,392 total         156 total         │
│   ✓ 892 verified     ✓ 4,215 verified                      │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

| Metric | Source | Field |
|--------|--------|-------|
| Total terms | `dictionary_*.csv` | `COUNT(*)` |
| Verified terms | `dictionary_*.csv` | `COUNT(*) WHERE sme_reviewed = TRUE` |
| Total examples | `examples_*.csv` | `COUNT(*)` |
| Verified examples | `examples_*.csv` | `COUNT(*) WHERE sme_reviewed = TRUE` |
| Total legal sources | `registry_legal_sources.csv` | `COUNT(*)` |

### Dictionary Page Structure

Each dictionary term page (`/dictionary/nl-nl-en-gb/{term}`) displays:
1. **Term header** - Source term + translation
2. **Usage examples** - Context from legislation/treaties of relevant jurisdictions
3. **Cross-references** - Related terms
4. **Source links** - Links to full document pages within jurisdictions

---

## Next Steps

1. **Extract Article References**
   - Parse XML to populate `term_occurrences` automatically
   - Map each term to article numbers

2. **Add Context Windows**
   - Extract surrounding sentences for better examples
   - Store paragraph-level context

3. **Cross-Reference Analysis**
   - Which treaty articles cite which concepts?
   - Which terms appear in definitions vs. operative clauses?

4. **Expand to Case Law**
   - Court decisions citing this treaty
   - Same term_id links to judicial interpretations

5. **Build Knowledge Graph**
   - Terms → Articles → Treaties → Court Cases
   - All linked through UUIDs
