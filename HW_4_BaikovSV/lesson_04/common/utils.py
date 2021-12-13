"""Утилиты"""

import json
from lesson_04.common.variables import MAX_PACKAGE_LENGTH, ENCODING
from lesson_04.decos import log
from lesson_04.errors import IncorrectDataReceivedError, NonDictInputError



@log
def get_message(sock):
    """
    Утилита приёма и декодирования сообщения принимает байты выдаёт словарь,
    если принято что-то другое отдаёт ошибку значения

    """

    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        else:
            raise IncorrectDataReceivedError
    else:
        raise IncorrectDataReceivedError


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его

    """

    if not isinstance(message, dict):
        raise NonDictInputError
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
