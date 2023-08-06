def print_rec(li,indent=False , level=0):
        for each_item in li:
                if isinstance(each_item,list):
                        print_rec(each_item,indent,level+1)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print('\t',end='')
                        print(each_item)
