""" This module nester.py() contains function to act on nested lists """

def print_nested_list(input_list):
    """This function acts on nested lists of upto 1000 nested levels and
    prints out the output on individual lines
    """
    for item in input_list:
        if isinstance(item,list):
            print_nested_list(item)
        else:
            print(item)