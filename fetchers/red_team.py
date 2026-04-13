# 功能：抓取 red.anthropic.com（Anthropic 红队/安全研究博客）的文章列表和内容
# 输入：https://red.anthropic.com/（公开静态 HTML）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "YYYY-MM-DD", "source": "red_team"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4
# 项目作用：Anthropic 安全研究内容的发现层
# 最后修改：2026-04-13

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

BASE_URL = "https://red.anthropic.com"
INDEX_URL = "https://red.anthropic.com/"
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
# 文章 URL 路径模式：YYYY/slug/ 或 YYYY/slug/index.html
_ARTICLE_PATH_RE = re.compile(r"^(20\d{2})/[^/]+/(?:index\.html)?$")


def _parse_text_date(text: str) -> str:
    """'April 7, 2026' → '2026-04-07'，失败返回空字符串"""
    m = _DATE_RE.search(text)
    if not m:
        return ""
    month = _MONTH_MAP.get(m.group(1).lower()[:3], "")
    day = m.group(2).zfill(2)
    year = m.group(3)
    return f"{year}-{month}-{day}" if month else ""


def fetch_article_list() -> list[dict]:
    """从首页解析所有文章卡片（<a class='note'>），无日期，日期在文章页内"""
    try:
        resp = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[red_team] 获取首页失败: {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml")
    articles = []
    seen = set()

    for a in soup.find_all("a", class_="note", href=True):
        href = a["href"].strip().lstrip("/")
        if not _ARTICLE_PATH_RE.match(href):
            continue

        # 统一去掉 index.html 后缀
        href = re.sub(r"index\.html$", "", href).rstrip("/") + "/"
        url = f"{BASE_URL}/{href}"
        if url in seen:
            continue
        seen.add(url)

        title = a.find("h3")
        title = title.get_text(strip=True) if title else href.split("/")[-2]

        desc_el = a.find("div", class_="description")
        description = desc_el.get_text(strip=True) if desc_el else ""

        articles.append({
            "url": url,
            "title": title,
            "description": description,
            "date": "",  # 日期只在文章页内，fetch_article_content 时提取
            "source": "red_team",
        })

    print(f"[red_team] 发现 {len(articles)} 篇文章")
    return articles


def fetch_article_content(url: str) -> tuple[Optional[str], str, str]:
    """抓取单篇文章正文、标题和发布日期。返回 (content, title, pub_date)"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[red_team] 抓取文章失败 {url}: {e}")
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

    # 发布日期：在 <d-article> 或 <article> 里的第一段文字，格式 "April 7, 2026"
    pub_date = ""
    article_el = soup.find("d-article") or soup.find("article") or soup.find("main")
    if article_el:
        for p in article_el.find_all("p", limit=5):
            text = p.get_text(strip=True)
            pub_date = _parse_text_date(text)
            if pub_date:
                break

    # 正文
    content = None
    if article_el:
        text = article_el.get_text(separator="\n", strip=True)
        if len(text) > 200:
            content = text[:6000]

    if not content:
        body = soup.find("body")
        content = body.get_text(separator="\n", strip=True)[:6000] if body else None

    return content, title, pub_date
