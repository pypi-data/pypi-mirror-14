# -*- coding: cp936 -*-
"""
这是Yag_lib模块，提供了一个明伟print_list()的函数，这个函数的作用是打印列表，其中有可能包含
嵌套列表。
"""
def print_list(the_list):
    """
    这是个一函数用来递归输出嵌套列表中的所有元素，每个元素独占一行
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item)
        else:
            print(each_item)
