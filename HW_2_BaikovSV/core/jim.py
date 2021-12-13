import json


def pack(dict_msg): # упаковка в формат
    """
    Создание сообщения, пригодного для отправки через TCP
    :param dict_msg: dict
    :return: str
    """
    str_msg = json.dumps(dict_msg)
    return str_msg.encode('utf-8')


def unpack(bt_str): # распаковка из формата
    """
    Распаквка полученного сообщения
    :param bt_str: str
    :return: dict
    """
    str_decoded = bt_str.decode('utf-8')
    return json.loads(str_decoded)