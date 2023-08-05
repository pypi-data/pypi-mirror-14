"""This is the "listprinting.py" module and it provides one function called
list_printing() which prints lists that may or may not include nested lists."""
def list_printing(the_list):
    """This function takes one positional argument called "the_list", which
is any Python list (or - possibly - nested lists). Each data item in the
provided list is (recurcively) printed to the screen on it's own line."""
    for each_item in the_list:
        if isinstance(each_item, list):
            list_printing(each_item)
        else:
            print(each_item)
