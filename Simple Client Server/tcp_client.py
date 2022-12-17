import socket

target_host = "127.0.0.1"
target_port = 4444

# create socket obj
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connecting client
client.connect((target_host, target_port))
# send something
client.send(b'Send some data to server\r\nAnd Hello Word!\r\n')
# getting data
response = client.recv(4096)
print(response.decode())
client.close()
