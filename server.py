from aiohttp import web

from main import process_articles


async def index(request):
    urls = []
    for url in request.query.get('urls', '').split(','):
        if url:
            urls.append(url.strip())

    results = await process_articles(urls)

    response = []
    for article_info in results:
        response.append({
            "status": article_info['status'].value,
            "url": article_info['url'],
            "score": article_info['rate'],
            "words_count": article_info['words_count']
        })

    return web.json_response(data=response)


app = web.Application()
app.add_routes([web.get('/', index)])
web.run_app(app)
