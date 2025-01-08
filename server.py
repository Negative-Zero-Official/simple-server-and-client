import socket
import threading
import sys
import signal
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 50000

server = None
shutdown_flag = threading.Event()
client_socket = None

def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, port))
            return True
        except OSError:
            return False

print(f"Server is running on {HOST}")

if is_port_free(PORT):
    print(f"Port {PORT} is free.")
else:
    print(f"Port {PORT} is in use.")
    
def handle_client(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"{addr}: {message}")
                client_socket.send((f"{addr}: {message}").encode('utf-8'))
            else:
                break
        except ConnectionAbortedError as e:
            print(f"Server closed. Message: {e}")
            break
        except ConnectionResetError as e:
            print(f"Connection reset by peer: {e}")
            break
    client_socket.close()

def start_server():
    global server
    global client_socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")
    
    while not shutdown_flag.is_set():
        try:
            server.settimeout(1)
            client_socket, addr = server.accept()
            print(f"Connection established with {addr}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
        except socket.timeout:
            continue
        except OSError:
            break

def stop_server(signum, frame):
    global client_socket
    print("Shutting down server...")
    if client_socket:
        client_socket.close()
    if server:
        server.close()
    sys.exit(0)

if __name__=="__main__":
    signal.signal(signal.SIGINT, stop_server)
    start_server()