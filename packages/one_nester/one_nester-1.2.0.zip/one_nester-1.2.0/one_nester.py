"""这是one_nester模块，有一个名为print_list的函数，函数作用是打印列表所有元素，其中列表可为复杂嵌套式列表;第二个参数是当元素中有嵌套列表的时候，控制制表符数量"""

def print_list(the_list,level=0):
    """函数中有个参数the_list，通过判断是否列中元素为嵌套列表，若为嵌套列表则递归，对嵌套列表元素进行输出，若列表中元素不为列表则直接输出"""
    for each_list in the_list:
        if isinstance(each_list,list):
            print_list(each_list,level+1)
        else:
            for each_tab in range(level):
                print("\t",end=' ')
            print(each_list)
