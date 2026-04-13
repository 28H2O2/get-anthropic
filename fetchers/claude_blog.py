# 功能：抓取 claude.com/blog 的最新博客文章列表和内容
# 输入：https://claude.com/blog（公开 HTML，Webflow 渲染）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "YYYY-MM-DD", "source": "claude_blog"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4
# 项目作用：Claude 官方博客内容（面向用户和企业）的发现层
# 最后修改：2026-04-13

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

INDEX_URL = "https://claude.com/blog"
BASE_URL = "https://claude.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

_MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}
_DATE_RE = re.compile(
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{1,2}),\s+(20\d{2})",
    re.IGNORECASE,
)


def _parse_text_date(text: str) -> str:
    """'April 10, 2026' → '2026-04-10'，失败返回空字符串"""
    m = _DATE_RE.search(text)
    if not m:
        return ""
    month = _MONTH_MAP.get(m.group(1).lower()[:3], "")
    day = m.group(2).zfill(2)
    year = m.group(3)
    return f"{year}-{month}-{day}" if month else ""


def fetch_article_list() -> list[dict]:
    """从 claude.com/blog 列表页解析所有文章卡片（含标题和日期）"""
    try:
        resp = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[claude_blog] 获取列表页失败: {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml")
    articles = []
    seen = set()

    def _add(href, title, date_text):
        if not href.startswith("/blog/") or "category" in href:
            return
        url = BASE_URL + href
        if url in seen:
            return
        seen.add(url)
        articles.append({
            "url": url,
            "title": title or href.split("/")[-1],
            "date": _parse_text_date(date_text),
            "source": "claude_blog",
        })

    # 旧卡片格式：div.marquee_cms_blog_list_item
    for card in soup.find_all("div", class_=lambda c: c and "marquee_cms_blog_list_item" in c and "content" not in c):
        link_el = card.find("a", href=True)
        if not link_el:
            continue
        title_el = card.find(["h1", "h2", "h3", "h4"])
        date_el = card.find("div", class_=lambda c: c and "u-text-style-caption" in c)
        _add(link_el["href"],
             title_el.get_text(strip=True) if title_el else "",
             date_el.get_text(strip=True) if date_el else "")

    # 新卡片格式：div.card_blog_wrap（含大图封面卡片）
    for card in soup.find_all("div", class_=lambda c: c and "card_blog_wrap" in c):
        link_el = card.find("a", href=True)
        if not link_el:
            continue
        title_el = card.find(class_=lambda c: c and "card_blog_title" in c)
        date_el = card.find("div", class_=lambda c: c and "u-text-style-caption" in c)
        _add(link_el["href"],
             title_el.get_text(strip=True) if title_el else "",
             date_el.get_text(strip=True) if date_el else "")

    # 新列表格式：article.card_blog_list_wrap（博客列表条目）
    for card in soup.find_all("article", class_=lambda c: c and "card_blog_list_wrap" in c):
        link_el = card.find("a", href=True)
        if not link_el:
            # 列表条目的链接可能在外层 div 上
            parent = card.parent
            link_el = parent.find("a", href=True) if parent else None
        if not link_el:
            continue
        title_el = card.find(class_=lambda c: c and "card_blog_list_title" in c)
        # 列表条目的日期在 card_blog_list_meta 里
        date_el = card.find(class_=lambda c: c and "u-text-style-caption" in c)
        _add(link_el["href"],
             title_el.get_text(strip=True) if title_el else "",
             date_el.get_text(strip=True) if date_el else "")

    print(f"[claude_blog] 发现 {len(articles)} 篇文章")
    return articles


def fetch_article_content(url: str) -> tuple[Optional[str], str, str]:
    """抓取单篇博客文章的正文、标题和发布日期。返回 (content, title, pub_date)"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[claude_blog] 抓取文章失败 {url}: {e}")
        return None, "", ""

    soup = BeautifulSoup(resp.content, "lxml")

    # 标题
    title = ""
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)
    if not title:
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            title = og["content"].strip()

    # 发布日期（页面正文区同样有 u-text-style-caption 日期）
    pub_date = ""
    date_el = soup.find("div", class_=lambda c: c and "u-text-style-caption" in c)
    if date_el:
        pub_date = _parse_text_date(date_el.get_text(strip=True))

    # 正文
    content = None
    for selector in ["article", "main", '[class*="rich-text"]', '[class*="blog"]']:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 200:
                content = text[:5000]
                break

    if not content:
        body = soup.find("body")
        content = body.get_text(separator="\n", strip=True)[:5000] if body else None

    return content, title, pub_date
