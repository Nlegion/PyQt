import datetime
import logging
import socket
import sys
import time
from argparse import ArgumentParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

from core import jim
import core.settings as settings


def get_presence_msg(action, data):
    msg_time = datetime.datetime.now()
    msg = {
        "action": action,
        "time": msg_time.isoformat(),
        "user": {"account_name": "anonim", "status": "I am here!"},
        "data": data}
    return jim.pack(msg)


# args
host = getattr(settings, 'HOST', '127.0.0.1')
port = getattr(settings, 'PORT', 7777)
count_sends = -1
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

# logging
logger = logging.getLogger('main')
handler = logging.FileHandler('client.log', encoding=settings.ENCODING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def run_client():
    sock = socket.socket()
    sock.connect((host, port))
    logger.info(f'Client started with {host}:{port}')
    print(f'Client started with {host}:{port}')

    is_continue = True
    i = 0

    if args.mode == 'w':
        while is_continue:
            if args.action:
                action = args.action
            else:
                action = input('Enter action to send:')

            data = args.data or input('Enter data to send:')
            if args.exit and i == (count_sends - 1):
                msg = get_presence_msg('exit', 'exit')
            else:
                msg = get_presence_msg(action, data)
            print(f'msg: {msg}')
            sock.sendall(msg)

            if args.action and args.data:
                time.sleep(1)

            i += 1
            if i == count_sends:
                is_continue = False
    else:
        while True:
            response = sock.recv(settings.BUFFERSIZE)
            response = jim.unpack(response)
            logger.info(f'Got next response from server: {response}')
            print(f'Got next response from server: {response}')
            if response['action'] == 'exit':
                break


def main():
    try:
        run_client()
    except KeyboardInterrupt:
        logger.info('Client  closed')
        print('Client closed')


main()
