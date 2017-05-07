#!/usr/bin/python
"""
Author: Sa Phi saphi070@gmail.com
Perform embed and retriev binary to/from image
"""
import sys
from common import log
LOG = log.setup_log(__name__)


class Stegano(object):
    def __init__(self, image):
        self.image = image

    def embed(self, binary):
        """
        Embed function
        """
        with open(self.image, 'rb') as image:
            f = image.read()
            b_array = bytearray(f)
        if len(b_array) < (3300 + len(binary)*8):
            LOG.error('The image is too small to process')
            sys.exit(0)
        # embed length of cipher binary
        length = format(len(binary), '08b')
        for i in range(0, len(length), 2):
            origin = format(b_array[3001+i/2], '08b')
            origin = origin[:6] + length[i] + origin[7:]
            origin = origin[:7] + length[i+1] + origin[8:]
            b_array[3001+i/2] = int(origin, 2)
        # embed cipher text
        next_index1 = 6
        next_index2 = 7
        for i in range(0, len(binary), 2):
            origin = format(b_array[3301 + i/2], '08b')
            origin = origin[:next_index1] + str(binary[i]
                                                ) + origin[next_index1+1:]
            origin = origin[:next_index2] + str(binary[i+1]
                                                ) + origin[next_index2+1:]
            b_array[3301+i/2] = int(origin, 2)
            if binary[i] == 0 and binary[i+1] == 0:
                next_index1 = 6
                next_index2 = 7
            elif binary[i] == 0 and binary[i+1] == 1:
                next_index1 = 7
                next_index2 = 6
            elif binary[i] == 1 and binary[i+1] == 0:
                next_index1 = 5
                next_index2 = 6
            elif binary[i] == 1 and binary[i+1] == 1:
                next_index1 = 6
                next_index2 = 5
        return b_array

    def retriev(self):
        """
        Retriev function
        """
        with open(self.image, 'rb') as image:
            f = image.read()
            b_array = bytearray(f)
        # Retriev length of embedded message
        length = ''
        for i in range(0, 4):
            embed_byte = '{0:8b}'.format(b_array[3001+i])
            length += embed_byte[6]
            length += embed_byte[7]
        length = int(length, 2)
        # Retriev message
        next_index1 = 6
        next_index2 = 7
        # binary
        binary = []
        for i in range(0, length, 2):
            embed_byte = format(b_array[3301+i/2], '08b')
            bin_1 = int(embed_byte[next_index1])
            bin_2 = int(embed_byte[next_index2])
            binary.append(bin_1)
            binary.append(bin_2)
            if bin_1 == 1 and bin_2 == 1:
                next_index1 = 6
                next_index2 = 5
            elif bin_1 == 1 and bin_2 == 0:
                next_index1 = 5
                next_index2 = 6
            elif bin_1 == 0 and bin_2 == 1:
                next_index1 = 7
                next_index2 = 6
            elif bin_1 == 0 and bin_2 == 0:
                next_index1 = 6
                next_index2 = 7
        return binary


def main():
    print "Embed binary in picture"
    print "+++++++++++++++++++++++"
    s = Stegano('before.png')
    binary = [1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1]
    print "Perform embed list binary {0} on image {1}".format(binary,
                                                              "before.png")
    b = s.embed(binary=binary)
    print "======================="
    print "Write result in image after.png"
    with open('after.png', 'wb') as f:
        f.write(bytearray(b))
    print "***********************"
    print "Perform retriev binary in image after.png"
    s = Stegano('after.png')
    b = s.retriev()
    print "Result: ", b


if __name__ == '__main__':
    main()
