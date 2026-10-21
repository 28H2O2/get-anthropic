"""HTTP, article metadata and content extraction shared by the eight sources."""
import calendar
import json
import re
import time
from datetime import date
from urllib.parse import urljoin, urlsplit, urlunsplit

import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AnthropicDigest/2.0)"}
SOURCE_URLS = {
    "anthropic_news": "https://www.anthropic.com/sitemap.xml",
    "anthropic_research": "https://www.anthropic.com/sitemap.xml",
    "cookbook": "https://platform.claude.com/cookbook",
    "transformer_circuits": "https://transformer-circuits.pub/",
    "red_team": "https://www.anthropic.com/research/team/frontier-red-team",
    "claude_blog": "https://claude.com/resources/articles",
    "alignment": "https://alignment.anthropic.com/",
    "engineering": "https://www.anthropic.com/engineering",
}
CATEGORIES = {"announcements", "features", "models", "partnerships", "policy", "product", "safeguards", "security", "societal-impacts"}


def normalize_url(url):
    p = urlsplit(url)
    return urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip("/") or "/", "", ""))


def get(url):
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def parse_date(text):
    """Return a date at its actual precision; never invent month/day values."""
    text = str(text or "").strip()
    m = re.match(r"^(20\d{2}-\d{2}-\d{2})(?:T|$)", text)
    if m:
        try:
            return date.fromisoformat(m[1]).isoformat()
        except ValueError:
            return ""
    months = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}
    months.update({name.lower(): i for i, name in enumerate(calendar.month_abbr) if name})
    m = re.search(r"\b([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(20\d{2})\b", text)
    if m and m[1].lower() in months:
        try:
            return date(int(m[3]), months[m[1].lower()], int(m[2])).isoformat()
        except ValueError:
            return ""
    m = re.fullmatch(r"([A-Za-z]+)\s+(20\d{2})", text)
    if m and m[1].lower() in months:
        return f"{m[2]}-{months[m[1].lower()]:02}"
    if re.fullmatch(r"20\d{2}(?:-(?:0[1-9]|1[0-2]))?", text):
        return text
    return ""


def is_article(url, source):
    p = urlsplit(url)
    path = p.path.rstrip("/")
    if source in {"anthropic_news", "anthropic_research", "engineering", "red_team"}:
        if p.netloc == "red.anthropic.com" and source == "red_team":
            return bool(re.fullmatch(r"/20\d{2}/[^/]+(?:/index.html)?", path))
        if p.netloc != "www.anthropic.com":
            return False
        prefix = {"anthropic_news": "news", "anthropic_research": "research"}.get(source)
        pattern = rf"/{prefix}/[^/]+" if prefix else r"/(research|engineering)/[^/]+"
        return bool(re.fullmatch(pattern, path)) and path.split("/")[-1] not in CATEGORIES
    if source == "claude_blog":
        return (p.netloc == "claude.com" and bool(re.fullmatch(r"/(?:resources/articles|blog)/[^/]+", path)) and "/category/" not in path) or (p.netloc == "claude.dev" and bool(re.fullmatch(r"/blog/[^/]+", path)))
    if source == "cookbook":
        return p.netloc == "platform.claude.com" and bool(re.fullmatch(r"/cookbook/[^/]+", path))
    if source == "alignment":
        return p.netloc == "alignment.anthropic.com" and bool(re.fullmatch(r"/20\d{2}/[^/]+", path))
    return p.netloc == "transformer-circuits.pub" and bool(re.fullmatch(r"/20\d{2}/[^/]+/[\w-]+\.html", path))


def sitemap_entries(url, visited=None):
    visited = set() if visited is None else visited
    if url in visited:
        return []
    visited.add(url)
    soup = BeautifulSoup(get(url).content, "xml")
    entries = []
    for item in soup.find_all("sitemap"):
        loc = item.find("loc")
        if loc and urlsplit(loc.text).netloc == urlsplit(url).netloc:
            entries.extend(sitemap_entries(loc.text.strip(), visited))
    for item in soup.find_all("url"):
        loc, mod = item.find("loc"), item.find("lastmod")
        if loc:
            entries.append((loc.text.strip(), mod.text.strip()[:10] if mod else ""))
    return entries


