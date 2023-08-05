# -*- coding: utf-8 -*-
"""
Created on Sun Mar 06 10:41:58 2016

This is the "nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists.
"""
def print_lol(the_list,level=0):
    """This function takes one positional argument called "the list",which is 
    any python list.
    """
    for each_tiem in the_list:
        if isinstance(each_tiem,list):
            print_lol(each_tiem,level)
        else:
            for tab_stop in range(level):
                print("\t")
            print(each_tiem)
