#! /usr/bin/env python3
# -*- coding: utf8 -*-

import sys

"""This is the module of "nester.py", it provides a function named print_lol(),the role of the function
is to print a list"""
def print_lol(the_list, indent=False, level=0, fn=sys.stdout):
    """The function takes a location parameter named "the_list" that is any list of python
    (Can also be a list containing nested lists).Each data item in the list specified will Recursive output 
    to the screen, and each data item for each.The second parameter named "level" is used to insert
    tab in a nested list. The third parameter named "indent" decides whether to open the indent.
    The fourth parameter named "fn" specifies the output file and when it isn't given, it will
    output to the screen"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fn)
        else:
            if indent:
                for tab in range(level):
                    print("\t", end='', file=fn)
            print(each_item, file=fn)

#"""Recursive function test.There gives a test list named "temp_list".
#If you run this file directly as main,it will run the following code,
#and use the function print_lol to recursive print the test list "temp_list"."""
#if __name__ == "__main__":
#    temp_list = [1, 32, 43, [12, 23, [123, 4321]], [2, 3, 4],[3, 5, 6, [1234, 234, 54, [23, 42, 43, 12, [23, 23, 2, 1231]]]]]
#    print_lol(temp_list, True)
