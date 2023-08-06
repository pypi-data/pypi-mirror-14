#这个函数可以遍历整个列表并打印每一项
#参数0：列表名
#参数1：是否缩进
#参数2：缩进宽度
#参数3：输出文件，默认屏幕
import sys
def PrintList (the_list,isindent=False,Level=0,outfile=sys.stdout):
    for k in the_list:
        if isinstance(k,list): #判别列表项是否还为一个列表
            PrintList(k,isindent,Level+1,outfile)
        else:
            if isindent:#是否缩进
                for tab_stop in range(Level):#缩进宽度
                    print("\t",end='',file=outfile)
            print(k,file=outfile)

