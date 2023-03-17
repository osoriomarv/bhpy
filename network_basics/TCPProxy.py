import sys # Importing sys module for system-specific parameters and functions
import socket # Importing socket module for networking functions
import threading # Importing threading module for multi-threading

# Hex Dump function from Black Hat Python 2nd Edition

HEX_FILTER = ''.join([(len(repr(chr(i)))) == 3 and chr (i) or '.' for i in range(256)])

# Hexdump function to print hexadecimal and printable representation of data
def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i+length])

        printable = word.translate(HEX_FILTER)
        hexa = ''.join([f'{ord(c):02x} ' for c in word])
        hexwidth = length * 3

        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')
        if show:
            for line in results:
                print(line)
        else:
            return results

# Function to receive data from a connection
def receive_from(connection):
    buffer = b""

    connection.settimeout(5) # Setting a timeout of 5 seconds on the connection
    try:
        while True:
            data = connection.recv(4096) # Receiving data in chunks of 4096 bytes
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

# Proxy_handler function to modify the data
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a socket object

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))

        

def request_handler(buffer):
    #perform packet modifications
    return buffer

def response_handler(buffer):
    #perform packet modifications
    return buffer


