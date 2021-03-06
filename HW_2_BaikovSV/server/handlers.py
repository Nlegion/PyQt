import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

from core import jim # преобразование в формат
from server.protocol import ( # логирование события
    validate_request, make_response,
    make_400, make_404
)
from server.routes import resolve


def handle_request(raw_request):
    request = jim.unpack(raw_request)

    action_name = request.get('action')

    if validate_request(request):
        controller = resolve(action_name)
        if controller:
            try:
                response = controller(request)
                if response.get('code') != 200:
                    logging.error('Wrong request format')
                else:
                    logging.info(f'Request is valid and processed by controller')
            except Exception as err:
                logging.critical(err)
                response = make_response(
                    request, 500, 'Internal server error'
                )
        else:
            logging.error(f'Action {action_name} does not exits')
            response = make_404(request)
    else:
        logging.error('Request is not valid')
        response = make_400(request)

    return jim.pack(response)
