from datetime import datetime
import logging
import socket
import sys
from argparse import ArgumentParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

from core import jim
import client.settings as settings
from core.meta import ClientVerifier


def get_presence_msg(action, data):  # вывод текущего действия
    msg_time = datetime.datetime.now()
    msg = {
        "action": action,
        "time": msg_time.isoformat(),
        "user": {
            "account_name": "anonim",
            "status": "I am here!"
        },
        "data": data
    }
    return jim.pack(msg)


# args
host = getattr(settings, 'HOST', '127.0.0.1')
port = getattr(settings, 'PORT', 7777)
count_sends = -1

# параметры запуска/отправки
parser = ArgumentParser()
parser.add_argument('-a', '--addr', type=str, help='Sets ip address', default=host)
parser.add_argument('-p', '--port', type=int, help='Sets port', default=port)
parser.add_argument('-m', '--mode', type=str, default='w')
parser.add_argument('-t', '--action', type=str, help='Set action')
parser.add_argument('-d', '--data', type=str, help='Set data')
parser.add_argument('-c', '--count', type=int, help='Count for sends repeat', default=count_sends)
parser.add_argument('-e', '--exit', type=str, help='Set "yes" if need to send exit msg when finalize')

args = parser.parse_args()
host = args.addr
port = args.port
count_sends = args.count
encoding_name = settings.ENCODING
buffersize = settings.BUFFERSIZE

# logging
logger = logging.getLogger('main')
handler = logging.FileHandler('client.log', encoding=settings.ENCODING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class Client(metaclass=ClientVerifier):
    def __init__(self, host, port, buffersize):
        self.host = host
        self.port = port
        self.buffersize = buffersize

    def run_client(self):
        try:
            sock = socket.socket()
            sock.connect((self.host, self.port))
            logger.info(f'Client started with {host}:{port}')
            print(f'Client started with {self.host}:{self.port}')

            if args.mode == 'w':

                while True:
                    value = input('Enter data to send:')
                    response = {
                        'action': 'echo',
                        'time': datetime.now().timestamp(),
                        'data': value
                    }
                    response = sock.recv(settings.BUFFERSIZE)
                    response = jim.unpack(response)
                    logger.info(f'Got next response from server: {response}')
                    print(f'Got next response from server: {response}')
                    sock.send(response)
            else:
                while True:
                    data = sock.recv(self.buffersize)
                    print(data.decode(encoding_name))
        except KeyboardInterrupt:
            print('Client closed')


if __name__ == '__main__':
    client = Client(host, port, buffersize)
    client.run_client()

# def run_client():  # запуск клиента
#     sock = socket.socket()
#     sock.connect((host, port))
#     logger.info(f'Client started with {host}:{port}')
#     print(f'Client started with {host}:{port}')
#
#     is_continue = True
#     i = 0
#
#     if args.mode == 'w':
#         while is_continue:
#             if args.action:
#                 action = args.action
#             else:
#                 action = input('Enter action to send:')
#
#             data = args.data or input('Enter data to send:')
#             if args.exit and i == (count_sends - 1):
#                 msg = get_presence_msg('exit', 'exit')
#             else:
#                 msg = get_presence_msg(action, data)
#             print(f'msg: {msg}')
#             sock.sendall(msg)
#
#             if args.action and args.data:
#                 time.sleep(1)
#
#             i += 1
#             if i == count_sends:
#                 is_continue = False
#     else:
#         while True:
#             response = sock.recv(settings.BUFFERSIZE)
#             response = jim.unpack(response)
#             logger.info(f'Got next response from server: {response}')
#             print(f'Got next response from server: {response}')
#             if response['action'] == 'exit':
#                 break
#
#
# def main():  # запуск основного кода
#     try:
#         run_client()
#     except KeyboardInterrupt:
#         logger.info('Client  closed')
#         print('Client closed')
#
#
# main()
