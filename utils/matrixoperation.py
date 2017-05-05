#!/usr/bin/python
"""
Author: Sa Pham saphi070@gmail.com
All operation with matrix
"""
import modulo
import numpy
import copy

from numpy import linalg
from numpy import matrix


class MatrixOperations(object):
    def stir(self, matrixA):
        """
        Stir Operation in matrix A
        """
        matrixB = []
        for row in range(len(matrixA)):
            row_in_B = []
            for col in range(len(matrixA[row])):
                val = ''
                for i in range(4):
                    val += matrixA[row][i][col*2:col*2+2]
                row_in_B.append(val)
            matrixB.append(row_in_B)
        return matrixB

    def xor(self, matrixA, matrixB):
        """
        XOR operation
        matrixC = matrixA xor matrixB
        For example if A=10101011 and B=10011001,
            then C= XOR (A, B) = 00110010
        """
        matrixC = []
        if len(matrixA) != len(matrixB):
            return False
        else:
            for row in range(len(matrixA)):
                row_in_C = []
                for col in range(len(matrixA[row])):
                    a = int(matrixA[row][col], 2)
                    b = int(matrixB[row][col], 2)
                    result_xor = format(a ^ b, '08b')
                    row_in_C.append(result_xor)
                matrixC.append(row_in_C)
        return matrixC

    def multiple(self, matrixA, matrixB, modulo):
        """
        Multiple matrixA with matrixB in module
        Example: matrixC = (matrixA * matrixB) mod 127
        return matrixC
        """
        matrixC = numpy.dot(numpy.array(matrixA),
                            numpy.array(matrixB))
        matrixC = matrixC % modulo
        return matrixC

    def convert_matrix_bin_to_decimal(self, matrixA):
        """
        Input: matrix A use binary
        output: matrix B use decimal
        """
        matrixB = copy.deepcopy(matrixA)
        for row in range(len(matrixB)):
            for col in range(len(matrixB[row])):
                matrixB[row][col] = int(matrixB[row][col], 2)
        return matrixB

    def convert_matrix_demcimal_to_bin(self, matrixA):
        """
        Input: matrix A use decimal
        Output: matrix A use binary
        """
        n_row = len(matrixA)
        n_col = len(matrixA[0])
        matrixB = []
        for i in range(n_row):
            row_in_B = []
            for j in range(n_col):
                row_in_B.append('{0:08b}'.format(int(matrixA[i][j])))
            matrixB.append(row_in_B)
        return matrixB

    def determinant(self, matrixA):
        """
        Compute determinant of matrix 4*4
        """
        matrixA = self.convert_matrix_bin_to_decimal(matrixA=matrixA)
        m = numpy.array(matrixA)
        return numpy.linalg.det(m)

    def inverse_matrix_with_modulo(self, A, p):
        """
        Finds the inverse of matrix A mod p
        """
        n = len(A)
        A = matrix(A)
        adj = numpy.zeros(shape=(n, n))
        for i in range(n):
            for j in range(n):
                minor_matrix = self.minor(A, j, i)
                det_minor = linalg.det(minor_matrix)
                adj[i][j] = ((-1)**(i+j)*int(round(det_minor))) % p
        detA = linalg.det(numpy.array(A))
        inv_detA = modulo.Modulo.modInv(int(round(detA)), p)
        return (inv_detA * adj) % p

    def minor(self, A, i, j):
        # Return matrix A with the ith row and jth column deleted
        A = numpy.array(A)
        minor = numpy.zeros(shape=(len(A)-1, len(A)-1))
        p = 0
        for s in range(len(minor)):
            if p == i:
                p = p+1
            q = 0
            for t in range(len(minor)):
                if q == j:
                    q = q+1
                minor[s][t] = A[p][q]
                q = q+1
            p = p+1
        return minor


if __name__ == '__main__':
    A = [['00111001', '01100101', '00110110', '00110110'],
         ['01100010', '00111000', '01100011', '00111001'],
         ['00110100', '00110111', '01100001', '00110001'],
         ['01100010', '00110011', '00111001', '00110010']]
    m = MatrixOperations()
    B = m.stir(A)
    print B
    C = m.xor(A, B)
    print C
