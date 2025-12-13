#!/usr/bin/env python3
"""
Static Site Generator for LexLink Legal Dictionary
Generates SEO-optimized individual pages for each term and article.
Output: docs/ folder for GitHub Pages hosting.
"""

import csv
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import quote
import json

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text[:100]  # Limit length

def create_base_template(title, content, lang_pair="nl-en", breadcrumb=""):
    """Generate base HTML template with parallel language layout."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="LexLink Legal Dictionary - {title}">
    <meta name="keywords" content="legal translation, Dutch law, German law, English law, legal dictionary">
    <meta property="og:title" content="{title} - LexLink">
    <meta property="og:type" content="website">
    <meta property="og:description" content="Multilingual legal dictionary for Dutch, German, and English legal terminology">
    <title>{title} - LexLink Legal Dictionary</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="../index.html">LexLink</a></h1>
            <p class="tagline">Multilingual Legal Translation Dictionary</p>
            <nav>
                <a href="../index.html">Home</a>
                <a href="../dictionaries/nl-nl_en-gb/index.html">NL-EN Dictionary</a>
                <a href="../dictionaries/nl-nl_de-de/index.html">NL-DE Dictionary</a>
                <a href="../articles/index.html">Articles</a>
                <a href="../about.html">About</a>
            </nav>
        </div>
    </header>

    {breadcrumb}

    <main class="container">
        {content}
    </main>

    <footer>
        <div class="container">
            <p>&copy; {datetime.now().year} LexLink Legal Dictionary. Data from professional legal translations.</p>
            <p>
                <a href="https://github.com/yourusername/legislation-library-lexlink">GitHub Repository</a> |
                <a href="../about.html">About</a> |
                <a href="../license.html">License</a>
            </p>
        </div>
    </footer>
</body>
</html>"""

def create_term_page(term_data, lang_pair):
    """Generate individual term page with parallel language display."""
    term_id = term_data.get('dictionary_term_id', '')

    if lang_pair == 'nl-en':
        term_source = term_data.get('term_nl_nl', '')
        lang_source = 'nl-nl'
        lang_source_name = 'Dutch'
        term_target = term_data.get('term_en_gb', '')
        lang_target = 'en-gb'
        lang_target_name = 'English'
    else:  # nl-de
        term_source = term_data.get('term_nl', term_data.get('source', ''))
        lang_source = 'nl-nl'
        lang_source_name = 'Dutch'
        term_target = term_data.get('term_de', term_data.get('target', ''))
        lang_target = 'de-de'
        lang_target_name = 'German'

    translator = term_data.get('translator_name', term_data.get('author', 'Unknown'))
    translation_date = term_data.get('translation_date', '')
    domain = term_data.get('legal_domain', term_data.get('term_category', 'Legal terminology'))
    expert_reviewed = term_data.get('expert_reviewed', term_data.get('sme-reviewed', 'no'))

    slug = slugify(term_source)

    breadcrumb = f"""
    <div class="breadcrumb container">
        <a href="../index.html">Home</a> &gt;
        <a href="../dictionaries/{lang_source}_{lang_target}/index.html">{lang_source_name}-{lang_target_name} Dictionary</a> &gt;
        <span>{term_source}</span>
    </div>"""

    content = f"""
    <article class="term-page">
        <header class="term-header">
            <h2>Legal Term Translation</h2>
            <p class="term-id">ID: {term_id}</p>
        </header>

        <div class="parallel-view">
            <div class="language-column source-column">
                <div class="language-label">{lang_source_name} ({lang_source})</div>
                <div class="term-text">{term_source}</div>
            </div>

            <div class="translation-arrow">→</div>

            <div class="language-column target-column">
                <div class="language-label">{lang_target_name} ({lang_target})</div>
                <div class="term-text">{term_target}</div>
            </div>
        </div>

        <section class="metadata">
            <h3>Metadata</h3>
            <dl>
                <dt>Legal Domain</dt>
                <dd>{domain}</dd>

                <dt>Translator</dt>
                <dd>{translator}</dd>

                <dt>Translation Date</dt>
                <dd>{translation_date}</dd>

                <dt>Expert Reviewed</dt>
                <dd>{'✓ Yes' if expert_reviewed.lower() == 'yes' else '✗ No'}</dd>
            </dl>
        </section>

        <nav class="term-navigation">
            <a href="../dictionaries/{lang_source}_{lang_target}/index.html" class="btn">← Back to Dictionary</a>
        </nav>
    </article>"""

    title = f"{term_source} → {term_target}"
    return create_base_template(title, content, f"{lang_source}-{lang_target}", breadcrumb)

