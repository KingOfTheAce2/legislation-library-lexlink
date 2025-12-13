# Import Folder

Drop raw files here for processing into the legislation library.

## Folder Structure

```
import/
├── dictionaries/              ← Monolingual definitions (what terms mean)
│                                 e.g., French legal dictionary
│
├── translation-dictionaries/  ← Bilingual term pairs (how terms translate)
│                                 e.g., NL↔EN legal glossary
│
├── treaties/                  ← Treaty documents (XML, PDF, Word)
│
├── excel/                     ← Excel files (glossaries, term lists)
│
└── glossaries/                ← TMX, TBX, CSV, TSV files
```

## Supported Formats

| Folder | Formats | Notes |
|--------|---------|-------|
| `dictionaries/` | Any | Monolingual - term + definition in same language |
| `translation-dictionaries/` | Any | Bilingual - source term + target term |
| `treaties/` | `.xml`, `.pdf`, `.docx` | XML with bilingual structure works best |
| `excel/` | `.xlsx`, `.xls` | Any structure |
| `glossaries/` | `.tmx`, `.tbx`, `.csv`, `.tsv` | Standard translation formats |

## Processing

After dropping files, run:
```bash
python scripts/process_imports.py
```

Files are processed and moved to `data/` with proper naming conventions.

## Language Codes

Use BCP 47 codes in filenames when possible:
- `nl-nl` - Dutch (Netherlands)
- `de-de` - German (Germany)
- `en-gb` - English (British)
- `fr-fr` - French (France)

Example: `glossary_nl-nl_fr-fr_tax-terms.xlsx`
