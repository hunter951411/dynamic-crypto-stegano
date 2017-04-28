#!/usr/bin/python
"""
Author: Sa Pham saphi070@gmail.com
Perform encrypt or decrypt text
"""
from utils import genkey
from utils import matrixoperation
from common import log
LOG = log.setup_log(__name__)


class Crypto(object):
    def __init__(self, text, key):
        self.text = text
        self.key = key
        self.matrix = matrixoperation.MatrixOperations()
        self.sub_keys = self.get_sub_keys()

    def conver_string_to_matrix(self, text):
        """
        Input: string with 16 charaters
        Output: Matrix 4*4
        """
        text = [format(ord(x), '08b') for x in text]
        return [[text[i + 3*j] for i in range(4)] for j in range(4)]

    def get_sub_keys(self):
        _gen = genkey.GenerateKeys(K=self.key)
        sub_keys = _gen.generate_sub_keys()
        if not sub_keys:
            LOG.error('The master key has length %r, expected 32',
                      len(self.key))
            exit(0)
        else:
            return sub_keys

    def encrypt(self):
        C = []
        for count in range(len(self.text)/16):
            sub_p = ''
            if (count+1)*16 < len(self.text):
                sub_p = self.text[count*16:(count+1)*16]
            else:
                extra = len(self.text) - count*16
                sub_p = self.text[count*16:] + ' ' * extra

            P = self.conver_string_to_matrix(sub_p)
            for i in range(len(self.sub_keys)):
                P1 = self.matrix.multiple(matrixA=self.sub_keys[i],
                                          matrixB=P,
                                          modulo=127)
                P = P1
            for i in range(len(self.sub_keys)):
                P2 = self.matrix.stir(P)
                P3 = self.matrix.xor(matrixA=self.sub_keys[i],
                                     matrixB=P2)
                P = P3
            C += P
        return C

    # def decrypt(self):


if __name__ == '__main__':
    key = '778b9e660d5b8c9d7247a1194b3fsthb'
    plain_text = 'repository from the command line'
    print "======================"
    print "[-] Master key ", key
    print "**********************"
    print "[-] Plain text ", plain_text

    c = Crypto(key=key,
               text=plain_text)
    C = c.encrypt()
    print "+++++++++++++++++++++"
    print "[+] Encrypted to binary ", C
