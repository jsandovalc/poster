from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web


class TestMainView(AioHTTPTestCase):
    """Main poster web page tests."""
    def get_app(self, loop):
        return web.Application(loop=loop)

    @unittest_run_loop
    async def test_example(self):
        request = await self.client.request("GET", "/")
        assert request.status == 200
        text = await request.text()
        assert "Hello, world" in text
