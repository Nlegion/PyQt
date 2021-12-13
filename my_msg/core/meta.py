import dis
import inspect
import socket


class ClientVerifier(type):
    def __init__(self, cls_name, bases, cls_dict):
        for key, value in cls_dict.items():
            assert not isinstance(value, socket.socket), 'Запрещено создавать сокет на уровне класса'

            try:
                instructions = dis.get_instructions(value)
            except TypeError:
                continue
            if instructions:
                for el in instructions:
                    assert not el.argval == 'accept' or not el.argval == 'listen', \
                        'Запрещено вызывать accept и listen для сокетов'

                    if el.opname == 'LOAD_ATTR':
                        assert not el.argval == 'SOCK_DGRAM', 'Запрещено использовать сокеты для UDP'
        type.__init__(self, cls_name, bases, cls_dict)


class ServerVerifier(type):
    def __init__(self, cls_name, bases, cls_dict):
        for key, value in cls_dict.items():
            try:
                instructions = dis.get_instructions(value)
            except TypeError:
                continue
            if instructions:
                for el in instructions:
                    assert not el.argval == 'connect', 'Запрещено вызывать connect для сокетов'

                    if el.opname == 'LOAD_ATTR':
                        assert not el.argval == 'SOCK_DGRAM', 'Запрещено использовать сокеты для UDP'
        type.__init__(self, cls_name, bases, cls_dict)

class PortVerifier:
    def __init__(self):
        self._port = 7777

    def __get__(self, instance, owner):
        return self._port

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Порт должен быть типа int')
        if not value >= 0:
            raise ValueError('Порт должен быть >= 0')
        self._port = value