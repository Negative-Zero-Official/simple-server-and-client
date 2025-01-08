import socket
import threading
import queue
import sys

def receive_messages(client_socket, message_queue, stop_event):
    while not stop_event.is_set():
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                message_queue.put(f"{message}")
            else:
                message_queue.put("Disconnected from server.")
                stop_event.set()
                sys.exit(0)
        except ConnectionAbortedError as e:
            message_queue.put("Client closed connection.")
            break
        except ConnectionResetError as e:
            message_queue.put(f"Error: {e}")
            message_queue.put("Connection lost. Server might have shut down.")
            break
    client_socket.close()

def handle_user_input(input_queue, stop_event):
    while not stop_event.is_set():
        try:
            message = input()
            input_queue.put(message)
            if message.lower() == "exit":
                break
            sys.stdout.write("\033[F\033[K")
        except EOFError:
            stop_event.set()
            break

def send_messages(client_socket, input_queue, message_queue, stop_event):
    while not stop_event.is_set():
        try:
            if not input_queue.empty():
                message = input_queue.get()
                if message.lower() == "exit":
                    message_queue.put("Closing connection...")
                    stop_event.set()
                    client_socket.close()
                    break
                client_socket.send(message.encode('utf-8'))
        except OSError:
            message_queue.put("Connection closed.")
            break

def print_messages(message_queue, stop_event):
    while not stop_event.is_set() or not message_queue.empty():
        try:
            message = message_queue.get(timeout=0.1)
            print(message)
        except queue.Empty:
            continue

if __name__=="__main__":
    HOST = input("Enter server IP: ")
    PORT = int(input("Enter server port: "))
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stop_event = threading.Event()
    message_queue = queue.Queue()
    input_queue = queue.Queue()
    
    try:
        client_socket.connect((HOST,PORT))
        print(f"Connected to {HOST}:{PORT}")
        
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket, message_queue, stop_event), daemon=True)
        input_thread = threading.Thread(target=handle_user_input, args=(input_queue, stop_event), daemon=True)
        send_thread = threading.Thread(target=send_messages, args=(client_socket, input_queue, message_queue, stop_event), daemon=True)
        print_thread = threading.Thread(target=print_messages, args=(message_queue, stop_event), daemon=True)
        
        receive_thread.start()
        input_thread.start()
        send_thread.start()
        print_thread.start()
        
        receive_thread.join()
        input_thread.join()
        send_thread.join()
        print_thread.join()
    except ConnectionRefusedError as e:
        print(f"Error: {e}")
        print(f"Unable to connect to server at {HOST}:{PORT}. Is the server running?")
    except KeyboardInterrupt:
        print("Closing client...")
        client_socket.close()