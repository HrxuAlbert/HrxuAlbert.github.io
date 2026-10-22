# Learning Contributions

A GitHub-style heatmap of daily learning activity, published at
<https://hrxualbert.github.io/learning-contributions/> and embedded in Notion.
No server, database, API key or build step: GitHub Pages serves the two files below.

## Files

- `index.html`: the heatmap. It reads `contributions.json` from the same directory on every load.
- `contributions.json`: the learning record and the single source of truth. **Normally the only file you edit.**

## Recording learning

`records` maps a date to a level:

```json
{
  "version": 1,
  "timezone": "Europe/London",
  "records": {
    "2026-10-21": 1,
    "2026-10-22": 2
  }
}
```

| Level | Meaning |
| --- | --- |
| 0 | No recorded learning (same as leaving the date out) |
| 1 | Light learning or review |
| 2 | Completed one learning question |
| 3 | Deep reasoning or conceptual understanding |
| 4 | Practical implementation or knowledge integration |

Rules:

- Dates are `YYYY-MM-DD` calendar days in Europe/London.
- Levels are integers 1–4. To clear a day, delete its entry.
- Keep entries in date order, keep `version` and `timezone` unchanged, and keep the file valid JSON.
- Only record days that actually happened. Never back-fill or invent history.
- Store levels only. Everything in this repository is public, so no notes, names or other personal details.

### For AI assistants (Codex, ChatGPT)

A request like "Record learning level 2 for 2026-10-22" means:

1. Edit `learning-contributions/contributions.json` only: set `records["2026-10-22"] = 2` (overwriting any existing value), or delete the key for level 0.
2. Validate the JSON (for example `python3 -m json.tool learning-contributions/contributions.json`).
3. Commit to `main` with a message like `Record learning level 2 for 2026-10-22` and push (or open a PR to `main` if direct pushes aren't available).
4. Do not modify `index.html`, the root homepage, or any other file.

"Today" means today's date in Europe/London.

## Publishing and refresh

GitHub Pages builds `main` (repository root) automatically, usually within a minute or two of a push.
The page fetches `contributions.json` with a cache-busting query, so a reload shows the latest published data.
An open embed also refreshes every 10 minutes and when its tab regains focus.

## Embedding in Notion

Type `/embed` in a Notion page, paste `https://hrxualbert.github.io/learning-contributions/`, then drag the embed to about 200–230 px tall.
The colours follow the device's light/dark setting. To pin one, embed
`https://hrxualbert.github.io/learning-contributions/?theme=dark` or `?theme=light` instead.
