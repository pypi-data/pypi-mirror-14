"""This is the "listitems.py" module, it provides one function called print_listofitems() which prints lists and the nested lists within them"""
def print_listitems(the_list, level=0):
    """This function takes a positional argument called "the_list", which is any Python list(of, possibly, nested lists). Each data item in the provided list is (recursively) printed to the screen on a new line."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_listitems(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
