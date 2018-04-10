import logging
import pathlib

import yaml

from aiohttp import web

from .mongo import init_mongodb, close_mongodb
from . import views

def create_app(config=None, **kwargs):
    """ 
    I create aiohttp.web.Application object and configure it
    and return it.
    """
    app = web.Application(**kwargs)
    config_logging()
    configure_app(app, config)
    configure_database(app)
    setup_routes(app)

    return app

def config_logging():
    FORMAT = 'Error at %(name)s | %(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT)

def configure_database(app):
    app.on_startup.append(init_mongodb)
    app.on_cleanup.append(close_mongodb)

def configure_app(app, config):
    if not config:
        config = pathlib.Path(__file__).parent / 'config.yaml'

    with open(config, 'r') as f:
        config = yaml.load(f.read())
    app['config'] = config

def setup_routes(app):
    app.router.add_routes(views.routes)