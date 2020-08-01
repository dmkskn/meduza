import pytest

import meduza


ARTICLE_RELATIVE_URL = "feature/2018/07/03/astronomam-udalos-zafiksirovat-rozhdenie-novoy-planety-temperatura-na-ney-okolo-tysyachi-gradusov-po-tselsiyu"


def test_all_stocks():
    stocks = meduza.stocks()
    assert "usd" in stocks


def test_stocks_by_key():
    usd = meduza.stocks("usd")
    assert "current" in usd


def test_get_from_full_url():
    url = f"{meduza._BASEURL}/{ARTICLE_RELATIVE_URL}"
    article = meduza.get(url)
    assert "title" in article
    assert url.endswith(article["url"])


def test_get_from_url_with_api_suffix():
    url = f"{meduza._BASEURL}/{meduza._W5}/{ARTICLE_RELATIVE_URL}"
    article = meduza.get(url)
    assert "title" in article
    assert url.endswith(article["url"])


def test_get_from_relative_url():
    article = meduza.get(ARTICLE_RELATIVE_URL)
    assert "title" in article
    assert ARTICLE_RELATIVE_URL.endswith(article["url"])


def test_section():
    shapito = meduza.section("shapito", n=24, lang="ru")
    shapito_list = list(shapito)
    assert len(shapito_list) == 24


def test_tag():
    shapito = meduza.tag("шапито", n=24, lang="ru")
    shapito_list = list(shapito)
    assert len(shapito_list) == 24
    for shapito_article in shapito_list:
        assert shapito_article["tag"]["name"] == "шапито"


def test_iter_reactions_for():
    articles = meduza.tag("шапито", n=3, lang="ru")
    urls = [a["url"] for a in articles]
    reactions = meduza.reactions_for(*urls)
    for url in urls:
        assert url in reactions


def test_getting_latest_push():
    latest_push = meduza.latest_push()
    assert "url" in latest_push


def test_search():
    sobaka = meduza.search("собака", n=24, lang="ru")
    sobaka_list = list(sobaka)
    assert len(sobaka_list) == 24


def test_section_and_tag_kwargs():
    with pytest.raises(TypeError):
        meduza.section("news", 24)
    with pytest.raises(TypeError):
        meduza.tag("новости", 24)
