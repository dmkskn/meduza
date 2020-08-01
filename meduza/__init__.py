"""A simple Python module that wraps the meduza.io API."""

import gzip
import json
from typing import Any, Iterator, Optional
from urllib.parse import urlencode, urljoin
from urllib.request import urlopen

__all__ = [
    "LANGUAGES",
    "EN_SECTIONS",
    "RU_SECTIONS",
    "EN_TAGS",
    "RU_TAGS",
    "stocks",
    "get",
    "section",
    "tag",
    "reactions_for",
    "latest_push",
]


LANGUAGES = ["ru", "en"]

EN_SECTIONS = ["news"]

RU_SECTIONS = ["news", "articles", "shapito", "razbor", "games", "podcasts"]

EN_TAGS = ["news", "like it or not", "games"]

RU_TAGS = [
    "новости",
    "истории",
    "разбор",
    "шапито",
    "игры",
    "подкасты",
    "партнерский материал",
]

REQUEST_TYPES = ["term", "chrono"]

_BASEURL = "https://meduza.io"
_V3 = "api/v3"
_W5 = "api/w5"
_MISC = "api/misc"
_SEARCH_API = f"{_BASEURL}/{_W5}/search?"
_SOCIAL_API = f"{_BASEURL}/{_MISC}/social?"
_STOCK_API = f"{_BASEURL}/{_MISC}/stock/all"
_LATEST_PUSH = f"{_BASEURL}/{_V3}/push/chrome/latest"


# maps tags to sections (russian)
_rus_section_from = {
    "новости": "news",
    "истории": "articles",
    "шапито": "shapito",
    "разбор": "razbor",
    "игры": "games",
    "подкасты": "podcasts",
    "партнерский материал": "news",
}

# maps tags to sections (english)
_eng_section_from = {"news": "news", "games": "news", "like it or not": "news"}


# open URL and return JSON response (as dict)
def _GET(url: str) -> Any:
    # open url
    response = urlopen(url)
    headers = dict(response.headers)
    data = response.read()
    # if the data is compressed using gzip, then decompress this.
    # (u is a gzip file if the first two bytes are '0x1f' and '0x8b')
    if headers.get("Content-Encoding") == "gzip":
        data = gzip.decompress(data)
    # remove all non-breaking spaces
    data = data.decode("utf-8").replace("\xa0", " ")
    return json.loads(data)


def stocks(key: Optional[str] = None) -> Any:
    """Returns stocks."""
    response = _GET(_STOCK_API)
    return response if key is None else response[key]


def get(url: str) -> Any:
    """Gets the article for the url.

    `url` - the url of a page."""
    if not url.startswith(_BASEURL):
        url = urljoin(_BASEURL, url)
    if _W5 not in url:
        url = url.replace(_BASEURL, f"{_BASEURL}/{_W5}")
    return _GET(url)["root"]


def api_request(request_type: str, request: str, *, n: int = 24, lang: str = "ru", page: int = 0) -> Iterator[Any]:
    """Gets articles from the `api_request`.

    `request_type` - Type of request (see
    `meduza.REQUEST_TYPES` constant);
    `n` - How many articles to return;
    `lang` - Russian or English version of meduza.io (see
    `meduza.LANGUAGES`).;
    `page` - Page number"""

    def _article_urls(url: str) -> Iterator[str]:
        documents = _GET(url)["documents"]
        for url in documents:
            if url == "nil":
                url = documents["nil"]["root"]["url"]
            yield url

    payload = {request_type: request, "locale": lang, "page": page, "per_page": n}
    for url in _article_urls(_SEARCH_API + urlencode(payload)):
        yield get(url)


def section(section: str, *, n: int = 24, lang: str = "ru", page: int = 0) -> Iterator[Any]:
    """Gets articles from the `section`.

    `section` - Section name (see `meduza.EN_SECTIONS` and
    `meduza.RU_SECTIONS` constants);
    `n` - How many articles to return;
    `lang` - Russian or English version of meduza.io (see
    `meduza.LANGUAGES`).;
    `page` - Page number"""

    return api_request("chrono", section, n=n, lang=lang, page=page)


def search(search_term: str, *, n: int = 24, lang: str = "ru", page: int = 0) -> Iterator[Any]:
    """Gets articles from the `search_term`.

    `search_term` - Term to be searched.
    Either in Cyrillic or English;
    `n` - How many articles to return;
    `lang` - Russian or English version of meduza.io (see
    `meduza.LANGUAGES`).;
    `page` - Page number"""

    return api_request("term", search_term, n=n, lang=lang, page=page)


def _choose_section_if_tag(tag: str, *, lang: str) -> str:
    return _rus_section_from[tag] if lang == "ru" else _eng_section_from[tag]


def tag(tag: str, *, n: int = 24, lang: str = "ru") -> Iterator[Any]:
    """Gets articles with the `tag`.

    `tag` - An article tag. Same as in `article['tag']['name']` (see
    `meduza.EN_TAG`S and `meduza.RU_TAGS` constants);
    `n`  -- How many articles to return;
    `lang` -- Russian or English version of meduza.io (see
    `meduza.LANGUAGES`)."""
    section_name = _choose_section_if_tag(tag, lang=lang)
    page = 0
    m = n
    while m > 0:
        for article in section(section_name, n=n, lang=lang, page=page):
            if m > 0 and article["tag"]["name"] == tag:
                yield article
                m -= 1
        page += 1


def reactions_for(*urls: str) -> Any:
    """Gets number of reactions in social networks (and number of
    comments on meduza.io) for urls."""
    url = _SOCIAL_API + urlencode({"links": json.dumps([*urls])})
    return _GET(url)


def latest_push() -> Any:
    """Gets the latest push."""
    return _GET(_LATEST_PUSH)["notification"]
