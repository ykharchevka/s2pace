from pathlib import Path

import aiohttp_jinja2
import aiohttp_session
import asyncpg
import jinja2
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from .views import index, message_data, messages, replay_upload
from .config import DB_DSN, AUTH_KEY, COOKIE_NAME

THIS_DIR = Path(__file__).parent


async def startup(app: web.Application):
    # TODO: trigger create_tables here to get db ready
    app['pg'] = await asyncpg.create_pool(dsn=DB_DSN, min_size=2)  # TODO: change to connecting by means of aiopg


async def cleanup(app: web.Application):
    app['db'].close()
    await app['db'].wait_closed()


async def create_app():
    app = web.Application()
    app.update(
        static_root_url='/static/',
    )

    jinja2_loader = jinja2.FileSystemLoader(str(THIS_DIR / 'templates'))
    aiohttp_jinja2.setup(app, loader=jinja2_loader)

    app.on_startup.append(startup)
    app.on_cleanup.append(cleanup)

    aiohttp_session.setup(app, EncryptedCookieStorage(AUTH_KEY, cookie_name=COOKIE_NAME))

    app.router.add_get('/', index, name='index')
    # app.router.add_route('*', '/messages', messages, name='messages')
    # app.router.add_get('/messages/data', message_data, name='message-data')
    app.router.add_post('/replay_upload', replay_upload, name='replay-upload')
    return app