def create_article_page(example_data, lang_pair='nl-en'):
    """Generate individual article/example page with parallel text."""
    example_id = example_data.get('example_id', '')
    sentence_nl = example_data.get('sentence_nl_nl', '')
    sentence_en = example_data.get('sentence_en_gb', '')
    legal_source = example_data.get('legal_source_id', '')
    book_id = example_data.get('book_identifier', '')
    article_num = example_data.get('article_number', '')
    article_title_nl = example_data.get('article_title_nl_nl', '')
    article_title_en = example_data.get('article_title_en_gb', '')
    trans_date = example_data.get('translation_date', '')

    slug = slugify(f"{book_id}-{example_id[:8]}")

    breadcrumb = f"""
    <div class="breadcrumb container">
        <a href="../index.html">Home</a> &gt;
        <a href="../articles/index.html">Articles</a> &gt;
        <a href="../articles/{book_id}/index.html">{book_id.upper()}</a> &gt;
        <span>Example {example_id[:8]}</span>
    </div>"""

    content = f"""
    <article class="article-page">
        <header class="article-header">
            <h2>Legal Text Example</h2>
            <p class="article-meta">
                Source: {legal_source} | Book: {book_id.upper()}
                {f' | Article: {article_num}' if article_num else ''}
            </p>
        </header>

        <div class="parallel-view parallel-text">
            <div class="language-column source-column">
                <div class="language-label">Dutch (nl-nl)</div>
                {f'<h3 class="article-title">{article_title_nl}</h3>' if article_title_nl else ''}
                <div class="article-text">{sentence_nl}</div>
            </div>

            <div class="divider"></div>

            <div class="language-column target-column">
                <div class="language-label">English (en-gb)</div>
                {f'<h3 class="article-title">{article_title_en}</h3>' if article_title_en else ''}
                <div class="article-text">{sentence_en}</div>
            </div>
        </div>

        <section class="metadata">
            <h3>Source Information</h3>
            <dl>
                <dt>Legal Source ID</dt>
                <dd>{legal_source}</dd>

                <dt>Book Identifier</dt>
                <dd>{book_id}</dd>

                {f'<dt>Article Number</dt><dd>{article_num}</dd>' if article_num else ''}

                <dt>Translation Date</dt>
                <dd>{trans_date}</dd>

                <dt>Example ID</dt>
                <dd>{example_id}</dd>
            </dl>
        </section>

        <nav class="term-navigation">
            <a href="../articles/{book_id}/index.html" class="btn">← Back to {book_id.upper()}</a>
            <a href="../articles/index.html" class="btn">All Articles</a>
        </nav>
    </article>"""

    title = f"Article Example - {book_id.upper()}"
    return create_base_template(title, content, "nl-en", breadcrumb)

