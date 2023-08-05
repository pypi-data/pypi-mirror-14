def hanshu(the_liebiao,indent = False,level=0):
    """这个函数取一个目标标识参数，还有个变量，被赋了缺省值，名为the_liebiao，这可以是任何python列表（也可以是包含嵌套列表的列表）。所指定的列表中的每个数据项会（递归的）输入到屏幕上，每一个数据项各占一行。"""
    for each_item in the_liebiao:
        if isinstance(each_item,list):
            hanshu(each_item,indent,level+1)
        else:
            if indent:
               """每嵌套一次就进行一次缩进,你不想也行"""
               for tab_stop in range(level):
                   """print("\t"*level,end='')"""
                   print("\t",end='')
            print(each_item)

			

