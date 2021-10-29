import sys
import time
import select
import logging
import main.body as chat
import main.params as jim
import log.client_log_config
import multiprocessing

logger = logging.getLogger('chat.client')


def send(sock):
    while True:
        msg = input('Введите сообщение ("exit" для выхода): ')

        if msg:
            print(msg)
            jim.MESSAGE['message'] = msg

            try:
                chat.send_data(sock, jim.MESSAGE)
            except ConnectionResetError as e:
                logger.error(e)
                break


def receive(sock):
    while True:
        try:
            data = chat.get_data(sock)
        except ConnectionResetError as e:
            logger.error(e)
            break

        if data['response'] != '200':
            logger.debug('App ending')
            break

        if 'messages' in data:
            for message in data['messages']:
                sys.stdout.write(f'{message["time"]} - {message["from"]}: {message["message"]}')


if __name__ == '__main__':
    logger.debug('App started')

    parser = chat.create_parser()
    namespace = parser.parse_args()

    client_name = input('Введите имя: ')

    sock = chat.get_client_socket(namespace.addr, namespace.port)
    serv_addr = sock.getpeername()
    start_info = f'Connected to server: {serv_addr[0]}:{serv_addr[1]}'
    print(start_info)
    logger.info(start_info)

    jim.PRESENCE['user']['account_name'] = client_name
    try:
        chat.send_data(sock, jim.PRESENCE)
    except ConnectionResetError as e:
        logger.error(e)
        sock.close()
        exit(1)

    p_send = multiprocessing.Process(target=send, args=(sock,))
    p_receive = multiprocessing.Process(target=receive, args=(sock,))

    p_send.start()
    p_receive.start()

    if not p_send.is_alive() or not p_receive.is_alive():
        exit(1)

    p_send.join()
    p_receive.join()
    sock.close()
