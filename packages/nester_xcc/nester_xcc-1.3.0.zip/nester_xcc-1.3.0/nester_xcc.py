'''这是一个模块，可以打印列表，其中可能包含嵌套列表'''
def print_list(the_list,indent=False,level=0):
    """这个函数取一个位置参数the_list，他可以是任何列表，该列表中的每个数据都会递归地打印到屏幕上，各数据项各占一行;
    level参数用来在遇到嵌套列表时插入制表符，实现缩进打印。
    indent参数用来控制实现缩进的代码，默认为false，即不嵌套打印"""
    for each_item in the_list:
        if isinstance (each_item,list):
            print_list(each_item,indent,level+1)  #在每次递归调用函数时将level值增加1
        else:
            if indent:  #如果为真，则打印制表符；否则，不打印制表符
                for tab_stop in range(level):
                    print ('\t',end='')
            print(each_item)
    
