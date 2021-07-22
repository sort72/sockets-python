from threading import Thread
from socket import socket
import json
from os import path
from os import remove
import os
from settings import bcolors

users = {
    'albeiro' : [1,0,6031],
    'rosa' : [2,0,6032],
    'antonio' : [3,0,6033],
    'pierre' : [4,0,6034],
    'Tom' : [5,0,6035],
    'niels' : [6,0,6036]
}

files = {}


class Client(Thread):
    
    def __init__(self, conn, addr,s):
        # Inicializar clase padre.
        Thread.__init__(self)
        
        self.conn = conn
        self.addr = addr
        self.s = s

    
    def run(self):
        while True:
            data = self.conn.recv(1024)
            try:
                data = json.loads(data.decode('UTF-8'))
                step = data.get('step')

                if step == 1:
                    username = data.get('username')
                    userid = data.get('id')
                    if username not in users:
                        response = json.dumps({"step": 1, "response": '403'})
                    else:
                        if users[username][1] == 0:
                            if str(users[username][0]) in userid:
                                users[username][1] = 1
                                response = json.dumps({"step": 1, "response": '200', 'userid': users[username][0]})
                                print(f"{bcolors.OKBLUE}%s:%d se ha conectado con nombre {bcolors.ENDC}"% self.addr, end=f"{bcolors.OKGREEN}{username}{bcolors.ENDC}\n")
                            else:
                                response = json.dumps({"step": 1, "response": '404'})
                        else:
                            response = json.dumps({"step": 1, "response": '402'})

                elif step == 2:
                    username = data.get('username')
                    files[username] = data.get('files')
                    response = json.dumps({"step": 2, "response": 'Archivos recibidos con éxito.'})

                elif step == 3:
                    response = json.dumps({"step": 3, "response": files})

                elif step == 4:
                    input_data = data.get('filename')
                    input_data = input_data.split('/')
                    user_ip = users[input_data[0]][2]
                    sClient = socket()
                    sClient.connect(('localhost', user_ip))
                    data = json.dumps({"step": 1, "fileName":input_data[1]})
                    sClient.send( data.encode("UTF-8") )
                    responseC = sClient.recv(1024)
                    responseC = json.loads(responseC.decode('UTF-8'))
                    responseC = responseC.get('response')
                    response = json.dumps({"step": 4, "response": responseC})

                elif step == 5:
                    input_data = data.get('filename')
                    input_data = input_data.split('/')
                    user_ip = users[input_data[0]][2]
                    sClient = socket()
                    sClient.connect(('localhost', user_ip));
                    data = json.dumps({"step": 2, "fileName":input_data[1]})
                    sClient.send( data.encode("UTF-8") )
                    responseC = sClient.recv(1024)
                    responseC = json.loads(responseC.decode('UTF-8'))
                    responseC = responseC.get('response')

                    if(responseC == -1):
                        response = json.dumps({"step": 5, "response": -1})
                    else:
                        files[input_data[0]].remove(input_data[1])
                        response = json.dumps({"step": 5, "response": responseC})

                elif step == 6:
                    username = data.get('username')
                    users[username][1] = 0
                    user_ip = users[username][2]
                    del files[username]
                    print(f"{bcolors.FAIL}{username} se ha desconectado{bcolors.ENDC}")
                    self.join()
                    break

                self.conn.send( response.encode( "UTF-8" ) )
            
            except:
                return False




def main():
    s = socket()
    
    # Escuchar peticiones en el puerto 6030.
    s.bind(("localhost", 6030))
    s.listen(0)
    
    while True:
        conn, addr = s.accept()
        client = Client(conn, addr,s)
        client.start()
        print(f"{bcolors.OKBLUE}%s:%d se ha conectado.{bcolors.ENDC}"% addr)

if __name__ == "__main__":
    main()
