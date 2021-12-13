import select
import threading
from socket import *
from pathlib import Path
import sys
import logging
from handlers import handle_request
from argparse import ArgumentParser

# путь к папке
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

import core.settings as settings
import core.utils as utils

# получение параметров
host = getattr(settings, 'HOST', '127.0.0.1')
port = getattr(settings, 'PORT', 7777)
coding = getattr(settings, 'ENCODING', 'ascii')
buffersize = settings.BUFFERSIZE
parser = ArgumentParser()
parser.add_argument('-a', '--addr', type=str, help='Sets ip address', default=host)
parser.add_argument('-p', '--port', type=int, help='Sets port', default=port)
args = parser.parse_args()
host = args.addr
port = args.port
# logging
handler = logging.FileHandler('server.log', encoding=settings.ENCODING)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[handler, ])


def read_client_data(client, requests, buffersize):
    try:
        b_request = client.recv(buffersize)
    except ConnectionResetError:
        b_request = b''
    if b_request != b'':
        requests.append(b_request)


def write_client_data(client, response):
    client.send(response)


def main():
    s = socket(AF_INET, SOCK_STREAM)  # сокет будет сетевым и потоковым
    s.bind((host, port))  # привязка сокета к адресу
    s.listen(5)  # 5 запросов одновременно
    s.settimeout(0)
    connections = []  # список клиентов
    requests = []  # список запросов
    r, w, e = [], [], []
    logging.info(f'Сервер начал с параметрами: {host}:{port}')
    print(f'Сервер начал с параметрами: {host}:{port}')

    while True:  # ожидание сообщения
        try:  # поиск новых соединений
            client, addr = s.accept()  # создание соединения
        except OSError as e:
            pass
        else:
            print(f'Соединение с: {addr}')
            logging.info(f'Client detected {addr}')
            connections.append(client)  # добавление нового клиента
        finally:
            try:
                if connections != []:  # если в списке клиентов кто то есть
                    r, w, e = select.select(connections, connections, connections, 0)

                for r_client in r:
                    thread = threading.Thread(
                        target=read_client_data,
                        args=(r_client, requests, settings.BUFFERSIZE)
                    )
                    thread.start()
            except Exception as e:
                client.close()

            try:
                if requests:
                    b_request = requests.pop()
                    print(f'request: {b_request}')
                    if b_request != b'':
                        b_response = handle_request(b_request)
                    for w_client in w:
                        thread = threading.Thread(  # разделение по потокам
                            target=write_client_data,  # вызов функции отправки сообщения
                            args=(w_client, b_response)  # клиент и битовый ответ
                        )
                        thread.start()  # начать отправку
            except(ValueError):
                client.close()


if __name__ == '__main__':
    main()
