import socket
import threading

IP = '0.0.0.0'
PORT = 4444


def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    # listen no more 5 clients
    server.listen(5)
    print(f'[*] Listening on {IP}:{PORT}')

    while True:
        # connecting client
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        # create new thread with client connect
        client_handler.start()


def handle_client(client_socket):
    with client_socket as sock:
        # receive some data and send message
        request = sock.recv(1024)
        print(f'[*] Receive: {request.decode("utf-8")}')
        sock.send(b'ACK')


tcp_server()
