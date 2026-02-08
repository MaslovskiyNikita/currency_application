import zlib
from django.http import HttpResponse

class SignatureCRC32Middleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: HttpResponse = self.get_response(request)

        if request.path.startswith('/api/'):
            
            try:
                content = response.content
            except AttributeError:
                return response

            if content:
                checksum = zlib.crc32(content) & 0xffffffff
                response['X-Response-Signature'] = f"{checksum:08x}"

        return response