# 功能：Anthropic 内容聚合主脚本，每天拉取新文章并翻译生成中文日报
# 输入：
#   - config.json（配置文件，来自项目根目录）
#   - article_index.json（全量文章索引，来自项目根目录）
#   - 各信息源网页（anthropic.com, platform.claude.com, transformer-circuits.pub）
# 输出：
#   - output/YYYY-MM-DD/digest.md（当日中文日报，只含近期新文章）
#   - article_index.json（更新后的全量文章索引，含标题/链接/日期/来源）
# 如何运行：
#   python3 main.py                         # 正常运行（只处理近 lookback_days 天的新文章）
#   python3 main.py --date 2026-04-09       # 模拟指定日期运行
#   python3 main.py --lookback 7            # 向前看 7 天（默认 3 天）
#   python3 main.py --force                 # 忽略已处理记录，强制重新处理符合日期的文章
#   python3 main.py --limit 5              # 每次最多处理 N 篇新文章
# 依赖文件：
#   fetchers/anthropic_blog.py, fetchers/cookbook.py, fetchers/transformer.py
#   translator.py, config.json
# 项目作用：主协调器，调度 fetcher → 对比索引 → 日期过滤 → 翻译 → 输出日报
# 最后修改：2026-04-13

import json
import argparse
from datetime import date, timedelta
from pathlib import Path

from fetchers import anthropic_blog, cookbook, transformer, red_team, claude_blog
from translator import translate

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
INDEX_FILE = BASE_DIR / "article_index.json"


def load_config() -> dict:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_index() -> dict:
    """加载文章索引 {url: {title, date, source}}"""
    if not INDEX_FILE.exists():
        return {}
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index: dict):
    """持久化文章索引，按 date 倒序排列"""
    sorted_index = dict(
        sorted(index.items(), key=lambda x: x[1].get("date", ""), reverse=True)
    )
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_index, f, ensure_ascii=False, indent=2)


def fetch_all_articles(config: dict) -> list[dict]:
    """调用各 fetcher 获取文章列表"""
    articles = []
    sources = config.get("sources", {})

    if sources.get("anthropic_news") or sources.get("anthropic_research"):
        for a in anthropic_blog.fetch_article_list():
            if a["source"] == "anthropic_news" and sources.get("anthropic_news"):
                articles.append(a)
            elif a["source"] == "anthropic_research" and sources.get("anthropic_research"):
                articles.append(a)

    if sources.get("cookbook"):
        articles.extend(cookbook.fetch_article_list())

    if sources.get("transformer_circuits"):
        articles.extend(transformer.fetch_article_list())

    if sources.get("red_team"):
        articles.extend(red_team.fetch_article_list())

    if sources.get("claude_blog"):
        articles.extend(claude_blog.fetch_article_list())

    return articles


def fetch_content(article: dict, since_str: str, today_str: str) -> str:
    """获取文章正文，同时回写标题和真实发布日期到 article 字典。

    对于 Anthropic 文章，会从页面 meta 标签提取真实发布日期覆盖 lastmod，
    如果真实日期不在时间窗口内则返回空字符串（调用方跳过该文章）。
    """
    source = article["source"]
    url = article["url"]

    if source == "cookbook" and article.get("description"):
        return article["description"]

    if source in ("anthropic_news", "anthropic_research"):
        content, title, pub_date = anthropic_blog.fetch_article_content(url)
        if title and not article.get("title"):
            article["title"] = title
        # 用真实发布日期覆盖 sitemap 的 lastmod
        if pub_date:
            article["date"] = pub_date
            # 真实日期不在时间窗口内，跳过（lastmod 更新误触发）
            if not (since_str <= pub_date <= today_str):
                print(f"  → 真实发布日期 {pub_date} 超出窗口，跳过")
                return ""
        return content or ""
    elif source == "red_team":
        if article.get("description"):
            # 首页有 description 时优先用于翻译，同时补充日期
            content, title, pub_date = red_team.fetch_article_content(url)
            if title and not article.get("title"):
                article["title"] = title
            if pub_date:
                article["date"] = pub_date
                if not (since_str <= pub_date <= today_str):
                    print(f"  → 真实发布日期 {pub_date} 超出窗口，跳过")
                    return ""
            return article["description"]
        content, title, pub_date = red_team.fetch_article_content(url)
        if title and not article.get("title"):
            article["title"] = title
        if pub_date:
            article["date"] = pub_date
            if not (since_str <= pub_date <= today_str):
                print(f"  → 真实发布日期 {pub_date} 超出窗口，跳过")
                return ""
        return content or ""
    elif source == "claude_blog":
        content, title, pub_date = claude_blog.fetch_article_content(url)
        if title and not article.get("title"):
            article["title"] = title
        if pub_date:
            article["date"] = pub_date
            if not (since_str <= pub_date <= today_str):
                print(f"  → 真实发布日期 {pub_date} 超出窗口，跳过")
                return ""
        return content or ""
    elif source == "cookbook":
        return cookbook.fetch_article_content(url) or ""
    elif source == "transformer_circuits":
        return transformer.fetch_article_content(url) or ""
    return ""


