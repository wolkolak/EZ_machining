
num1 = [1, 4, 9, 6, 8, 2]
target = 11

#dict1 = {}
#for i in range(len(num1)): dict1[num1[i]] = i
def two_sum(num1, target):
    dict1 = {key:index for index, key in enumerate(num1)}
    for i in range(len(num1)):
        res = target-num1[i]
        if res in dict1:# and dict1[res] != num1[i]:
            return [i, dict1[res]]
    return -1

print(two_sum(num1, target))