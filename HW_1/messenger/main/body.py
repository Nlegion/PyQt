import argparse
import socket
import json
import logging
import inspect
from functools import wraps

ADDRESS = 'localhost'
PORT = 7777
CONNECTIONS = 10
TIMEOUT = 0.5

server_logger = logging.getLogger('chat.server')
client_logger = logging.getLogger('chat.client')


def log(func):
    @wraps(func)
    def call(*args, **kwargs):
        outer_func = inspect.stack()[1][3]
        server_logger.debug(f'Function "{func.__name__}" is called into "{outer_func}"')
        client_logger.debug(f'Function "{func.__name__}" is called into "{outer_func}"')
        return func(*args, **kwargs)

    return call


@log
def get_server_socket(addr, port):
    s = socket.socket()
    s.bind((addr, port))
    s.listen(CONNECTIONS)
    s.settimeout(TIMEOUT)
    return s


@log
def get_client_socket(addr, port):
    s = socket.socket()
    s.connect((addr, port))
    return s


@log
def send_data(recipient, data):
    recipient.send(json.dumps(data).encode('utf-8'))


@log
def get_data(sender):
    return json.loads(sender.recv(1048576).decode("utf-8"))


def create_parser():
    parser = argparse.ArgumentParser(
        description='JSON instant messaging'
    )

    parser_group = parser.add_argument_group(title='Parameters')
    parser_group.add_argument('-a', '--addr', default=ADDRESS, help='IP address')
    parser_group.add_argument('-p', '--port', type=int, default=PORT, help='TCP port')

    return parser
