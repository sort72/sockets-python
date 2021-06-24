from socket import socket
import json
import os
    
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
                print('Usuario no encontrado')
            elif code == '402':
                print('El usuario ingresado ya se encuentra conectado')
            else:
                userid = res.get('userid')
                name = userName
            print( "------------------------------------------------")

        if not userid:
            userName = input("| Por favor ingrese el nombre del usuario : ")
            data = json.dumps({"step": 1, "username": userName})
            s.send( data.encode("UTF-8") )
            response = s.recv(1024)

    user_files = os.listdir(f'files/client_{userid}/')
    data = json.dumps({"step": 2, "files": user_files, "username": name})
    s.send( data.encode("UTF-8") )
    print(json.loads(s.recv(1024).decode('UTF-8')).get('response'))

    while True:
        option = int(input('¿Qué desea hacer a continuación?\n1. Listar archivos\n2. Leer archivo\n3. Borrar archivo\n4. Cerrar sesión\n\nSeleccione: '))

        if option == 1:
            data = json.dumps({"step": 2 + option})
            s.send( data.encode("UTF-8") )
            response = s.recv(1024)
            response = json.loads(response.decode('UTF-8'))
            response = response.get('response')
            print('Archivos disponibles:')
            for user, files in response.items():
                print(f"\tArchivos de {user}: ")
                for file in files:
                    print(f"\t\t{file}")
                print("")                    

        elif option == 2:
            filename = input('Ingrese el nombre del propietario del archivo que desea leer, seguido del nombre del archivo. Ejemplo: rosa/hola.txt\n')
            data = json.dumps({"step": 2 + option, "filename": filename})
            s.send( data.encode("UTF-8") )
            response = s.recv(1024)
            response = json.loads(response.decode('UTF-8'))
            file_content = response.get('response')
            if file_content == -1:
                print(f"El archivo {filename} no existe")
            else:
                print(f"El archivo {filename} contiene lo siguiente:")
                print(file_content)

        elif option == 3:
            filename = input('Ingrese el nombre del propietario del archivo que desea borrar, seguido del nombre del archivo. Ejemplo: rosa/hola.txt\n')
            data = json.dumps({"step": 2 + option, "filename": filename})
            s.send( data.encode("UTF-8") )
            response = s.recv(1024)
            response = json.loads(response.decode('UTF-8'))
            file_content = response.get('response')
            if file_content == -1:
                print(f"El archivo {filename} no existe o no pudo ser borrado")
            else:
                print(f"El archivo {filename} ha sido borrado")

        elif option == 4:
            data = json.dumps({"step": 2 + option, "username": name})
            s.send( data.encode("UTF-8") )
            s.close()
            break

if __name__ == "__main__":
    main()