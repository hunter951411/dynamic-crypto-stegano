#!/usr/bin/python
"""
Author: Sa Pham saphi070@gmail.com
Generate all key for Encrypt or decrypt
"""
import copy
from common import log

LOG = log.setup_log(__name__)


class GenerateKeys(object):
    def __init__(self, K):
        self.K = self.convert_master_key(K)
        self.keys = self.generate_sub_keys()

    def convert_master_key(self, K):
        """
        Convert master key to two dimensional array
        Convert char in array to binary with length=8
        """
        if len(K) < 32:
            return False
        else:
            K = [format(ord(x), '08b') for x in K]
            return [[K[i + 7*j] for i in range(8)] for j in range(4)]

    def generate_sub_keys(self):
        """
        Generate 8 sub keys from master key
        """
        Keys = []
        for key_num in range(8):
            key = []
            if key_num % 4 == 0:
                for row in range(4):
                    key.append(self.K[row][key_num:(key_num+4)])
            else:
                if key_num < 4:
                    inter_key = copy.deepcopy(Keys[0])
                    key = self.inter_exchange(key=inter_key,
                                              index=key_num)
                else:
                    inter_key = copy.deepcopy(Keys[4])
                    key = self.inter_exchange(key=inter_key,
                                              index=(key_num-4))
            LOG.info('Generated Key %r: %s', key_num, str(key))
            Keys.append(key)
        return Keys

    def inter_exchange(self, key, index):
        """
        Exchange in subkey to generate other keys
        """
        for row in range(len(key)):
            for col in range(len(key[row])):
                if col == index:
                    temp = key[row][0]
                    key[row][0] = key[row][index]
                    key[row][index] = temp

        return key


if __name__ == '__main__':
    K = '778b9e660d5b8c9d7247a1194b39228b'
    dyn = DynamicCrypto(K)
    keys = dyn.keys
    for i in keys:
        print "Keys " + str(keys.index(i))
        print i
