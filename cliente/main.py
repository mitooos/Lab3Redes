import socket

host = '127.0.0.1'
port = 12345

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port)) 

    s.send('ehlo'.encode('ascii'))

    print(s.recv(1024).decode('ascii'))

    #envia numero de archivo que desea descargar
    numero_archivo = 1
    s.send(str(numero_archivo).encode('ascii'))

    #recibe archivo
    nombre_archivo = s.recv(1024).decode('ascii')
    f = open(nombre_archivo, 'wb')
    
    # recibe segmentos del archivo
    while True:
        # print('Recibiendo')
        seg = s.recv(2014)
        print(seg)
        if seg == b'':
            print('Recibido todo el archivo')
            break
        f.write(seg)
    f.close()

    s.close()


if __name__ == '__main__':
    connect()



