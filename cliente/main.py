import socket

host = '127.0.0.1'
port = 12345

def connect():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((host,port)) 

    s.send('Listo para recibir el archivo'.encode('ascii'))

    print(s.recv(1024).decode('ascii'))

    #envia numero de archivo que desea descargar
    numero_archivo = 1
    s.send(numero_archivo.to_bytes(1,'big'))

    #recibe archivo
    size_nombre_archivo = int.from_bytes(s.recv(4), 'big')
    nombre_archivo = s.recv(size_nombre_archivo)
    f = open(nombre_archivo, 'wb')
    s.send('Recibido nombre del archivo'.encode('ascii'))
    
    tamano_archivo = int.from_bytes(s.recv(8),'big')
    total = 0 #cantidad de archivo recibido
    s.send(('Recibido tamano del archivo' + str(tamano_archivo)).encode('ascii'))
    
    # recibe segmentos del archivo
    while True:
        # print('Recibiendo')
        if tamano_archivo == total:
            print('Recibido todo el archivo')
            break
        seg = s.recv(1024)
        total += len(seg)
        f.write(seg)
    f.close()

    #espera el hash
    hash_archivo_enviado = s.recv(2014)
    print(hash_archivo_enviado)

    s.close()


if __name__ == '__main__':
    connect()



