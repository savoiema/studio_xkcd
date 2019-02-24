from peewee import *
from utils.settings import Settings

settings = Settings.get_instance()

mysql_db = MySQLDatabase(
    settings['mysql']['database'],
    user=settings['mysql']['username'],
    password=settings['mysql']['password'],
    host=settings['mysql']['hostname'],
    port=settings['mysql']['hostport']
)


class BaseModel(Model):
    class Meta:
        database = mysql_db


class Favorite(BaseModel):
    # id = IntegerField(null=False)
    user_id = CharField(max_length=36, null=False)
    xkcd_id = IntegerField(null=False)

    class Meta:
        db_table = 'favorites'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'xkcd_id': self.xkcd_id
        }

    @classmethod
    def from_dict(cls, favorite_dict):
        favorite = Favorite(
            id=favorite_dict.get('id'),
            user_id=favorite_dict.get('user_id'),
            xkcd_id=favorite_dict.get('xkcd_id')
        )
        return favorite

    @classmethod
    def delete_favorite(cls, user_id, xkcd_id):
        try:
            delete_count = 0
            item = cls.select().where(cls.user_id == user_id, cls.xkcd_id == xkcd_id).get()
            if item:
                delete_count = item.delete_instance()
        except cls.DoesNotExist:
            item = None
            delete_count = 0
        return delete_count, item

    @classmethod
    def save_favorite(cls, favorite_object):
        favorite = Favorite.from_dict(favorite_object)
        favorite.save()

        favorite_response = cls.select().where(cls.user_id == favorite.user_id, cls.xkcd_id == favorite.xkcd_id).get()
        if favorite_response:
            return favorite_response.to_dict()
        raise Exception('there were issues saving the data')

    @classmethod
    def get_user_favorites(cls, user_id):
        if not user_id:
            return []

        try:
            favorites_json = []
            favorites = cls.select().where(cls.user_id == user_id).order_by(cls.id)
            for item in favorites:
                favorites_json.append(Favorite.to_dict(item))
        except cls.DoesNotExist:
            favorites_json = []

        return favorites_json

    @classmethod
    def get_user_favorites_array(cls, user_id):
        favorites_data = Favorite.get_user_favorites(user_id)

        favorites = []
        for f in favorites_data:
            favorites.append(f["xkcd_id"])
        return favorites
