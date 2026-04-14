# 功能：抓取 Claude Cookbook 页面的最新 recipe 列表，并从详情页提取发布日期
# 输入：https://platform.claude.com/cookbook（公开静态 HTML）
# 输出：文章列表 [{"url": "...", "title": "...", "date": "...", "source": "cookbook"}]
# 运行方式：被 main.py 调用，不单独运行
# 依赖：requests, beautifulsoup4
# 项目作用：Cookbook 新教程的发现层
# 最后修改：2026-04-14

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional

COOKBOOK_URL = "https://platform.claude.com/cookbook"
BASE_URL = "https://platform.claude.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def fetch_article_list() -> list[dict]:
    """从 Cookbook 列表页获取所有 recipe 链接（卡片式布局）"""
    try:
        resp = requests.get(COOKBOOK_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[cookbook] 获取列表页失败: {e}")
        return []

    soup = BeautifulSoup(resp.content, "lxml")
    articles = []
    seen = set()

    # 页面结构：每篇 recipe 是一个 <a href="/cookbook/xxx"> 卡片
    # 卡片内依次是：图标 SVG、标题文字、描述文字
    for a in soup.find_all("a", href=True):
        href = a["href"]
        # 跳过根路径和非文章链接
        if not href.startswith("/cookbook/") or href.rstrip("/") == "/cookbook":
            continue

        url = BASE_URL + href
        if url in seen:
            continue
        seen.add(url)

        texts = [t.strip() for t in a.stripped_strings]
        title = texts[0] if texts else href.split("/")[-1]
        description = texts[1] if len(texts) > 1 else ""

        articles.append({
            "url": url,
            "title": title,
            "description": description,
            "date": "",  # 页面卡片不显示日期，以 URL 状态变化检测新增
            "source": "cookbook"
        })

    print(f"[cookbook] 发现 {len(articles)} 个 recipe")
    return articles


def _parse_pub_date(soup: BeautifulSoup) -> str:
    """从详情页提取发布日期，返回 YYYY-MM-DD 或空字符串。
    页面文本格式：'Published on April 10, 2026'
    """
    text = soup.get_text(" ", strip=True)
    m = re.search(r"Published on ([A-Za-z]+ \d{1,2},?\s*\d{4})", text)
    if m:
        try:
            return datetime.strptime(m.group(1).replace(",", "").strip(), "%B %d %Y").strftime("%Y-%m-%d")
        except ValueError:
            pass
    # 兜底：查找 <time datetime="...">
    time_el = soup.find("time", attrs={"datetime": True})
    if time_el:
        raw = time_el["datetime"][:10]
        if re.match(r"\d{4}-\d{2}-\d{2}", raw):
            return raw
    return ""


def fetch_article_content(url: str) -> tuple[Optional[str], str, str]:
    """抓取单个 recipe 的正文，返回 (content, title, pub_date)。"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[cookbook] 抓取 recipe 失败 {url}: {e}")
        return None, "", ""

    soup = BeautifulSoup(resp.content, "lxml")

    # 提取标题
    title = ""
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    elif soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)

    # 提取发布日期
    pub_date = _parse_pub_date(soup)

    # 提取正文
    content = None
    for selector in ["article", "main", ".notebook-content", '[class*="content"]']:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 100:
                content = text
                break
    if not content:
        body = soup.find("body")
        content = body.get_text(separator="\n", strip=True) if body else None

    return content, title, pub_date
