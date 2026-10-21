# 功能：将 article_index.json 和 output/*/digest.md 合并为前端可读的 JSON 数据文件
# 输入：
#   - article_index.json（全量文章索引，项目根目录）
#   - output/YYYY-MM-DD/digest.md（各日期翻译日报）
# 输出：public/data.json（前端展示数据，含近14天摘要 + 全量原文链接）
# 如何运行：python3 build_data.py
# 依赖文件：article_index.json, output/ 目录
# 项目作用：数据构建层，将本地运行产物转成 Vercel 静态站可读的 JSON
# 最后修改：2026-04-13

import json
import re
from pathlib import Path
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from translator import valid_translation
from fetchers.common import is_article, normalize_url

BASE_DIR = Path(__file__).parent
INDEX_FILE = BASE_DIR / "article_index.json"
OUTPUT_DIR = BASE_DIR / "output"
PUBLIC_DIR = BASE_DIR / "public"

SOURCE_LABELS = {
    "anthropic_news": "Anthropic News",
    "anthropic_research": "Anthropic Research",
    "cookbook": "Claude Cookbook",
    "transformer_circuits": "Transformer Circuits",
    "red_team": "Red Team",
    "claude_blog": "Claude Blog",
    "alignment": "Alignment Science",
    "engineering": "Engineering Blog",
}

SOURCE_DESC = {
    "anthropic_news": "Anthropic 官方新闻与产品公告",
    "anthropic_research": "Anthropic 研究论文与技术博客",
    "cookbook": "Claude 官方开发示例与教程",
    "transformer_circuits": "Transformer 可解释性研究（Anthropic Circuits 团队）",
    "red_team": "Anthropic 红队安全研究（red.anthropic.com）",
    "claude_blog": "Claude 官方博客（面向用户与企业）",
    "alignment": "Anthropic 对齐科学专项博客（alignment.anthropic.com）",
    "engineering": "Anthropic 工程实践博客（anthropic.com/engineering）",
}

LOOKBACK_DAYS = 30

# 固定参考链接（不通过 fetcher 抓取，直接写入归档区）
STATIC_REFS = [
    {
        "key": "references",
        "title": "References",
        "desc": "Anthropic 重要参考文档",
        "items": [
            {
                "url": "https://www.anthropic.com/constitution",
                "title": "Claude's Constitution",
                "desc": "Claude 的价值观与行为准则",
                "date": "2024-05-08",
            },
        ],
    }
]


def parse_digest(md_path: Path) -> dict[str, dict]:
    """解析单个 digest.md，提取每篇文章的中文摘要和标题。
    返回 {url: {"summary_zh": "...", "title_zh": "..."}}
    """
    result = {}
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return result

    # 按 "---" 分隔每篇文章的块
    blocks = text.split("\n---\n")
    for block in blocks:
        # 提取 URL：**原文**: https://...
        url_match = re.search(r"\*\*原文\*\*:\s*(https?://\S+)", block)
        if not url_match:
            continue
        url = url_match.group(1).strip()

        # 提取中文标题（### [...](url) 行）
        title_zh = ""
        title_match = re.search(r"###\s+\[(.+?)\]\(https?://", block)
        if title_match:
            title_zh = title_match.group(1).strip()

        # 提取中文摘要（**中文摘要** 或 **中文译文** 后到下一个 ## 或末尾）
        summary_zh = ""
        summary_match = re.search(
            r"\*\*中文(?:摘要|译文|摘录)\*\*[：:]\s*\n\n([\s\S]+?)(?=\n---|\Z)", block
        )
        if summary_match:
            summary_zh = summary_match.group(1).strip()

        result[url] = {"title_zh": title_zh, "summary_zh": summary_zh}

    return result


