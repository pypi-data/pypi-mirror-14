#这个函数可以遍历整个列表并打印每一项
def PaintList (the_list):
    for k in the_list:
        if isinstance(k,list):
            PaintList(k)
        else:
            print(k)

