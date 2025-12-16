from .models import Visit

VALID_STATUS_RANGE = range(200, 400)


class VisitsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code in VALID_STATUS_RANGE:
            Visit.create(request, response)

        return response
