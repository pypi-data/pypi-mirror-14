# 定义递归函数(Python 3中默认递归深度不能超过100)
def printListMethod(moviesList, level):
    
    for each_item in moviesList:
        if isinstance(each_item, list):
            printListMethod(each_item,level + 1)
        else:
            for teb_stop in range(level):
                print("\t",end='')
            print (each_item)
