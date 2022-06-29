from aiohttp import web


async def index(request):
    response = {'urls': []}
    for url in request.query.get('urls', '').split(','):
        if url:
            response['urls'].append(url.strip())
    return web.json_response(data=response)


app = web.Application()
app.add_routes([web.get('/', index)])
web.run_app(app)
