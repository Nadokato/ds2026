from mpi4py import MPI
import os
import sys

# Configuration
CHUNK_SIZE = 1024 * 1024 
TAG_FILENAME = 1
TAG_DATA = 2
TAG_END = 3

def sender(filename, dest_rank):
    """
    Logic for the sender process (Rank 0).
    """
    comm = MPI.COMM_WORLD
    
    if not os.path.exists(filename):
        print(f"[Sender] Error: File '{filename}' not found.")
        comm.send(None, dest=dest_rank, tag=TAG_FILENAME)
        return

    print(f"[Sender] Sending filename: {filename}")
    comm.send(os.path.basename(filename), dest=dest_rank, tag=TAG_FILENAME)

    print(f"[Sender] Sending data...")
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            comm.send(chunk, dest=dest_rank, tag=TAG_DATA)
    
    comm.send(None, dest=dest_rank, tag=TAG_END)
    print("[Sender] File transfer complete.")

def receiver(source_rank):
    """
    Logic for the receiver process (Rank 1).
    """
    comm = MPI.COMM_WORLD
    
    print("[Receiver] Waiting for filename...")
    filename = comm.recv(source=source_rank, tag=TAG_FILENAME)
    
    if filename is None:
        print("[Receiver] Sender reported an error.")
        return

    output_filename = f"received_{filename}"
    print(f"[Receiver] Saving to: {output_filename}")

    with open(output_filename, 'wb') as f:
        while True:
            status = MPI.Status()
            comm.probe(source=source_rank, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()

            if tag == TAG_DATA:
                chunk = comm.recv(source=source_rank, tag=TAG_DATA)
                f.write(chunk)
            elif tag == TAG_END:
                comm.recv(source=source_rank, tag=TAG_END)
                break

    print(f"[Receiver] Successfully received {output_filename}")

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if size < 2:
        print("Error: This program requires at least 2 processes (Sender and Receiver).")
        print("Usage: mpiexec -n 2 python mpi_file_transfer.py <filename_to_send>")
        sys.exit(1)

    if rank == 0:
        if len(sys.argv) < 2:
            print("Usage: mpiexec -n 2 python mpi_file_transfer.py <filename>")
            comm.send(None, dest=1, tag=TAG_FILENAME) 
        else:
            filename = sys.argv[1]
            sender(filename, dest_rank=1)
    elif rank == 1:
        receiver(source_rank=0)