"""A simple Python module that wraps the meduza.io API."""

import json as _json
import gzip as _gzip
from datetime import date as _date
from datetime import datetime as _datetime
from urllib.parse import urljoin as _urljoin
from urllib.parse import urlencode as _urlencode
from urllib.request import urlopen as _urlopen
from itertools import islice as _islice


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
    "iter_reactions_for",
    "latest_push",
    "is_today",
]


LANGUAGES = [
    "ru", 
    "en",
]

EN_SECTIONS = [
    "news",
]

RU_SECTIONS = [
    "news", 
    "articles", 
    "shapito", 
    "razbor", 
    "games", 
    "podcasts",
]

EN_TAGS = [
    "news", 
    "like it or not", 
    "games",
]

RU_TAGS = [
    "новости",
    "истории",
    "разбор",
    "шапито",
    "игры",
    "подкасты",
    "партнерский материал",
]



_BASEURL = "https://meduza.io"
_API_SUFFIX = "api/v3"
_SEARCH_API = f"{_BASEURL}/{_API_SUFFIX}/search?"
_SOCIAL_API = f"{_BASEURL}/{_API_SUFFIX}/social?"
_STOCK_API = f"{_BASEURL}/{_API_SUFFIX}/stock/all"
_LATEST_PUSH = f"{_BASEURL}/{_API_SUFFIX}/push/chrome/latest"


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
_eng_section_from = {
    "news": "news",
    "games": "news",
    "like it or not": "news",
}


# open URL and return JSON response (as dict)
def _urlopenjson(url):
    # open url
    response = _urlopen(url)
    headers = dict(response.headers)
    data = response.read()
    # if the data is compressed using gzip, then decompress this.
    # (u is a gzip file if the first two bytes are '0x1f' and '0x8b')
    if headers.get("Content-Encoding") == "gzip":
        data = _gzip.decompress(data)
    # remove all non-breaking spaces
    data = data.decode("utf-8").replace("\xa0", " ")
    return _json.loads(data)


def stocks(key=None) -> dict:
    """Returns stocks."""
    response = _urlopenjson(_STOCK_API)
    if key is None:
        return response
    else:
        return response[key]


def get(url: str, as_dict=False) -> dict:
    """Gets the article for the url.

    `url` - the url of a page."""
    if not url.startswith(_BASEURL):
        url = _urljoin(_BASEURL, url)
    if _API_SUFFIX not in url:
        url = url.replace(_BASEURL, f"{_BASEURL}/{_API_SUFFIX}")
    json_as_dict = _urlopenjson(url)["root"]
    return json_as_dict if as_dict else Article(json_as_dict)


def section(section: str, results=24, language="ru", as_dict=False):
    """Gets articles from the `section`.

    `section` - Section name (see `meduza.EN_SECTIONS` and q
    `meduza.RU_SECTIONS` constants);
    `results` - How many articles to return;
    `language` - Russian or English version of meduza.io (see 
    `meduza.LANGUAGES`)."""
    page = 0
    while results and page <= 10:  # (more pages are not available)
        payload = {
            "chrono": section,
            "locale": language,
            "page": page,
            "per_page": "24",
        }
        url = _SEARCH_API + _urlencode(payload)
        for full_dict_url in _urlopenjson(url)["documents"].keys():
            if results:
                yield get(full_dict_url, as_dict=as_dict)
                results -= 1
            else:
                break
        page += 1


def tag(tag, results=24, language="ru", as_dict=False):
    """Gets articles with the `tag`.

    `tag` - An article tag. Same as in `article['tag']['name']` (see
    `meduza.EN_TAG`S and `meduza.RU_TAGS` constants);
    `results`  -- How many articles to return;
    `language` -- Russian or English version of meduza.io (see 
    `meduza.LANGUAGES`)."""
    # choose a section
    if language == "ru":
        section_ = _rus_section_from[tag]
    else:
        section_ = _eng_section_from[tag]
    # key function
    valid_tag = lambda a: a["tag"]["name"] == tag
    # generator of the current section `section_`
    # `results=24*10` because probably this is the maximum value
    section_generator = section(section_, 24 * 10, language, as_dict=as_dict)
    # a slice of filtered by tag articles
    yield from _islice(filter(valid_tag, section_generator), results)


def reactions_for(article: dict) -> dict:
    """Gets number of reactions in social networks (and number of 
    comments on meduza.io) for the `article`."""
    return next(iter_reactions_for(article))


def iter_reactions_for(*articles):
    """Gets number of reactions in social networks (and number of 
    comments on meduza.io) for all articles."""
    urls = (a["url"] for a in articles)
    url = _SOCIAL_API + _urlencode({"links": _json.dumps([*urls])})
    dirty_dict = _urlopenjson(url)
    result = (dirty_dict[url]["stats"] for url in dirty_dict)
    return result


def latest_push() -> dict:
    """Gets the latest push."""
    push = _urlopenjson(_LATEST_PUSH)["notification"]
    return {"title": push["title"], "body": push["body"], "url": push["url"]}


def is_today(article: dict) -> bool:
    """Defines whether the `article` is published today.

    `article` - an article dict."""
    return _date.today() == _date.fromtimestamp(article["published_at"])


class Article:  # BETA
    def __init__(self, info: dict):
        self._info = info
        self.url = _BASEURL + info["url"]
        self.title = info["title"]
        self.second_title = info.get("second_title")
        self.description = info["description"]
        self.source = info["source"]
        self.reactions = reactions_for(info)
        self.tag = info["tag"]["name"]
        self.type = info["document_type"]
        self.footer = info["footer"]
        self.is_blocks = "blocks" in info["content"] or "slides" in info["content"]
        self.is_html = "body" in info["content"]
        self.image = self._get_image(info)
        self.blocks = self._get_blocks_or_none(info)
        self.html = self._get_html_or_none(info)
        self.datetime = {
            "modification": _datetime.fromtimestamp(info["modified_at"]),
            "publication": _datetime.fromtimestamp(info["published_at"]),
        }

    def _get_image(self, info):
        if info.get("image"):
            return {
                "url": _BASEURL + info["image"].get("large_url")
                or info["image"].get("small_url"),
                "caption": info["image"]["caption"],
                "credit": info["image"]["credit"],
            }
        else:
            return None

    def _get_blocks_or_none(self, info):
        if self.is_blocks:
            return info["content"].get("blocks") or info["content"].get("slides")
        else:
            return None

    def _get_html_or_none(self, info):
        if self.is_html:
            return info["content"]["body"]
        else:
            return None

    def __repr__(self):
        return f"<{self.tag.title()}: '{self.title}'>"

    def __iter__(self):
        iters = dict((x, y) for x, y in self.__dict__.items() if not x.startswith("_"))
        for x, y in iters.items():
            yield x, y

    def as_dict(self):
        return self._info
