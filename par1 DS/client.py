import socket
import sys
import os

# Configuration
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8080         # The port used by the server
BUFFER_SIZE = 1024

def send_file(filename):
    # 1.socket(): Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 2.connect(): Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"[+] Connected to server at {HOST}:{PORT}")

        # PROTOCOL STEP 1: Send Filename
        client_socket.sendall(filename.encode('utf-8'))

        # PROTOCOL STEP 2: Wait for ACK 
        ack = client_socket.recv(BUFFER_SIZE)
        if ack.decode('utf-8') != "ACK":
            print("[-] Server did not acknowledge filename.")
            return

        # PROTOCOL STEP 3: Send File Content
        print(f"[+] Sending file '{filename}'...")
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)

        print("[+] File sent successfully.")

    except ConnectionRefusedError:
        print("[-] Connection refused. Is the server running?")
    except FileNotFoundError:
        print(f"[-] File '{filename}' not found.")
    except Exception as e:
        print(f"[-] An error occurred: {e}")
    finally:
        # 4. close()
        client_socket.close()

if __name__ == "__main__":
    # Check if filename is provided
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <filename>")
        sys.exit(1)

    target_file = sys.argv[1]
    send_file(target_file)