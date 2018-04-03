from rs485 import Modbus
from mqtt import MQTT
import rasp_info
import time
import sys
import ast
import threading

random = 1
addr = 1
devdata = {}

tpin = rasp_info.rasp_get_id() + '/m2s'
tpout = rasp_info.rasp_get_id() + '/s2m'
modbus = Modbus('/dev/ttyUSB0')
mqtt = MQTT('iot.eclipse.org', 1883, tpin, tpout)

def deviceManager():
	global random
	global addr
	global devdata
	for rand in range(256):
		modbus.send_frame(0x00, 0x00, 0x30, 0x02, rand, addr)
		time.sleep(0.001)
		frame = modbus.get_frame(2)
		if frame == 'ERROR':
			pass
		else:
			#print(frame)
			devdata[str(addr)] = {'HARDWARE':0,'VERSION':0}
			devdata[str(addr)]['HARDWARE'] = frame['DATA'][0]
			devdata[str(addr)]['VERSION'] = frame['DATA'][1]
			print(devdata)
			addr = addr + 1

while(True):
	try:
		deviceManager()
		mqtt.run()
		msg = ''
		msg = mqtt.get()
		if(msg != ''):
			cmd = ast.literal_eval(msg)
			if(cmd['ADDR'] != rasp_info.rasp_get_id()):
				print('Wrong addr')
			else:
				if(cmd['FUNC'] == 'WRITE'):
					print('GET WRITE FUNC: \r\n' + str(cmd))
					modbus.send_frame(int(cmd['DEV1']), 0x02, 0x10, 0x01, int(cmd['DATA']['1']))
				elif(cmd['FUNC'] == 'READ'):
					print('GET READ FUNC: \r\n' + str(cmd))
					modbus.send_frame(int(cmd['DEV1']), 0x01, 0x10, 0x01)
				elif(cmd['FUNC'] == 'RULE'):
					print('Not supported')
		res = modbus.get_frame(1)
		if(res != 'ERROR'):
			print(res)
	except KeyboardInterrupt:
		print('Stop working\r\n')
		sys.exit()
