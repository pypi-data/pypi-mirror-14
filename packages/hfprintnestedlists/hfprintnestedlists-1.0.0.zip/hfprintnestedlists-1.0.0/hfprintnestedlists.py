''' This is the nester.py module, and it provides one function
called print_nested_list() which prints lists that may or may not have
include nested lists.'''

def print_nested_list(the_list):
    '''This function takes a positional argument called "the_list", which is any
       Python list(of, possibly, nested lists). Each data item in the provided
       list is (recursively) printed to the screen on its own line'''
    for each_item in the_list:
        if isinstance(each_item, list):
            print_nested_list(each_item)
        else:
            print(each_item)
