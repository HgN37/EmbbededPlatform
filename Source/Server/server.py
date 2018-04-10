
import socket
import ast
import os

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 33333))
server.listen(5)

def raspHandler(data):
   # try:
        jsondata = ast.literal_eval(data)
       # print(jsondata)
        raspid = jsondata['RASPID']
        filename = jsondata['FILE']
        if not os.path.isdir('./RASP/' + raspid):
            os.makedirs('./RASP/' + raspid)
       # print('Done mkdir')
        if not os.path.exists('./RASP/' + raspid + '/' + filename + '.txt'):
            f = open('./RASP/' + raspid + '/' + filename + '.txt', 'w')
            f.close()
        f = open('./RASP/' + raspid + '/' + filename + '.txt', 'r')
        current_data = f.read()
        f.close()
        if data != current_data:
            f = open('./RASP/' + raspid + '/' + filename + '.txt', 'w')
            f.write(data)
            f.close()
  #  except:
  #      print('ERROR')
        return

while True:
    client, addr = server.accept()
    print('Connect from addr {}: {}'.format(addr[0],addr[1]))
    data = client.recv(1024).decode('utf-8')
    raspHandler(data)
