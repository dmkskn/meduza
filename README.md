# Meduza

[![Build Status](https://travis-ci.org/dmkskn/meduza.svg?branch=master)](https://travis-ci.org/dmkskn/meduza)

A simple Python module that wraps the [meduza.io](https://meduza.io) API. (read about Meduza on [Buzzfeed](https://www.buzzfeed.com/bensmith/russians-try-to-build-a-normal-media-startup-across-the-bord))

## Installation

```
pip install meduza
```

## Usage

Get an article:

```python
>>> url = "https://meduza.io/en/brief/2018/07/16/the-real-russia-today"

>>> article = meduza.get(url)

>>> article["title"]
'The Real Russia. Today.'

>>> article["second_title"]
"Trump and Putin meet in Helsinki, the ‘Deep State’ consensus, and Pussy Riot's heart-to-heart with the police"
```

Get the latest articles on this section:

```python
# English version:

>>> for article in meduza.section('news', n=3, lang='en'): 
...     print(f" - '{article['title']}'")
 - 'Chechnya’s ruler has a stable full of prize-winning race horses, but you’d never know it, looking at his income declarations'
 - 'Russian musicians are being forced to cancel their concerts across the country, which makes now the perfect time to listen to their music'
 - 'The Real Russia. Today.'


# Russian version:

>>> for article in meduza.section('news', n=3, lang='ru'):
...     print(f" - '{article['title']}'")
 - 'Путина спросили про пенсионную реформу. Он ответил, что ему все не нравится'
 - 'В Екатеринбурге открыли барельеф с «условными» Дзержинским и Сталиным (или Кагановичем)'
 - 'Новая иллюзия: круги, раскрашенные в четыре разных цвета (на самом деле нет)'
```

You can find available tags and sections in constants:

```python
>>> meduza.EN_SECTIONS
'news'

>>> meduza.EN_TAGS
('news', 'like it or not', 'games')

>>> meduza.RU_SECTIONS
('news', 'articles', 'shapito', 'razbor', 'games', 'podcasts')

>>> meduza.RU_TAGS
('новости', 'истории', 'разбор', 'шапито', 'игры', 'подкасты', 'партнерский материал')
```
