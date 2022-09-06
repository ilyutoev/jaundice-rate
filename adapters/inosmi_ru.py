from bs4 import BeautifulSoup

from .exceptions import ArticleNotFound
from .html_tools import remove_buzz_attrs, remove_buzz_tags, remove_all_tags


def sanitize(html, plaintext=False):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select("div.article")

    if len(articles) != 1:
        raise ArticleNotFound()

    article = articles[0]
    article.attrs = {}

    buzz_blocks = [
        *article.select('.article__notice'),
        *article.select('.article__aggr'),
        *article.select('.article__tags'),
        *article.select('.article-disclaimer'),
        *article.select('footer.article-footer'),
        *article.select('aside'),
    ]
    for el in buzz_blocks:
        el.decompose()

    remove_buzz_attrs(article)
    remove_buzz_tags(article)

    if not plaintext:
        text = article.prettify()
    else:
        remove_all_tags(article)
        text = article.get_text()
    return text.strip()


def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.select('title')[0].get_text().split('|')[0].strip()
