from redis_helper import RedisHelper
from pylimit_exception import PyLimitException
import time


class PyLimit(object):
    redis_helper = None     # type: RedisHelper

    def __init__(self):
        self.namespace = None   # type: str
        self.period = None      # type: int
        self.limit = None       # type: int

    @classmethod
    def init(cls, redis_host: str, redis_port: int, is_sentinel_redis=False, redis_sentinel_service="mymaster"):
        """
        Initializes redis connection
        :param redis_host: Hostname of redis server
        :type redis_host: str

        :param redis_port: Port at which redis server is listening
        :type redis_port:int

        :param is_sentinel_redis: Parameter indicating if redis server is a sentinel server. Default is false
        :type: bool

        :param redis_sentinel_service: If redis server is a sentinel server, service name for redis sentinel
        :type str

        """
        if not cls.redis_helper:
            cls.redis_helper = RedisHelper(host=redis_host, port=redis_port, is_sentinel=is_sentinel_redis,
                                           sentinel_service=redis_sentinel_service)

    def create(self, namespace: str, period: int, limit: int):
        """
        Creates a namespace for which rate limiting is to be implemented

        :param namespace: Rate limiting namespace
        :type: str

        :param period: Rate limiting period in seconds
        :type: int

        :param limit: Number of attempts permitted by rate limiting within a given period
        :type: int

        """
        self.namespace = namespace
        self.period = period
        self.limit = limit

    def attempt(self, namespace: str) -> bool:
        """
        Records an attempt and returns true of false depending on whether attempt can go through or not

        :param namespace: Rate limiting namespace
        :type: str

        :return: Returns true if attempt can go ahead under current rate limiting rules, false otherwise
        """
        can_attempt = False
        if not PyLimit.redis_helper:
            raise PyLimitException("redis connection information not provided")
        connection = PyLimit.redis_helper.get_atomic_connection()
        current_time = int(round(time.time() * 1000))
        old_time_limit = current_time - (self.period * 1000)
        connection.zremrangebyscore(namespace, 0, old_time_limit)
        connection.expire(namespace, self.period)
        connection.zadd(namespace, current_time, current_time)
        connection.zrange(namespace, 0, -1, withscores=True)
        redis_result = connection.execute()
        current_count = len(redis_result[-1])
        if current_count <= self.limit:
            can_attempt = True
        return can_attempt

