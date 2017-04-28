#!/usr/bin/python
"""
Author: Sa Pham saphi070@gmail.com
All operation with matrix
"""


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
        matrixC = []
        for row in range(len(matrixA)):
            row_in_C = []
            for col in range(len(matrixA[row])):
                a = int(matrixA[row][col], 2)
                b = int(matrixB[row][col], 2)
                result_multip = format((a * b) % modulo, '08b')
                row_in_C.append(result_multip)
            matrixC.append(row_in_C)
        return matrixC



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
