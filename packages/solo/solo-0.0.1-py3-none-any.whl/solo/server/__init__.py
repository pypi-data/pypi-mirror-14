import asyncio
from typing import Any, Dict
import logging

from aiohttp import web

from . import db
from ..configurator import Configurator
from ..configurator.view import PredicatedHandler


log = logging.getLogger(__name__)


async def init_webapp(loop: asyncio.AbstractEventLoop,
                      config: Dict[str, Any]) -> web.Application:
    webapp = web.Application(loop=loop,
                             debug=config['debug'])

    configurator = Configurator()
    #configurator.include('pacific.db')

    apps = config['apps']
    for app_name, app_options in apps.items():
        configurator.include(app_name, app_options['url_prefix'])

    #configurator.scan()
    # We must also scan applications' packages
    for app_name in apps:
        configurator.scan(app_name)
        webapp = register_routes(webapp, configurator)

    # Setup database connection pool
    # ------------------------------
    engine = await db.setup_database(loop, config)
    setattr(webapp, 'dbengine', engine)
    return webapp


def register_routes(webapp: web.Application, configurator: Configurator) -> web.Application:
    # app.router.add_route("GET", "/probabilities/{attrs:.+}",
    #                     probabilities.handlers.handler)
    # Setup routes
    # ------------
    for route in configurator.routes.values():
        log.debug('Registering route {}'.format(route.name))
        handler = PredicatedHandler(route.viewlist)
        webapp.router.add_route(method='*',
                                path=route.pattern,
                                name=route.name,
                                handler=handler)
    return webapp
