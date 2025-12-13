#!/usr/bin/env python3
"""
Parse TMX (Translation Memory eXchange) files to extract Dutch-English legal terminology.

Converts professional translation memory files from the Dutch Code of Civil Procedure
into clean CSV dictionaries matching the human-readable architecture with ISO language codes.
"""

import xml.etree.ElementTree as ET
import csv
import uuid
from pathlib import Path
from datetime import datetime
import chardet

def detect_encoding(file_path):
    """Detect file encoding (TMX files may use UTF-16)."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # Read first 10KB
        result = chardet.detect(raw_data)
        return result['encoding']

def parse_tmx_glossary(tmx_file_path, output_csv_path):
    """
    Parse TMX glossary file and extract term pairs.

    Args:
        tmx_file_path: Path to TMX file
        output_csv_path: Path for output CSV
    """
    print(f"Parsing: {tmx_file_path}")

    # Detect encoding
    encoding = detect_encoding(tmx_file_path)
    print(f"Detected encoding: {encoding}")

    # Parse TMX XML
    try:
        tree = ET.parse(tmx_file_path)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        # Try with detected encoding explicitly
        with open(tmx_file_path, 'r', encoding=encoding) as f:
            content = f.read()
        tree = ET.ElementTree(ET.fromstring(content))

    root = tree.getroot()

    # Extract header info
    header = root.find('header')
    creation_tool = header.get('creationtool', 'Unknown') if header is not None else 'Unknown'
    creation_tool_version = header.get('creationtoolversion', '') if header is not None else ''

    print(f"Tool: {creation_tool} {creation_tool_version}")

    # Extract translation units
    terms = []
    body = root.find('body')

    if body is None:
        print("Error: No <body> element found in TMX")
        return 0

    translation_units = body.findall('tu')
    print(f"Found {len(translation_units)} translation units")

    for tu in translation_units:
        tuid = tu.get('tuid', '')

        # Get translation unit variants (tuv)
        tuvs = tu.findall('tuv')

        if len(tuvs) < 2:
            continue  # Need at least source and target

        # Extract Dutch and English segments
        nl_seg = None
        en_seg = None
        nl_creator = None
        en_creator = None
        nl_date = None
        en_date = None

        for tuv in tuvs:
            lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang', '')
            seg = tuv.find('seg')

            if seg is None or seg.text is None:
                continue

            creation_date = tuv.get('creationdate', '')
            creation_id = tuv.get('creationid', '')

            if lang == 'nl':
                nl_seg = seg.text.strip()
                nl_creator = creation_id
                nl_date = creation_date
            elif lang == 'en-gb' or lang == 'en':
                en_seg = seg.text.strip()
                en_creator = creation_id
                en_date = creation_date

        # Only add if we have both Dutch and English
        if nl_seg and en_seg:
            # Get metadata from props
            project = None
            filename = None

            props = tu.findall('prop')
            for prop in props:
                prop_type = prop.get('type', '')
                if prop_type == 'x-project':
                    project = prop.text
                elif prop_type == 'x-filename':
                    filename = prop.text

            terms.append({
                'tuid': tuid,
                'term_nl': nl_seg,
                'term_en': en_seg,
                'translator': en_creator or nl_creator or 'Unknown',
                'creation_date': en_date or nl_date,
                'project': project,
                'source_file': filename
            })

    print(f"Extracted {len(terms)} term pairs")

    # Write to CSV with human-readable schema and ISO codes
    fieldnames = [
        'dictionary_term_id',
        'term_nl_nl',              # ISO: nl-nl
        'language_source',
        'term_en_gb',              # ISO: en-gb
        'language_target',
        'translator_name',
        'translation_date',
        'usage_license',
        'expert_reviewed',
        'premium_content',
        'external_dictionary_reference',
        'term_category',
        'legal_domain',
        'tmx_source_file',
        'tmx_tuid',
        'source_project',
        'source_filename'
    ]

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for term in terms:
            # Parse date if available
            trans_date = ''
            if term['creation_date']:
                try:
                    # Format: 20250225T143122Z
                    dt = datetime.strptime(term['creation_date'], '%Y%m%dT%H%M%SZ')
                    trans_date = dt.strftime('%Y-%m-%d')
                except:
                    trans_date = term['creation_date']

            writer.writerow({
                'dictionary_term_id': str(uuid.uuid4()),
                'term_nl_nl': term['term_nl'],
                'language_source': 'nl-nl',
                'term_en_gb': term['term_en'],
                'language_target': 'en-gb',
                'translator_name': 'Burrough/Machon/Oranje/Frakes/Visser',  # Translation team
                'translation_date': trans_date,
                'usage_license': 'All rights reserved',
                'expert_reviewed': 'yes',  # Professional translator
                'premium_content': 'no',
                'external_dictionary_reference': '',
                'term_category': 'civil_procedure_term',
                'legal_domain': 'civil_procedure',
                'tmx_source_file': Path(tmx_file_path).name,
                'tmx_tuid': term['tuid'],
                'source_project': term.get('project', ''),
                'source_filename': term.get('source_file', '')
            })

    print(f"[OK] Wrote {len(terms)} terms to: {output_csv_path}")
    return len(terms)

def parse_tmx_sentences(tmx_file_path, output_csv_path, book_name):
    """
    Parse TMX file with full sentence translations (Book 1-4).

    Creates usage examples linked to articles.
    """
    print(f"\nParsing sentences from: {tmx_file_path}")
    print(f"Book: {book_name}")

    encoding = detect_encoding(tmx_file_path)
    print(f"Detected encoding: {encoding}")

    # Parse TMX
    try:
        tree = ET.parse(tmx_file_path)
    except ET.ParseError:
        with open(tmx_file_path, 'r', encoding=encoding) as f:
            content = f.read()
        tree = ET.ElementTree(ET.fromstring(content))

    root = tree.getroot()
    body = root.find('body')

    if body is None:
        print("Error: No <body> element found")
        return 0

    translation_units = body.findall('tu')
    print(f"Found {len(translation_units)} translation units")

    # Extract sentence pairs
    sentences = []

    for tu in translation_units:
        tuid = tu.get('tuid', '')
        tuvs = tu.findall('tuv')

        nl_text = None
        en_text = None
        nl_date = None
        en_date = None

        for tuv in tuvs:
            lang = tuv.get('{http://www.w3.org/XML/1998/namespace}lang', '')
            seg = tuv.find('seg')
            creation_date = tuv.get('creationdate', '')

            if seg is not None and seg.text:
                if lang == 'nl':
                    nl_text = seg.text.strip()
                    nl_date = creation_date
                elif lang == 'en-gb' or lang == 'en':
                    en_text = seg.text.strip()
                    en_date = creation_date

        if nl_text and en_text:
            sentences.append({
                'tuid': tuid,
                'sentence_nl': nl_text,
                'sentence_en': en_text,
                'translation_date': en_date or nl_date
            })

    print(f"Extracted {len(sentences)} sentence pairs")

    # Write to CSV with ISO naming
    fieldnames = [
        'example_id',
        'sentence_nl_nl',         # ISO: nl-nl
        'sentence_en_gb',         # ISO: en-gb
        'legal_source_id',
        'book_identifier',
        'article_number',
        'article_title_nl_nl',
        'article_title_en_gb',
        'translation_date',
        'tmx_source_file',
        'tmx_tuid'
    ]

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for sent in sentences:
            # Parse date if available
            trans_date = ''
            if sent['translation_date']:
                try:
                    dt = datetime.strptime(sent['translation_date'], '%Y%m%dT%H%M%SZ')
                    trans_date = dt.strftime('%Y-%m-%d')
                except:
                    trans_date = sent['translation_date']

            writer.writerow({
                'example_id': str(uuid.uuid4()),
                'sentence_nl_nl': sent['sentence_nl'],
                'sentence_en_gb': sent['sentence_en'],
                'legal_source_id': 'nl-nl_civil-procedure-code-2025',
                'book_identifier': book_name,
                'article_number': '',  # To be filled by article matcher
                'article_title_nl_nl': '',
                'article_title_en_gb': '',
                'translation_date': trans_date,
                'tmx_source_file': Path(tmx_file_path).name,
                'tmx_tuid': sent['tuid']
            })

    print(f"[OK] Wrote {len(sentences)} sentence pairs to: {output_csv_path}")
    return len(sentences)

def main():
    """Main processing function."""

    # Use Path objects for cross-platform compatibility
    base_dir = Path(__file__).parent.parent  # Go up to repo root
    tmx_dir = base_dir / 'data' / 'raw' / 'tmx'
    dict_output_dir = base_dir / 'data' / 'dictionaries' / 'nl-nl_en-gb'
    examples_output_dir = base_dir / 'data' / 'examples'

    # Ensure output directories exist
    dict_output_dir.mkdir(parents=True, exist_ok=True)
    examples_output_dir.mkdir(parents=True, exist_ok=True)

    print("="*80)
    print("TMX TO DICTIONARY CONVERTER")
    print("ISO Language Codes: nl-nl (Dutch) -> en-gb (English)")
    print("="*80)
    print(f"TMX Directory: {tmx_dir}")
    print(f"Dictionary Output: {dict_output_dir}")
    print(f"Examples Output: {examples_output_dir}")
    print()

    total_terms = 0
    total_sentences = 0

    # Parse Glossary (terms)
    glossary_path = tmx_dir / 'Glossary_Dutch_Code_of_Civil_Procedure.tmx'
    if glossary_path.exists():
        output_csv = dict_output_dir / 'dictionary_nl-nl_en-gb_civil-procedure.csv'
        count = parse_tmx_glossary(glossary_path, output_csv)
        total_terms = count
        print(f"\n[SUCCESS] Extracted {count} legal terms from glossary")
    else:
        print(f"[WARNING] Glossary not found: {glossary_path}")

    # Parse Book translations (sentences)
    book_files = [
        ('Dutch_Code_of_Civil_Procecudre_Book_1.tmx', 'book-1', 'examples_nl-nl_en-gb_civil-procedure_book-1.csv'),
        ('Dutch_Code_of_Civil_Procecudre_Book_2_and_3.tmx', 'book-2-3', 'examples_nl-nl_en-gb_civil-procedure_book-2-3.csv'),
        ('Dutch_Code_of_Civil_Procecudre_Book_4.tmx', 'book-4', 'examples_nl-nl_en-gb_civil-procedure_book-4.csv')
    ]

    for tmx_file, book_name, output_file in book_files:
        tmx_path = tmx_dir / tmx_file
        if tmx_path.exists():
            output_csv = examples_output_dir / output_file
            count = parse_tmx_sentences(tmx_path, output_csv, book_name)
            total_sentences += count
        else:
            print(f"[WARNING] File not found: {tmx_path}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Glossary terms extracted:      {total_terms}")
    print(f"Sentence pairs extracted:      {total_sentences}")
    print(f"Total translation units:       {total_terms + total_sentences}")
    print()
    print(f"Dictionary output:             {dict_output_dir}")
    print(f"Examples output:               {examples_output_dir}")
    print()
    print("Files created:")
    print("  - dictionary_nl-nl_en-gb_civil-procedure.csv")
    print("  - examples_nl-nl_en-gb_civil-procedure_book-1.csv")
    print("  - examples_nl-nl_en-gb_civil-procedure_book-2-3.csv")
    print("  - examples_nl-nl_en-gb_civil-procedure_book-4.csv")
    print()
    print("Next steps:")
    print("1. Review extracted files in data/dictionaries/ and data/examples/")
    print("2. Run article matcher to link sentences to XML articles")
    print("3. Merge with existing nl-nl_de-de dictionary for trilingual support")
    print()

if __name__ == '__main__':
    main()
