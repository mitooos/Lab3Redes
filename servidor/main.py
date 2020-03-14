import socket
from _thread import *
import threading
import hashlib
import os
import time

buff_size = 1024

port = 8080

conexiones_esperadas = 1

host = '0.0.0.0'

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

    numero_archivo = int.from_bytes(conn.recv(1),'big')

    #espera a que todos los clientes esten listos para enviar el archivo
    while True:
        if esperando:
            print('Esperando el numero de clientes')
        else:
            break

    tiempo_inicio=time.time()


    if numero_archivo == 1:
        conn.send(len(arch1).to_bytes(4,'big'))
        conn.send(arch1.encode('ascii')) #envia nombre del archivo
        conn.send(os.path.getsize(arch1).to_bytes(8,'big')) # envia tamaño del archivo
        f = open(arch1, 'rb')

    if numero_archivo == 2:
        conn.send(len(arch2).to_bytes(4,'big'))
        conn.send(arch1.encode('ascii')) #envia nombre del archivo
        conn.send(os.path.getsize(arch2).to_bytes(8,'big')) # envia tamaño del archivo
        f = open(arch2, 'rb')
    
    conn.recv(1024)

    # objeto hash
    h = hashlib.sha1()

    #envia segmentos del archivo
    seg = f.read(buff_size)
    while seg:
        conn.send(seg)
        h.update(seg) #actualiza el hash
        seg = f.read(buff_size)
    f.close()

    print('Se envio el archivo al cliente: ', i)

    hash_archivo = h.hexdigest()
    conn.send(hash_archivo.encode('ascii'))
    print('se envio el hash del archivo al cliente: ', i)
    print(hash_archivo)

    tiempo_final = round(time.time() - tiempo_inicio,5)
    print("El tiempo transcurrido fue: "+ str(tiempo_final)+" segundos")
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

        #avisa que ya hay la cantidad de clientes necesarios para enviar el archivo
        global esperando
        esperando =  conexiones < conexiones_esperadas
        
    s.close()


if __name__ == '__main__':
    receive_connections()

