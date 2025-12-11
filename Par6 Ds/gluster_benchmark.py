import os
import time
import shutil

#Configuration
MOUNT_POINT = "/mnt/gluster_storage"
SMALL_FILES_COUNT = 1000
SMALL_FILE_SIZE = 1024 
LARGE_FILE_SIZE = 100 * 1024 * 1024  

def benchmark_small_files():
    print(f"--- Benchmarking Small Files ({SMALL_FILES_COUNT} files, {SMALL_FILE_SIZE} bytes each) ---")
    test_dir = os.path.join(MOUNT_POINT, "bench_small")
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir)

    #Write
    start_time = time.time()
    for i in range(SMALL_FILES_COUNT):
        with open(os.path.join(test_dir, f"file_{i}"), "wb") as f:
            f.write(os.urandom(SMALL_FILE_SIZE))
    end_time = time.time()
    write_fps = SMALL_FILES_COUNT / (end_time - start_time)
    print(f"Write Speed: {write_fps:.2f} accesses/second")

    #Read
    start_time = time.time()
    for i in range(SMALL_FILES_COUNT):
        with open(os.path.join(test_dir, f"file_{i}"), "rb") as f:
            _ = f.read()
    end_time = time.time()
    read_fps = SMALL_FILES_COUNT / (end_time - start_time)
    print(f"Read Speed:  {read_fps:.2f} accesses/second")

    #Cleanup
    shutil.rmtree(test_dir)

def benchmark_large_file():
    print(f"\n--- Benchmarking Large File ({LARGE_FILE_SIZE / (1024*1024)} MB) ---")
    file_path = os.path.join(MOUNT_POINT, "bench_large.dat")

    # Generate random data 
    data = os.urandom(LARGE_FILE_SIZE)

    #Write
    start_time = time.time()
    with open(file_path, "wb") as f:
        f.write(data)
    end_time = time.time()
    duration = end_time - start_time
    write_speed = (LARGE_FILE_SIZE / (1024 * 1024)) / duration
    print(f"Write Speed: {write_speed:.2f} MB/s")

    os.system("sync; echo 3 > /proc/sys/vm/drop_caches")
    
    start_time = time.time()
    with open(file_path, "rb") as f:
        _ = f.read()
    end_time = time.time()
    duration = end_time - start_time
    read_speed = (LARGE_FILE_SIZE / (1024 * 1024)) / duration
    print(f"Read Speed:  {read_speed:.2f} MB/s")

    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == "__main__":
    if not os.path.exists(MOUNT_POINT):
        print(f"Error: Mount point {MOUNT_POINT} does not exist.")
        print("Please mount your GlusterFS volume first.")
    else:
        try:
            test_file = os.path.join(MOUNT_POINT, "test_perm")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            
            benchmark_small_files()
            benchmark_large_file()
        except PermissionError:
            print("Error: Permission denied. Try running with 'sudo python3 ...' or chmod the mount point.")