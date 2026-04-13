# 功能：抓取 Anthropic 官网的最新博客（/news）和研究文章（/research）
# 输入：anthropic.com/sitemap.xml（公开 XML，无需认证）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "YYYY-MM-DD", "source": "anthropic_news/research"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4, lxml
# 项目作用：Anthropic 官网内容的发现层，通过 sitemap 检测新文章
# 最后修改：2026-04-13

import requests
from bs4 import BeautifulSoup
from typing import Optional

SITEMAP_URL = "https://www.anthropic.com/sitemap.xml"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def fetch_article_list() -> list[dict]:
    """从 sitemap.xml 获取所有 /news 和 /research 文章 URL"""
    try:
        resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[anthropic_blog] 获取 sitemap 失败: {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml-xml")
    articles = []

    for url_tag in soup.find_all("url"):
        loc = url_tag.find("loc")
        if not loc:
            continue
        url = loc.text.strip()

        if "/news/" in url:
            source = "anthropic_news"
        elif "/research/" in url:
            source = "anthropic_research"
        else:
            continue

        # 排除列表页本身
        if url.rstrip("/") in ("https://www.anthropic.com/news", "https://www.anthropic.com/research"):
            continue

        # 从 lastmod 提取日期（格式：2026-04-09T...）
        lastmod_tag = url_tag.find("lastmod")
        date = lastmod_tag.text.strip()[:10] if lastmod_tag else ""

        articles.append({"url": url, "title": "", "date": date, "source": source})

    print(f"[anthropic_blog] 从 sitemap 发现 {len(articles)} 篇文章")
    return articles


def fetch_article_content(url: str) -> tuple[Optional[str], str, str]:
    """抓取单篇文章的正文文本、标题和真实发布日期。返回 (content, title, pub_date)

    pub_date 优先从 article:published_time meta 标签提取，
    其次尝试 <time datetime> 元素，最后返回空字符串。
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[anthropic_blog] 抓取文章失败 {url}: {e}")
        return None, "", ""

    soup = BeautifulSoup(resp.content, "lxml")

    # 提取标题
    title = ""
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        title = og["content"].strip()
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)

    # 提取真实发布日期（而非 sitemap 的 lastmod，后者是修改日期会误判为新文章）
    pub_date = ""
    pub_time_tag = soup.find("meta", property="article:published_time")
    if pub_time_tag and pub_time_tag.get("content"):
        pub_date = pub_time_tag["content"][:10]
    if not pub_date:
        time_el = soup.find("time", attrs={"datetime": True})
        if time_el:
            raw = time_el["datetime"]
            if len(raw) >= 10:
                pub_date = raw[:10]

    # 提取正文
    content = None
    for selector in ["article", "main", '[class*="post-content"]', '[class*="article"]']:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 200:
                content = text
                break

    if not content:
        body = soup.find("body")
        content = body.get_text(separator="\n", strip=True) if body else None

    return content, title, pub_date
