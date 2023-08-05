'''这是一个模块，可以打印列表，其中可能包含嵌套列表'''
def print_list(the_list):
    """这个函数取一个位置参数the_list，他可以是任何列表，该列表中的每个数据都会递归地打印到屏幕上，各数据项各占一行"""
    for each_item in the_list:
        if isinstance (each_item,list):
            print_list(each_item)
        else:
                print(each_item)
    
