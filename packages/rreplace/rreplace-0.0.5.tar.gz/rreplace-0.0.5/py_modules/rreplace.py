#!/usr/bin/env python
from public import *

def reverse(string):
    l = list(string)
    l.reverse()
    return "".join(l)

@public
def rreplace(string,old,new,count=None):
    """string right replace"""
    string = str(string)
    reversed = reverse(string)
    if count is None:
        count = -1
    reversed = reversed.replace(reverse(old),reverse(new),count)
    return type(string)(reverse(reversed))

if __name__=="__main__":
    print(rreplace("old_old","old","new",1)) # old_new


