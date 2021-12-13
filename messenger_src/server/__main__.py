import logging
import select
import socket
import sys
import threading
from argparse import ArgumentParser
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

import server.settings as settings
from handlers import handle_request


def read_client_data(client, requests, buffersize):
    try:
        b_request = client.recv(buffersize)
    except ConnectionResetError:
        b_request = b''
    if b_request != b'':
        requests.append(b_request)


def write_client_data(client, response):
    client.send(response)


# args
host = getattr(settings, 'HOST', '127.0.0.1')
port = getattr(settings, 'PORT', 7777)

parser = ArgumentParser()
parser.add_argument('-a', '--addr', type=str, help='Sets ip address', default=host)
parser.add_argument('-p', '--port', type=int, help='Sets port', default=port)

args = parser.parse_args()
host = args.addr
port = args.port

# logging
handler = logging.FileHandler('server.log', encoding=settings.ENCODING)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        handler,
    ]
)


def main():
    requests = []
    connections = []

    try:
        sock = socket.socket()
        sock.bind((host, port))
        sock.settimeout(0)
        sock.listen(5)
        logging.info(f'Server started with {host}:{port}')
        while True:
            try:
                client, address = sock.accept()
                logging.info(f'Client detected {address}')
                connections.append(client)
            except Exception as e:
                pass

            if connections != []:
                rlist, wlist, xlist = select.select(
                    connections, connections, connections, 0
                )

                for r_client in rlist:
                    thread = threading.Thread(
                        target=read_client_data,
                        args=(r_client, requests, settings.BUFFERSIZE)
                    )
                    thread.start()

                if requests:
                    b_request = requests.pop()
                    print(f'request: {b_request}')

                    if b_request != b'':
                        b_response = handle_request(b_request)
                        # print(f'response: {b_response}')

                        for w_client in wlist:
                            thread = threading.Thread(
                                target=write_client_data,
                                args=(w_client, b_response)
                            )
                            thread.start()

    except KeyboardInterrupt:
        logging.info('Server  closed')


main()
