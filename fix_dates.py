# 功能：一次性修复 article_index.json 中 anthropic_news/research 的错误日期
#        （之前用了 sitemap lastmod，现在改为从文章页面提取真实发布日期）
# 输入：article_index.json
# 输出：article_index.json（更新日期字段）
# 如何运行：python3 fix_dates.py
# 依赖文件：article_index.json, fetchers/anthropic_blog.py
# 项目作用：维护工具，通常只运行一次
# 最后修改：2026-04-13

import json
import time
from pathlib import Path
from fetchers.anthropic_blog import fetch_article_content

BASE_DIR = Path(__file__).parent
INDEX_FILE = BASE_DIR / "article_index.json"


def main():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        index = json.load(f)

    targets = {
        url: meta for url, meta in index.items()
        if meta.get("source") in ("anthropic_news", "anthropic_research")
    }
    print(f"共 {len(targets)} 篇 Anthropic 文章需要校验日期")

    updated = 0
    for i, (url, meta) in enumerate(targets.items(), 1):
        old_date = meta.get("date", "")
        _, _, pub_date = fetch_article_content(url)
        if pub_date and pub_date != old_date:
            print(f"  [{i}/{len(targets)}] 更新: {old_date} → {pub_date}  {url.split('/')[-1]}")
            index[url]["date"] = pub_date
            updated += 1
        else:
            print(f"  [{i}/{len(targets)}] 保持: {old_date}  {url.split('/')[-1]}")
        time.sleep(0.5)  # 礼貌性限速

    # 按日期倒序保存
    sorted_index = dict(
        sorted(index.items(), key=lambda x: x[1].get("date", ""), reverse=True)
    )
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_index, f, ensure_ascii=False, indent=2)

    print(f"\n完成：共更新 {updated} 条日期，已保存到 article_index.json")


if __name__ == "__main__":
    main()
