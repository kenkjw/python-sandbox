def heapsort(c):
    heapify(c)
    for end in reversed(range(1,len(c))):
        tmp = c[0]
        c[0] = c[end]
        c[end] = tmp
        siftdown(c,0,end-1)

def heapify(c):
    for i in range(1,len(c)):
        n = i
        parent = (n-1) >> 1
        while n != 0 and c[n] > c[parent]:
            tmp = c[n]
            c[n] = c[parent]
            c[parent] = tmp
            n = parent
            parent = (n-1) >> 1

def siftdown(c,start,end):
    root = start
    while 2*root + 1 <= end:
        swap_index = 2*root+1
        if 2*root + 2 <= end:
            if c[swap_index] < c[swap_index+1]:
                swap_index += 1
        if c[root] < c[swap_index]:
            tmp = c[root]
            c[root] = c[swap_index]
            c[swap_index] = tmp
            root = swap_index

        else:
            break




if __name__ == "__main__":
    import random
    from time import time
    random.seed()
    c = []
    for i in range(40000):
        c.append(random.randint(1,1000000))
    #print c

    t0 = time()
    heapsort(c)
    t1 = time()
    #print c
    print "time: ", t1-t0, "s"

