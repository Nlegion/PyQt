from socket import *
from pathlib import Path
import sys
import logging

# путь к папке
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))
import core.settings as settings
import core.utils as utils

# logging
logger = logging.getLogger('main')
handler = logging.FileHandler('client.log', encoding=settings.ENCODING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# получение параметров
try:
    host = getattr(settings, 'HOST', '127.0.0.1')
    port = getattr(settings, 'PORT', 7777)
    coding = getattr(settings, 'ENCODING', 'ascii')
    buffersize = settings.BUFFERSIZE
except IndexError:
    print('Ошибка с параметрами')
    sys.exit(1)


def main():
    s = socket(AF_INET, SOCK_STREAM)  # сокет будет сетевым и потоковым
    s.connect((host, port))
    logger.info(f'Клиент начал с параметрами: {host}:{port}')
    print(f'Клиент начал с параметрами: {host}:{port}')
    msg_to_server = 'сообщение'
    try:
        s.send(utils.send_message(msg_to_server, coding))
    except(ValueError):
        print('Сообщение не отправлено')
        logger.info(f'Клиент закрыт из-за ошибки отпраления')
        sys.exit(1)
    try:
        data = utils.get_message(s, buffersize, coding)
        logger.info(f'Ответ сервера: {data}')
        print(f'Ответ сервера: {data}')
    except(ValueError):
        print('Сообщение не получено')
        logger.info(f'Клиент закрыт из-за ошибки получения')
        sys.exit(1)
    s.close()


if __name__ == '__main__':
    main()
