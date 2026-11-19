"""Check Task 4 source integrity; --final also requires a four-page PDF."""
import argparse
import re
from pathlib import Path


def check(root, final=False, pdf=None):
    paper = Path(root) / 'paper'
    main = (paper / 'main.tex').read_text(encoding='utf-8')
    paths = [paper / (name + '.tex') for name in re.findall(r'\\input\{([^}]+)\}', main)]
    assert len(paths) == 4, 'Expected four IMRaD section files'
    source = main
    for path in paths:
        source = source.replace('\\input{' + path.relative_to(paper).as_posix()[:-4] + '}', path.read_text(encoding='utf-8'))
    source = re.sub(r'(?m)(?<!\\)%.*$', '', source)
    bib = (paper / 'references.bib').read_text(encoding='utf-8')
    keys = re.findall(r'(?m)^@\w+\{([^,]+),', bib)
    assert len(keys) == len(set(keys)), 'Duplicate bibliography keys'
    citations = {key.strip() for group in re.findall(r'\\cite\{([^}]+)\}', source) for key in group.split(',')}
    assert len(citations) >= 12, f'Only {len(citations)} cited sources; require 12'
    assert not citations - set(keys), f'Unknown citations: {citations - set(keys)}'
    assert not set(keys) - citations, f'Unused bibliography entries: {set(keys) - citations}'
    assert not re.search(r'(?im)^\s*(abstract|file|bdsk-url-\d+)\s*=', bib), 'Clutter bibliography fields'
    labels = re.findall(r'\\label\{([^}]+)\}', source)
    assert len(labels) == len(set(labels)), 'Duplicate labels'
    references = re.findall(r'\\(?:auto|eq)?ref\{([^}]+)\}', source)
    assert not set(references) - set(labels), f'Unknown cross-references: {set(references) - set(labels)}'
    for kind in ('figure', 'table', 'equation'):
        for block in re.finditer(r'\\begin\{' + kind + r'\}.*?\\end\{' + kind + r'\}', source, re.S):
            match = re.search(r'\\label\{([^}]+)\}', block[0])
            assert match, f'Unlabelled {kind}'
            key = match[1]
            assert re.search(r'\\(?:auto|eq)?ref\{' + re.escape(key) + r'\}', source[:block.start()]), f'{key} must be introduced before its environment'
    abstract = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', main, re.S)[1]
    words = len(abstract.split())
    assert 150 <= words <= 250, f'Abstract has {words} words'
    keywords = re.search(r'\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}', main, re.S)[1].split(',')
    assert 4 <= len(keywords) <= 6, 'Require four to six keywords'
    assert r'\documentclass[conference]{IEEEtran}' in main, 'Expected IEEE conference class'
    pending = [path.name for path in paths if re.search(r'TASK4_PENDING|reserved for|will be written after', path.read_text(encoding='utf-8'), re.I)]
    if final:
        assert not pending, f'Unfinished sections: {pending}'
        assert pdf and Path(pdf).is_file(), 'Supply --pdf with the compiled final PDF'
        from pypdf import PdfReader
        reader = PdfReader(pdf)
        assert len(reader.pages) == 4, f'PDF has {len(reader.pages)} pages; require exactly four'
        rendered_text = '\n'.join(page.extract_text() for page in reader.pages)
        assert '??' not in rendered_text, 'Unresolved reference in PDF'
        assert 'References' in rendered_text or 'REFERENCES' in rendered_text, 'PDF bibliography is missing'
        log = Path(pdf).with_suffix('.log')
        assert log.is_file(), 'Keep the compiler log alongside the PDF'
        text = log.read_text(encoding='utf-8', errors='replace')
        assert not re.search(r'undefined|multiply defined|Overfull \\[hv]box|LaTeX Error|^!', text, re.I | re.M), 'Resolve compiler errors, undefined references, and overfull boxes'
    print(f'Paper source checks passed: {len(citations)} citations, {len(labels)} unique labels, {words}-word abstract.')
    if pending:
        print('Draft only; second contribution pending: ' + ', '.join(pending))
    if final:
        print('Final PDF checks passed: four pages and clean reference/overflow checks. Visual page review is still required.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', action='store_true')
    parser.add_argument('--pdf', type=Path)
    args = parser.parse_args()
    check(Path(__file__).resolve().parents[1], args.final, args.pdf)
