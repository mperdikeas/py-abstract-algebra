#
#  Abstract Algebra: Theory and Applications
#  Chapter 2, Programming Exercise #1
#
#  The Sieve of Eratosthenes (various implementatons)
#
#  - the [sieve_with_map] is by far the most performant but requires
#    linear space
#
#  - the [naive_implementation] is somewhere in the middle between
#    [sieve_with_lists] and [sieve_with_map] but it only requires constant
#    space, hence it's not so bad
#


from __future__ import division
import unittest
from math import sqrt
from math import floor
import time

def inc(n):
    return n+1

def sieve_with_lists(n):
    '''
    returns all primes <= n
    >>> sieve_with_lists(2)
    [2]
    >>> sieve_with_lists(4)
    [2, 3]
    >>> sieve_with_lists(10)
    [2, 3, 5, 7]

    '''
    if n<=1:
        return []
    rv = xrange(2, inc(n))
    for i in range(2, inc(int(floor(sqrt(n))))):
        # we filter out the multiples of a number for multiples 2, 3, ... i.e. not the number itself
        rv = filter(lambda x: x == i or x % i != 0, rv)
    
    return list(rv)

def prepare_membership(n):
    if (n<2):
        raise ValueError('n has to be >=2 (was: {})'.format(n))
    single_element_maps = map(lambda x: {x: True}, xrange(2, inc(n)))
    rv = {}
    for single_element_map in single_element_maps:
        rv.update(single_element_map)
    return rv
    

def sieve_with_map(n):
    rv = prepare_membership(n)
    for i in range(2, inc(int(floor(sqrt(n))))):
        for j in range(2, inc(n // i)):
            ij = i*j
            rv[ij]=False
    return [k for k, v in rv.items() if v==True]


def naive_implementation(n):
    rv = []
    for i in xrange(2, inc(n)):
        divided_by_some = False
        for j in xrange(2, inc(int(floor(sqrt(i))))):
            assert j < i
            if (i % j == 0):
                divided_by_some = True
                break
        if (not divided_by_some):
            rv.append(i)
    return rv



class PrepareMembershipTestCases(unittest.TestCase):

    def setup(self):
        pass
    
    def test_a(self):
        self.assertEquals(prepare_membership(2), {2: True})
        self.assertEquals(prepare_membership(5), {2: True, 3: True, 4: True, 5: True})        

class SieveTestCase(unittest.TestCase):
    def test_a(self):
        for sieve in [naive_implementation, sieve_with_lists, sieve_with_map]:
            self.assertEquals(sieve(2), [2])
            self.assertEquals(sieve(19), [2, 3, 5, 7, 11, 13, 17, 19])
            self.assertEquals(sieve(20), [2, 3, 5, 7, 11, 13, 17, 19])
            self.assertEquals(sieve(199), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199])
    def test_b(self):
        implementations = {naive_implementation: None, sieve_with_lists: None, sieve_with_map: None}
        N = 500000
        for sieve in implementations.keys():
            print('testing how fast {} is (this may take a while ...)'.format(sieve.__name__))
            t1 = time.time()
            sieve(N)
            t2 = time.time()
            implementations[sieve]=t2-t1
        for sieve in implementations.keys():
            print ('function [{}] was able to sieve up to (and including) {} in: {} secs'.format(sieve.__name__, N, implementations[sieve]))

            


                
        
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
