# 功能：抓取 transformer-circuits.pub 的最新可解释性研究文章
# 输入：https://transformer-circuits.pub/（公开静态 HTML）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "...", "source": "transformer_circuits"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4
# 项目作用：Anthropic 可解释性研究（Circuits 团队）的发现层
# 最后修改：2026-04-10

import requests
from bs4 import BeautifulSoup
import re
from typing import Optional

BASE_URL = "https://transformer-circuits.pub"
INDEX_URL = "https://transformer-circuits.pub/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

# 匹配文章路径：年份/名称/index.html 或类似结构
ARTICLE_PATH_RE = re.compile(r"^(20\d{2})/[^/]+/(index\.html|[\w-]+\.html)$")


def fetch_article_list() -> list[dict]:
    """从首页解析所有正式文章链接（跳过外部链接和 updates）"""
    try:
        resp = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[transformer] 获取首页失败: {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml")
    articles = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()

        # 只处理相对路径的本站文章
        if href.startswith("http"):
            continue
        if not ARTICLE_PATH_RE.match(href):
            continue

        url = f"{BASE_URL}/{href}"
        if url in seen:
            continue
        seen.add(url)

        title = a.get_text(strip=True)
        if not title:
            continue

        # 从路径提取年份作为日期估算
        year_match = re.match(r"(\d{4})/", href)
        date = year_match.group(1) if year_match else ""

        articles.append({
            "url": url,
            "title": title,
            "date": date,
            "source": "transformer_circuits"
        })

    print(f"[transformer] 发现 {len(articles)} 篇文章")
    return articles


def fetch_article_content(url: str) -> Optional[str]:
    """抓取 transformer-circuits 文章正文（纯静态 HTML）"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[transformer] 抓取文章失败 {url}: {e}")
        return None

    soup = BeautifulSoup(resp.content, "lxml")

    # transformer-circuits 论文通常有 <article> 或 <d-article>（Distill 格式）
    for selector in ["d-article", "article", "main", ".l-body"]:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 200:
                return text[:8000]  # 论文较长，截取前 8000 字符

    body = soup.find("body")
    return body.get_text(separator="\n", strip=True)[:8000] if body else None
