from socket import socket
from ClientClass import Client
from settings import bcolors

def main():
    s = socket()
    
    # Escuchar peticiones en el puerto 6030.
    s.bind(("localhost", 6030))
    s.listen(0)
    
    while True:
        conn, addr = s.accept()
        client = Client(conn, addr)
        client.start()
        print(f"{bcolors.OKBLUE}%s:%d se ha conectado.{bcolors.ENDC}"% addr)

if __name__ == "__main__":
    main()