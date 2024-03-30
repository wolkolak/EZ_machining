import time
import numpy as np


n = 11111111
cur_frame_address = np.zeros((n, 2), int)
cur_frame_address[:, 0] = np.arange(1, 1 + n)

t0 = time.time()
#cur_frame_address2 = np.zeros((n, 2), int)
#cur_frame_address2[:, 0] = np.arange(1, 1 + n)

cur_frame_address2 = np.copy(cur_frame_address[0:n+1])

t1 = time.time()

total = t1-t0
print(total)
#print(cur_frame_address)
#print('__________')
#print(cur_frame_address2)

def decorator_time_count(funcr):
    def wrapper_t(*args, times_to_execute=1000, **kwargs, ):
        t0 = time.time()
        for f in range(times_to_execute):
            funcr(*args, **kwargs)
        t1 = time.time()
        print(f'time for function {funcr.__name__}: {t1 - t0}')
    return wrapper_t