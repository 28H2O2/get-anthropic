# 功能：抓取 anthropic.com/engineering（Anthropic 工程博客）的文章列表和内容
# 输入：https://www.anthropic.com/engineering（公开 HTML）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "YYYY-MM-DD", "source": "engineering"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4
# 项目作用：Anthropic 工程技术文章（实战经验、工具评测等）的发现层
# 最后修改：2026-04-13

import re
import requests
from bs4 import BeautifulSoup
from typing import Optional

INDEX_URL = "https://www.anthropic.com/engineering"
BASE_URL = "https://www.anthropic.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}

_MONTH_MAP = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}
_DATE_RE = re.compile(
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\.?\s+(\d{1,2}),?\s*(20\d{2})",
    re.IGNORECASE,
)
_ARTICLE_PATH_RE = re.compile(r"^/engineering/[^/]+$")


def _parse_text_date(text: str) -> str:
    """'Mar 25, 2026' → '2026-03-25'，失败返回空字符串"""
    m = _DATE_RE.search(text)
    if not m:
        return ""
    month = _MONTH_MAP.get(m.group(1).lower()[:3], "")
    day = m.group(2).zfill(2)
    year = m.group(3)
    return f"{year}-{month}-{day}" if month else ""


def fetch_article_list() -> list[dict]:
    """从 anthropic.com/engineering 列表页解析所有工程文章"""
    try:
        resp = requests.get(INDEX_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[engineering] 获取列表页失败: {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml")
    articles = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if not _ARTICLE_PATH_RE.match(href):
            continue
        url = BASE_URL + href
        if url in seen:
            continue
        seen.add(url)

        # 链接文字包含标题+日期拼接，如 "Claude Code auto mode: a safer wayMar 25, 2026"
        full_text = a.get_text(separator=" ", strip=True)
        # 从末尾提取日期，剩余部分为标题
        date = _parse_text_date(full_text)
        if date:
            # 去掉日期部分，还原标题
            title = _DATE_RE.sub("", full_text).strip().rstrip(" ,")
        else:
            title = full_text

        if not title:
            title = href.split("/")[-1].replace("-", " ").title()

        articles.append({
            "url": url,
            "title": title,
            "date": date,
            "source": "engineering",
        })

    print(f"[engineering] 发现 {len(articles)} 篇文章")
    return articles


def fetch_article_content(url: str) -> tuple[Optional[str], str, str]:
    """抓取工程文章正文、标题和发布日期。返回 (content, title, pub_date)"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[engineering] 抓取文章失败 {url}: {e}")
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

    # 发布日期：从 Next.js payload 中提取 publishedOn 字段（YYYY-MM-DD）
    # payload 里双引号被转义为 \\"，故匹配两种格式
    pub_date = ""
    m = re.search(r'(?:\\"|")publishedOn(?:\\"|")\s*:\s*(?:\\"|")(20\d{2}-\d{2}-\d{2})(?:\\"|")', resp.text)
    if m:
        pub_date = m.group(1)

    # 兜底：搜索 "Published" 文字后紧跟日期
    if not pub_date:
        for el in soup.find_all(string=re.compile(r"Published\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)", re.I)):
            pub_date = _parse_text_date(el)
            if pub_date:
                break

    # 正文
    content = None
    for selector in ["article", "main", '[class*="Engineering"]', '[class*="content"]']:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 200:
                content = text[:6000]
                break
    if not content:
        body = soup.find("body")
        content = body.get_text(separator="\n", strip=True)[:6000] if body else None

    return content, title, pub_date
