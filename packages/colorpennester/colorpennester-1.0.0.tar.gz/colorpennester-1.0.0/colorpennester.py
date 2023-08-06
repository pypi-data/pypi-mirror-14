# 定义递归函数(Python 3中默认递归深度不能超过100)
def printListMethod(moviesList):
    
    for each_item in moviesList:
        if isinstance(each_item, list):
            printListMethod(each_item)
        else:
            print (each_item)