SOURCE_LABELS = {
    "anthropic_news": "Anthropic News",
    "anthropic_research": "Anthropic Research",
    "cookbook": "Claude Cookbook",
    "transformer_circuits": "Transformer Circuits",
    "red_team": "Red Team",
    "claude_blog": "Claude Blog",
}


def build_digest(new_articles: list[dict], config: dict, today_str: str, since_str: str = "") -> tuple[str, list[dict]]:
    """生成 Markdown 格式的每日日报"""
    engine = config.get("translate_engine", "aliyun")
    mode = config.get("translate_mode", "summary")
    claude_model = config.get("claude_model", "claude-haiku-4-5-20251001")

    lines = [
        f"# Anthropic 每日简报 {today_str}",
        f"",
        f"> 共发现 **{len(new_articles)}** 篇新文章",
        f"> 翻译引擎：{engine} | 模式：{'摘要' if mode == 'summary' else '全文'}",
        f"",
        "---",
        "",
    ]

    actually_processed = []  # 只记录真正翻译成功的文章

    for i, article in enumerate(new_articles, 1):
        url = article["url"]
        raw_title = article.get("title", "")
        source_label = SOURCE_LABELS.get(article["source"], article["source"])
        date_str = article.get("date", today_str)

        print(f"[{i}/{len(new_articles)}] 处理：{raw_title or url}")

        content = fetch_content(article, since_str, today_str)
        if not content:
            # 真实发布日期超出窗口或内容获取失败，跳过，不标记为已处理
            continue
        title = article.get("title") or raw_title or url

        zh_text = translate(title, content, engine, mode, claude_model) if content else "[无法获取正文内容]"

        lines += [
            f"### [{title}]({url})",
            f"",
            f"**来源**: {source_label}  ",
            f"**发布日期**: {date_str}  ",
            f"**原文**: {url}",
            f"",
            f"**中文{'摘要' if mode == 'summary' else '译文'}**：",
            f"",
            zh_text,
            f"",
            "---",
            "",
        ]
        actually_processed.append(article)

    return "\n".join(lines), actually_processed


def init_index(config: dict):
    """初始化索引：抓取全量文章列表，建立基准，无日期文章标记为已知（不再重复处理）"""
    print("=== 初始化文章索引（只运行一次）===")
    index = {}
    for a in fetch_all_articles(config):
        url = a["url"]
        has_date = bool(a.get("date"))
        index[url] = {
            "title": a.get("title", ""),
            "date": a.get("date", ""),
            "source": a["source"],
            # 无日期文章（Cookbook/transformer）标记为已知，避免首次运行时全量处理
            "processed": not has_date,
        }
    save_index(index)
    no_date = sum(1 for v in index.values() if not v.get("date"))
    print(f"索引初始化完成：共 {len(index)} 篇，其中 {no_date} 篇无日期（已标记为已知）")
    print("之后运行 python3 main.py 即可正常使用。")


