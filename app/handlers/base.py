import json
import tornado.web

from uuid import UUID


class ApiBaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        self._json_body = None
        super(ApiBaseHandler, self).__init__(*args, **kwargs)

    def data_received(self, chunk):
        pass

    @staticmethod
    def validate_uuid(user_id):
        if user_id:
            try:
                uuid_object = str(UUID(user_id, version=4))
                return str(uuid_object)
            except ValueError:
                pass
        return None

    def get_user_id(self):
        user_id = self.request.headers.get('X-User-ID')
        return ApiBaseHandler.validate_uuid(user_id)

    @property
    def json_body(self):
        if self._json_body:
            return self._json_body

        try:
            self._json_body = json.loads(self.request.body)
        except ValueError:
            raise tornado.web.HTTPError(400, 'Invalid JSON')

        return self._json_body

    def api_response(self, data, code=200):
        self.set_status(code, reason='error')
        self.set_header('Content-Type', 'application/json')
        if not 200 <= code < 300:
            data = {'message': data}
        if not isinstance(data, str):
            data = json.dumps(data)
        self.finish(data)
