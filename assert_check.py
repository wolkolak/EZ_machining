import numpy as np
k = [1., 2., 3]
ar = np.array([1., 2., 3])
ar2 = np.array([0., 0., 0])
from technical_floor.time_check import decorator_time_count

@decorator_time_count
def foo1():
    k = [*ar]
@decorator_time_count
def foo2():
    ar2 = ar[:]


foo1(times_to_execute=100000)
foo2(times_to_execute=100000)

print(ar)
ar2 = ar[:]
ar[0] = 1000
print(ar2)