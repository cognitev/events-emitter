from django.http import HttpResponse, HttpResponseServerError
from django.db import connection


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
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                row = cursor.fetchone()
                if row is None:
                    return HttpResponseServerError("invalid response")
        except Exception as e:
            return HttpResponseServerError(f"cannot connect to database {e}")

        return HttpResponse("OK")
