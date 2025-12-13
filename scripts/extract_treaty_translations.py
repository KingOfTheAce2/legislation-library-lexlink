#!/usr/bin/env python3
"""
Extract Dutch-French translation terms from bilingual treaty XML files.

Parses treaty XML files that contain both Dutch (nl) and French (fr) authentic texts,
extracting matching article titles, chapter titles, and key terms.
"""

import xml.etree.ElementTree as ET
import csv
import uuid
import re
from pathlib import Path
from datetime import datetime


def clean_text(text):
    """Clean and normalize text."""
    if text is None:
        return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_all_text(element):
    """Get all text content from an element and its children."""
    if element is None:
        return ""
    texts = []
    if element.text:
        texts.append(element.text)
    for child in element:
        texts.append(get_all_text(child))
        if child.tail:
            texts.append(child.tail)
    return clean_text(' '.join(texts))


def extract_titles_and_content(verdrag_element):
    """Extract titles and content from a verdrag (treaty) element."""
    data = {
        'intitule': '',
        'chapters': [],
        'articles': []
    }

    # Extract chapter and article information
    for element in verdrag_element.iter():
        tag = element.tag

        if tag == 'hoofdstuk':
            chapter_info = {
                'label': element.get('label', ''),
                'bwb_ng': element.get('bwb-ng-variabel-deel', ''),
                'title': ''
            }
            kop = element.find('kop')
            if kop is not None:
                titel = kop.find('titel')
                if titel is not None:
                    chapter_info['title'] = get_all_text(titel)
            data['chapters'].append(chapter_info)

        elif tag == 'artikel':
            article_info = {
                'label': element.get('label', ''),
                'bwb_ng': element.get('bwb-ng-variabel-deel', ''),
                'title': '',
                'paragraphs': []
            }
            kop = element.find('kop')
            if kop is not None:
                titel = kop.find('titel')
                if titel is not None:
                    article_info['title'] = get_all_text(titel)

            # Get direct al (paragraph) children of artikel
            for al in element.findall('.//al'):
                text = get_all_text(al)
                if text and len(text) > 5:  # Skip very short fragments
                    article_info['paragraphs'].append(text)

            data['articles'].append(article_info)

    return data


def match_article_by_number(nl_article, fr_articles):
    """Match Dutch article with French article by article number."""
    # Extract article number from label (e.g., "Artikel 1" -> "1")
    nl_label = nl_article.get('label', '')
    nl_num_match = re.search(r'\d+', nl_label)
    if not nl_num_match:
        return None
    nl_num = nl_num_match.group()

    for fr_article in fr_articles:
        fr_label = fr_article.get('label', '')
        fr_num_match = re.search(r'\d+', fr_label)
        if fr_num_match and fr_num_match.group() == nl_num:
            return fr_article
    return None


def match_chapter_by_number(nl_chapter, fr_chapters):
    """Match Dutch chapter with French chapter by chapter number."""
    nl_label = nl_chapter.get('label', '')
    nl_num_match = re.search(r'[IVX]+|\d+', nl_label)
    if not nl_num_match:
        return None
    nl_num = nl_num_match.group()

    for fr_chapter in fr_chapters:
        fr_label = fr_chapter.get('label', '')
        fr_num_match = re.search(r'[IVX]+|\d+', fr_label)
        if fr_num_match and fr_num_match.group() == nl_num:
            return fr_chapter
    return None


