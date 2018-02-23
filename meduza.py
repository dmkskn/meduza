"""
A simple Python module that wraps the meduza.io API.

"""

import json as _json
import gzip as _gzip
from time import localtime as _localtime
from datetime import date as _date
from urllib.parse import urljoin as _urljoin
from urllib.parse import urlencode as _urlencode
from urllib.request import urlopen as _urlopen
from itertools import islice as _islice



__all__ = ['LANGUAGES', 'EN_SECTIONS', 'RU_SECTIONS', 'EN_TAGS', 'RU_TAGS',
           'stocks', 'get', 'section', 'tag', 'reactions_for',
           'iter_reactions_for', 'latest_push', 'is_today']


# Constants 
LANGUAGES = ("ru", "en")

EN_SECTIONS = ("news")

RU_SECTIONS = ("news", "articles", "shapito", "razbor", "games", "podcasts")

EN_TAGS = ("news", "like it or not", "games")

RU_TAGS = ("новости", "истории", "разбор", "шапито", "игры", "подкасты"
           "партнерский материал")


_BASEURL = 'https://meduza.io'
_API_SUFFIX = 'api/v3'
_SEARCH_API = f'{_BASEURL}/{_API_SUFFIX}/search?'
_SOCIAL_API = f'{_BASEURL}/{_API_SUFFIX}/social?'
_STOCK_API = f'{_BASEURL}/{_API_SUFFIX}/stock/all'
_LATEST_PUSH = f'{_BASEURL}/{_API_SUFFIX}/push/chrome/latest'


# maps tags to sections (russian)
_rus_section_from = {
    'новости': 'news',
    'истории': 'articles',
    'шапито': 'shapito',
    'разбор': 'razbor',
    'игры': 'games',
    'подкасты': 'podcasts',
    'партнерский материал': 'news',
    }


# maps tags to sections (english)
_eng_section_from = {
    'news' : 'news',
    'games': 'news',
    'like it or not': 'news',
    }


# open URL and return JSON response (as dict)
def _urlopenjson(url):
    # open url
    data = _urlopen(url).read()
    # if the data is compressed using gzip, then decompress this.
    # (u is a gzip file if the first two bytes are '0x1f' and '0x8b')
    if data.startswith(b'\x1f\x8b'):
        data = _gzip.decompress(data)
    # remove all non-breaking spaces
    data = data.decode('utf-8').replace('\xa0', ' ')
    return _json.loads(data)


def stocks(key=None):
    """Get stocks

    Return a dict object."""
    response = _urlopenjson(_STOCK_API)
    if key is None:
        return response
    else:
        return response[key]


def get(url):
    """Get the article for a given page URL.

    url -- URL of a page.

    Return a dict object."""
    if not url.startswith(_BASEURL):
        url = _urljoin(_BASEURL, url)
    if _API_SUFFIX not in url:
        url = url.replace(_BASEURL, f'{_BASEURL}/{_API_SUFFIX}')
    return _urlopenjson(url)['root']


def section(section, results=24, language='ru'):
    """Get articles from a given section.

    section  -- Section name (see meduza.EN_SECTIONS and 
                meduza.RU_SECTIONS constants);
    results  -- How many articles to return;
    language -- Russian or English version of meduza.io (see 
                meduza.LANGUAGES).

    Return a generator object."""
    page = 0
    while results and page <= 10: # (more pages are not available)
        payload = {
            'chrono': section,
            'locale': language, 
            'page': page, 
            'per_page': '24'
            }
        url = _SEARCH_API + _urlencode(payload)
        for full_dict_url in _urlopenjson(url)['documents'].keys():
            if results:
                yield get(full_dict_url)
                results -= 1
            else:
                break
        page += 1


def tag(tag, results=24, language='ru'):
    """Get articles with a given tag.

    tag      -- Article tag. Same as in article['tag']['name'] (see
                meduza.EN_TAGS and meduza.RU_TAGS constants);
    results  -- How many articles to return;
    language -- Russian or English version of meduza.io (see 
                meduza.LANGUAGES).

    Return a generator object."""
    # choose a section 
    if language == 'ru':
        section_ = _rus_section_from[tag]
    else:
        section_ = _eng_section_from[tag]
    # key function 
    valid_tag = lambda a: a['tag']['name'] == tag
    # generator of the current section `section_`
    # `results=24*10` because probably this is the maximum value
    section_generator = section(section_, 24 * 10, language)
    # a slice of filtered by tag articles
    yield from _islice(filter(valid_tag, section_generator), results)


def reactions_for(article):
    """Get number of reactions in social networks (and number of 
    comments on meduza.io) for an article.

    Return a dict object like 
    {'vk': 0, 'fb': 0, 'ok': 0, 'reactions': 0}."""
    return list(iter_reactions_for(article))[0]


def iter_reactions_for(*articles):
    """Get number of reactions in social networks (and number of 
    comments on meduza.io) for all articles.

    Return a generator object."""
    urls = [a['url'] for a in articles]
    url = _SOCIAL_API + _urlencode({'links':_json.dumps([*urls])})
    dirty_dict = _urlopenjson(url)
    result = (dirty_dict[url]['stats'] for url in dirty_dict)
    return result


def latest_push():
    """Get the latest push.

    Return a dict object with three keys like 
    {'url': '...', 'title': '...', 'body': '...'}."""
    push = _urlopenjson(_LATEST_PUSH)['notification']
    return {'title': push['title'], 'body': push['body'], 'url': push['url']}


def is_today(article):
    """Defines whether the article is published today.

    article -- an article dict.

    Return True if the article was published today, otherwise 
    return False."""
    t = _localtime(article['published_at'])
    article_date = _date(t.tm_year, t.tm_mon, t.tm_mday)
    return article_date == _date.today()
