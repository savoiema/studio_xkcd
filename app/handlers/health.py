import tornado.web


class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish('OK')