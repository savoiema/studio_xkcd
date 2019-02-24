#!/usr/bin/env python

import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen

from tornado.web import URLSpec as Url

from handlers.health import HealthHandler
from handlers.xkcd import XkcdHandler
from handlers.favorites import FavoritesHandler
from utils.settings import Settings

settings = Settings.get_instance()


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'debug': settings['general']['debug']
        }

        app_handlers = [
            Url(r'^/api/health$', HealthHandler, name='health'),
            Url(r'^/api/?(\d+)?$', XkcdHandler, name='xkcd'),
            Url(r'^/api/favorites', FavoritesHandler, name='favorites'),
            Url(r'^/api/favorites/?(\d+)?$', FavoritesHandler, name='favorites')
        ]
        super().__init__(app_handlers, **app_settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()

    if settings['general']['debug']:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug('debug logging enabled')

    name = settings['general']['name']
    port = settings['general']['port']
    address = settings['general']['address']
    logging.info('starting %s on %s:%d', name, address, port)

    http_server = tornado.httpserver.HTTPServer(
        request_callback=Application(),
        xheaders=True
    )
    http_server.listen(port, address=address)

    tornado.ioloop.IOLoop.instance().start()
