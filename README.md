# leapps-website

Source for [leapps.org](https://leapps.org) — the website for the LEAPPs digital forensics tools: iLEAPP, ALEAPP, RLEAPP, VLEAPP, and LAVA.

The site is hosted on Squarespace and served as static HTML. A Cloudflare Worker handles dynamic data (GitHub stats, releases, blog posts, changelog, search index).

---

## Repo structure

```
leapps-website/
├── *.html               # All site pages (one file per page)
├── blog/
│   └── posts/
│       ├── index.json   # Blog post manifest (title, slug, date, tags, excerpt)
│       └── *.md         # Individual blog post content in Markdown
├── leapps-worker.js     # Cloudflare Worker — API proxy, blog feed, search index
├── sitemap.xml          # Sitemap for all pages
├── robots.txt           # Crawler rules
└── logos/               # Logo assets
```

### Pages

| File | URL |
|---|---|
| `home.html` | leapps.org/ |
| `about.html` | leapps.org/about |
| `artifacts.html` | leapps.org/artifacts |
| `blog.html` | leapps.org/blog |
| `blog-post.html` | leapps.org/blog-post (template for all posts) |
| `changelog.html` | leapps.org/changelog |
| `docs.html` | leapps.org/docs |
| `mailing.html` | leapps.org/mailing |
| `releases.html` | leapps.org/releases |
| `resources.html` | leapps.org/resources |
| `scoreboard.html` | leapps.org/scoreboard |
| `stats.html` | leapps.org/stats |
| `404.html` | leapps.org/404 |

---

## Cloudflare Worker

**Deployed at:** `https://leapps-api.4n6-198.workers.dev`

The worker is the backend for all dynamic content. Squarespace cannot serve arbitrary files or APIs, so the worker handles everything that requires live data or JSON endpoints.

### Routes

| Route | Description |
|---|---|
| `/repos/:repo/releases` | GitHub releases proxy with caching |
| `/repos/:repo/contributors` | GitHub contributors proxy |
| `/repos/:repo/contents/:path` | GitHub repo contents proxy (used for artifact list) |
| `/blog/posts/index.json` | Blog post manifest |
| `/blog/posts/:slug` | Individual blog post Markdown content |
| `/blog/feed` | RSS feed for blog posts |
| `/changelog/feed` | RSS feed aggregating releases across all tools |
| `/search-index` | Static JSON index of all site pages for search |

To update the worker: edit `leapps-worker.js` and deploy via the Cloudflare dashboard (Workers → leapps-api → Edit).

---

## Adding a blog post

Blog posts are plain Markdown files. Adding a post takes two file changes and a pull request.

### 1. Create the Markdown file

Add a file to `blog/posts/` named with this format:

```
YYYY-MM-DD-your-post-title.md
```

Start the file with YAML frontmatter:

```markdown
---
title: Your Post Title
date: 2026-06-05
author: Your Name
tags: [forensics, android, artifacts]
excerpt: A one or two sentence summary shown on the blog index and in search results.
---

Your content starts here...
```

**Frontmatter fields:**

| Field | Required | Notes |
|---|---|---|
| `title` | ✅ | Shown on blog index and post page |
| `date` | ✅ | Format: `YYYY-MM-DD` |
| `author` | ✅ | Your name or handle |
| `tags` | ✅ | Array of lowercase strings — used for filtering on the blog page |
| `excerpt` | ✅ | 1–2 sentences — shown on index card, og:description, and RSS |

### 2. Update the index

Open `blog/posts/index.json` and add an entry at the **top** of the array (newest first):

```json
{
  "slug": "2026-06-05-your-post-title",
  "title": "Your Post Title",
  "date": "2026-06-05",
  "author": "Your Name",
  "tags": ["forensics", "android", "artifacts"],
  "excerpt": "A one or two sentence summary shown on the blog index and in search results."
}
```

The `slug` must match the filename exactly (without the `.md` extension).

### 3. Open a pull request

Submit your PR against the `main` branch. Posts are reviewed before merging. Once merged, the post is live immediately — the worker serves the Markdown directly from the GitHub API.

### Markdown support

Posts support standard Markdown:

- Headings (`#`, `##`, `###`)
- Bold, italic, strikethrough
- Ordered and unordered lists
- Links and images
- Code blocks with syntax highlighting (fenced with backticks)
- Tables
- Blockquotes
- Horizontal rules

---

## Development

The site is static HTML — open any `.html` file in a browser or run a local server:

```bash
python3 -m http.server 3456
```

Then open `http://localhost:3456/home.html`.

Pages that fetch live data (stats, releases, changelog, artifacts, blog, search) pull from the worker and GitHub API directly, so they work from localhost without any local backend.

---

## Branching

| Branch | Purpose |
|---|---|
| `main` | Production — deployed to Squarespace |
| `brigs-working` | Active development branch — PRs merge here first |

---

## Contributing

- **Blog posts** — see [Adding a blog post](#adding-a-blog-post) above
- **Parsers and artifacts** — contribute to the individual tool repos ([iLEAPP](https://github.com/abrignoni/iLEAPP), [ALEAPP](https://github.com/abrignoni/ALEAPP), [RLEAPP](https://github.com/abrignoni/RLEAPP), [VLEAPP](https://github.com/abrignoni/VLEAPP))
- **Site bugs or improvements** — open an issue or PR against this repo
