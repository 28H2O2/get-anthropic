# Anthropic News Daily

Automatically scrapes new articles from 8 official Anthropic information sources every morning, translates them into Chinese, generates a local Markdown daily report, and builds a static frontend to display content from the last 30 days.

## Information Sources

| Source | Content |
|------|------|
| [Anthropic News](https://www.anthropic.com/news) | Official news and product announcements |
| [Anthropic Research](https://www.anthropic.com/research) | Research papers and technical blogs |
| [Claude Blog](https://www.anthropic.com/claude-blog) | Claude blog for users and enterprises |
| [Alignment Science](https://alignment.anthropic.com) | Dedicated blog for alignment science |
| [Engineering Blog](https://www.anthropic.com/engineering) | Engineering practice blog |
| [Red Team](https://red.anthropic.com) | Red teaming security research |
| [Claude Cookbook](https://platform.claude.com/cookbook) | Official development examples and tutorials |
| [Transformer Circuits](https://transformer-circuits.pub) | Interpretability research |

## Architecture

```
main.py          # Main scheduler: Scrape → Compare Index → Filter Date → Translate → Write Report
fetchers/        # Scraping layer for each source (returns article lists only)
translator.py    # Translation layer, supports aliyun / claude / deepl engines
build_data.py    # Merges daily reports and index into frontend JSON (public/data.json)
public/          # Static frontend, deployable to Vercel / GitHub Pages
article_index.json  # Full article index (persistence to prevent duplicate processing)
output/          # Daily Chinese reports (output/YYYY-MM-DD/digest.md)
```

## Quick Start

**1. Install Dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure Environment Variables** (Aliyun Machine Translation)

```bash
export ALIYUN_ACCESS_KEY_ID=your_key
export ALIYUN_ACCESS_KEY_SECRET=your_secret
```

**3. First Run: Initialize Index** (Marks all existing articles as known to avoid processing a large volume of historical articles on first run)

```bash
python3 main.py --init
```

**4. Run**

```bash
python3 main.py
```

The daily report is output to `output/YYYY-MM-DD/digest.md`.

## Automation (Daily Schedule)

Run automatically every day at 7:30 via crontab:

```bash
# crontab -e
30 7 * * * /path/to/get_anthropic/run.sh
```

`run.sh` executes `main.py` (scraping and translation) followed by `build_data.py` (updating frontend data).

## Common Parameters

```bash
python3 main.py --lookback 7   # Look back 7 days (default 3 days)
python3 main.py --limit 5      # Maximum of 5 articles per run
python3 main.py --force        # Ignore processed records, force re-processing
python3 main.py --date 2026-04-09  # Simulate running on a specific date
```

## Translation Engine Switching

Modify `translate_engine` in `config.json`:

| Engine | Required Environment Variables |
|------|-------------|
| `aliyun` (Default) | `ALIYUN_ACCESS_KEY_ID` / `ALIYUN_ACCESS_KEY_SECRET` |
| `claude` | `ANTHROPIC_API_KEY` |
| `deepl` | `DEEPL_API_KEY` |

`translate_mode` can be set to `summary` (first 500 words summary, default) or `full` (full text translation).

## Frontend Deployment

```bash
python3 build_data.py   # Generate public/data.json
```

Deploy the `public/` directory to Vercel or GitHub Pages to browse articles from the last 30 days in your browser.
