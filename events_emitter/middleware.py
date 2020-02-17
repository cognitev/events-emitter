import redis
from django.http import HttpResponse, HttpResponseServerError
from django.db import connection
from django.conf import settings


class HealthCheckMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "GET":
            if request.path == "/readiness":
                return self.readiness()
            elif request.path == "/liveness":
                return self.liveness()

        return self.get_response(request)

    def liveness(self):
        return HttpResponse("OK")

    def readiness(self):
        try:
            assert self.database_check(), "Error in database check"
            assert self.redis_check(), "Error in redis check"
        except Exception as e:
            return HttpResponseServerError(f"cannot connect to database {e}")

        return HttpResponse("OK")

    def database_check(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            if row is None:
                return HttpResponseServerError("invalid response")
            return True

    def redis_check(self):
        REDIS_CONNECTION_POOL = redis.ConnectionPool.from_url(settings.CELERY_BROKER_URL,
                                                              charset="utf-8",
                                                              decode_responses=True)
        redis_conn = redis.Redis(connection_pool=REDIS_CONNECTION_POOL)
        return redis_conn.ping()
