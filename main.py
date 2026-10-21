"""Discover, verify publication metadata, and persist retryable Chinese excerpts."""
import argparse
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from fetchers.common import SOURCE_URLS, discover, fetch_article, is_article, normalize_url
from translator import translate, valid_translation

BASE_DIR = Path(__file__).resolve().parent
INDEX_FILE = BASE_DIR / "article_index.json"
STATUS_FILE = BASE_DIR / "fetch_status.json"
SOURCE_LABELS = {
    "anthropic_news": "Anthropic News", "anthropic_research": "Anthropic Research",
    "cookbook": "Claude Cookbook", "transformer_circuits": "Transformer Circuits",
    "red_team": "Red Team", "claude_blog": "Claude Blog", "alignment": "Alignment Science", "engineering": "Engineering Blog",
}
# A specialized source owns articles also present in the general research sitemap.
SOURCE_PRIORITY = {s: i for i, s in enumerate(SOURCE_LABELS)}


def article_source(url, *sources):
    source = max((s for s in sources if s), key=lambda s: SOURCE_PRIORITY.get(s, -1))
    if source in {"anthropic_news", "anthropic_research"}:
        if "/news/" in url:
            return "anthropic_news"
        if "/research/" in url:
            return "anthropic_research"
    return source


def read_json(path, default=None):
    return json.loads(path.read_text()) if path.exists() else ({} if default is None else default)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_config():
    return read_json(BASE_DIR / "config.json")


def load_index():
    return read_json(INDEX_FILE)


def save_index(index):
    write_json(INDEX_FILE, dict(sorted(index.items(), key=lambda item: (item[1].get("date", ""), item[0]), reverse=True)))


def migrate(index, output_dir):
    """Import the latest *valid* legacy excerpt, once; records become authoritative."""
    from build_data import parse_digest
    summaries = {}
    for path in sorted(output_dir.glob("*/digest.md")):
        for url, item in parse_digest(path).items():
            text = re.sub(r"^【机器翻译摘要】\s*", "", item.get("summary_zh", "")).strip()
            if valid_translation(text):
                summaries[normalize_url(url)] = {**item, "summary_zh": text}
    result = {}
    for url, original in index.items():
        key, meta = normalize_url(url), dict(original)
        if "summary_status" not in meta:
            cached = summaries.get(key, {})
            meta.update(cached)
            meta["summary_status"] = "ready" if cached else "pending"
            meta["processed"] = bool(cached)
            # Legacy date may be a sitemap lastmod or an estimate; verify before publishing.
            meta["date_verified"] = False
            meta["date_precision"] = {10: "day", 7: "month", 4: "year"}.get(len(meta.get("date", "")), "unknown")
        if not valid_translation(meta.get("summary_zh", "")):
            meta.pop("summary_zh", None)
            meta["processed"] = False
            if meta.get("summary_status") == "ready":
                meta["summary_status"] = "pending"
        result[key] = merge_records(result.get(key, {}), meta)
    return result


def merge_records(existing, incoming):
    """Canonical duplicates keep a valid cached excerpt and verified publication date."""
    result = {**existing, **incoming}
    for name in ("summary_zh", "title_zh", "summary_updated_at"):
        if not incoming.get(name) and existing.get(name):
            result[name] = existing[name]
    if existing.get("date_verified") and not incoming.get("date_verified"):
        for name in ("date", "date_precision", "date_verified"):
            result[name] = existing[name]
    if valid_translation(result.get("summary_zh", "")):
        result.update(summary_status="ready", processed=True)
    sources = [s for s in (existing.get("source"), incoming.get("source")) if s]
    if sources:
        result["source"] = max(sources, key=lambda s: SOURCE_PRIORITY.get(s, -1))
    result["aliases"] = sorted(set(existing.get("aliases", []) + incoming.get("aliases", [])))
    return result


def recent(meta, since, today):
    # Month-only/year-only dates stay visible at their actual precision in the archive.
    return len(meta.get("date", "")) == 10 and since <= meta["date"] <= today


def needs_metadata(meta, since, today, repair=False):
    if recent(meta, since, today) and (repair or not meta.get("date_verified")):
        return True
    if not meta.get("metadata_checked_at") and meta.get("first_seen_at", "") >= since:
        return True
    if meta.get("fetch_status") == "failed" and meta.get("first_seen_at", "") >= since:
        return True
    return repair and meta.get("source") in {"alignment", "transformer_circuits", "cookbook"} and (not meta.get("date") or (not meta.get("metadata_checked_at") and meta["date"].startswith(today[:4])))


