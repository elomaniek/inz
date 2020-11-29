import socket
import errno
import os



'''
def find_free_port(port,max_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while port <= max_port:
        try:
            s.bind(("127.0.0.1", port))

        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print("Port is already in use")
                port += 1
            else:
                # something else raised the socket.error exception
                print(e)

        s.close()

port = find_free_port(5000,9000)
print(port)'''


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

#port = str(find_free_port())

#print(port)
hostname = socket.gethostname()

local_ip = socket.gethostbyname(hostname)


print(local_ip)