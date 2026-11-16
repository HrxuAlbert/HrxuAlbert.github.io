# Haoran Xu — academic homepage

Personal academic website at <https://hrxualbert.github.io/>. GitHub Pages
builds **`main`, repository root** with its existing Jekyll branch build.
No new deployment workflow, frontend framework, or backend is required.

## Architecture

```text
index.html                  Homepage with Liquid-powered latest notes
_config.yml                 Site settings and /notes/:title/ permalinks
_layouts/default.html       Shared document shell
_layouts/note.html          Markdown article layout
_includes/                  Navigation, footer, shared post listing
_posts/                     Published YYYY-MM-DD-slug.md files
_drafts/                     Unpublished writing template and drafts
notes/index.html            Automatic notes index
assets/site.css             Shared visual design and homepage styles
assets/notes.css             Article typography, code, figures, tables
assets/notes.js              Table/code keyboard access; optional math rendering
assets/profile.jpg          Existing profile photograph
scripts/check_site.py       Build and publishing-workflow checks
```

Both lists use `site.posts`, newest first. The homepage shows the latest three;
the index shows all published notes. With no published notes, both show an
introductory state. No example research articles are published.

The Gemfile pins Jekyll 3.10.0, Kramdown, its GFM parser, Liquid, and Rouge to
the [GitHub Pages core versions](https://pages.github.com/versions/). WEBrick
supports local preview. No custom Jekyll plugins are used. KaTeX 0.19.1 is
loaded from jsDelivr with integrity checks **only on articles with `math: true`**.
The homepage and notes index need no JavaScript or external fonts. The visual
design uses a white background, neutral text, system sans-serif typography,
and compact headings; it does not depend on OpenAI brand fonts or assets.

## Preview locally

Use Ruby (preferably a maintained Ruby 3.3 installation) and Bundler:

```bash
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

Open <http://127.0.0.1:4000/> and <http://127.0.0.1:4000/notes/>. Jekyll rebuilds
when source files change; restart after changing `_config.yml`. Opening the
source `index.html` directly or serving the repository with a plain file server
will not process Liquid or Markdown. Only serve `_site` if using a static server.

## Publish one Markdown article

1. Create **one file**, `_posts/YYYY-MM-DD-your-slug.md`. Start from
   `_drafts/research-note-template.md` if useful.
2. Add the metadata below and write the article. If copying the template, remove
   its `published: false` only when ready for public release.
3. Preview locally; review claims, references, permissions, links, and figures.
4. Commit and push to a feature branch, then review and merge its PR into `main`.
   GitHub Pages builds automatically. No index or homepage HTML edits are needed.

```yaml
---
layout: note
title: "Your article title"
date: 2026-11-16
type: "Experiment Note"
tags:
  - agent-evaluation
description: "The question and scope of this note."
math: false
---
```

`type`, `tags`, `description`, and `math` are optional. Type defaults to
`Research Note`; other useful labels include Negative Result, Research
Perspective, Literature Commentary, and Reproducibility Note. These labels
are descriptive, not separate publishing systems.

The filename determines a stable URL such as `/notes/your-slug/`. Keep the slug
unique and unchanged after publication; changing the displayed title does not
change the URL. Match the front-matter date to the filename, using Europe/London
calendar dates. Future-dated posts are excluded; scheduled publication is not
configured.

Scientific content requires Haoran Xu's review before publication. Clearly
distinguish observations, hypotheses, interpretations, and limitations. Verify
citations and publication statuses; do not publish private logs, unreviewed
manuscripts, credentials, or collaborator material without permission.

## Drafts

Keep drafts as `_drafts/your-slug.md`, without a date prefix. The template also
has `published: false` as an extra safeguard. To preview these locally:

```bash
bundle exec jekyll serve --host 127.0.0.1 --drafts --unpublished
```

Those flags are **local preview only**. Normal builds omit drafts and posts
marked `published: false`. Never commit `_site` or enable drafts in the
production configuration. This is a public repository: draft source files are
still visible on GitHub even when absent from the website. Keep confidential
drafts outside this repository; the tracked template contains no research results.

## Figures, code, tables, and mathematics

Use ordinary Markdown headings, lists, blockquotes, tables, fenced code blocks
(with a language such as `python`), and links. Start article sections at `##`;
the layout supplies the `h1` title. Wide tables and code blocks scroll within
the article and are keyboard-accessible.

Store public images under `assets/notes/your-slug/` and use `relative_url` so
paths work from nested articles:

```liquid
![A meaningful description]({{ '/assets/notes/your-slug/figure.png' | relative_url }})
```

For captions, use semantic HTML (relative URL filters also work here):

```html
<figure>
  <img src="{{ '/assets/notes/your-slug/figure.png' | relative_url }}"
       alt="Describe the figure and its key information">
  <figcaption>Figure 1. Explain what is measured and any relevant limitations.</figcaption>
</figure>
```

Set `math: true` for LaTeX. Kramdown accepts `$$ ... $$` inline within a
paragraph, or on separate lines for a display equation:

```text
Inline: $$p(y \mid e)$$.

$$
\hat{y} = \arg\max_y p(y \mid e)
$$
```

Math requires access to the pinned KaTeX CDN; if it is blocked, the source
notation remains visible. Code blocks are excluded from math rendering.
When showing literal Liquid syntax in articles, wrap it in Liquid `raw` /
`endraw` tags so Jekyll does not evaluate it.

## Validate and troubleshoot

```bash
bundle exec jekyll build --strict_front_matter
python3 scripts/check_site.py
git diff --check
```

The Python check uses only the standard library and the installed bundle. It
builds the real site, then builds a temporary copy with test-only posts to check
ordering, latest-post synchronization, metadata, stable URLs, Markdown features,
nested assets, and exclusion of unpublished material. Fixtures never enter the
real `_posts` directory. It also checks that the profile photo survives the
build byte-for-byte and that the retired learning-contributions directory is
absent from both the source tree and built output.

If Pages fails, inspect the repository's Pages build/deployment logs. Confirm
the publishing source remains `main` at `/`, `.nojekyll` has not been added,
YAML front matter is valid, and required gems match the lockfile. Do not add
custom plugins or a new deployment workflow to fix a content error. To clear
stale local output, run `bundle exec jekyll clean`, then rebuild. Check nested
asset URLs for missing `relative_url` and file-name case mismatches. An unchanged
page may also be browser-cached; wait for the deployment to complete and reload.

The learning-contributions feature has been removed, including its page,
activity data, and maintenance documentation. After this change is merged
and deployed, `/learning-contributions/` and its JSON endpoint will no longer
be available; old Notion embeds will stop working. This is an intentional
removal, with no replacement route or data redirect. Earlier Git history
remains unchanged.
