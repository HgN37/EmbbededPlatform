import socket

socketServer = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostname())
socketServer.bind(('3.7.96.104', 37777))
socketServer.listen(5)

while True:
  print('Wait for connection')
  (client, address) = socketServer.accept()
  try:
    print('Connect from ', address)
  finally:
    client.close()
