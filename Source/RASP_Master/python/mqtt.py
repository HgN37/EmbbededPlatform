import paho.mqtt.client as mqtt

class MQTT():
	''' Communication with server via WiFi or Ethernet '''
	def __init__(self, broker, port):
		def on_connect(client, userdata, flags, rc):
			print('Connected with code ' + str(rc))
			client.subscribe('hgn')

		def on_message(client, userdata, msg):
			print(msg.topic + ': ' + str(msg.payload))
			client.publish('ngh', str(msg.payload))

		self.client = mqtt.Client()
		self.client.on_connect = on_connect
		self.client.on_message = on_message

		self.client.connect(broker, port, 60)

	def run(self):
		self.client.loop_forever()

def main():
	mqtt = MQTT('iot.eclipse.org', 1883)
	mqtt.run()

if __name__ == '__main__':
	main()
