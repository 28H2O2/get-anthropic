# 功能：抓取 alignment.anthropic.com（Anthropic 对齐科学博客）的文章列表和内容
# 输入：https://alignment.anthropic.com/（公开静态 HTML，distill.pub 风格）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "YYYY-MM-DD", "source": "alignment"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4
# 项目作用：Anthropic 对齐研究专项博客的发现层（与 /research 内容不同）
# 最后修改：2026-04-13

import re
import json
import requests
from bs4 import BeautifulSoup
from typing import Optional

BASE_URL = "https://alignment.anthropic.com"
INDEX_URL = "https://alignment.anthropic.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

_MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}
# 匹配 "April 7, 2026" 或 "April 2026"（无日，day 默认 01）
_DATE_FULL_RE = re.compile(
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(\d{1,2}),\s*(20\d{2})",
    re.IGNORECASE,
)
_DATE_MONTH_RE = re.compile(
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+(20\d{2})",
    re.IGNORECASE,
)
# URL 路径中的年份
_YEAR_RE = re.compile(r"/(20\d{2})/")
# 文章 URL 路径模式
_ARTICLE_PATH_RE = re.compile(r"^(20\d{2})/[^/]+/?$")


def _parse_text_date(text: str) -> str:
    """解析文本日期，返回 YYYY-MM-DD；有日期用全格式，无则用月份首日"""
    m = _DATE_FULL_RE.search(text)
    if m:
        month = _MONTH_MAP.get(m.group(1).lower()[:3], "")
        day = m.group(2).zfill(2)
        year = m.group(3)
        return f"{year}-{month}-{day}" if month else ""
    m2 = _DATE_MONTH_RE.search(text)
    if m2:
        month = _MONTH_MAP.get(m2.group(1).lower()[:3], "")
        year = m2.group(2)
        return f"{year}-{month}-01" if month else ""
    return ""


def fetch_article_list() -> list[dict]:
    """从首页解析所有文章卡片（<a class='note'>），结构与 red.anthropic.com 相同"""
    try:
        resp = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[alignment] 获取首页失败: {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml")
    articles = []
    seen = set()

    for a in soup.find_all("a", class_="note", href=True):
        href = a["href"].strip().lstrip("/")
        if not _ARTICLE_PATH_RE.match(href):
            continue

        href = href.rstrip("/") + "/"
        url = f"{BASE_URL}/{href}"
        if url in seen:
            continue
        seen.add(url)

        title_el = a.find("h3")
        title = title_el.get_text(strip=True) if title_el else href.split("/")[-2]

        desc_el = a.find("div", class_="description")
        description = desc_el.get_text(strip=True) if desc_el else ""

        articles.append({
            "url": url,
            "title": title,
            "description": description,
            "date": "",  # 日期在文章页内提取
            "source": "alignment",
        })

    print(f"[alignment] 发现 {len(articles)} 篇文章")
    return articles


def fetch_article_content(url: str) -> tuple[Optional[str], str, str]:
    """抓取单篇文章正文、标题和发布日期。返回 (content, title, pub_date)"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[alignment] 抓取文章失败 {url}: {e}")
        return None, "", ""

    soup = BeautifulSoup(resp.content, "lxml")

    # 标题：d-title 元素或 h1
    title = ""
    title_el = soup.find("d-title") or soup.find("h1")
    if title_el:
        title = title_el.get_text(strip=True)
    if not title:
        # d-front-matter JSON
        fm = soup.find("d-front-matter")
        if fm:
            script = fm.find("script", type="text/json")
            if script and script.string:
                try:
                    data = json.loads(script.string)
                    title = data.get("title", "")
                except Exception:
                    pass
    if not title:
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            title = og["content"].strip()

    # 发布日期：页面里有 "Month Year" 或 "Month D, Year" 格式的短文本节点
    pub_date = ""
    for text_node in soup.find_all(string=True):
        text = text_node.strip()
        # 限制长度：避免命中文章正文里碰巧含年份的句子
        if 5 < len(text) < 30 and _DATE_MONTH_RE.match(text):
            d = _parse_text_date(text)
            if d:
                pub_date = d
                break

    # 兜底：从 URL 路径提取年份，默认月份 01 日 01
    if not pub_date:
        m = _YEAR_RE.search(url)
        if m:
            pub_date = f"{m.group(1)}-01-01"

    # 正文
    content = None
    article_el = soup.find("d-article") or soup.find("article") or soup.find("main")
    if article_el:
        text = article_el.get_text(separator="\n", strip=True)
        if len(text) > 200:
            content = text[:6000]
    if not content:
        body = soup.find("body")
        content = body.get_text(separator="\n", strip=True)[:6000] if body else None

    return content, title, pub_date
