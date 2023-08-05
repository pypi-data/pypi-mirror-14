"""This is the "listsprint.py" module, and it provides one function called
custom_print() which prints lists that may or may not include nested lists."""

def custom_print(the_list):

    """This function takes a positional argument called "the_list", which is
    any Python list(of, possibly, nested lists). Each data item in the provided
    list is (recurcively) printed to the screen on its own line."""
    
    for each_item in the_list:
        if isinstance(each_item, list):
            custom_print(each_item)
        else:
            print(each_item)
