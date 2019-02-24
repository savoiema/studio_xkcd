from handlers.base import ApiBaseHandler


class HealthHandler(ApiBaseHandler):
    def get(self):
        self.finish('OK')
