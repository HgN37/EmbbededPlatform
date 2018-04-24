<<<<<<< HEAD
from mqtt import MQTT
import socket
import ast
import os
import threading
import datetime
import time

server = socket.socket()
user = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
user.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 33333))
user.bind(('', 55555))
server.listen(5)
user.listen(5)

class threadSystem(threading.Thread):
	systemList = []
	def __init__(self, raspid):
		threading.Thread.__init__(self)
		print('Init new thread')
		self.raspid = raspid
		self.devlistdir = './RASP/' + self.raspid + '/' + 'DEVLIST' + '.txt'
		self.devlist = {'FILE':'DEVLIST', 'RASPID':str(self.raspid)}
		self.rulelistdir = './RASP/' + self.raspid + '/' + 'RULELIST' + '.txt'
		self.rulelist = {'FILE':'RULELIST', 'RASPID':str(self.raspid)}
		self.devdatadir = './RASP/' + self.raspid + '/' + 'DEVDATA' + '.txt'
		self.devdata = {'FILE':'DEVDATA', 'RASPID':str(self.raspid)}
		threadSystem.systemList.append(self.raspid)
		tpin = self.raspid + '/s2m'
		tpout = self.raspid + '/m2s'
		self.mqtt = MQTT('iot.eclipse.org', 1883, tpin, tpout)
		print('Init Done')
	def run(self):
		print('Thread start')
		start_time = datetime.datetime.now()
		while True:
			#print('Calculate time out')
			delta = (datetime.datetime.now() - start_time).seconds
			if delta > 10:
				print('System {} disconnected'.format(self.raspid))
				threadSystem.systemList.remove(self.raspid)
				return
			#print('Connecting to MQTT Broker')
			self.mqtt.run()
			msg = ''
			msg = self.mqtt.get()
			if msg != '':
				start_time = datetime.datetime.now()
				cmd = ast.literal_eval(msg)
				if cmd['FUNC'] == 'UPDATE' and cmd['DEV1'] != '0':
					if cmd['DEV1'] in self.devdata:
						if len(self.devdata[cmd['DEV1']]) > 100:
							del self.devdata[cmd['DEV1']][0]
						new_data = (str(datetime.datetime.now()), cmd['DATA']['1'])
						self.devdata[cmd['DEV1']].append(new_data)
					else:
						self.devdata[cmd['DEV1']] = []
						new_data = (str(datetime.datetime.now()), cmd['DATA']['1'])
						self.devdata[cmd['DEV1']].append(new_data)
					f = open(self.devdatadir, 'w')
					f.write(str(self.devdata))
					f.close()

def raspHandler(data):
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
	if raspid not in threadSystem.systemList:
		print('Create new thread')
		newThread = threadSystem(raspid)
		newThread.start()
	else:
		print(threadSystem.systemList)
		print(raspid)
		print('Already')

def userHandler(user_client):
	print('Start thread user')
	sign_in = False;
	while True:
		msg = user_client.recv(1024).decode('utf-8')
		if msg != '':
			jsondata = ast.literal_eval(msg)
			username = jsondata['USER']
			password = jsondata['PASS']
			func = jsondata['FUNC']
			data = jsondata['DATA']
			res = jsondata.copy()
			if sign_in is False:
				try:
					print('Opening user database')
					f = open('./USER/' + username + '.txt', 'r')
					user_database = f.read()
					f.close()
					print(user_database)
					user_database = ast.literal_eval(user_database)
					print('Check func')
					if func != 'SIGNIN':
						raise ValueError
					print('Check password')
					if password != user_database['Password']:
						raise ValueError
					print('Done')
					sign_in = True
					res['DATA'] = 'OK'
					user_client.send(str(res).encode('utf-8'))
				except:
					res['DATA'] = 'FAIL'
					user_client.send(str(res).encode('utf-8'))
					#user_client.close()
			if sign_in is True:
				if func == 'ADDSYS':
					print('GET ADDSYS FUNC')
					user_database['SystemList'].append(data)
					res['DATA'] = data
					user_client.send(str(res).encode('utf-8'))
				elif func == 'DELSYS':
					print('GET DELSYS FUNC')
					for system in user_database['SystemList']:
						if data == system['NAME']:
							data2res = system
							user_database['SystemList'].remove(system)
							break
					res['DATA'] = data2res
					user_client.send(str(res).encode('utf-8'))
				elif func == 'LISTSYS':
					print('GET LISTSYS FUNC')
					res['DATA'] = user_database['SystemList']
					user_client.send(str(res).encode('utf-8'))
				elif func == 'READ':
					print('GET READ FUNC')
					system_name = jsondata['DATA']
					system = ''
					for sys in user_database['SystemList']:
						if sys['NAME'] == system_name:
							system = sys['ID']
					f = open('./RASP/' + system + '/DEVLIST.txt')
					file_data = f.read()
					f.close()
					res['DATA'] = ast.literal_eval(file_data)
					user_client.send(str(res).encode('utf-8'))
					time.sleep(0.1)
					f = open('./RASP/' + system + '/DEVDATA.txt')
					file_data = f.read()
					f.close()
					res['DATA'] = ast.literal_eval(file_data)
					user_client.send(str(res).encode('utf-8'))
					time.sleep(0.1)
					f = open('./RASP/' + system + '/RULELIST.txt')
					file_data = f.read()
					f.close()
					res['DATA'] = ast.literal_eval(file_data)
					user_client.send(str(res).encode('utf-8'))
					time.sleep(0.1)
				elif func == 'WRITE':
					system = jsondata['DATA']['ADDR']
					tpin = system + '/s2m'
					tpin = system + '/m2s'		

				f = open('./USER/' + username + '.txt', 'w')
				f.write(str(user_database))
				f.close()

def serverRasp():
    while True:
        client1, addr1 = server.accept()
        print('RASP Connect from addr {}: {}'.format(addr1[0],addr1[1]))
        data = client1.recv(1024).decode('utf-8')
        raspHandler(data)

def serverUser():
    while True:
        client2, addr2 = user.accept()
        print('USER Connect from addr {}: {}'.format(addr2[0],addr2[1]))
        new_thread = threading.Thread(target=userHandler,args=(client2,))
        new_thread.start()
threadRasp = threading.Thread(target=serverRasp)
threadUser = threading.Thread(target=serverUser)
threadRasp.start()
threadUser.start()
=======

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
>>>>>>> 58c0732ccba179373605a6ae3085b5bd6a8fcfbd
