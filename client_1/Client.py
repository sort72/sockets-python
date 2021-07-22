from socket import socket
from settings import bcolors
from threading import Thread
import json
import sys
from os import path
from os import remove
import os 
from os import system
import threading

class Server(Thread):
    
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
                    fileName = data.get('fileName')
                    file_path = f'files/{fileName}'
                    if path.exists(file_path) == True:
                        res = open(file_path, 'r+', encoding='UTF-8')
                    else:
                        res = -1

                    completeText = []
                    endOfFile = True
                    while endOfFile:
                        archivo = res.read(900)
                        if not archivo:
                            endOfFile = False
                        else:
                            completeText.append(archivo)

                    response = json.dumps({"step": 4, "response": completeText[0]})

                elif step == 2:
                    fileName = data.get('fileName')
                    file_path = f"files/{fileName}"
                    if path.exists(file_path) == True:
                        try:
                            res = remove(file_path)
                        except:
                            res = -1
                    else:
                        res = -1

                    response = json.dumps({"step": 5, "response": res})

                elif step == 3:
                    print(f"{bcolors.FAIL}El servidor se ha desconectado{bcolors.ENDC}")
                    self.join()
                    break

                self.conn.send( response.encode( "UTF-8" ) )
            except:
                return False

def Cliente():
    s = socket()
    s.connect(("localhost", 6030))

    userid = 0
    name = ''
    response = ''
    option = 0
    boolean = True
    
    while userid < 1:
        if response != '':
            res = json.loads(response.decode('UTF-8'))
            code = res.get('response')

            if code == '404':
                print(f"{bcolors.PURPLE}Usuario incorrecto.{bcolors.ENDC}")
            elif code == '403':
                print(f"{bcolors.WARNING}Usuario no encontrado.{bcolors.ENDC}")
            elif code == '402':
                print(f"{bcolors.PURPLE}El usuario ingresado ya se encuentra conectado.{bcolors.ENDC}")
            elif code == '404':
                print(f"{bcolors.PURPLE}Usuario incorrecto.{bcolors.ENDC}")
            else:
                userid = res.get('userid')
                name = userName
            print( f"{bcolors.CYAN}------------------------------------------------{bcolors.ENDC}")

        if not userid:
            currentRoute= os.getcwd()
            id = str(currentRoute.split('\\')[-1])
            userName = input(f"| {bcolors.darkgrey} Por favor ingrese el nombre del usuario : {bcolors.ENDC}")
            data = json.dumps({"step": 1, "username": userName, "id": id})
            s.send( data.encode("UTF-8") )
            response = s.recv(1024)
    
    user_files = os.listdir(f'files/')
    data = json.dumps({"step": 2, "files": user_files, "username": name})
    s.send( data.encode("UTF-8") )
    print(json.loads(s.recv(1024).decode('UTF-8')).get('response'))

    while True:

        option = input(f'{bcolors.darkgrey}¿Qué desea hacer a continuación?\n1. Listar archivos\n2. Leer archivo\n3. Borrar archivo\n4. Cerrar sesión\n\nSeleccione: {bcolors.ENDC}')

        if(option.isdigit()):
            option = int(option)
            if option == 1:
                system("cls")
                data = json.dumps({"step": 2 + option})
                s.send( data.encode("UTF-8") )
                response = s.recv(1024)
                response = json.loads(response.decode('UTF-8'))
                response = response.get('response')
                print(f'{bcolors.WARNING}Archivos disponibles:{bcolors.ENDC}')
                for user, files in response.items():
                    print(f"\tArchivos de {bcolors.OKBLUE}{user}{bcolors.ENDC}: ")
                    if(files):
                        for file in files:
                            print(f"{bcolors.OKGREEN}\t\t{file}{bcolors.ENDC}")
                    else: 
                        print(f"{bcolors.FAIL}\t\t El usuario no tiene archivos.{bcolors.ENDC}")
                    print("")                    

            elif option == 2:
                system("cls")
                filename = input(f'{bcolors.darkgrey}Ingrese el nombre del propietario del archivo que desea leer, seguido del nombre del archivo. Ejemplo:{bcolors.ENDC} {bcolors.CYAN}rosa/hola.txt {bcolors.ENDC}\n')
                data = json.dumps({"step": 2 + option, "filename": filename})
                s.send( data.encode("UTF-8") )
                response = s.recv(1024)
                response = json.loads(response.decode('UTF-8'))
                file_content = response.get('response')
                if file_content == -1:
                    print(f"{bcolors.FAIL}El archivo {filename} no existe{bcolors.ENDC}")
                else:
                    print(f"{bcolors.HEADER}El archivo {filename} contiene lo siguiente:{bcolors.ENDC}")
                    print(f"{bcolors.lightgrey}{file_content}{bcolors.ENDC}")
                    print('')

            elif option == 3:
                system("cls")
                filename = input(f'{bcolors.darkgrey}Ingrese el nombre del propietario del archivo que desea borrar, seguido del nombre del archivo. Ejemplo:{bcolors.ENDC} {bcolors.CYAN}rosa/hola.txt {bcolors.ENDC}\n')
                data = json.dumps({"step": 2 + option, "filename": filename})
                s.send( data.encode("UTF-8") )
                response = s.recv(1024)
                response = json.loads(response.decode('UTF-8'))
                file_content = response.get('response')
                if file_content == -1:
                    print(f"{bcolors.FAIL}El archivo {filename} no existe o no pudo ser borrado{bcolors.ENDC}")
                else:
                    print(f"{bcolors.OKGREEN}El archivo {filename} ha sido borrado{bcolors.ENDC}")

            elif option == 4:
                system("cls")
                data = json.dumps({"step": 2 + option, "username": name})
                s.send( data.encode("UTF-8") )
                s.close()
                break

            elif(option<1 or option>4):
                system("cls")
                print(f"{bcolors.FAIL}Opción inválida.{bcolors.ENDC}")
        else:
            system("cls")
            print(f"{bcolors.FAIL}Opción inválida.{bcolors.ENDC}")

def Servidor():
    s = socket()
    
    # Escuchar peticiones en el puerto 6031.
    s.bind(("localhost", 6031))
    s.listen(0)
    while True:
        conn, addr = s.accept()
        client = Server(conn, addr,s)
        client.start()

thread1 = threading.Thread(target=Cliente)
thread2 = threading.Thread(target=Servidor)
thread1.start()
thread2.start()
thread1.join()
thread2.join()