def discover(source):
    start = SOURCE_URLS[source]
    found = {}
    if source in {"anthropic_news", "anthropic_research"}:
        for url, lastmod in sitemap_entries(start):
            if is_article(url, source):
                found[normalize_url(url)] = {"url": normalize_url(url), "title": "", "date": "", "sitemap_lastmod": lastmod, "source": source}
        return list(found.values())
    # Follow actual pagination links, including Webflow query-string pagination.
    queue, visited = [start], set()
    while queue:
        page = queue.pop(0)
        if page in visited:
            continue
        visited.add(page)
        r = get(page)
        soup = BeautifulSoup(r.content, "lxml")
        for a in soup.find_all("a", href=True):
            url = urljoin(r.url, a["href"])
            if is_article(url, source):
                key = normalize_url(url)
                title = a.find(["h1", "h2", "h3", "h4"])
                title = title.get_text(" ", strip=True) if title else a.get_text(" ", strip=True)
                time_el = a.find("time")
                hint = parse_date(time_el.get("datetime") or time_el.get_text(" ", strip=True)) if time_el else ""
                old = found.get(key, {})
                found[key] = {"url": key, "source": source, "title": old.get("title") or title, "date": old.get("date") or hint}
            elif urlsplit(url).netloc == urlsplit(r.url).netloc and urlsplit(url).path == urlsplit(r.url).path and (a.get("rel") == ["next"] or re.search(r"(?:[?&](?:\w*_)?page=|/page/)", url)):
                if url not in visited and url not in queue:
                    queue.append(url)
    # The migrated Claude listing is client-paginated; its sitemap exposes the full archive.
    if source == "claude_blog":
        for url, mod in sitemap_entries("https://claude.com/sitemap.xml"):
            if is_article(url, source):
                key = normalize_url(url)
                found.setdefault(key, {"url": key, "source": source, "title": "", "date": "", "sitemap_lastmod": mod})
    return list(found.values())


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def extract_article(html, url):
    soup = BeautifulSoup(html, "lxml")
    canonical = soup.select_one('link[rel="canonical"]')
    canonical_url = urljoin(url, canonical.get("href", "")) if canonical else url
    # Only accept a canonical on the response host (redirects already resolved by requests).
    if urlsplit(canonical_url).netloc != urlsplit(url).netloc:
        canonical_url = url
    title_el = soup.select_one('meta[property="og:title"]')
    heading = soup.find("h1")
    title = (title_el.get("content", "") if title_el else "") or (heading.get_text(" ", strip=True) if heading else "")
    published, description = "", ""
    for script in soup.select('script[type="application/ld+json"],d-front-matter script'):
        try:
            data = json.loads(script.get_text())
        except (ValueError, TypeError):
            continue
        for obj in walk_json(data):
            if obj.get("datePublished") or obj.get("published"):
                published = published or parse_date(obj.get("datePublished") or obj.get("published"))
                description = description or obj.get("description", "")
    for selector, attr in [('meta[property="article:published_time"]', "content"), ('meta[name="citation_publication_date"]', "content"), ('time[datetime]', "datetime")]:
        el = soup.select_one(selector)
        if el:
            published = published or parse_date(el.get(attr))
    # Distill front matter uses YAML-like date fields inside a script.
    if not published:
        m = re.search(r'(?:published|datePublished)\s*[":]+\s*["\s]*(20\d{2}-\d{2}-\d{2})', html)
        published = parse_date(m[1]) if m else ""
    if not published:
        text = soup.get_text(" ", strip=True)
        m = re.search(r"Published(?:\s+on)?\s+([A-Za-z]+\s+\d{1,2},?\s+20\d{2})", text, re.I)
        if m:
            published = parse_date(m[1])
    if not published:
        # Short, standalone date labels; never search arbitrary body citations.
        for node in soup.select("d-byline, time, .agate, [class*='date'], [class*='Date'], #mDate, div[style*='float'], d-title > div"):
            text = node.get_text(" ", strip=True)
            if len(text) < 45:
                published = parse_date(text)
                if published:
                    break
    if not description:
        el = soup.select_one('meta[name="description"],meta[property="og:description"]')
        description = el.get("content", "") if el else ""
    # Prefer actual rich text over the outer main/article containing team/navigation panels.
    body = None
    for selector in ["d-article", ".prose", "[class*='PortableText']", "[class*='portableText']", "[class*='rich-text']", "[class*='RichText']", ".notebook-content", "article", "main"]:
        candidate = soup.select_one(selector)
        if candidate and len(candidate.get_text(" ", strip=True)) > 100 and any(len(p.get_text(" ", strip=True)) >= 65 for p in candidate.find_all("p")):
            body = candidate
            break
    paragraphs = []
    if body:
        for junk in body.select("nav,header,footer,aside,script,style,[class*='related'],[class*='Related'],[class*='share'],[class*='Share'],[class*='byline']"):
            junk.decompose()
        for p in body.find_all("p"):
            text = re.sub(r"\s+", " ", p.get_text(" ", strip=True))
            classes = " ".join(p.get("class", []))
            if len(text) >= 65 and not re.search("caption|author|finePrint", classes, re.I) and not re.search(r"subscribe|unsubscribe|privacy policy|cookie policy", text, re.I):
                paragraphs.append(text)
    content = "\n\n".join(paragraphs)
    if not content:
        raise ValueError("article body not found")
    # Original site descriptions are useful abstracts, but not generic site marketing copy.
    if isinstance(description, str) and len(description) >= 80 and description.strip() not in content[:1000] and not re.search(r"learn more about Claude|meet Claude|AI assistant from Anthropic", description, re.I):
        content = description.strip() + "\n\n" + content
    return {"url": normalize_url(canonical_url), "title": title.strip(), "date": published, "date_precision": {10: "day", 7: "month", 4: "year"}.get(len(published), "unknown"), "content": content}


def fetch_article(url):
    r = get(url)
    return extract_article(r.text, r.url)
