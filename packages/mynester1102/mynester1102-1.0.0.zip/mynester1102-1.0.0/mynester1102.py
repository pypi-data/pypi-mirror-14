def print_lol(a_list):
    for name in a_list:
        if isinstance(name,list):
            print_lol(name)
        else:
            print(name)
