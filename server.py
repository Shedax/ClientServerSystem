import socket
import datetime
import threading
import random
import string

#создаём лог если он не существует
with open('log.txt', 'a+'):
    pass

#обработчик новых клиентов
def new_client(client_sock):

    #генерация уникального восьмизначного кода для клиента
    def generate_passw():
        uniq = True
        letters = string.ascii_lowercase
        passw = ''.join(random.choice(letters) for i in range(8))
        with open('users.txt', 'r+') as users:
            for line in users.readlines():
                #проверка кода на уникальность
                if line.split(' - ')[1].split(']')[0] == passw:
                    uniq = False
                    break
            if uniq:
                return passw
            else:
                generate_passw()

    def new_client_2(client_sock2):
        while True:
            #информация о сообщении, идентификаторе и коде
            data2 = client_sock2.recv(1024)
            if not data2:
                break
            with open('users.txt', 'r+') as users:
                line = '[' + data2.decode().split('\n')[1] + ' - ' + data2.decode().split('\n')[2] + ']'
                lines2 = list()
                #получаем список строк в users.txt без \n
                for l in users.readlines():
                    lines2.append(l[:len(l) - 1])
                if line not in lines2:
                    client_sock2.send('Ошибка!'.encode())
                else:
                    #запись информации в лог(время, id клиента и сообщение)
                    with open('log.txt', 'a+') as log:
                        now = datetime.datetime.now()
                        current_time = str(now.strftime("%d-%m-%Y %H:%M:%S"))
                        log.write(
                            current_time + ' ' + data2.decode().split('\n')[1] + ' - ' + '"' +
                            data2.decode().split('\n')[
                                0] + '"' + '\n')
    while True:
        #получение идентификатора пользователя
        data = client_sock.recv(1024)
        if not data:
            break
        # отправка кода пользователю
        client_sock.send(generate_passw().encode())
    client_sock.close()
    sock2 = socket.socket()
    sock2.bind(('localhost', 8001))
    sock2.listen(50)
    while True:
        client_sock2, addr2 = sock2.accept()
        threading.Thread(target=new_client_2, args=(client_sock2,), daemon=True).start()
sock = socket.socket()
sock.bind(('', 8000))
sock.listen(50)
while True:
    client_sock, client_addr = sock.accept()
    threading.Thread(target=new_client, args=(client_sock,), daemon=True).start()
