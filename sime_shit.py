
import numpy as np
import timeit, traceback
import time

"""a = np.ascontiguousarray(np.random.randint(1, 200.0, 10000000))
a = np.repeat(a, 7)
print(a.shape)
start_time = time.process_time_ns()
a = np.insert(a, 0, 11, axis=0)
#b = np.array(a)
#print(timeit.timeit('output1 = np.array(a)'))
print("--- %s seconds ---" % (time.process_time_ns() - start_time))"""

a = np.array([1,2,3])
print('a=', a)
a = np.insert(a, 3, [9], axis=0)
print('a=', a)