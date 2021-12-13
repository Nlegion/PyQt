from subprocess import Popen, check_call, PIPE, TimeoutExpired
import os
import psutil
from threading import Thread


def is_running(script):
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            if len(q.cmdline()) > 1 and script in q.cmdline()[1] and q.pid != os.getpid():
                print(f'{script} процесс уже запущен')
                return True

    return False


def output(pop):
    while pop.poll() is None:
        print(pop.stdout.readline().decode())


def thread_for_app(app):
    Thread(target=output(app), daemon=True).start()


def main():
    try:
        quantity_of_clients_app = int(input("как много чатов надо запустить?: "))
    except ValueError:
        print('неправильное количество')
    if not is_running("server.py"):
        print('Процесс не найден')
        serv = Popen('python3 server.py', shell=True, stdout=PIPE, stderr=PIPE)
    for app in range(1, quantity_of_clients_app + 1):
        if app % 2 == 0:
            cl2 = Popen('python3 client.py', shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
            try:
                cl2.communicate(input=f'Name-{app}\n2\n{app - 1}\nHallo Name-{app}!\n'.encode(), timeout=10)
            except TimeoutExpired:
                cl2.kill()
                cl1.kill()
        else:
            cl1 = Popen('python3 client.py', shell=True, stdout=PIPE, stdin=PIPE, stderr=PIPE)
            try:
                cl1.communicate(input=f'Name-{app}\n'.encode(), timeout=1)
            except TimeoutExpired:
                pass
    serv.kill()


if __name__ == "__main__":
    try:
        check_call(["pkill", "-9", "-f", "server.py"])
        check_call(["pkill", "-9", "-f", "client.py"])
    except:
        print('Запуск основной программы')
    finally:
        main()