def create_dictionary_index(terms, lang_pair, lang_source_name, lang_target_name):
    """Create index page for a dictionary."""
    lang_source, lang_target = lang_pair.split('_')

    content = f"""
    <div class="dictionary-index">
        <header class="page-header">
            <h2>{lang_source_name} → {lang_target_name} Legal Dictionary</h2>
            <p class="subtitle">Professional legal terminology with {len(terms)} terms</p>
        </header>

        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search terms..." onkeyup="filterTerms()">
        </div>

        <div class="term-list" id="termList">
            <table>
                <thead>
                    <tr>
                        <th>{lang_source_name}</th>
                        <th>{lang_target_name}</th>
                        <th>Domain</th>
                    </tr>
                </thead>
                <tbody>"""

    for term in sorted(terms, key=lambda x: x.get('source_term', x.get('term_nl_nl', '')).lower()):
        source_term = term.get('source_term', term.get('term_nl_nl', term.get('term_nl', '')))
        target_term = term.get('target_term', term.get('term_en_gb', term.get('term_de', '')))
        domain = term.get('domain', term.get('legal_domain', term.get('term_category', '')))
        slug = term.get('slug', slugify(source_term))

        content += f"""
                    <tr>
                        <td><a href="{slug}.html">{source_term}</a></td>
                        <td>{target_term}</td>
                        <td class="domain-tag">{domain}</td>
                    </tr>"""

    content += """
                </tbody>
            </table>
        </div>
    </div>

    <script>
    function filterTerms() {
        const input = document.getElementById('searchInput');
        const filter = input.value.toLowerCase();
        const rows = document.querySelectorAll('#termList tbody tr');

        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
        });
    }
    </script>"""

    breadcrumb = f"""
    <div class="breadcrumb container">
        <a href="../../index.html">Home</a> &gt;
        <span>{lang_source_name}-{lang_target_name} Dictionary</span>
    </div>"""

    title = f"{lang_source_name}-{lang_target_name} Legal Dictionary"
    return create_base_template(title, content, lang_pair.replace('_', '-'), breadcrumb)

def create_main_index(stats):
    """Create main landing page."""
    content = f"""
    <div class="hero">
        <h2>Multilingual Legal Translation Dictionary</h2>
        <p class="hero-subtitle">Professional legal terminology from authoritative sources</p>
    </div>

    <section class="stats">
        <div class="stat-card">
            <div class="stat-number">{stats['total_terms']}</div>
            <div class="stat-label">Legal Terms</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{stats['total_examples']}</div>
            <div class="stat-label">Usage Examples</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{stats['language_pairs']}</div>
            <div class="stat-label">Language Pairs</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{stats['legal_domains']}</div>
            <div class="stat-label">Legal Domains</div>
        </div>
    </section>

    <section class="dictionaries">
        <h3>Available Dictionaries</h3>
        <div class="dictionary-cards">
            <div class="dict-card">
                <h4>Dutch → English</h4>
                <p>{stats['nl_en_terms']} terms from Civil Procedure Code</p>
                <a href="dictionaries/nl-nl_en-gb/index.html" class="btn">Browse Dictionary →</a>
            </div>
            <div class="dict-card">
                <h4>Dutch → German</h4>
                <p>{stats['nl_de_terms']} terms from Tax Treaty</p>
                <a href="dictionaries/nl-nl_de-de/index.html" class="btn">Browse Dictionary →</a>
            </div>
        </div>
    </section>

    <section class="articles">
        <h3>Legal Text Examples</h3>
        <p>Parallel translations of complete articles from official legislation</p>
        <a href="articles/index.html" class="btn">Browse Examples →</a>
    </section>

    <section class="features">
        <h3>Features</h3>
        <ul class="feature-list">
            <li>✓ Professional translations by legal experts</li>
            <li>✓ Expert-reviewed terminology</li>
            <li>✓ Parallel language display for easy comparison</li>
            <li>✓ Complete source metadata and traceability</li>
            <li>✓ SEO-optimized individual pages for each term</li>
            <li>✓ Free and open source</li>
        </ul>
    </section>"""

    title = "Home"
    return create_base_template(title, content, "", "")

