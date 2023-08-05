def print_lol(a_list,level):
    for name in a_list:
        if isinstance(name,list):
            print_lol(name,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(name)
