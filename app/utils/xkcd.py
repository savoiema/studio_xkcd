import logging
from tornado.httpclient import HTTPError
from utils.cachedhttpclient import CachedClient
from utils.settings import Settings


class Randall:
    def __init__(self):
        self.settings = Settings.get_instance()
        self._http_client = CachedClient(
            redis_hostname=self.settings['redis']['hostname'],
            cache_expires=self.settings['redis']['cache_expires'])
        self._max_count = 20
        self._default_count = 20

    @property
    def xkcd_api_url(self):
        return 'https://xkcd.now.sh/'

    @staticmethod
    def validate_xkcd_id(num):
        input_type = type(num)
        if not num:
            return None
        elif input_type is int:
            return num
        else:
            try:
                return int(num)
            except ValueError:
                pass
            return None

    def get_count(self, count):
        input_type = type(count)
        if not count:
            return self._default_count
        else:
            try:
                if input_type is not int:
                    count = int(count)
                return count if count <= self._max_count else self._max_count
            except ValueError:
                pass
            return self._default_count

    async def fetch(self, num=None):
        num = Randall.validate_xkcd_id(num)
        url = '{}{}'.format(self.xkcd_api_url,  str(num) if num else '')
        logging.info('url: {}'.format(url))

        try:
            response = await self._http_client.fetch(url)
        except HTTPError as e:
            raise e
        except Exception as e:
            raise e

        return response

    async def fetch_many(self, num=None, count=20):
        response = []
        num = Randall.validate_xkcd_id(num)
        count = self.get_count(count)
        for i in range(count):
            item = await self.fetch(num)
            if not num:
                num = item['num']
            response.append(item)
            num -= 1
        return {'next': num, 'count': len(response), 'results': response}
