from pathlib import Path
from typing import Optional, List

import aiohttp_jinja2
import aiopg.sa
from aiohttp import web
import jinja2

from new_poster.routes import init_routes
from new_poster.utils.common import init_config


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    '''
    Initialize jinja2 template for application.
    '''
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


async def database(app: web.Application) -> None:
    '''
    A function that, when the server is started, connects to postgresql,
    and after stopping it breaks the connection (after yield)
    '''
    config = app['config']['postgres']

    engine = await aiopg.sa.create_engine(**config)
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


def init_app(config: Optional[List[str]] = None) -> web.Application:
    app = web.Application()

    init_jinja2(app)
    init_config(app, config=config)
    init_routes(app)

    app.cleanup_ctx.extend([
        database,
    ])

    return app
