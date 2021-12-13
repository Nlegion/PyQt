import subprocess
import ipaddress
import tabulate

net = ['8.8.8.8', 'ya.ru', 'localhost', 'local']  # базовые адреса Задание 1
PING_COUNT = 1
net.insert(0, ipaddress.ip_address('192.168.0.1'))  # доп адрес Задание 1
base_ip = '192.168.0.'  # базовый адрес Задание 2
count_of_adr = 5  # количество для генератора адресов Задание 2
result = {'Reachable': [],
          'Unreachable': []}


def host_ping(address):  # задача 1
    for addr in address:
        res = subprocess.call(f'ping -c {PING_COUNT} {addr}', shell=True, stdout=open("/dev/null"),
                              stderr=open("/dev/null"))
        if res == 0:
            print(f'Узел {addr} доступен')
        else:
            print(f'Узел {addr} недоступен')


def gen_ip(base_adr, count):  # задача 2
    add_adr = [item for item in range(count)]
    new_adr = []
    for adr in add_adr:
        new_adr.append(f'{base_adr + str(adr)}')
    return new_adr


def ping(addr):  # прозвон ip для 3 задачи
    res = subprocess.call(f'ping -c {PING_COUNT} {addr}', shell=True, stdout=open("/dev/null"),
                          stderr=open("/dev/null"))
    if res == 0:
        result.get("Reachable").append(addr)
    else:
        result.get("Unreachable").append(addr)


def host_range_ping_tab(a, b):  # тело для 3 задачи
    gen_adr = gen_ip(base_ip, count_of_adr)
    a = a - 1
    try:
        if a >= b:
            while not a < b:
                ping(gen_adr[a])
                a -= 1
        elif a < b:
            while not a > b:
                ping(gen_adr[a])
                a += 1
        print(tabulate.tabulate(result, headers='keys', tablefmt="grid"))
    except:
        print('Неверно задан диапазон')


host_ping(net)
host_ping(gen_ip(base_ip, count_of_adr))
host_range_ping_tab(count_of_adr, 0)
