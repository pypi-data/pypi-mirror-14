def print_list(a_list):
    for str in a_list:
        if isinstance(str,list):
            print_list(str)
        else:
            print(str)
