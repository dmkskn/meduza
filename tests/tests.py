import meduza
import unittest
from inspect import isgenerator
from urllib.request import urlopen


class TestPublicAPI(unittest.TestCase):
    def test_stocks(self):
        stocks = meduza.stocks()
        self.assertIsInstance(stocks, dict)
        self.assertIsInstance(stocks["usd"]["current"], float)

    def test_get(self):
        url_1 = (
            "https://meduza.io/api/w4/feature/2018/07/03/"
            "astronomam-udalos-zafiksirovat-rozhdenie-novoy"
            "-planety-temperatura-na-ney-okolo-tysyachi-"
            "gradusov-po-tselsiyu"
        )
        url_2 = (
            "https://meduza.io/feature/2018/07/03/astronomam"
            "-udalos-zafiksirovat-rozhdenie-novoy-planety-"
            "temperatura-na-ney-okolo-tysyachi-gradusov-po-tselsiyu"
        )
        article_1 = meduza.get(url_1)
        article_2 = meduza.get(url_2)
        self.assertIsInstance(article_1, dict)
        self.assertIsInstance(article_2, dict)
        self.assertEqual(article_1, article_2)
        self.assertIsNotNone(article_1.get("title"))

    def test_section(self):
        shapito = meduza.section("shapito", n=24, lang="ru")
        self.assertTrue(isgenerator(shapito))
        shapito_list = list(shapito)
        self.assertEqual(len(shapito_list), 24)

    def test_tag(self):
        shapito = meduza.tag("шапито", n=24, lang="ru")
        self.assertTrue(isgenerator(shapito))
        shapito_list = list(shapito)
        self.assertEqual(len(shapito_list), 24)
        for a in shapito_list:
            self.assertEqual(a["tag"]["name"], "шапито")

    def test_iter_reactions_for(self):
        articles = meduza.tag("шапито", n=3, lang="ru")
        urls = [a["url"] for a in articles]
        reactions = meduza.reactions_for(*urls)
        self.assertIsInstance(reactions, dict)
        for url in urls:
            self.assertIn(url, reactions)

    def test_getting_latest_push(self):
        push = meduza.latest_push()
        self.assertIsInstance(push, dict)
        self.assertTrue(bool(push["url"]))

    def test_section_and_tag_kwargs(self):
        with self.assertRaises(TypeError):
            meduza.section("news", 24)
        with self.assertRaises(TypeError):
            meduza.tag("новости", 24)
