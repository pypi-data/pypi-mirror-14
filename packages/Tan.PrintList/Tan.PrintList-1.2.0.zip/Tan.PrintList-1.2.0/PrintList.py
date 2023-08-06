#这个函数可以遍历整个列表并打印每一项
def PaintList (the_list,Level=0):
    for k in the_list:
        if isinstance(k,list):
            PaintList(k,Level+1)
        else:
            for tab_stop in range(Level):
                print("\t",end='')
            print(k)
