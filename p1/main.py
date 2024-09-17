from utils import execution_time_decorator, generate_random_array, remove_outliers
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

import matplotlib.pyplot as plt

@execution_time_decorator
def builtin_method(arr):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i]
    return sum / len(arr)


@execution_time_decorator
def map_reduce_method(arr, chunks_amount):
    def map(arr, left, right):
        sum = 0
        for i in range(left, right + 1):
            sum += arr[i]
        return sum

    elements_per_chunk = len(arr) // chunks_amount 
    if (len(arr) % chunks_amount != 0):
        chunks_amount += 1

    futures = []
    with ThreadPoolExecutor() as executor:

        for i in range(chunks_amount):
            first_index = i * elements_per_chunk
            last_index = min(len(arr), (i + 1) * elements_per_chunk) - 1
            futures.append(executor.submit(map, arr, first_index, last_index))

        results = []
        for future in as_completed(futures):
            results.append(future.result())
        
    return sum(results) / len(arr)    


def test_range():
    builtin_times = []
    map_reduce_times = []
    maxNumber = 500000
    sizes = range(1, maxNumber, maxNumber // 20)
    # chunk_size = 1500 
    processes = 16

    for i in sizes:
        print(i)
        arr = generate_random_array(i)

        builtin_time = builtin_method(arr)['time']
        builtin_times.append(builtin_time)

        map_reduce_time = map_reduce_method(arr, i // processes + 1)['time']
        map_reduce_times.append(map_reduce_time)

    filtered_map_reduce_times = remove_outliers(map_reduce_times)

    plt.plot(sizes, builtin_times, label='Built-in Method Time')

    if len(filtered_map_reduce_times) == len(sizes):
        plt.plot(sizes, filtered_map_reduce_times, label='Map-Reduce Method Time (Filtered)')
    else:
        # If outliers were removed, we can plot based on the indices that remain
        filtered_sizes = sizes[:len(filtered_map_reduce_times)]
        plt.plot(filtered_sizes, filtered_map_reduce_times, label='Map-Reduce Method Time (Filtered)')

    plt.xlabel('Array Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time: Built-in Method vs Map-Reduce Method')
    plt.legend()
    plt.grid(True)

    current_timestamp = round(time.time())
    plt.savefig(f"execution_time_comparison_python_p{processes}_{current_timestamp}.png")

if __name__ == '__main__':
    test_range()
