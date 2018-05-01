#
#  Abstract Algebra: Theory and Applications
#  Chapter 2, Programming Exercise #2
#
#  The Ackermann function
#
#        A(0, y) = y+1
#      A(x+1, 0) = A(x, 1)
#    A(x+1, y+1) = A(x, A(x+1, y))
#


from __future__ import division
import unittest
from math import sqrt
from math import floor
import time


def ack_recursive(m, n):
    '''
    implements recursively the Ackerman function
    >>> ack_recursive(0, 4)
    5
    '''
    if (m==0):
        return n+1
    else:
        if (n==0):
            return ack_recursive(m-1, 1)
        else:
            return ack_recursive(m-1, ack_recursive(m, n-1))

def ack_non_recursive(m, n):
    '''
    implements non-recursively the Ackerman function
    >>> ack_non_recursive(3, 4)
    125
    '''    
    stack = []
    stack.append((m, n))
    while True:
        m, n = stack.pop()
        r = None
        if (m==0):
            r = n+1
        else:
            if (n==0):
                stack.append((m-1, 1))
            else:
                stack.append((m-1, 'x'))
                stack.append((m  , n-1))
        if (not r == None):
            if (len(stack)==0):
                return r
            else:
                m, n = stack.pop()
                assert n=='x'
                stack.append((m, r))
    
    
        

class AckermannTestCases(unittest.TestCase):
    def test_1_recursive_and_non_recursive(self):
        print 'entering [test_1_recursive_and_non_recursive]: takes about half a minute'
        for ack in [ack_recursive, ack_non_recursive]:
            for m, n, r in [(0, 0, 1), (1, 1, 3), (2, 2, 7), (3, 1, 13), (3, 2, 29), (3, 3, 61), (3, 4, 125), (4, 0, 13)]:
                self.assertEquals(ack(m, n), r)
        for n in range(5, 11):
            self.assertEquals(ack(3, n), 2**(n+3)-3)

                
        
        
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
