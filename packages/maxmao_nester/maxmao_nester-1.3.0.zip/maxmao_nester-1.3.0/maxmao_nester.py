def print_lol(the_list,level=0,indent=false):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1,indent)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",end='')
            print(each_item)
        
    
#just for fun
