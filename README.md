# Meduza

A simple Python module that wraps the [meduza.io](https://meduza.io) API. (read about Meduza on [Buzzfeed](https://www.buzzfeed.com/bensmith/russians-try-to-build-a-normal-media-startup-across-the-bord))

## Installation
```
pip3 install meduza
```

## Usage

Get an article:

```
>>> url = "https://meduza.io/en/brief/2018/07/16/the-real-russia-today"

>>> article = meduza.get(url)

>>> article.title
'The Real Russia. Today.'

>>> article.second_title
"Trump and Putin meet in Helsinki, the ‘Deep State’ consensus, and Pussy Riot's heart-to-heart with the police"

>>> article.description
'Ahead of the July 16 summit between Vladimir Putin and Donald Trump in Helsinki...'

# and so on:
>>> for attr in filter(lambda x: not x.startswith('_'), dir(article)):
...     print(f"article.{attr}")
article.as_dict
article.blocks
article.datetime
article.description
article.footer
article.html
article.image
article.is_blocks
article.is_html
article.reactions
article.second_title
article.source
article.tag
article.title
article.type
article.url
```

Read latest articles:

```
# English version:

>>> for article in meduza.section('news', language='en', results=3):
...     print(article)
<News: 'A good news month'>
<Like It Or Not: 'A masterclass in imprecision'>
<Like It Or Not: 'Dancy dancy McInternet dance'>


# Russian version:

>>> for article in meduza.section('news', language='ru', results=3):
...     print(article)
<Новости: 'Путина спросили про пенсионную реформу. Он ответил, что ему все не нравится'>
<Шапито: 'В Екатеринбурге открыли барельеф с «условными» Дзержинским и Сталиным (или Кагановичем)'>
<Шапито: 'Новая иллюзия: круги, раскрашенные в четыре разных цвета (на самом деле нет)'>

```

You can find available tags and sections in constants:

```
>>> meduza.EN_SECTIONS
'news'

>>> meduza.EN_TAGS
('news', 'like it or not', 'games')

>>> meduza.RU_SECTIONS
('news', 'articles', 'shapito', 'razbor', 'games', 'podcasts')

>>> meduza.RU_TAGS
('новости', 'истории', 'разбор', 'шапито', 'игры', 'подкасты', 'партнерский материал')

```