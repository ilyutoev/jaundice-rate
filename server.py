import json

from aiohttp import web

from main import process_articles

ARTICLE_URLS_LIMIT = 10


async def index(request):

    urls = [url.strip() for url in request.query.get('urls', '').split(',') if url]
    if len(urls) > ARTICLE_URLS_LIMIT:
        raise web.HTTPBadRequest(
            body=json.dumps({"error": f"too many urls in request, should be {ARTICLE_URLS_LIMIT} or less"})
        )

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
