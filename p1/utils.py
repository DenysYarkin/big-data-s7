import random
import time

import numpy as np

def generate_random_array(size, min_element=0, max_element=2**32-1):
    return [random.randint(min_element, max_element) for i in range(size)]

def execution_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return { 
            'result': result, 
            'time': execution_time 
        }
    return wrapper

def remove_outliers(data):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return [x for x in data if lower_bound <= x <= upper_bound]
