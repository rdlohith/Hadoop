import threading

# Mapper function
def mapper(data, results):
    words = data.split()
    for word in words:
        results.append((word, 1))

# Reducer function
def reducer(data):
    word_counts = {}
    for item in data:
        if item[0] in word_counts:
            word_counts[item[0]] += item[1]
        else:
            word_counts[item[0]] = item[1]
    return word_counts


if __name__ == '__main__':
    # Read input data
    with open('input1.txt', 'r') as f:
        data = f.read()

    # Split data into chunks
    chunk_size = len(data) // threading.active_count()
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # Map phase
    results = []
    threads = []
    for chunk in chunks:
        thread = threading.Thread(target=mapper, args=(chunk, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Shuffle phase
    shuffled_data = {}
    for item in results:
        if item[0] in shuffled_data:
            shuffled_data[item[0]].append(item[1])
        else:
            shuffled_data[item[0]] = [item[1]]

    # Reduce phase
    reduced_data = reducer(shuffled_data.items())

    # Print word counts
    for word, count in reduced_data.items():
        print(f'{word} - {len(count)}')
    print()