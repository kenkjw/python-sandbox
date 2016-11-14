def mergesort_top(c):
    if len(c) <= 1:
        return c
    left = c[:len(c)/2]
    right = c[len(c)/2:]
    left = mergesort_top(left)
    right = mergesort_top(right)

    return merge(left,right)

def merge(left,right):
    result = []
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    if left:
        result.extend(left)
    if right:
        result.extend(right)
    return result

def mergesort_bottom(c):
    split = 1
    while split < len(c):
        size = split << 1
        start = 0
        while start < len(c):
            end = start+size
            if end > len(c):
                end = len(c)
            merged = merge2(c,start,end,split)
            c[start:end] = merged
            start += size
        split = size


def merge2(c,start,end,size):
    if start + size > end:
        return c[start:end]
    result = []
    
    left = c[start:start+size]
    right = c[start+size:end]
    while left and right:
        if left[0] < right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    if left:
        result.extend(left)
    if right:
        result.extend(right)
    return result

if __name__ == "__main__":
    import random
    from time import time
    random.seed()
    c = []
    for i in range(100000):
        c.append(random.randint(1,1000000))
    #print c
    d = c[:]
    t0 = time()
    c = mergesort_top(c)

    t1 = time()
    t2 = time()
    mergesort_bottom(d)
    t3 = time()
    #print c
    print "time: ", t1-t0, "s"
    print "time2: ", t3-t2, "s"


