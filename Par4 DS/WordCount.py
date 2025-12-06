import multiprocessing
import string
import os
from collections import defaultdict

#Configuration
NUM_MAPPERS = 4
NUM_REDUCERS = 4

def mapper(text_chunk):
    """
    Map function: Takes a chunk of text and emits key-value pairs (word, 1).
    """
    # Remove punctuation and convert to lowercase
    translator = str.maketrans('', '', string.punctuation)
    clean_text = text_chunk.translate(translator).lower()
    
    words = clean_text.split()
    mapped_data = []
    for word in words:
        if word:
            mapped_data.append((word, 1))
    return mapped_data

def reducer(item):
    """
    Reduce function: Takes a tuple (word, list_of_counts) and sums the counts.
    """
    word, counts = item
    return (word, sum(counts))

def partitioner(mapped_values):
    """
    Shuffle & Sort phase: Groups values by key (word).
    """
    partitioned_data = defaultdict(list)
    for word, count in mapped_values:
        partitioned_data[word].append(count)
    return list(partitioned_data.items())

def chunk_file(filename, num_chunks):
    """
    Helper to split file into chunks for mappers.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    chunk_size = len(content) // num_chunks
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

def run_mapreduce(filename):
    print(f"--- Starting MapReduce WordCount on {filename} ---")

    #Input Split
    print("1. Splitting input...")
    chunks = chunk_file(filename, NUM_MAPPERS)

    # Map Phase 
    print(f"2. Running {NUM_MAPPERS} Mappers in parallel...")
    with multiprocessing.Pool(processes=NUM_MAPPERS) as pool:
        map_results = pool.map(mapper, chunks)
    
    flat_map_results = [item for sublist in map_results for item in sublist]
    print(f"   -> Mappers produced {len(flat_map_results)} key-value pairs.")

    # Shuffle & Sort Phase
    print("3. Shuffling and Sorting...")
    grouped_data = partitioner(flat_map_results)
    
    #Reduce Phase
    print(f"4. Running {NUM_REDUCERS} Reducers in parallel...")
    with multiprocessing.Pool(processes=NUM_REDUCERS) as pool:
        reduced_results = pool.map(reducer, grouped_data)

    # Output
    print("5. Writing output...")
    reduced_results.sort(key=lambda x: x[1], reverse=True)
    
    output_file = "wordcount_output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, count in reduced_results:
            f.write(f"{word}: {count}\n")
            
    print(f"--- Job Complete. Results saved to {output_file} ---")

if __name__ == '__main__':
    # Create a dummy file for testing if it doesn't exist
    target_file = 'sample_text.txt'
    if not os.path.exists(target_file):
        with open(target_file, 'w') as f:
            f.write("Hello world mapreduce hello map reduce python python python")
        print(f"Created dummy input file: {target_file}")

    run_mapreduce(target_file)