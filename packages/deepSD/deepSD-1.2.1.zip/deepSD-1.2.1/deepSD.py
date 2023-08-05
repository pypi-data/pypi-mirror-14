# Encoding:utf-8
__author__ = 'Dongdong.Su'

"""
    递归遍历列表的方法
"""
def print_lof(the_list,isSuo=True,level=0):
    for itr in the_list:
        if isinstance(itr, list):
            if isSuo:
                print_lof(itr,isSuo,level+1)
            else:
                print_lof(itr,isSuo)
        else:
            if isSuo:
                if level > 0:
                    for i in range(level):
                        print(" ")
                print(itr)
            else:
                print(itr)