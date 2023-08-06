# -*- coding: utf-8 -*-


import sys
import argparse

from . import helloworld


def main():
    parser = argparse.ArgumentParser(description='ADD YOUR DESCRIPTION HERE')
    parser.add_argument('-i', '--input', help='Input file name',
                        required=False)
    parser.add_argument('-o', '--output', help='Output file name',
                        required=False)
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        print(args)
        helloworld.show()

if __name__ == "__main__":
    main()
