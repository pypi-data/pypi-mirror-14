def print_lol(this_list,indent=False,leve=0):
    for each_item in this_list:
        if isinstance(each_item,list):
            print_lol(each_item,leve+1)
        else:
            if indent:
                for tab_space in range(leve):
                    print "\t",  
            print(each_item)
