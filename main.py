import socket

def get_id():
    #создание файла с данными пользователя, если не существует
    with open('users.txt', 'a+') as users:
        pass
    while True:
        unic = True
        ident =  input('Введите уникальный идентификатор:\n')
        with open('users.txt', 'r+') as users:
            for line in users.readlines():
                if line.split(' - ')[0].split('[')[1] == ident:
                    unic = False
                    break
            if unic:
                return ident
            else:
                print('Данный идентификатор уже существует!\n')

ident = get_id()
sock = socket.socket()
try:
    sock.connect(('localhost', 8000))
except ConnectionRefusedError:
    print('Сначала запустите сервер!')
else:
    try:
        #запись идентификатора в users.txt
        with open('users.txt', 'a+') as users:
            users.write('[' + ident + ' - ')
        #отправление идентификатора на сервер
        sock.send(ident.encode())
        #получение кода с сервера
        passw = sock.recv(1024)
        print('Ваш уникальный код: ' + passw.decode())
        # запись кода в users.txt
        with open('users.txt', 'a+') as users:
            users.write(passw.decode() + ']\n')
        sock.close()
        sock2 = socket.socket()
        sock2.connect(('localhost', 8001))
        message = input('Введите сообщение:\n')
        myid = input('Введите свой идентификатор:\n')
        code = input('Введите свой код:\n')
        text = '\n'.join([message, myid, code])
        #отправка информации на сервер
        sock2.sendall(text.encode())
        #сообщение об ошибке
        data2 = sock2.recv(1024)
        print(data2.decode())
        sock2.close()
    except ConnectionRefusedError:
        print('Сервер был отключен!')