def extract_treaty_translations(xml_path, output_csv_path):
    """
    Extract Dutch-French translation pairs from treaty XML.

    Args:
        xml_path: Path to the treaty XML file
        output_csv_path: Path for output CSV
    """
    print(f"Parsing: {xml_path}")

    # Parse XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Find Dutch and French versions
    nl_verdrag = None
    fr_verdrag = None

    for verdrag in root.findall('.//verdrag'):
        lang = verdrag.get('{http://www.w3.org/XML/1998/namespace}lang', '')
        if lang == 'nl':
            nl_verdrag = verdrag
            print(f"Found Dutch version (xml:lang='nl')")
        elif lang == 'fr':
            fr_verdrag = verdrag
            print(f"Found French version (xml:lang='fr')")

    if nl_verdrag is None or fr_verdrag is None:
        print("ERROR: Could not find both Dutch and French versions")
        return 0

    # Extract data from both versions
    nl_data = extract_titles_and_content(nl_verdrag)
    fr_data = extract_titles_and_content(fr_verdrag)

    print(f"Dutch version: {len(nl_data['chapters'])} chapters, {len(nl_data['articles'])} articles")
    print(f"French version: {len(fr_data['chapters'])} chapters, {len(fr_data['articles'])} articles")

    # Prepare translation pairs
    translation_pairs = []

    # Match and extract chapter titles
    for nl_chapter in nl_data['chapters']:
        fr_chapter = match_chapter_by_number(nl_chapter, fr_data['chapters'])
        if fr_chapter and nl_chapter['title'] and fr_chapter['title']:
            translation_pairs.append({
                'type': 'chapter_title',
                'reference': nl_chapter['label'],
                'nl_text': nl_chapter['title'],
                'fr_text': fr_chapter['title']
            })

    # Match and extract article titles
    for nl_article in nl_data['articles']:
        fr_article = match_article_by_number(nl_article, fr_data['articles'])
        if fr_article and nl_article['title'] and fr_article['title']:
            translation_pairs.append({
                'type': 'article_title',
                'reference': nl_article['label'],
                'nl_text': nl_article['title'],
                'fr_text': fr_article['title']
            })

    print(f"Extracted {len(translation_pairs)} translation pairs (titles)")

    # Also extract matching paragraphs (first paragraph of each article)
    paragraph_pairs = []
    for nl_article in nl_data['articles']:
        fr_article = match_article_by_number(nl_article, fr_data['articles'])
        if fr_article:
            nl_paragraphs = nl_article.get('paragraphs', [])
            fr_paragraphs = fr_article.get('paragraphs', [])

            # Match paragraphs by position
            for i, (nl_para, fr_para) in enumerate(zip(nl_paragraphs, fr_paragraphs)):
                if nl_para and fr_para:
                    paragraph_pairs.append({
                        'type': 'paragraph',
                        'reference': f"{nl_article['label']} para {i+1}",
                        'nl_text': nl_para,
                        'fr_text': fr_para
                    })

    print(f"Extracted {len(paragraph_pairs)} paragraph pairs")

    # Combine all pairs
    all_pairs = translation_pairs + paragraph_pairs

    # Write to CSV
    bwb_id = Path(xml_path).stem.split('_')[0]  # e.g., BWBV0004110

    fieldnames = [
        'term_id',
        'term_nl_nl',
        'language_source',
        'term_fr_fr',
        'language_target',
        'term_type',
        'legal_reference',
        'source_file',
        'bwb_id',
        'extraction_date',
        'legal_domain'
    ]

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for pair in all_pairs:
            writer.writerow({
                'term_id': str(uuid.uuid4()),
                'term_nl_nl': pair['nl_text'],
                'language_source': 'nl-nl',
                'term_fr_fr': pair['fr_text'],
                'language_target': 'fr-fr',
                'term_type': pair['type'],
                'legal_reference': pair['reference'],
                'source_file': Path(xml_path).name,
                'bwb_id': bwb_id,
                'extraction_date': datetime.now().strftime('%Y-%m-%d'),
                'legal_domain': 'tax_treaty'
            })

    print(f"[OK] Wrote {len(all_pairs)} translation pairs to: {output_csv_path}")
    return len(all_pairs)


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_treaty_translations.py <xml_file> [output_csv]")
        print("\nExample:")
        print("  python extract_treaty_translations.py ../treaty/netherlands/BWBV0004110_2005-07-24_0/BWBV0004110_2005-07-24_0.xml")
        sys.exit(1)

    xml_path = Path(sys.argv[1])

    if not xml_path.exists():
        print(f"ERROR: File not found: {xml_path}")
        sys.exit(1)

    # Default output path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        # Create output in data/dictionaries/nl-nl_fr-fr
        base_dir = Path(__file__).parent.parent
        output_dir = base_dir / 'data' / 'dictionaries' / 'nl-nl_fr-fr'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"dictionary_{xml_path.stem}_nl-fr.csv"

    print("="*80)
    print("TREATY XML TO DICTIONARY EXTRACTOR")
    print("ISO Language Codes: nl-nl (Dutch) -> fr-fr (French)")
    print("="*80)

    count = extract_treaty_translations(xml_path, output_path)

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Translation pairs extracted: {count}")
    print(f"Output file: {output_path}")


if __name__ == '__main__':
    main()
