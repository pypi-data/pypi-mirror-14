"""这是"gynester.py"模块，提供了一个名为print_lol()的函数,这个函数的作用是打印列表，
其中有可能包含(也可能不包含)嵌套列表。"""
def print_lol(list_item):
    """这个函数取一个位置参数，名为"list_item",这可以是任何Python列表(也可以是包
    含嵌套列表的列表)。所指定的列表中的每个数据项会(递归地)输出到屏幕上，各数据
    项各占一行"""
    for each_item in list_item:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
