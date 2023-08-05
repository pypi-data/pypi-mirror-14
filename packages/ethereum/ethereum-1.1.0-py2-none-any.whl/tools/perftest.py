import random
import time, sys

NUM = 1000 * 1000


P = 2**256-2**32-2**9-2**8-2**7-2**6-2**4-1
def subcoords(c1, c2):
    return ((c1[0] * c2[1] - c2[0] * c1[1]) % P, c1[1] * c2[1] % P)


def mulcoords(c1, c2):
    return (c1[0] * c2[0] % P, c1[1] * c2[1] % P)


def prepare_data(max_int):
    longs = [random.randint(0, max_int) for x in range(NUM)]
    def shuffled():
        l = longs[:]
        random.shuffle(l)
        return l
    return zip(zip(shuffled(),shuffled()), zip(shuffled(),shuffled()))

for max_int in (sys.maxint, 2**256):
    print '----- max_int:%r -------' % max_int
    data = prepare_data(max_int)
    s = time.time()
    for c1,c2 in data:
        mulcoords(c1,c2)
    print 'mulcoords took', time.time()-s

    s = time.time()
    for c1,c2 in data:
        subcoords(c1,c2)
    print 'subcoords took', time.time()-s

"""
(default) ~/dev/ethereum/pyethereum/tmp (git)-[master] % python perftest.py
----- max_int:9223372036854775807 -------
mulcoords took 0.134918928146
subcoords took 0.182271957397
----- max_int:115792089237316195423570985008687907853269984665640564039457584007913129639936L -------
mulcoords took 0.283133983612
subcoords took 0.346531867981
(default) ~/dev/ethereum/pyethereum/tmp (git)-[master] % pypy perftest.py
----- max_int:9223372036854775807 -------
mulcoords took 0.0226409435272
subcoords took 0.0327508449554
----- max_int:115792089237316195423570985008687907853269984665640564039457584007913129639936L -------
mulcoords took 0.38102889061
subcoords took 0.406507015228

"""