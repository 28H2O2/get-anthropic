# 功能：抓取 transformer-circuits.pub 的最新可解释性研究文章
# 输入：https://transformer-circuits.pub/（公开静态 HTML）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "...", "source": "transformer_circuits"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4
# 项目作用：Anthropic 可解释性研究（Circuits 团队）的发现层
# 最后修改：2026-04-14

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional

_MONTH_MAP = {
    "january":"01","february":"02","march":"03","april":"04",
    "may":"05","june":"06","july":"07","august":"08",
    "september":"09","october":"10","november":"11","december":"12",
}
_DATE_RE = re.compile(
    r"(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2}),?\s+(20\d{2})",
    re.IGNORECASE,
)

def _parse_pub_date(html_text: str) -> str:
    """从页面原始 HTML 中提取 'Month DD, YYYY' 格式日期，返回 YYYY-MM-DD 或空字符串"""
    m = _DATE_RE.search(html_text)
    if not m:
        return ""
    month = _MONTH_MAP.get(m.group(1).lower(), "")
    day   = m.group(2).zfill(2)
    year  = m.group(3)
    return f"{year}-{month}-{day}" if month else ""

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


def fetch_article_content(url: str) -> tuple[Optional[str], str, str]:
    """抓取 transformer-circuits 文章正文，返回 (content, title, pub_date)"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[transformer] 抓取文章失败 {url}: {e}")
        return None, "", ""

    soup = BeautifulSoup(resp.content, "lxml")

    # 从原始 HTML 中提取精确日期（页面文本含 "Published March 27, 2025"）
    pub_date = _parse_pub_date(resp.text)

    # 标题
    title = ""
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        title = og["content"].strip()
    elif soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)

    # 正文
    content = None
    for selector in ["d-article", "article", "main", ".l-body"]:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 200:
                content = text[:8000]
                break

    if not content:
        body = soup.find("body")
        content = body.get_text(separator="\n", strip=True)[:8000] if body else None

    return content, title, pub_date
