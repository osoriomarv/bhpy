import sys # Importing sys module for system-specific parameters and functions
import socket # Importing socket module for networking functions
import threading # Importing threading module for multi-threading

# Hex Dump function from Black Hat Python 2nd Edition
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
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes from localhost." % len(local_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = receive_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Sent to localhost.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections")
            break

def server_loop(local_buffer, local_port, remote_host, remote_port, receive_first):
    # Create a socket then bind to the local host and listens for port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print('problem on bind: %r' % e)

        print("[!!] Failed to listen on %s:%d" % (local_host,
            local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)

    # When a fresh connection request comes in we hand it to proxy handler in new thread
    # 
    while True:
        client_socket, addr = server.accept()
        # print out the local connection information
        line = "> Received incoming connection from %s:%d" % (addr[0], addr[1])
        print(line)
        # start a thread to talk to the remote host
        # Sends and receives 
        proxy_thread = threading.Thread(
                    target = proxy_handler,
                    args=(client_socket, remote_host,
                    remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) !=5:
        print("Usage: ./TCPproxy.py [localhost] [localport]",
            end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./TCPproxy 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host =sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5] 

    if "True" in receive_first:
        receive_first = True
    else:
        recieve_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()



