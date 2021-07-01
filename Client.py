from socket import socket
from settings import bcolors
import json
import os
from os import system
    
def main():
    s = socket()
    s.connect(("localhost", 6030))
    userid = 0
    name = ''
    response = ''
    option = 0
    
    while userid < 1:
        if response != '':
            res = json.loads(response.decode('UTF-8'))
            code = res.get('response')
            if code == '403':
                print(f"{bcolors.WARNING}Usuario no encontrado.{bcolors.ENDC}")
            elif code == '402':
                print(f"{bcolors.PURPLE}El usuario ingresado ya se encuentra conectado.{bcolors.ENDC}")
            else:
                userid = res.get('userid')
                name = userName
            print( f"{bcolors.CYAN}------------------------------------------------{bcolors.ENDC}")

        if not userid:
            userName = input(f"| {bcolors.darkgrey} Por favor ingrese el nombre del usuario : {bcolors.ENDC}")
            data = json.dumps({"step": 1, "username": userName})
            s.send( data.encode("UTF-8") )
            response = s.recv(1024)

    user_files = os.listdir(f'files/client_{userid}/')
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
                    if(type(file_content) == 'str'):
                        print(f"{bcolors.HEADER}El archivo {filename} contiene lo siguiente:{bcolors.ENDC}")
                        print(f"{bcolors.lightgrey}{file_content}{bcolors.ENDC}")
                        print('')
                    else:
                        print(f"{bcolors.PURPLE}Debido a que el archivo es demasiado grande te mostraremos un fragmento:{bcolors.ENDC}")
                        for line in file_content:
                            print(f"{bcolors.lightgrey}{line}{bcolors.ENDC}", end=" ")

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

if __name__ == "__main__":
    main()