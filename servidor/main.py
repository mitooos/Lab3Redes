import socket
from _thread import *
import threading

port = 12345

conexiones_esperadas = 1

host = ''

print_lock = threading.Lock()

esperando = True

arch1 = 'arch1.txt'

arch2 = 'arch2.txt'

#funcion que corre en paralelo para interactuar con los clientes
def thread(conn, i):
    ehlo = conn.recv(1024).decode('ascii')
    print('El cliente', i, 'se conecto')
    print(ehlo)

    conn.send('Que archivo desea?'.encode('ascii'))

    numero_archivo = int(conn.recv(1024).decode('ascii'))

    #espera a que todos los clientes esten listos para enviar el archivo
    while True:
        if esperando:
            print('Esperando el numero de clientes')
            continue
        else:
            break

    if numero_archivo == 1:
        conn.send(arch1.encode('ascii'))
        f = open(arch1, 'rb')

    if numero_archivo == 2:
        conn.send(arch1.encode('ascii'))
        f = open(arch2, 'rb')
    
    #envia sefmentos del archivo
    seg = f.read(1024)
    while seg:
        conn.send(seg)
        seg = f.read(1024)
    f.close()

    print('Se envio el archivo al cliente: ', i)

    conn.close()


def receive_connections():
    conexiones = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print('Socket esta escuchando en el puerto: ' + str(port))

    while True:
        c, addr = s.accept()
        conexiones += 1
        print('Conectado con el cliente en: ', addr[0], ':', addr[1])
        start_new_thread(thread, (c,conexiones))
        global esperando
        esperando =  conexiones < conexiones_esperadas
    s.close()


if __name__ == '__main__':
    receive_connections()

