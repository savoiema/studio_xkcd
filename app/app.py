#!/usr/bin/env python

import logging

import structlog

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen

from tornado.web import URLSpec as Url

from handlers.health import HealthHandler
from handlers.xkcd import XkcdHandler
from handlers.favorites import FavoritesHandler


logger = structlog.get_logger()


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'debug': True
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

    structlog.configure(
        processors=[
            structlog.processors.KeyValueRenderer(
                key_order=['event', 'request_id'],
            ),
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('debug logging enabled')

    name = 'Test App Name'
    port = 8086
    address = '0.0.0.0'
    logging.info('starting %s on %s:%d', name, address, port)

    http_server = tornado.httpserver.HTTPServer(
        request_callback=Application(), xheaders=True)
    http_server.listen(port, address=address)

    tornado.ioloop.IOLoop.instance().start()
