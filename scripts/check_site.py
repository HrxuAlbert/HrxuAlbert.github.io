#!/usr/bin/env python3
"""Exercise Jekyll publishing in a temporary copy; never publish fixtures."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.images = set(), [], []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate ID: {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'img':
            assert attrs.get('alt'), 'Image is missing meaningful alt text'
            self.images.append(attrs['src'])


def build(source, destination):
    # Jekyll 3 expects consistent real paths (macOS aliases /var to /private/var).
    source, destination = source.resolve(), destination.resolve()
    subprocess.run(['bundle', 'exec', 'jekyll', 'build', '--strict_front_matter',
                    '--source', str(source), '--destination', str(destination)],
                   cwd=source, check=True)


def check_routes(destination):
    for file in destination.rglob('*.html'):
        doc = Document(file.read_text())
        for reference in doc.links + doc.images:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            target = (destination / unquote(url.path.lstrip('/')) if url.path.startswith('/')
                      else file.parent / unquote(url.path)) if url.path else file
            if target.is_dir():
                target /= 'index.html'
            assert target.is_file(), f'{file}: broken local URL {reference}'
            if url.fragment and target.suffix == '.html':
                assert unquote(url.fragment) in Document(target.read_text()).ids, reference


def check_static(destination):
    for name in ['assets/profile.jpg', 'learning-contributions/index.html',
                 'learning-contributions/contributions.json']:
        assert (ROOT / name).read_bytes() == (destination / name).read_bytes(), name
    for excluded in ['_drafts', 'README.md', 'LOCAL_NOTES.md', 'publish.sh', 'scripts',
                     'Gemfile', 'Gemfile.lock', 'learning-contributions/README.md']:
        assert not (destination / excluded).exists(), f'Source leaked: {excluded}'
    json.loads((destination / 'learning-contributions/contributions.json').read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture-output', type=Path,
                        help='Keep a built, test-only site outside the repository for browser QA')
    args = parser.parse_args()
    if args.fixture_output:
        target = args.fixture_output.resolve()
        assert ROOT != target and ROOT not in target.parents, 'Keep fixture output outside the repository'
    slugs = [re.sub(r'^\d{4}-\d{2}-\d{2}-', '', p.stem) for p in (ROOT / '_posts').glob('*.md')]
    assert len(slugs) == len(set(slugs)), 'Duplicate post slug would overwrite an article URL'
    build(ROOT, ROOT / '_site')
    check_routes(ROOT / '_site')
    check_static(ROOT / '_site')
    if not slugs:
        for name in ['index.html', 'notes/index.html']:
            assert 'No notes published yet.' in (ROOT / '_site' / name).read_text()

    with tempfile.TemporaryDirectory(prefix='homepage-check-') as folder:
        temp = Path(folder)
        source = temp / 'source'
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns('.git', '_site', 'vendor', '.bundle', '.jekyll-cache'))
        shutil.rmtree(source / '_posts')
        (source / '_posts').mkdir()
        rich_body = r'''
## Rendering check

This is a local software test fixture, not a research article or result.

An inline equation: $$p(y \mid e)$$.

$$
\hat{y} = \arg\max_y p(y \mid e)
$$

> An observation is different from an interpretation.

1. First check
2. Second check

- A list item
- Another item

Inline `code`, a [paper link](https://arxiv.org/abs/2606.07316), and a
[repository link](https://github.com/HrxuAlbert/FBA_ENCODER).

```python
def rendering_check(evidence):
    return {"long_line": "this_is_a_deliberately_long_unbroken_test_string_to_verify_horizontal_scrolling_inside_code_blocks_on_a_small_mobile_screen"}
```

| Header one | Header two | Header three | Header four | Header five | Header six |
| --- | --- | --- | --- | --- | --- |
| Example | Example | Example | Example | Example | Example |

<figure>
<img src="{{ '/assets/notes/rendering-check.svg' | relative_url }}" alt="A labelled rendering test rectangle">
<figcaption>Figure 1. A local rendering fixture, with no research data.</figcaption>
</figure>
'''
        for number in range(1, 5):
            body = rich_body if number == 4 else 'A local software test fixture.\n'
            (source / '_posts' / f'2024-01-0{number}-rendering-check-{number}.md').write_text(
                f'---\nlayout: note\ntitle: "Rendering check {number} — local only"\n'
                f'date: 2024-01-0{number}\ntype: "Experiment Note"\n'
                'description: "Temporary fixture for checking the publishing system."\n'
                'tags: [test-only, rendering]\nmath: true\n---\n' + body)
        (source / '_posts/2024-02-01-unpublished-check.md').write_text(
            '---\ntitle: Hidden fixture\npublished: false\n---\nUNPUBLISHED_SENTINEL')
        (source / '_drafts/hidden-check.md').write_text('---\ntitle: Draft fixture\n---\nDRAFT_SENTINEL')
        (source / '_posts/2999-01-01-future-check.md').write_text('---\ntitle: Future fixture\n---\nFUTURE_SENTINEL')
        (source / 'assets/notes').mkdir(exist_ok=True)
        (source / 'assets/notes/rendering-check.svg').write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 180">'
            '<rect width="720" height="180" fill="#edf3f7"/>'
            '<text x="40" y="100" font-size="24" fill="#245d86">Local rendering check</text></svg>')
        destination = args.fixture_output.resolve() if args.fixture_output else temp / 'built'
        build(source, destination)
        check_routes(destination)
        check_static(destination)
        homepage = (destination / 'index.html').read_text()
        index = (destination / 'notes/index.html').read_text()
        expected = [f'/notes/rendering-check-{n}/' for n in [4, 3, 2, 1]]
        assert [link for link in Document(index).links if link in expected] == expected
        assert [link for link in Document(homepage).links if link in expected] == expected[:3]
        note = (destination / 'notes/rendering-check-4/index.html').read_text()
        for marker in ['Experiment Note', '2024-01-04', 'test-only', '<table>', '<blockquote>',
                       '<ol>', '<ul>', '<figcaption>', 'language-python', 'katex@0.19.1',
                       '/assets/notes.css', '/assets/notes.js', '/assets/notes/rendering-check.svg']:
            assert marker in note, f'Missing article feature: {marker}'
        for file in destination.rglob('*.html'):
            text = file.read_text()
            assert not any(marker in text for marker in ['UNPUBLISHED_SENTINEL', 'DRAFT_SENTINEL', 'FUTURE_SENTINEL'])
        assert not (destination / 'notes/research-note-template').exists()
        print('PASS: production build; local links; unchanged static routes; empty state; '
              'post ordering; latest-three preview; metadata; permanent URLs; Markdown; '
              'nested assets; drafts, unpublished posts, and future posts excluded.')


if __name__ == '__main__':
    main()
