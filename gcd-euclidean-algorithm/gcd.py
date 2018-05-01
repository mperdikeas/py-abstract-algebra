#
#  Abstract Algebra: Theory and Applications
#  Chapter 2, Programming Exercise #3
#
#      Write a computer program that will implement the Euclidean algo-
#      rithm. The program should accept two positive integers a and b as input
#      and should output gcd(a, b) as well as integers r and s such that
#      gcd(a, b) = ra + sb.
#
#  That function is [gcd_extended]
#
#  The [gcd_core_recursive] and [gcd_core_nonrecursive] functions are alternative cores
#  that simply calculate the GCD of two numbers (they don't also return r and s). They
#  need to be plugged into the [create_gcd] function to generate the actual GCD implementation
#  However, only the [gcd_extended] function generates r and s values. The [create_gcd] function
#  which accepts the two cores simply returns the GCD and nothing else.
#
#  The [inc], [dec] and [euclidean_division] functions are utility functions that are used both
#  by the GCD cores and the extended GCD function



from __future__ import division
import unittest
from math import sqrt
from math import floor
import time

############################################
#                                          #
#    U T I L I T Y    F U N C T I O N S    #
#                                          #
############################################

def inc(n):
    return n+1

def dec(n):
    return n-1

# If we want the gcd function to also work for negative numbers, we have to 'fix' integer division in Python
# as they way it is implemented (for negative numbers) does not actually correspond to Euclidean division
# What I am doing below is to define Euclidean division according to the Raymond T. Boute definition
# (https://en.wikipedia.org/wiki/Modulo_operation). This is the definition that is more consistent with
# number theory as attested by the fact that the Euclidean GCD computation algorithm (that also produces,
# in addition to the GCD, the r and s values) works for negative numbers only with the Raymond T. Boute definition
# of Euclidean division.
def euclidean_division(a, b):
    '''
        Returns quotient and remainder of a divided by b according to the Euclidean division algorihm.
        >>> euclidean_division(10, 3)
        (3, 1)

        It fixes the built-in Python integer division implementation to ensure it also works for negative
        numbers. In particular the remainder has to always be a non-negative number less than the divisor.
        This is not observed in the default implementation of integer division in Python for the case of
        negative divisors (though it is implemented correctly for both positive and negative dividends)
        E.g.
        >>> -10 // -3
        3
        >>> -10 % -3
        -1
        
        ... which are not correct results in my book. In my view q=4 and r=2 is the correct answer.
        This is exactly what my implementation produces:
        >>> euclidean_division(-10, -3)
        (4, 2)
        >>> euclidean_division(100, -20)
        (-5, 0)
        >>> euclidean_division(-100, -20)
        (5, 0)
        >>> euclidean_division(-100, 20)
        (-5, 0)
        >>> euclidean_division(-100, 21)
        (-5, 5)
    '''

    # This is exactly the Raymond T. Boute definition of Euclidean
    # division as found in Wikipedia.
    def alternate_impl(a, b):
        def sgn(b):
            assert b!=0
            if (b>0):
                return 1
            else:
                return -1
        q = sgn(b)*floor(a/abs(b))
        r = a - abs(b)*floor(a/abs(b))
        return (q, r)

    # below follows my own implementation which I assert (just before returning)
    # that yields results identical to the Raymond T. Boute definition
    if (b==0):
        raise ValueError('b cannot be zero')
    rv = None
    if (b>0): # Python implements this correctly for positive divisors (for both positive and negative dividends), see: https://stackoverflow.com/a/19518866/274677
        rv = (a // b, a % b)
    else: # problems (in my view at least) arise with negative divisors.
        rv = ( a // b if (a % b == 0) else inc(a // b), 0 if (a % b) == 0 else (a % b)-b)
    assert rv[1] >= 0
    assert rv[1] < abs(b), 'when dividing {} by {} a remainder of {} was computed - which is not less than the absolute value of {} ({})'.format(a, b, rv[1], b, abs(b))
    assert b*rv[0]+rv[1]==a
    assert rv==alternate_impl(a, b)
    return rv


def is_int(a):
    return type(a)==type(0)


############################################
#                                          #
#    S I M P L E    G C D                  #
#    I M P L E M E N T A T I O N S         #
#                                          #
############################################

def gcd_core_recursive(a, b):
    q, r = euclidean_division(b, a)
    if (r==0):
        return a
    else:
        return gcd_core_recursive(r, a)



def gcd_core_nonrecursive(_a, _b):
    a, b = _a, _b
    while True:
        q, r = euclidean_division(b, a)
        if (r==0):
            return a
        else:
            b, a = a, r

def create_gcd(gcd_core):
    def gcd(a, b):
        if (a==0) and (b==0):
            raise ValueError('a and b cannot both be zero')
        if (a==0):
            return abs(b)
        if (not (is_int(a) and is_int(b))):
            raise ValueError('both a and b must be integers (were: {} and {} respectively)'.format(a, b))
        if (a<0 or b<0):
            return gcd(abs(a), abs(b))
        if (abs(a)>abs(b)):
            return gcd(b, a)
        else:
            return gcd_core(a, b)
    return gcd

class SimpleGCDTestCases(unittest.TestCase):

    def setup(self):
        pass

    def test_a(self):
        testCases = [(1, 1, 1), (13, 13, 13), (0, 5, 5), (4, 0, 4),
                     (5, 7, 1), (15, 20, 5), (100, 20, 20), (100, 35, 5), (100, 30, 10),
                     (20050, 100, 50), (192348002, 123424, 14), (10003032, 92, 4)]
        for gcd_core in [gcd_core_recursive, gcd_core_nonrecursive]:
            gcd = create_gcd(gcd_core)
            for testCase in testCases:
                _a, _b, x = testCase
                for (a, b) in [(_a, _b), (_a, -_b), (-_a, _b), (-_a, -_b), (_b, _a), (_b, -_a), (-_b, _a), (-_b, -_a)]:
                    g = gcd(a, b)
                    self.assertEquals(g, x, 'gcd({}, {}) was {} and not {} as expected'.format(a, b, g, x))




############################################
#                                          #
#    E X T E N D E D    G C D              #
#    I M P L E M E N T A T I O N           #
#                                          #
############################################
                    
def calculate_r_s(A, B, remainder_to_dividend_divisor_quotient, a):
    assert abs(B)>=abs(A)
    if (a==B):
        return (0, 1)
    if (a==A):
        return (1, 0)
    if len(remainder_to_dividend_divisor_quotient)==1:
        # edge case
        assert remainder_to_dividend_divisor_quotient.has_key(0)
        b, a2, q = remainder_to_dividend_divisor_quotient.get(0)
        assert a2 == a
        return (1, -(q-1))
    else:
        b, a2, q = remainder_to_dividend_divisor_quotient.get(a)
        r_s_of_b  = calculate_r_s(A, B, remainder_to_dividend_divisor_quotient, b)
        r_s_of_a2 = calculate_r_s(A, B, remainder_to_dividend_divisor_quotient, a2)
        return (r_s_of_b[0]-q*r_s_of_a2[0],
                r_s_of_b[1]-q*r_s_of_a2[1])
        
    
    
def gcd_extended(a, b):
    if (a==0) and (b==0):
        raise ValueError('a and b cannot both be zero')
    if (not (is_int(a) and is_int(b))):
        raise ValueError('both a and b must be integers (were: {} and {} respectively)'.format(a, b))    
    if (a==0):
        return (abs(b), 0, 1 if b>0 else -1)
    if (b==0):
        return (abs(a), 1 if a>0 else -1, 0)
    def _gcd_extended(a, b):
        assert abs(b)>=abs(a)
        A, B = a, b
        remainder_to_dividend_divisor_quotient = {}
        while True:
            q, r = euclidean_division(b, a)
            remainder_to_dividend_divisor_quotient.update({r: (b, a, q)})
            if (r==0):
                r, s = calculate_r_s(A, B, remainder_to_dividend_divisor_quotient, a)
                return (a, r, s)
            else:
                b, a = a, r
    if (abs(b)>=abs(a)):
        q, r, s = _gcd_extended(a, b)
    else:
        q, s, r = _gcd_extended(b, a)
    if (q < 0):
        return (abs(q), -r, -s)
    else:
        return (q, r, s)
            


class ExtendedGCDTestCases(unittest.TestCase):

    def setup(self):
        pass

    def test_a(self):
        gcd = gcd_extended
        for (a, b, g_expected) in [(2, 10, 2), (4, 10, 2), (6, 10, 2), (25, 100, 25), (25, 105, 5)
                                   , (100, 20050, 50), (123424, 192348002, 14), (92, 10003032, 4),
                                   (2, 1, 1), (1, 8, 1), (17, 1, 1), (1000007, 10003, 1), (0, 3, 3), (-92, 0, 92)
        ]:
            for (_a, _b) in [(a, b), (b, a), (-a, b), (a, -b), (-a, -b), (-b, a), (-b, -a), (-b, -a)]:
                g, r, s = gcd(_a, _b)
                assert g==g_expected, 'gcd({}, {}) calculated g = {} (was expecting: {})'.format(_a, _b, g, g_expected)
                assert g == r*_a+s*_b, 'gcd({}, {}) yielded the triplet ({}, {}, {}), which fails to satisfy {}={}*{}+{}*{}'.format(_a, _b, g, r, s, g, r, _a, s, _b)


def printMostComplexUseCase():
    a = 10003032
    b = 92
    
    (q, r, s) = gcd_extended(a, b)
    assert q == a*r+b*s
    print ('gcd({}, {}) = {}. Also: {} = {}*{} + {}*{}'.format(a, b, q, q, r, a, s, b))

printMostComplexUseCase()
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()

