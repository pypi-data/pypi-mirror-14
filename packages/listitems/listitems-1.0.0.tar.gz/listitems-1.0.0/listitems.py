"""This is the "listitems.py" module, it provides one function called print_listofitems() which prints lists and the nested lists within them"""
def print_listitems(the_list):
    """This function takes a positional argument called "the_list", which is any Python list(of, possibly, nested lists). Each data item in the provided list is (recursively) printed to the screen on a new line."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_listitems(each_item)
        else:
            print(each_item) 
