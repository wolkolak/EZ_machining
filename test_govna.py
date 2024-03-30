#a = [1, 2 ,3, 4, 5, 6, 7, 8, 9, 10]





from technical_floor.time_check import decorator_time_count
a = [x for x in range(9)]
len_a = len(a)
half_l_a = int(len_a/2)

@decorator_time_count
def foo():
    for i, a_ in enumerate(a):#+ a[half_l_a-1 :]
        #print(i, a_)
        f = a_
        #f2 = a[i]

@decorator_time_count
def foo2():
    for ff in a:
        f = ff

@decorator_time_count
def foo3():
    for ff in range(len_a):
        #f = a[ff]
        f2 = a[ff]

@decorator_time_count
def foo4():
    for i, a_ in enumerate(a[0:2] + a[6:9]):
        #f = a_
        f2 = a[i]
        print((f'i = {i}, a_ = {a_}'))
#foo(times_to_execute=100)

#foo2(times_to_execute=100)

foo3(times_to_execute=1)

foo4(times_to_execute=1)

