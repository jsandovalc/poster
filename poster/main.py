from aiohttp import web

async def post(request):
    """Page to post a message."""
    return web.Response(body=b'prueba')

app = web.Application()
app.router.add_route('GET', '/', post)

web.run_app(app)
