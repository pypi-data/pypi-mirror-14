def print_list(a_list,i):
    for str in a_list:
        if isinstance(str,list):
            print_list(str,i+1)
        else:
            for ii in range(i):
                print("\t",end='')
            print(str)
