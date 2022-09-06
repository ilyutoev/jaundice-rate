import asyncio
from unittest.mock import patch

from aiohttp import ClientError

from adapters.constants import ProcessingStatus
from main import process_article


def test_process_article_client_error():
    result = []
    with patch('main.fetch', side_effect=ClientError):
        asyncio.run(process_article(None, None, None, 'inosmi.ru', result))

    assert len(result) == 1
    assert result[0]['status'] == ProcessingStatus.FETCH_ERROR


def test_process_article_parsing_error():
    result = []
    with patch('main.fetch', side_effect=ClientError):
        asyncio.run(process_article(None, None, None, 'news.ru', result))

    assert len(result) == 1
    assert result[0]['status'] == ProcessingStatus.PARSING_ERROR


def test_process_article_timeouts():
    result = []
    with patch('main.fetch', side_effect=asyncio.TimeoutError):
        asyncio.run(process_article(None, None, None, 'inosmi.ru', result))

    assert len(result) == 1
    assert result[0]['status'] == ProcessingStatus.TIMEOUT

    result = []

    with (
        patch('main.fetch'),
        patch('main.sanitize'),
        patch('main.split_by_words', side_effect=asyncio.TimeoutError)
    ):
        asyncio.run(process_article(None, None, None, 'inosmi.ru', result))

    assert len(result) == 1
    assert result[0]['status'] == ProcessingStatus.TIMEOUT


