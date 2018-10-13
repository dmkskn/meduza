import meduza
import unittest
from inspect import isgenerator
from urllib.request import urlopen


class TestPublicAPI(unittest.TestCase):
    def test_stocks_function(self):
        stocks = meduza.stocks()

        self.assertIsInstance(stocks, dict)
        self.assertIsInstance(stocks["usd"]["current"], float)

    def test_get_function(self):
        url_with_api_suffix = (
            "https://meduza.io/api/v3/feature/2018/07/03/"
            "astronomam-udalos-zafiksirovat-rozhdenie-novoy"
            "-planety-temperatura-na-ney-okolo-tysyachi-"
            "gradusov-po-tselsiyu"
        )
        url_without_api_suffix = (
            "https://meduza.io/feature/2018/07/03/astronomam"
            "-udalos-zafiksirovat-rozhdenie-novoy-planety-"
            "temperatura-na-ney-okolo-tysyachi-gradusov-po-tselsiyu"
        )
        article_created_by_url_with_api_suffix = meduza.get(
            url_with_api_suffix, as_dict=True
        )
        article_created_by_url_without_api_suffix = meduza.get(
            url_without_api_suffix, as_dict=True
        )

        self.assertIsInstance(article_created_by_url_with_api_suffix, dict)
        self.assertIsInstance(article_created_by_url_without_api_suffix, dict)

        self.assertEqual(
            article_created_by_url_with_api_suffix,
            article_created_by_url_without_api_suffix,
        )
        self.assertIsNotNone(article_created_by_url_with_api_suffix.get("title"))

    def test_section_function(self):
        shapito = meduza.section("shapito", n=24, lang="ru")
        self.assertTrue(isgenerator(shapito))

        shapito_list = list(shapito)
        self.assertEqual(len(shapito_list), 24)

    def test_tag_function(self):
        shapito = meduza.tag("шапито", n=24, lang="ru", as_dict=True)
        self.assertTrue(isgenerator(shapito))

        shapito_list = list(shapito)
        self.assertEqual(len(shapito_list), 24)

        for a in shapito_list:
            self.assertEqual(a["tag"]["name"], "шапито")

    def test_reactions_for_function(self):
        shapito, *_ = meduza.tag("шапито", n=1, lang="ru", as_dict=True)
        reactions_for_shapito = meduza.reactions_for(shapito)
        self.assertIsInstance(reactions_for_shapito, dict)
        self.assertNotEqual(reactions_for_shapito, {})

    def test_iter_reactions_for_function(self):
        shapito_articles = meduza.tag("шапито", n=3, lang="ru", as_dict=True)
        reactions = meduza.iter_reactions_for(*shapito_articles)
        self.assertTrue(isgenerator(reactions))
        for r in reactions:
            self.assertNotEqual(r, {})

    def test_getting_latest_push(self):
        push = meduza.latest_push()
        self.assertIsInstance(push, dict)
        self.assertTrue(bool(push["url"]))

    def test_section_and_tag_kwargs(self):
        with self.assertRaises(TypeError):
            meduza.section("news", 24)
        with self.assertRaises(TypeError):
            meduza.tag("новости", 24)


class TestArticle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        url = (
            "https://meduza.io/feature/2018/07/03/"
            "astronomam-udalos-zafiksirovat-rozhdenie"
            "-novoy-planety-temperatura-na-ney-okolo-"
            "tysyachi-gradusov-po-tselsiyu"
        )
        cls.a = meduza.get(url)
        cls.da = meduza.get(url, as_dict=True)

    def test_getting_article_as_dict(self):
        self.assertEqual(self.a.as_dict(), self.da)

    def test_iterate_article(self):
        for attr_name, attr_value in self.a:
            self.assertIn(attr_name, self.a.__dict__)
            self.assertEqual(getattr(self.a, attr_name), attr_value)
