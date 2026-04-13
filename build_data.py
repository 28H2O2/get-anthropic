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
from datetime import date, timedelta

BASE_DIR = Path(__file__).parent
INDEX_FILE = BASE_DIR / "article_index.json"
OUTPUT_DIR = BASE_DIR / "output"
PUBLIC_DIR = BASE_DIR / "public"

SOURCE_LABELS = {
    "anthropic_news": "Anthropic News",
    "anthropic_research": "Anthropic Research",
    "cookbook": "Claude Cookbook",
    "transformer_circuits": "Transformer Circuits",
}

SOURCE_DESC = {
    "anthropic_news": "Anthropic 官方新闻与产品公告",
    "anthropic_research": "Anthropic 研究论文与技术博客",
    "cookbook": "Claude 官方开发示例与教程",
    "transformer_circuits": "Transformer 可解释性研究（Anthropic Circuits 团队）",
}

LOOKBACK_DAYS = 30


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
            r"\*\*中文(?:摘要|译文)\*\*[：:]\s*\n\n([\s\S]+?)(?=\n---|\Z)", block
        )
        if summary_match:
            summary_zh = summary_match.group(1).strip()

        result[url] = {"title_zh": title_zh, "summary_zh": summary_zh}

    return result


def build():
    if not INDEX_FILE.exists():
        print("[build_data] 找不到 article_index.json，请先运行 main.py")
        return

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index: dict = json.load(f)

    today = date.today()
    since = today - timedelta(days=LOOKBACK_DAYS)
    since_str = since.isoformat()
    today_str = today.isoformat()

    # 收集所有 digest 的摘要映射
    digest_map: dict[str, dict] = {}
    if OUTPUT_DIR.exists():
        for day_dir in sorted(OUTPUT_DIR.iterdir(), reverse=True):
            md = day_dir / "digest.md"
            if md.exists():
                digest_map.update(parse_digest(md))

    # 按日期分组，只取近 LOOKBACK_DAYS 天有真实日期的文章
    days: dict[str, list] = {}
    all_urls_by_source: dict[str, list] = {k: [] for k in SOURCE_LABELS}

    for url, meta in index.items():
        source = meta.get("source", "")
        title_en = meta.get("title", "") or url.split("/")[-1]
        art_date = meta.get("date", "")

        # 全量链接归档（用于底部展示）
        if source in all_urls_by_source:
            all_urls_by_source[source].append({
                "url": url,
                "title": title_en,
                "desc": SOURCE_DESC.get(source, ""),
                "date": art_date,  # 文章发布日期
            })

        # 只展示近 30 天内有日期的文章（无论是否翻译，无摘要显示占位）
        if not art_date:
            continue
        if not (since_str <= art_date <= today_str):
            continue

        digest_info = digest_map.get(url, {})
        article = {
            "url": url,
            "title_en": title_en,
            "title_zh": digest_info.get("title_zh", title_en),
            "summary_zh": digest_info.get("summary_zh", ""),
            "source": SOURCE_LABELS.get(source, source),
            "source_key": source,
            "date": art_date,
        }
        days.setdefault(art_date, []).append(article)

    # 按日期倒序
    digests = [
        {"date": d, "articles": sorted(articles, key=lambda x: x["date"], reverse=True)}
        for d, articles in sorted(days.items(), reverse=True)
    ]

    data = {
        "generated_at": today_str,
        "lookback_days": LOOKBACK_DAYS,
        "digests": digests,
        "all_urls": all_urls_by_source,
    }

    PUBLIC_DIR.mkdir(exist_ok=True)
    out_file = PUBLIC_DIR / "data.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total = sum(len(d["articles"]) for d in digests)
    print(f"[build_data] 已生成 {out_file}，近 {LOOKBACK_DAYS} 天共 {total} 篇文章")


if __name__ == "__main__":
    build()
