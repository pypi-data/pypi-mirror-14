# -*- coding: cp936 -*-
"""
����Yag_libģ�飬�ṩ��һ����ΰprint_list()�ĺ�������������������Ǵ�ӡ�б������п��ܰ���
Ƕ���б�
"""
def print_list(the_list):
    """
    ���Ǹ�һ���������ݹ����Ƕ���б��е�����Ԫ�أ�ÿ��Ԫ�ض�ռһ��
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_list(each_item)
        else:
            print(each_item)
