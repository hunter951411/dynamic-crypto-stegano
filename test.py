import numpy
import math
from numpy import matrix
from numpy import linalg

def modMatInv(A,p):
    # Finds the inverse of matrix A mod p
    n = len(A)
    A = matrix(A)
    adj = numpy.zeros(shape=(n, n))
    for i in range(0, n):
        for j in range(0, n):
            remove_row_col = minor(A, j, i)
            det_after_remove = linalg.det(remove_row_col)
            adj[i][j] = ((-1)**(i+j)*int(round(det_after_remove))) % p
    detA = linalg.det(numpy.array(A))
    inv_detA = modInv(int(round(detA)), p)
    return (inv_detA * adj) % p


def modInv(a,p):
    """
    """
    # Finds the inverse of a mod p, if it exists
    for i in range(1, p):
        if (i*a) % p == 1:
            return i
    raise ValueError(str(a)+" has no inverse mod "+str(p))


def minor(A,i,j):
    # Return matrix A with the ith row and jth column deleted
    A = numpy.array(A)
    minor = numpy.zeros(shape=(len(A)-1, len(A)-1))
    p = 0
    for s in range(0, len(minor)):
        if p == i:
            p = p+1
        q = 0
        for t in range(0, len(minor)):
            if q == j:
                q = q+1
            minor[s][t] = A[p][q]
            q = q+1
        p = p+1
    return minor

def main():
    A = [[11, 8], [3, 7]]
    print A
    B = modMatInv(A, 26)
    print B
if __name__ == '__main__':
    main()
