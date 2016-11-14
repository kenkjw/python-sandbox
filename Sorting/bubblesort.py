def bubblesort(c):
    for i in range(len(c)-1,0,-1):
        for j in range(0,i):
            if c[j] > c[j+1]:
                tmp = c[j]
                c[j] = c[j+1]
                c[j+1] = tmp


if __name__ == "__main__":
    import random
    from time import time
    random.seed()
    c = []
    for i in range(20):
        c.append(random.randint(1,1000))
    print c

    t0 = time()
    bubblesort(c)
    t1 = time()
    print c
    print "time: ", t1-t0, "s"