import json
import redis
import structlog

from tornado.httpclient import AsyncHTTPClient, HTTPError

cache = redis.Redis(host='172.18.0.4', port=6379)
logger = structlog.get_logger()


class Randall:
    def __init__(self):
        self._cache_expires = 604800
        self._max_count = 20
        self._default_count = 20
        self._http_client = AsyncHTTPClient()

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
        logger.info('url: {}'.format(url))

        if num:
            value = cache.get(url)
        else:
            value = None

        if value:
            logger.info('Cache hit - {}'.format(url))
            response_body = json.loads(value)
        else:
            logger.info('Cache miss - {}'.format(url))

            try:
                response = await self._http_client.fetch(url)
                response_body = json.loads(response.body)
                cache.set(url, response.body, ex=self._cache_expires)
            except HTTPError as e:
                raise e
            except Exception as e:
                raise e

        return response_body

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
