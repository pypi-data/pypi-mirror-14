#!/usr/bin/env python

from argparse import ArgumentParser
from time import time
import os


def main():
    args = ArgumentParser()
    args.add_argument('file', help="The file to test the xattr on")
    args.add_argument("-c", "--count", help="the ammount of times to repeat setting a xattr (default: %(default)s)",
        default=100000, type=int)
        
    options = args.parse_args()
    
    start = time()
    for i in range(options.count):
        os.setxattr(options.file, b'user.myval', b'yes')
    end = time()
    
    period = end - start
    
    print("Compleated {} setxattr's in {:.3f}s".format(options.count, period))
    print("{:.0f}/s setxattrs performed".format(options.count/period))

    print()

    start = time()
    for i in range(options.count):
        os.getxattr(options.file, b'user.myval')
    end = time()
    
    period = end - start
    
    print("Compleated {} getxattr's in {:.3f}s".format(options.count, period))
    print("{:.0f}/s setxattrs performed".format(options.count/period))


if __name__ == "__main__":
    main()
