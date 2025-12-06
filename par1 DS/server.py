import socket
import os

# Configuration
HOST = '127.0.0.1'  # localhost
PORT = 8080         # Port to listen on 
BUFFER_SIZE = 1024  # Size

def start_server():
    # 1. socket(): Create a socket object
    # AF_INET = IPv4, SOCK_STREAM = TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. bind(): Associate the socket with a specific network interface and port
    try:
        server_socket.bind((HOST, PORT))
    except socket.error as e:
        print(f"[-] Bind failed. Error: {e}")
        return

    # 3. listen(): Put the socket into listening mode
    server_socket.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        # 4. accept(): Wait for an incoming connection
        client_socket, client_addr = server_socket.accept()
        print(f"[+] Accepted connection from {client_addr[0]}:{client_addr[1]}")

        try:
            # PROTOCOL STEP 1: Receive Filename
            filename_bytes = client_socket.recv(BUFFER_SIZE)
            if not filename_bytes:
                break
            
            filename = filename_bytes.decode('utf-8')
            filename = os.path.basename(filename)
            print(f"[+] Receiving file: {filename}")

            # PROTOCOL STEP 2: Send ACK
            client_socket.sendall(b"ACK")

            # PROTOCOL STEP 3: Receive File Content 
            with open(filename, "wb") as f:
                while True:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
            
            print(f"[+] File '{filename}' downloaded successfully.")

        except Exception as e:
            print(f"[-] Error during transfer: {e}")
        finally:
            # 5.close(): 
            client_socket.close()
            print("[-] Connection closed.\n")

if __name__ == "__main__":
    start_server()