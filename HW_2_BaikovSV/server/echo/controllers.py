from server.decorators import logged
from server.protocol import make_response, make_400


@logged
def get_echo(request):
    data = request.get('data')
    if data:
        return make_response(
            request, 200, data
        )

    return make_400(request)
