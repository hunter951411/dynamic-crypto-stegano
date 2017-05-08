#!/usr/bin/python
"""
Author: Sa Phi saphi070@gmail.com
Perform embed and retriev binary to/from image
"""
import sys
import argparse
import crypto
import math
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

def start_embed(plaintext, key, image_embed, image_retriev):
    print "Embed binary in picture"
    print "+++++++++++++++++++++++"
    s = Stegano(image_embed)
    binary = []
    c = crypto.Crypto(key=key,
               text=plaintext)
    C = c.encrypt()
    # Change binary in C to bits in binary
    [[[[binary.append(int(l)) for l in k]for k in j]for j in i]for i in C]
    b = s.embed(binary=binary)
    print "======================="
    print "Write result in image after.png"
    with open(image_retriev, 'wb') as f:
        f.write(bytearray(b))
    print "***********************"


def start_retriev(key, image_retriev):
    print "Perform retriev binary in image after.png"
    s = Stegano(image_retriev)
    b = s.retriev()
    C = []
    LIST_BINARY = []
    # Change bits to binary
    for i in range(0, len(b), 8):
        exp = 7   # exp: 7 -> 1
        sum = 0   # sum is decimal of 8 bit sequent 
        for j in b[0+i:8+i]:
            sum = j * math.pow(2,exp) + sum
            exp = exp-1
        binary = format(int(sum), '08b')
        LIST_BINARY.append(binary)
    for i in range(0, len(LIST_BINARY), 4):
        LIST_SPLIT = []
        [LIST_SPLIT.append(j) for j in LIST_BINARY[0+i:4+i]]
        C.append(LIST_SPLIT)
    p = crypto.Crypto(key=key,
               text=[C])
    P = p.decrypt()
    print "Result: Data Embed is: ", P    


def main():
    parser = argparse.ArgumentParser(description="Dynamic Crypto Stegano Daemon")
    parser.add_argument('-i','--image_embed',dest='image_embed',required=True,help='Put your image you want embed data into it',metavar='')
    parser.add_argument('-o','--image_retriev',dest='image_retriev',required=True,help='Put your image you want embed data into it',metavar='')
    parser.add_argument('-k','--key',dest='key',required=True,help='Key use to encrypt plaintext',metavar='')
    parser.add_argument('-t','--plaintext',dest='plaintext',required=True,help='Plain text embed private into image',metavar='')
    args = parser.parse_args()
    ans=True
    while ans:
        print ("""
        1.Embed plaintext in picture
        2.Perform retriev plaintext in image
        3.Exit/Quit
        """)
        number_select=input("What would you like to do?" )
        if number_select==1: 
            print("\nEmbed plaintext in picture")
            start_embed(args.plaintext, args.key, args.image_embed, args.image_retriev)
            ans=True 
        elif number_select==2:
            print "\n Perform retriev plaintext in image"
            start_retriev(args.key, args.image_retriev)
            ans=True  
        elif number_select==3:
            print("\n Goodbye")
            ans=False
        elif ans !="":
            print("\n Not Valid Choice Try again")


if __name__ == '__main__':
    main()
