import structlog

from model import Favorite
from utils.xkcd import Randall
from handlers.base import ApiBaseHandler

randall = Randall()
logger = structlog.get_logger()


class XkcdHandler(ApiBaseHandler):

    def data_received(self, chunk):
        pass

    async def get(self, num=None):
        user_id = self.get_user_id()
        count = self.get_argument('count', None)

        xkcd_data = await randall.fetch_many(num, count)

        favorites = []
        if user_id:
            favorites = set(Favorite.get_user_favorites_array(user_id))

        for item in xkcd_data['results']:
            item['is_favorite'] = True if item['num'] in favorites else False

        self.api_response(xkcd_data)