def should_translate(meta, since, today, force=False):
    in_scope = recent(meta, since, today) if meta.get("date") else bool(meta.get("first_seen_at") and meta["first_seen_at"] >= since)
    return in_scope and meta.get("fetch_status") == "ok" and (force or not valid_translation(meta.get("summary_zh", "")))


def discover_all(config, previous, stamp):
    articles, statuses = [], {}
    for source in SOURCE_LABELS:
        if not config.get("sources", {}).get(source):
            continue
        prior = previous.get("sources", {}).get(source, {})
        try:
            found = discover(source)
            if not found:
                raise ValueError("source returned zero articles")
            articles.extend(found)
            statuses[source] = {"status": "ok", "discovered": len(found), "last_success_at": stamp, "url": SOURCE_URLS[source]}
            print(f"[{source}] discovered {len(found)}", flush=True)
        except Exception as exc:
            statuses[source] = {"status": "failed", "discovered": 0, "last_success_at": prior.get("last_success_at"), "url": SOURCE_URLS[source], "error": type(exc).__name__}
            print(f"[{source}] FAILED ({type(exc).__name__})", flush=True)
    return articles, statuses


def update_metadata(index, candidates, stamp):
    def fetch(url):
        try:
            return url, fetch_article(url), None
        except Exception as exc:
            return url, None, type(exc).__name__
    contents = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for old_url, details, error in pool.map(fetch, candidates):
            meta = index[old_url]
            meta["metadata_checked_at"] = stamp
            if error:
                meta.update(fetch_status="failed", summary_status="failed", last_error="正文获取暂时失败")
                print(f"[metadata] FAILED {old_url}: {error}", flush=True)
                continue
            details = dict(details)
            canonical = details.pop("url")
            content = details.pop("content")
            # A non-article redirect must not turn a listing page into a news item.
            if not any(is_article(canonical, source) for source in SOURCE_LABELS):
                meta.update(excluded=True, fetch_status="not_article")
                continue
            meta.update(details, date_verified=True, fetch_status="ok")
            meta["source"] = article_source(canonical, meta["source"])
            if valid_translation(meta.get("summary_zh", "")):
                meta.update(summary_status="ready", processed=True)
                meta.pop("last_error", None)
            if old_url != canonical:
                meta["aliases"] = sorted(set(meta.get("aliases", []) + [old_url]))
                index[canonical] = merge_records(index.get(canonical, {}), meta)
                index[canonical]["source"] = article_source(canonical, index[canonical]["source"])
                del index[old_url]
            contents[canonical] = content
            print(f"[metadata] {details['date'] or 'unknown'} {canonical}", flush=True)
    return contents


def render_digest(records, today):
    lines = [f"# Anthropic 每日简报 {today}", "", f"> 共 **{len(records)}** 篇中文摘录", "", "---", ""]
    for url, meta in records:
        lines += [f"### [{meta.get('title_zh') or meta.get('title')}]({url})", "", f"**来源**: {SOURCE_LABELS.get(meta['source'], meta['source'])}", "", f"**发布日期**: {meta.get('date') or '未提供'}", "", f"**原文**: {url}", "", "**中文摘录**：", "", meta["summary_zh"], "", "---", ""]
    return "\n".join(lines)


