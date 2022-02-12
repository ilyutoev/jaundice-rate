import aiohttp
import asyncio

import pymorphy2

from adapters.inosmi_ru import sanitize
from text_tools import calculate_jaundice_rate
from text_tools import split_by_words


async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def main():
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        html = await fetch(session, 'https://inosmi.ru/20220209/ukraina-252938463.html')
    morph = pymorphy2.MorphAnalyzer()

    text = sanitize(html, plaintext=True)

    article_words = split_by_words(morph, text)

    test_charged_words = ['удар', 'атака', 'агрессия']
    rate = calculate_jaundice_rate(article_words, test_charged_words)

    print('Рейтинг: ', rate)
    print('Слов в статье: ', len(article_words))

asyncio.run(main())
