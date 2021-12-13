from decorators import logged
from protocol import make_response, make_400


@logged
def get_exit(request):
    data = request.get('data')
    if data:
        return make_response(
            request, 200, data
        )

    return make_400(request)
