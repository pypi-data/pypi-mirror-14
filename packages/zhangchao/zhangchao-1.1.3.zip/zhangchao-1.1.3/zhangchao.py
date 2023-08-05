'''
Created on 2016年3月15日

@author: zsuper
'''
def print_lol(the_list,indent=False,level=0):
    for each in the_list:
        if isinstance(each,list):
            print_lol(each,indent,level+1)
        else:
            if ident:
                for tap_stop in range(level):
                    print("\t",end='')
            print(each)
