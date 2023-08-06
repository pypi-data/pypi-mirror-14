'''这是"nester.py"模块，提供了一个名为print_lol()的函数，这个函数的作用是打印列表，
其中有可能包含(也不能不包含)嵌套列表'''
def print_lol(the_list):
    '''这个函数取一个位置函数，名为“the_list”,这可以是任何python列表(也可以是包含
嵌套列表的列表)。所制定的列表的每一个数据项会（递归的）输出到屏幕上，各数据项各占一行。'''
    for each_list in the_list:
        if isinstance(each_list,list):
            print_lol(each_list)
        else:
            print(each_list)
