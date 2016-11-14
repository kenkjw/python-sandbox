def quicksort(c):
    _qs(c,0,len(c)-1)

def _qs(c,lo,hi):
    if lo < hi:
        p = _qs_part(c,lo,hi)
        _qs(c,lo,p-1)
        _qs(c,p+1,hi)



def _qs_part(c,lo,hi):
    i = lo
    for j in range(lo,hi):
        if c[j] < c[hi]:
            tmp = c[i]
            c[i] = c[j]
            c[j] = tmp
            i += 1
    tmp = c[i]
    c[i] = c[hi]
    c[hi] = tmp
    return i


if __name__ == "__main__":
    import random
    from time import time
    random.seed()
    c = []
    for i in range(200000):
        c.append(random.randint(1,1000000))
    #print c

    t0 = time()
    quicksort(c)
    t1 = time()
    #print c
    print "time: ", t1-t0, "s"


