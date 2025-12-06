import multiprocessing
import os
import random
import string

#Configuration
NUM_MAPPERS = 4
NUM_REDUCERS = 1

def generate_dummy_data(filename, num_lines=1000):
    """
    Generates a file with random file paths to simulate 'find /' output.
    Some paths will be intentionally made very long.
    """
    print(f"Generating dummy input file: {filename}...")
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(num_lines):
            # Create random path depths
            depth = random.randint(1, 15)
            path_parts = []
            for _ in range(depth):
                # Random folder names
                name_len = random.randint(3, 10)
                folder = ''.join(random.choices(string.ascii_lowercase, k=name_len))
                path_parts.append(folder)
            
            if i % 100 == 0:
                 path_parts.extend(["very_long_directory_name"] * 5)
            
            full_path = "/" + "/".join(path_parts)
            f.write(full_path + "\n")

def mapper(text_chunk):
    lines = text_chunk.strip().split('\n')
    if not lines:
        return []

    local_max_path = ""
    local_max_len = -1

    for line in lines:
        path = line.strip()
        if not path:
            continue
        current_len = len(path)
        if current_len > local_max_len:
            local_max_len = current_len
            local_max_path = path
            
    # Key is 'global_max' 
    return [('global_max', (local_max_len, local_max_path))]

def reducer(item):
    key, values = item
    
    overall_max = max(values, key=lambda x: x[0])
    
    return (key, overall_max)

def partitioner(mapped_values):
    """
    Groups values by key.
    """
    from collections import defaultdict
    partitioned_data = defaultdict(list)
    for key, value in mapped_values:
        partitioned_data[key].append(value)
    return list(partitioned_data.items())

def chunk_file(filename, num_chunks):
    """
    Splits file content into chunks.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chunk_size = len(content) // num_chunks
    if chunk_size == 0: return [content]
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

def run_mapreduce(filename):
    print(f"--- Starting MapReduce LongestPath on {filename} ---")

    # Split Input
    chunks = chunk_file(filename, NUM_MAPPERS)

    # Map Phase
    print(f"Running {NUM_MAPPERS} Mappers...")
    with multiprocessing.Pool(processes=NUM_MAPPERS) as pool:
        map_results = pool.map(mapper, chunks)
    
    flat_map_results = [item for sublist in map_results for item in sublist]

    # Shuffle
    print("Shuffling...")
    grouped_data = partitioner(flat_map_results)

    # Reduce Phase
    print(f"Running {NUM_REDUCERS} Reducer...")
    with multiprocessing.Pool(processes=NUM_REDUCERS) as pool:
        reduced_results = pool.map(reducer, grouped_data)

    # Output Result
    print("\n--- RESULT ---")
    if reduced_results:
        _, (length, path) = reduced_results[0]
        print(f"Longest Path Found (Length: {length}):")
        print(path)
    else:
        print("No paths found.")

if __name__ == '__main__':
    input_file = "file_paths.txt"
    if not os.path.exists(input_file):
        generate_dummy_data(input_file)
    
    run_mapreduce(input_file)