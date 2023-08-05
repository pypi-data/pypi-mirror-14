from django.http import HttpRequest

from shark.models import Log


class Logging:
    def process_request(self, request):
        request = HttpRequest()

        log = Log()
        log.url = request.path
        log.referrer = request.META.get('HTTP_REFERER', '')
        log.user_agent = request.META.get('HTTP_USER_AGENT', '')
        cloudflare_ip = request.META.get('HTTP_TRUE-CLIENT-IP', '')
        ip_address = request.META.get('REMOTE_ADDR', '')
        log.ip_address = cloudflare_ip or ip_address
        # CF-IPCountry

        print ('Called', request.path)
        return None

    def process_response(self, request, response):
        print('Done', response)
        request.a += 1
        print(request.a)
        return response

