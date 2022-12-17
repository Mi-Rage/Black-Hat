## NetCat
Simple netcat utility. It can connect to a target, listen to a port, execute various commands, and allows you to get a reverse.

usage: main.py [-h] [-c] [-e EXECUTE] [-l] [-p PORT] [-t TARGET] [-u UPLOAD]

options:\
  -h, --help            show this help message and exit\
  -c, --command         command shell\
  -e EXECUTE, --execute execute specified command\
  -l, --listen          listen mode\
  -p PORT, --port PORT  specified port\
  -t TARGET, --target   specified IP\
  -u UPLOAD, --upload   upload file\

Example:\
netcat.py -t 192.168.1.108 -p 5555 -l -c                        # command shell\
netcat.py -t 192.168.1.108 -p 5555 -l -u=my_file.txt            # upload file\
netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"      # execute command\
echo 'ACK' | ./netcat.py -t 192.168.1.108 -p 135                # sent text to 135 port\
netcat.py -t 192.168.1.108 -p 5555                              # connecting to target  
