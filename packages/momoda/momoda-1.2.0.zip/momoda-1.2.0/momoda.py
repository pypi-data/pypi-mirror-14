
"""这是“nester.py”模块，提供了一个名为hanshu（）的函数，这个函数的作用是打印列表，其中有可能包含（也有可能不包含）嵌套列表"""
def hanshu(the_liebiao,level=0):
    """这个函数取一个目标标识参数，还有个变量，被赋了缺省值，名为the_liebiao，这可以是任何python列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归的）输入到屏幕上，每一个数据项各占一行。"""
    for each_item in the_liebiao:
        if isinstance(each_item,list):
            hanshu(each_item,level+1)
        else:
            """每嵌套一次就进行一次缩进"""
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)

			

