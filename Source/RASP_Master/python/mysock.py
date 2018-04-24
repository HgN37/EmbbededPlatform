import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.parity = serial.PARITY_EVEN
ser.port = '/dev/ttyUSB0'
ser.open()

while True:
	print('.')
	ser.write(0xFF)
	ser.flush()