def build():
    if not INDEX_FILE.exists():
        raise RuntimeError("article_index.json is missing")
    index = json.loads(INDEX_FILE.read_text())
    status_file = BASE_DIR / "fetch_status.json"
    status = json.loads(status_file.read_text()) if status_file.exists() else {}
    if not status.get("sources") or any(s["status"] != "ok" for s in status["sources"].values()):
        raise RuntimeError("source discovery failed or has not run; preserving published data")
    now = datetime.now(ZoneInfo("Asia/Taipei"))
    today = now.date().isoformat()
    since = (now.date() - timedelta(days=LOOKBACK_DAYS)).isoformat()
    days = {}
    archives = {k: [] for k in SOURCE_LABELS}
    for url, meta in index.items():
        source, published = meta.get("source", ""), meta.get("date", "")
        if source not in archives or meta.get("excluded") or not is_article(url, source):
            continue
        archives[source].append({"url": url, "title": meta.get("title") or url.rsplit("/", 1)[-1], "desc": SOURCE_DESC[source], "date": published if meta.get("date_verified") else "", "date_precision": meta.get("date_precision", "unknown")})
        dated = len(published) == 10 and since <= published <= today and meta.get("date_verified")
        undated = not published and meta.get("first_seen_at", "") >= since and meta.get("fetch_status") != "not_article"
        if not (dated or undated):
            continue
        summary = meta.get("summary_zh", "")
        ready = valid_translation(summary)
        article_status = "ready" if ready else meta.get("summary_status", "pending")
        if article_status not in {"ready", "pending", "failed"}:
            raise ValueError("invalid article status")
        article = {"url": normalize_url(url), "title_en": meta.get("title") or url.rsplit("/", 1)[-1], "title_zh": meta.get("title_zh", ""), "summary_zh": summary if ready else "", "summary_en": meta.get("summary_en", ""), "summary_status": article_status, "source": SOURCE_LABELS[source], "source_key": source, "date": published, "date_precision": meta.get("date_precision", "unknown")}
        days.setdefault(published, []).append(article)
    digests = [{"date": d, "articles": sorted(articles, key=lambda a: (a["source_key"], a["url"]))} for d, articles in sorted(days.items(), reverse=True)]
    for items in archives.values():
        items.sort(key=lambda a: (a["date"], a["url"]), reverse=True)
    articles = [a for day in digests for a in day["articles"]]
    counts = {key: sum(a["summary_status"] == key for a in articles) for key in ("ready", "pending", "failed")}
    data = {"generated_at": today, "generated_at_iso": now.isoformat(timespec="seconds"), "lookback_days": LOOKBACK_DAYS, "digests": digests, "all_urls": archives, "archive_order": ["anthropic_news", "anthropic_research", "claude_blog", "red_team", "alignment", "engineering", "cookbook", "transformer_circuits"], "static_refs": STATIC_REFS, "health": {"status": status["status"], "last_success_at": status.get("last_success_at"), "sources": status["sources"], "summary_coverage": {"total": len(articles), **counts, "ratio": round(counts["ready"] / len(articles), 4) if articles else 0}}}
    validate(data)
    PUBLIC_DIR.mkdir(exist_ok=True)
    temporary = PUBLIC_DIR / "data.json.tmp"
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(PUBLIC_DIR / "data.json")
    print(f"[build_data] {len(articles)} articles; ready={counts['ready']}; pending={counts['pending']}; failed={counts['failed']}")
    return data


def validate(data):
    seen = set()
    if not data["health"]["sources"] or any(s["status"] != "ok" or s["discovered"] <= 0 for s in data["health"]["sources"].values()):
        raise ValueError("invalid source health")
    for day in data["digests"]:
        for article in day["articles"]:
            if article["url"] in seen:
                raise ValueError("duplicate canonical article")
            seen.add(article["url"])
            if article["summary_status"] == "ready" and not valid_translation(article["summary_zh"]):
                raise ValueError("invalid successful excerpt")
            if article["date"] and len(article["date"]) != 10:
                raise ValueError("inexact publication date in daily timeline")
    if not seen:
        raise ValueError("refusing to publish an empty recent feed")


if __name__ == "__main__":
    build()