def main():
    parser = argparse.ArgumentParser(description="Anthropic 内容聚合 & 翻译日报")
    parser.add_argument("--init", action="store_true", help="初始化索引（首次使用时运行）")
    parser.add_argument("--date", type=str, default="", help="模拟指定日期运行，格式 YYYY-MM-DD")
    parser.add_argument("--lookback", type=int, default=3, help="向前看几天内的文章（默认 3 天）")
    parser.add_argument("--force", action="store_true", help="忽略已处理记录，重新处理符合日期的文章")
    parser.add_argument("--limit", type=int, default=0, help="单次最多处理 N 篇（0=不限）")
    args = parser.parse_args()

    config = load_config()

    if args.init:
        init_index(config)
        return

    today = date.fromisoformat(args.date) if args.date else date.today()
    today_str = today.isoformat()
    since_str = (today - timedelta(days=args.lookback)).isoformat()

    print(f"=== 运行日期：{today_str}，向前看：{args.lookback} 天（≥ {since_str}）===")

    index = load_index()

    print("=== 开始抓取各信息源 ===")
    all_articles = fetch_all_articles(config)
    print(f"共发现 {len(all_articles)} 篇文章")

    # 记录运行前的已知 URL 集合（用于判断「首次发现」）
    known_urls_before = set(index.keys())

    # 更新索引（补充新发现的 URL，不覆盖已有标题）
    for a in all_articles:
        url = a["url"]
        if url not in index:
            index[url] = {
                "title": a.get("title", ""),
                "date": a.get("date", ""),
                "source": a["source"],
            }
        elif not index[url].get("date") and a.get("date"):
            index[url]["date"] = a["date"]

    def is_new(a: dict) -> bool:
        url = a["url"]
        art_date = a.get("date", "")

        if not args.force and index.get(url, {}).get("processed"):
            return False   # 已处理过

        if art_date:
            # 有日期：必须在时间窗口内
            return since_str <= art_date <= today_str
        else:
            # 无日期（Cookbook/transformer）：只在首次发现时处理
            return url not in known_urls_before

    new_articles = [a for a in all_articles if is_new(a)]

    # 按日期倒序（最新的先处理）
    new_articles.sort(key=lambda x: x.get("date", ""), reverse=True)

    print(f"其中近 {args.lookback} 天内有 {len(new_articles)} 篇新文章")

    if not new_articles:
        print(f"近 {args.lookback} 天无新文章，跳过。")
        save_index(index)
        return

    if args.limit > 0:
        new_articles = new_articles[:args.limit]
        print(f"（已按 --limit {args.limit} 限制处理数量）")

    print("=== 开始翻译 ===")
    digest, actually_processed = build_digest(new_articles, config, today_str, since_str)

    # 写入日报（同一天多次运行时追加，避免覆盖已有摘要）
    output_dir = BASE_DIR / config.get("output_dir", "output") / today_str
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "digest.md"
    if output_file.exists():
        # 追加：去掉新 digest 的标题行，只保留文章条目部分
        existing = output_file.read_text(encoding="utf-8")
        # 提取新 digest 中的文章块（--- 之后的内容）
        parts = digest.split("\n---\n", 1)
        append_content = "\n---\n" + parts[1] if len(parts) > 1 else ""
        if append_content.strip():
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(append_content)
            print(f"=== 已追加到 {output_file} ===")
        else:
            print(f"=== 无新内容可追加 ===")
    else:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(digest)
        print(f"=== 日报已保存到 {output_file} ===")

    # 只标记实际翻译成功的文章为已处理（跳过的不标记，下次运行可重试）
    for a in actually_processed:
        url = a["url"]
        index[url]["processed"] = True
        if a.get("title"):
            index[url]["title"] = a["title"]
        if a.get("date"):
            index[url]["date"] = a["date"]  # 保存真实发布日期（覆盖 sitemap lastmod）

    save_index(index)
    processed_count = sum(1 for v in index.values() if v.get("processed"))
    print(f"article_index.json 已更新，共 {len(index)} 篇，已处理 {processed_count} 篇")


if __name__ == "__main__":
    main()