def write_run_summary(status):
    path = os.getenv("GITHUB_STEP_SUMMARY")
    if not path:
        return
    lines = ["## Anthropic 抓取与中文摘录", "", "| 来源 | 状态 | 发现数 | 最近成功时间 |", "|---|---|---:|---|"]
    for source, info in status.get("sources", {}).items():
        lines.append(f"| {SOURCE_LABELS[source]} | {info['status']} | {info['discovered']} | {info.get('last_success_at') or '—'} |")
    lines += ["", f"本次生成 {status.get('translated', 0)} 篇；失败 {status.get('failed', 0)} 篇。", ""]
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default="")
    parser.add_argument("--lookback", type=int, default=30)
    parser.add_argument("--repair-recent", action="store_true", help="重新核验近期元数据并恢复历史漏抓来源")
    parser.add_argument("--force", action="store_true", help="重做窗口内已有摘录")
    parser.add_argument("--limit", type=int, default=0, help="限制翻译数量，不限制元数据核验")
    parser.add_argument("--init", action="store_true", help="建立发现基线，不翻译；保留已有文章")
    parser.add_argument("--check-health", action="store_true")
    args = parser.parse_args()
    if args.check_health:
        status = read_json(STATUS_FILE)
        return 0 if status and status.get("status") == "ok" else 1
    today = args.date or datetime.now(ZoneInfo("Asia/Taipei")).date().isoformat()
    since = (date.fromisoformat(today) - timedelta(days=args.lookback)).isoformat()
    stamp = datetime.now(ZoneInfo("Asia/Taipei")).isoformat(timespec="seconds")
    config = load_config()
    output = BASE_DIR / config.get("output_dir", "output")
    index = migrate(load_index(), output)
    previous = read_json(STATUS_FILE)
    discovered, sources = discover_all(config, previous, stamp)
    status = {"checked_at": stamp, "sources": sources, "translated": 0, "failed": 0, "status": "ok"}
    if any(s["status"] != "ok" for s in sources.values()):
        status["status"] = "source_failed"
        write_json(STATUS_FILE, status)
        write_run_summary(status)
        return 2
    # Aliases suppress rediscovery under a pre-migration URL.
    aliases = {alias: url for url, meta in index.items() for alias in meta.get("aliases", [])}
    for item in discovered:
        url = aliases.get(item["url"], item["url"])
        meta = index.setdefault(url, {"summary_status": "pending", "processed": False, "first_seen_at": "" if args.init else today})
        meta["source"] = article_source(url, meta.get("source", ""), item["source"])
        if not meta.get("title"):
            meta["title"] = item.get("title", "")
        if item.get("sitemap_lastmod"):
            meta["sitemap_lastmod"] = item["sitemap_lastmod"]
        if item.get("date") and not meta.get("date_verified"):
            meta["date"] = item["date"]
        meta.setdefault("date", "")
        if args.init:
            meta["metadata_checked_at"] = stamp
    if args.init:
        save_index(index)
        write_json(STATUS_FILE, status)
        return 0
    # Remove known category pages without discarding historic article records.
    index = {u: m for u, m in index.items() if any(is_article(u, s) for s in SOURCE_LABELS)}
    candidates = [u for u, m in index.items() if needs_metadata(m, since, today, args.repair_recent)]
    # Missing excerpts need body retrieval on every retry, even after the 3-day discovery window.
    candidates += [u for u, m in index.items() if should_translate(m, since, today, args.force) and u not in candidates]
    print(f"Verifying {len(candidates)} article metadata records", flush=True)
    contents = update_metadata(index, candidates, stamp)
    save_index(index)
    translated = []
    attempted = 0
    for url, meta in list(index.items()):
        if not should_translate(meta, since, today, args.force):
            continue
        if args.limit and attempted >= args.limit:
            break
        attempted += 1
        try:
            body = contents.get(url)
            if not body:
                body = fetch_article(url)["content"]
            title_zh = translate(meta.get("title", ""), "", config.get("translate_engine", "aliyun"), "full", config.get("claude_model"))
            summary = translate("", body, config.get("translate_engine", "aliyun"), "summary", config.get("claude_model"))
            meta.update(title_zh=title_zh, summary_zh=summary, summary_status="ready", processed=True, summary_updated_at=stamp)
            meta.pop("last_error", None)
            translated.append((url, meta))
            print(f"[translated] {url}", flush=True)
        except Exception as exc:
            meta.update(summary_status="failed", processed=False, last_error="中文摘录生成暂时失败")
            print(f"[translation] FAILED {url}: {type(exc).__name__}", flush=True)
        save_index(index)
    status["translated"] = len(translated)
    status["failed"] = sum((recent(m, since, today) or (not m.get("date") and m.get("first_seen_at", "") >= since)) and (m.get("summary_status") == "failed" or m.get("fetch_status") == "failed") for m in index.values())
    status["status"] = "degraded" if status["failed"] else "ok"
    status["last_success_at"] = stamp
    write_json(STATUS_FILE, status)
    if translated:
        # Rebuild today's document from authoritative records, preserving earlier same-day runs.
        records = [(u, m) for u, m in index.items() if m.get("summary_updated_at", "").startswith(today) and valid_translation(m.get("summary_zh", ""))]
        destination = output / today / "digest.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(render_digest(records, today), encoding="utf-8")
    write_run_summary(status)
    print(f"Run: {status['status']}; translated={status['translated']}; failed={status['failed']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
