# 定义递归函数(Python 3中默认递归深度不能超过100)
# 增加一个缺省值level = 0使得‘level’变成一个可选的参数
def printListMethod(moviesList, indent = False, level = 0):
    
    for each_item in moviesList:
        if isinstance(each_item, list):
            printListMethod(each_item, indent, level + 1)
        else:
            if indent:
                for teb_stop in range(level):
                    print("\t",end='')
            print (each_item)
