import logging

from model import Favorite
from utils.xkcd import Randall
from handlers.base import ApiBaseHandler

randall = Randall()


class FavoritesHandler(ApiBaseHandler):
    def data_received(self, chunk):
        pass

    async def get(self, detailed=False):
        user_id = self.get_user_id()
        detailed = self.get_argument('detailed', None)

        if user_id:
            favorites = Favorite.get_user_favorites_array(user_id)
        else:
            self.api_response('Missing user_id in header', 400)
            return

        if detailed:
            detailed_results = []
            for favorite in favorites:
                details = await randall.fetch(favorite)
                detailed_results.append(details)
            favorites = detailed_results

        self.api_response({"count": len(favorites), "results": favorites})

    def post(self):
        user_id = self.get_user_id()
        xkcd_id = self.json_body.get('num')

        if user_id and xkcd_id:
            try:
                xkcd_id = int(xkcd_id)
            except ValueError:
                self.api_response('xkcd article number must be numeric', 400)
                return

            try:
                favorite = Favorite.save_favorite({'user_id': user_id, 'xkcd_id': xkcd_id})
                self.api_response({'results': favorite})
            except Exception as e:
                logging.error("Error: {}".format(e))
                self.api_response('Unexpected error saving favorite', 500)
        else:
            self.api_response('missing information', 400)

    def delete(self, num=None):
        user_id = self.get_user_id()
        if not user_id:
            self.api_response('Missing user_id in header', 400)
            return

        if not num:
            self.api_response('xkcd article number is required', 400)
            return

        try:
            xkcd_id = int(num)
        except ValueError:
            self.api_response('xkcd article number must be numeric', 400)
            return

        count, favorite = Favorite.delete_favorite(user_id, xkcd_id)

        if not favorite:
            self.api_response('Favorite cannot be deleted because it doesnt exist', 405)
        elif count == 0:
            self.api_response('db error', 500)
        else:
            self.api_response(favorite.to_dict(), 200)
