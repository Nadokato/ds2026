import xmlrpc.client
import os
import sys

# Configuration
SERVER_URL = 'http://localhost:8000'

def upload_file(path_to_file):
    if not os.path.exists(path_to_file):
        print(f"Error: File '{path_to_file}' not found.")
        return

    print(f"Connecting to RPC server at {SERVER_URL}...")
    
    proxy = xmlrpc.client.ServerProxy(SERVER_URL)
    
    filename = os.path.basename(path_to_file)
    
    try:
        print(f"Reading file: {filename}")
        with open(path_to_file, 'rb') as handle:
            binary_data = handle.read()
            
        rpc_binary = xmlrpc.client.Binary(binary_data)
        
        print(f"Sending {filename} via RPC...")
        response = proxy.upload_file(filename, rpc_binary)
        
        print(f"Server Response: {response}")
        
    except ConnectionRefusedError:
        print("Error: Could not connect to the server. Is it running?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python rpc_client.py <file_to_upload>")
        with open("test_rpc.txt", "w") as f:
            f.write("This is a test file for RPC transfer.")
        print("Created 'test_rpc.txt' for testing.")
        upload_file("test_rpc.txt")
    else:
        upload_file(sys.argv[1])