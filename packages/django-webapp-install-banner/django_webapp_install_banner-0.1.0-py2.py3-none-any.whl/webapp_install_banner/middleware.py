
from . import settings


class WebAppMiddleware(object):

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        if request.GET.get(settings.WEBAPP_FIELD):
            response.set_cookie(settings.WEBAPP_COOKIE, "1")
        return response
