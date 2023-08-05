# -*- coding: utf-8 -*-
"""
===============================================================================
AwesomeIP: IP for drying of a wetting phase
===============================================================================

"""
from numba import jit, void
import heapq as hq
import scipy as sp
from collections import namedtuple
from OpenPNM.Algorithms import GenericAlgorithm
from OpenPNM.Utilities.misc import tic, toc
Tinfo = namedtuple('queued_throat', ('order', 'number'))

tic()
a = sp.rand(20000000).tolist()
toc()
heap = []

#@jit
def poptop(heap, num):
    i = 0
    while i <= num:
        heap.pop()
        i += 1

@jit(void, (list, int))
def push(heap, val):
    hq.heappush(heap, val)

tic()
for i in range(0,100000):
    push(heap, a[i])
toc()

























