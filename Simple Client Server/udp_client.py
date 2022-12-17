import socket

target_host = "127.0.0.1"
target_port = 4444

# create socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send data
client.sendto(b"Hello to UDP cli", (target_host,target_port))
# getting data
data, addr = client.recvfrom(4096)
print(data.decode())
client.close()
