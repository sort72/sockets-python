from threading import Thread
import json
from os import path
from os import remove
import os
from settings import bcolors

users = {
    'albeiro' : [1,0],
    'rosa' : [2,0],
    'antonio' : [3,0],
    'pierre' : [4,0],
    'Tom' : [5,0],
    'niels' : [6,0]
}

files = {}

class Client(Thread):
    
    def __init__(self, conn, addr):
        # Inicializar clase padre.
        Thread.__init__(self)
        
        self.conn = conn
        self.addr = addr

    
    def run(self):
        while True:
            data = self.conn.recv(1024)
            try:
                data = json.loads(data.decode('UTF-8'))
                step = data.get('step')

                if step == 1:
                    username = data.get('username')
                    if username not in users:
                        response = json.dumps({"step": 1, "response": '403'})
                    else:
                        if users[username][1] == 0:
                            users[username][1] = 1
                            response = json.dumps({"step": 1, "response": '200', 'userid': users[username][0]})
                            print(f"{bcolors.OKBLUE}%s:%d se ha conectado con nombre {bcolors.ENDC}"% self.addr, end=f"{bcolors.OKGREEN}{username}{bcolors.ENDC}\n")
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
                    user_id = users[input_data[0]][0]
                    file_path = f"files/client_{user_id}/{input_data[1]}"
                    if path.exists(file_path) == True:
                        res = open(file_path, 'r+', encoding='UTF-8')
                    else:
                        res = -1
                    size = os.path.getsize (file_path)
                    if(int(size)>1000):
                        text = []
                        complete_text = []
                        lines = res.readlines()
                        count = 0
                        for line in lines: 
                            if((count != 0) and (count%16==0)):
                                complete_text.append(text)
                                text = []
                                text.append(line)
                            else:
                                text.append(line)
                            count+=1
                        res = complete_text[0]
                    else:
                        res = res.read()
                    
                    response = json.dumps({"step": 4, "response": res})

                elif step == 5:
                    input_data = data.get('filename')
                    input_data = input_data.split('/')
                    user_id = users[input_data[0]][0]
                    file_path = f"files/client_{user_id}/{input_data[1]}"
                    if path.exists(file_path) == True:
                        try:
                            res = remove(file_path)
                            files[input_data[0]].remove(input_data[1])
                        except:
                            res = -1
                    else:
                        res = -1

                    response = json.dumps({"step": 5, "response": res})
                elif step == 6:
                    username = data.get('username')
                    users[username][1] = 0
                    del files[username]
                    print(f"{bcolors.FAIL}{username} se ha desconectado{bcolors.ENDC}")
                    self.join()

                self.conn.send( response.encode( "UTF-8" ) )
            
            except:
                return False

