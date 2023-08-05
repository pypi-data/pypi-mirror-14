"""这是一个打印list的函数，list中可以嵌套多层list，并可以设置参数选择打印时是否
缩进以及缩进多少个tab"""

def print_list(inputList,level=0,indent=False):
    """参数inputList代表传入的list；level表示缩进大小，默认为0；indent为是否缩进，
    默认为False不缩进"""
    for each_item in inputList:
        if isinstance(each_item,list):
            print_list(each_item,level+1,indent)
        else:
            if indent:
                for x in range(level):
                    print("\t")
                print(each_item)
            else:
                print(each_item)
                
