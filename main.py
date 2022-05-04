import aiohttp
import asyncio

import pymorphy2
from anyio import create_task_group

from adapters.inosmi_ru import get_title
from adapters.inosmi_ru import sanitize
from text_tools import calculate_jaundice_rate
from text_tools import get_charged_words
from text_tools import split_by_words


async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def process_article(session, morph, charged_words, url, result):
    html = await fetch(session, url)

    text = sanitize(html, plaintext=True)
    article_words = split_by_words(morph, text)
    rate = calculate_jaundice_rate(article_words, charged_words)

    result.append({
        'title': get_title(html),
        'rate': rate,
        'words_count': len(article_words),
    })


async def main():
    charged_words = get_charged_words()

    TEST_ARTICLES = [
        'https://inosmi.ru/20220209/ukraina-252938463.html',
        'https://inosmi.ru/20220504/ukraina-254051228.html',
        'https://inosmi.ru/20220504/drova-254050630.html',
        'https://inosmi.ru/20220504/bayden-254047336.html',
        'https://inosmi.ru/20220504/ukraina-254051228.html',
    ]
    morph = pymorphy2.MorphAnalyzer()

    result = []

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with create_task_group() as tg:
            for url in TEST_ARTICLES:
                tg.start_soon(
                    process_article,
                    session, morph, charged_words, url, result
                )

    for article_info in result:
        print('Заголовок:', article_info['title'])
        print('Рейтинг:', article_info['rate'])
        print('Слов в статье:', article_info['words_count'])

asyncio.run(main())
