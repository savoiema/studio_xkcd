import json
import redis
import logging

from tornado.httpclient import AsyncHTTPClient, HTTPError


class CachedClient:
    def __init__(self, **kwargs):
        # Some Redis config
        self._redis_hostname = kwargs.get('redis_hostname', '127.0.0.1')
        self._redis_port = kwargs.get('redis_port', 6379)
        self._cache_expires = kwargs.get('cache_expires', 60)
        self._cache = redis.Redis(host=self._redis_hostname, port=self._redis_port)

        # Tornado AsyncHttpClient
        self._http_client = AsyncHTTPClient()

    async def fetch(self, request, callback=None, raise_error=True, skip_cache=False, **kwargs):
        value = self._cache.get(request) if not skip_cache else None

        if value:
            logging.info('Redis cache hit - {}'.format(request))
            response_body = json.loads(value)
        else:
            logging.info('Redis cache miss - {}'.format(request))

            try:
                response = await self._http_client.fetch(
                    request,
                    callback=callback,
                    raise_error=raise_error,
                    **kwargs
                )
                response_body = json.loads(response.body)

                if not skip_cache:
                    self._cache.set(request, response.body, ex=self._cache_expires)
            except HTTPError as e:
                raise e
            except Exception as e:
                raise e

        return response_body
