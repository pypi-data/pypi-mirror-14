import numpy
import sharedmem
import time

with sharedmem.MapReduce(np=64) as pool:
    def work(i):
        time.sleep(numpy.random.uniform())
        return i, 1
    def reduce(i, rank):
        print i
        return i
    pool.map(work, range(1000), reduce=reduce)
