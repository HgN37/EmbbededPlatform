import serial
import sys
# import time

class RS485():
	''' Communication with slave via RS485 '''

	def __init__(self, port):
		self.ser = serial.Serial()
		self.ser.baudrate = 9600
		self.ser.parity = serial.PARITY_EVEN
		self.ser.port = port
		try:
			self.ser.open()
		except:
			print("ERROR: Can't open port " + port)
	def send(self, array):
		self.ser.write(bytearray(array))
		self.ser.flush()
	def get(self):
		if self.ser.in_waiting:
			byte = ord(self.ser.read())
			print("0x{:02x}".format(byte))
			return byte
		
class Modbus(RS485):
	''' Modbus protocol '''

	def crc_generate(self, current_crc, new_byte):
		next_crc = current_crc ^ new_byte
		for loop in range(8):
			if (next_crc & 0x0001) != 0:
				next_crc = next_crc >> 1
				next_crc = next_crc ^ 0xA001
			else:
				next_crc = next_crc >> 1
		return next_crc
	def send_frame(self, addr, func, reg, num, *data):
		frame = []
		crc = 0xFFFF
		frame.append(addr)
		crc = self.crc_generate(crc, addr)
		frame.append(func)
		crc = self.crc_generate(crc, func)
		frame.append(reg)
		crc = self.crc_generate(crc, reg)
		frame.append(num)
		crc = self.crc_generate(crc, num)
		for byte in range(len(data)):
			frame.append(data[byte])
			crc = self.crc_generate(crc, data[byte])
		frame.append((crc & 0xFF00) >> 8)
		frame.append((crc & 0x00FF))
		print(frame)
		self.send(frame)

def main():
	print('Master - Slave Connection')
	slave = Modbus('/dev/ttyUSB0')
	slave.send_frame(0x01, 0x02, 0x10, 0x01, 0x64)
	#slave.send_frame(0x01, 0x02, 0x10, 0x01, 0x00)
	while True:
		slave.get()


if __name__ == '__main__':
	main()