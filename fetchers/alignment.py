"""Compatibility entry points for the shared, current source adapters."""
from .common import discover, fetch_article


def fetch_article_list():
    return discover("alignment")


def fetch_article_content(url):
    article = fetch_article(url)
    return article["content"], article["title"], article["date"]
