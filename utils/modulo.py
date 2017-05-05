#!/usr/bin/python
"""
Author: Sa Pham saphi070@gmail.com
Perform on modulo
"""

class Modulo(object):
    @staticmethod
    def modInv(a, p):
        """
        Finds the inverse of a mod p, if it exists
        """
        for i in range(1, p):
            if (i*a) % p == 1:
                return i
        raise ValueError(str(a)+" has no inverse mod "+str(p))
