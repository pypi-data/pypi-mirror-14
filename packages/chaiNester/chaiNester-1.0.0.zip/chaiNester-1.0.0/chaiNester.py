def printNestedList(lst):
    for each_item in lst:
       if isinstance(each_item,list):
           printNestedList(each_item)
       else:
           print each_item