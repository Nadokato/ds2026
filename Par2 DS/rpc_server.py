import xmlrpc.server
import os

# Configuration
HOST = 'localhost'
PORT = 8000
UPLOAD_DIR = 'server_files'

# Ensure upload directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_file_rpc(filename, file_data):
    try:
        file_path = os.path.join(UPLOAD_DIR, os.path.basename(filename))
        
        with open(file_path, 'wb') as handle:
            handle.write(file_data.data)
            
        print(f"Successfully received and saved: {filename}")
        return f"ACK: {filename} uploaded successfully."
    except Exception as e:
        print(f"Error saving file: {e}")
        return f"ERROR: Could not upload {filename}"

def run_server():
    print(f"Starting RPC Server on {HOST}:{PORT}...")
    with xmlrpc.server.SimpleXMLRPCServer((HOST, PORT), allow_none=True) as server:
        server.register_introspection_functions()
        
        server.register_function(save_file_rpc, 'upload_file')
        
        print("Server is ready to accept files. Press Ctrl+C to stop.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nStopping server...")

if __name__ == '__main__':
    run_server()