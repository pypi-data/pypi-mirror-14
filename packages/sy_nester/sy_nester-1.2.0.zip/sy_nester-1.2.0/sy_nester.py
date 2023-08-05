"""这是“nester.py模块”，提供了一个名为print_lol()的函数，这个函
数作用是用来打印列表，其中有可能包含（也有可能不包含）嵌套列表"""
def print_lol (the_list, level = 0):
        """将列表的中的每个数据项（包括嵌套列表的数据项）递归的输出
        在屏幕上，每个数据各占一行"""
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item, level+1)
                else:
                        for tab_stop in range(level):
                                print("\t", end='')
                        print(each_item)