def generate_site():
    """Main site generation function."""
    print("="*80)
    print("LEXLINK STATIC SITE GENERATOR")
    print("="*80)

    # Paths
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'data'
    output_dir = base_dir / 'docs'

    # Create output structure
    print("\nCreating directory structure...")
    (output_dir / 'css').mkdir(parents=True, exist_ok=True)
    (output_dir / 'dictionaries' / 'nl-nl_en-gb').mkdir(parents=True, exist_ok=True)
    (output_dir / 'dictionaries' / 'nl-nl_de-de').mkdir(parents=True, exist_ok=True)
    (output_dir / 'articles').mkdir(parents=True, exist_ok=True)

    stats = {
        'total_terms': 0,
        'total_examples': 0,
        'language_pairs': 2,
        'legal_domains': 2,
        'nl_en_terms': 0,
        'nl_de_terms': 0
    }

    # Process NL-EN dictionary
    print("\n[1/4] Processing NL-EN Civil Procedure dictionary...")
    nl_en_dict_path = data_dir / 'dictionaries' / 'nl-nl_en-gb' / 'dictionary_nl-nl_en-gb_civil-procedure.csv'

    if nl_en_dict_path.exists():
        nl_en_terms = []
        with open(nl_en_dict_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = slugify(row.get('term_nl_nl', ''))
                nl_en_terms.append({
                    'slug': slug,
                    'source_term': row.get('term_nl_nl', ''),
                    'target_term': row.get('term_en_gb', ''),
                    'domain': row.get('legal_domain', 'civil_procedure'),
                    'data': row
                })

                # Generate individual term page
                html = create_term_page(row, 'nl-en')
                output_path = output_dir / 'dictionaries' / 'nl-nl_en-gb' / f'{slug}.html'
                output_path.write_text(html, encoding='utf-8')

        # Generate dictionary index
        dict_index = create_dictionary_index(nl_en_terms, 'nl-nl_en-gb', 'Dutch', 'English')
        (output_dir / 'dictionaries' / 'nl-nl_en-gb' / 'index.html').write_text(dict_index, encoding='utf-8')

        stats['nl_en_terms'] = len(nl_en_terms)
        stats['total_terms'] += len(nl_en_terms)
        print(f"   Generated {len(nl_en_terms)} NL-EN term pages")

    # Process NL-DE dictionary
    print("\n[2/4] Processing NL-DE Tax Treaty dictionary...")
    nl_de_dict_path = data_dir / 'dictionaries' / 'nl-nl_de-de' / 'nl-nl-to-de-de.tsv'

    if nl_de_dict_path.exists():
        nl_de_terms = []
        with open(nl_de_dict_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                source_term = row.get('source', '')
                slug = slugify(source_term)
                nl_de_terms.append({
                    'slug': slug,
                    'source_term': source_term,
                    'target_term': row.get('target', ''),
                    'domain': 'tax_law',
                    'data': row
                })

                # Generate individual term page
                html = create_term_page(row, 'nl-de')
                output_path = output_dir / 'dictionaries' / 'nl-nl_de-de' / f'{slug}.html'
                output_path.write_text(html, encoding='utf-8')

        # Generate dictionary index
        dict_index = create_dictionary_index(nl_de_terms, 'nl-nl_de-de', 'Dutch', 'German')
        (output_dir / 'dictionaries' / 'nl-nl_de-de' / 'index.html').write_text(dict_index, encoding='utf-8')

        stats['nl_de_terms'] = len(nl_de_terms)
        stats['total_terms'] += len(nl_de_terms)
        print(f"   Generated {len(nl_de_terms)} NL-DE term pages")

    # Process example files
    print("\n[3/4] Processing article examples...")
    examples_dir = data_dir / 'examples'

    if examples_dir.exists():
        example_files = list(examples_dir.glob('examples_*.csv'))

        for example_file in example_files:
            book_match = re.search(r'book-[\d-]+', example_file.stem)
            book_id = book_match.group(0) if book_match else 'unknown'

            book_dir = output_dir / 'articles' / book_id
            book_dir.mkdir(parents=True, exist_ok=True)

            examples = []
            with open(example_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader):
                    example_id = row.get('example_id', f'ex-{idx}')
                    slug = slugify(f"{book_id}-{example_id[:8]}")

                    examples.append({
                        'slug': slug,
                        'sentence_nl': row.get('sentence_nl_nl', ''),
                        'sentence_en': row.get('sentence_en_gb', ''),
                        'data': row
                    })

                    # Generate individual article page
                    html = create_article_page(row, 'nl-en')
                    (book_dir / f'{slug}.html').write_text(html, encoding='utf-8')

            # Create book index
            book_index_content = f"""
    <div class="book-index">
        <h2>{book_id.upper()} - Sentence Examples</h2>
        <p>{len(examples)} professional translations</p>
        <div class="example-list">
            <ul>"""

            for ex in examples[:100]:  # Show first 100
                preview = ex['sentence_nl'][:100] + '...' if len(ex['sentence_nl']) > 100 else ex['sentence_nl']
                book_index_content += f"""
                <li><a href="{ex['slug']}.html">{preview}</a></li>"""

            book_index_content += """
            </ul>
        </div>
    </div>"""

            breadcrumb = f"""
    <div class="breadcrumb container">
        <a href="../../index.html">Home</a> &gt;
        <a href="../index.html">Articles</a> &gt;
        <span>{book_id.upper()}</span>
    </div>"""

            book_index_html = create_base_template(f"{book_id.upper()} Examples", book_index_content, "nl-en", breadcrumb)
            (book_dir / 'index.html').write_text(book_index_html, encoding='utf-8')

            stats['total_examples'] += len(examples)
            print(f"   Generated {len(examples)} pages for {book_id}")

    # Create main articles index
    articles_index_content = """
    <div class="articles-index">
        <h2>Legal Text Examples</h2>
        <p>Parallel translations from the Dutch Code of Civil Procedure</p>
        <div class="book-list">
            <div class="book-card">
                <h3>Book 1</h3>
                <p>General Provisions (2,750 examples)</p>
                <a href="book-1/index.html" class="btn">Browse →</a>
            </div>
            <div class="book-card">
                <h3>Books 2 & 3</h3>
                <p>Special Proceedings (809 examples)</p>
                <a href="book-2-3/index.html" class="btn">Browse →</a>
            </div>
            <div class="book-card">
                <h3>Book 4</h3>
                <p>Arbitration (693 examples)</p>
                <a href="book-4/index.html" class="btn">Browse →</a>
            </div>
        </div>
    </div>"""

    breadcrumb_articles = """
    <div class="breadcrumb container">
        <a href="../index.html">Home</a> &gt;
        <span>Articles</span>
    </div>"""

    articles_index_html = create_base_template("Legal Text Examples", articles_index_content, "nl-en", breadcrumb_articles)
    (output_dir / 'articles' / 'index.html').write_text(articles_index_html, encoding='utf-8')

    # Generate main index
    print("\n[4/4] Generating main index...")
    main_index = create_main_index(stats)
    (output_dir / 'index.html').write_text(main_index, encoding='utf-8')

    # Generate about page
    about_content = """
    <div class="about-page">
        <h2>About LexLink</h2>
        <p>LexLink is a multilingual legal translation dictionary built from professional legal translations.</p>

        <h3>Data Sources</h3>
        <ul>
            <li><strong>Dutch-English:</strong> Professional translations from the Dutch Code of Civil Procedure (Wetboek van Burgerlijke Rechtsvordering)</li>
            <li><strong>Dutch-German:</strong> Official treaty text from the Netherlands-Germany Tax Treaty</li>
        </ul>

        <h3>Translators</h3>
        <p><strong>Civil Procedure:</strong> Burrough/Machon/Oranje/Frakes/Visser</p>
        <p><strong>Tax Treaty:</strong> van Gassen</p>

        <h3>Technical Details</h3>
        <p>All translations are expert-reviewed and sourced from official legal documents. Each term and article has its own page for optimal SEO and findability.</p>

        <h3>Repository</h3>
        <p>Open source on GitHub: <a href="https://github.com/yourusername/legislation-library-lexlink">legislation-library-lexlink</a></p>
    </div>"""

    about_html = create_base_template("About", about_content, "", "")
    (output_dir / 'about.html').write_text(about_html, encoding='utf-8')

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total term pages generated:     {stats['total_terms']}")
    print(f"Total example pages generated:  {stats['total_examples']}")
    print(f"Total pages:                    {stats['total_terms'] + stats['total_examples'] + 10}")
    print(f"\nOutput directory:               {output_dir}")
    print("\nNext steps:")
    print("1. Generate CSS stylesheet (scripts will create style.css)")
    print("2. Commit docs/ folder to git")
    print("3. Enable GitHub Pages from docs/ folder in repository settings")
    print("4. Site will be available at: https://yourusername.github.io/legislation-library-lexlink/")
    print()

if __name__ == '__main__':
    generate_site()
