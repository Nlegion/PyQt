from datetime import datetime

from server.decorators import logged


@logged
def validate_request(raw):
    request_time = raw.get('time')
    request_action = raw.get('action')

    return request_action and request_time


@logged
def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'user': request.get('user'),
        'time': datetime.now().timestamp(),
        'data': data,
        'code': code
    }


@logged
def make_400(request):
    return make_response(request, 400, 'Wrong request format')


@logged
def make_404(request):
    return make_response(request, 404, 'Action is not supported')
