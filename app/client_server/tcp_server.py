import socket
import math
import os
import random

def create_data(type_of_data):
    '''
    Возвращает массив байтов с данными
    '''
    if type_of_data == 'afc':
        d="app\client_server\data_for_server\GL"
        l=os.listdir(path=d)
        rand = random.randint(0, l.__len__())
        t=l[rand]
        f = open(d+'/'+t, 'r')
        fr=f.read()
        # f.close()
        return bytes(fr,'utf-8')
    if type_of_data == 'gd':
        d="app\client_server\data_for_server\GD"
        l=os.listdir(path=d)
        rand = random.randint(0, l.__len__())
        t=l[rand]
        f = open(d+'/'+t, 'r')
        fr=f.read()
        f.close()
        return bytes(fr,'utf-8')
    if type_of_data == 'amam':
        d="app\client_server\data_for_server\GT"
        l=os.listdir(path=d)
        rand = random.randint(0, l.__len__())
        t=l[rand]
        f = open(d+'/'+t, 'r')
        fr=f.read()
        f.close()
        return bytes(fr,'utf-8')
    if type_of_data == 'pos':
        d="app\client_server\data_for_server\SP"
        l=os.listdir(path=d)
        rand = random.randint(0, l.__len__())
        t=l[rand]
        f = open(d+'/'+t, 'r')
        fr=f.read()
        f.close()
        return bytes(fr,'utf-8')


while True:
        sock = socket.socket()
        port = 33333
        isOk = False
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # эта строчка должна решить вопрос с незакрытием порта после окончания работы программы
        #ниже просто проверяем свободный порт, если занят, ищем следующий но с учетом ^^^ должно рабатать и так
        while not isOk:
            try:
                s = sock.bind(('127.0.0.1', port))
                isOk = True
                print('port number is: ', port)
            except OSError as err:
                print(err)
                port+=1

        sock.listen(10)
        conn, addr = sock.accept()
        print(addr)

        while True:
            data = conn.recv(1024)
            udata = data.decode("utf-8")
            print(udata)
            if data == b'\xff\xf4\xff\xfd\x06':  #эту строку получает data после закрытия соединения со стороны клиента
                print('Connection closed from client')
                conn.close()
                break
            if 'afc' in udata:
                conn.send(create_data('afc'))
            if 'gd' in udata:
                conn.send(create_data('gd'))
            if 'amam' in udata:
                conn.send(create_data('amam'))
            if 'pos' in udata:
                conn.send(create_data('pos'))
            if '@stop' in udata:
                conn.close()
                break
            else:
                conn.close()
                break
