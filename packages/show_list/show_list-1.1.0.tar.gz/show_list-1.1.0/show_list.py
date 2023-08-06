"""fuck you python"""
def print_lol(the_list, indent=false, level=0):
    """do you happy"""
    for the_item in the_list:
        if isinstance(the_item, list):
            print_lol(the_item, indent, level)
        else:
            if indent:
                for i in range(level):
                    print("\t", end='')
            print(the_item)
