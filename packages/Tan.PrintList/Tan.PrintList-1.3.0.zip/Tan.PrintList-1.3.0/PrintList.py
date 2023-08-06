#这个函数可以遍历整个列表并打印每一项
def PrintList (the_list,isindent=False,Level=0):
    for k in the_list:
        if isinstance(k,list):
            PrintList(k,isindent,Level+1)
        else:
            if isindent:
                for tab_stop in range(Level):
                    print("\t",end='')
            print(k)

