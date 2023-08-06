"""fuck you python"""
def print_lol(the_list):
    """do you happy"""
    for the_item in the_list:
        if isinstance(the_item, list):
            print_lol(the_item)
        else:
            print(the_item)