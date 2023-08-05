"""This is the "nester.py" module, and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""

import sys
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """This function takes one positional argument called "the_list" which
       is the Python list (of - possibly - nested lists). Each data item in the
       provided list is (recursively) printed to the screen on it's own line.
       A second argument called "indent" is used to determine whether the items in the list will be indented or not.
       A third argument called "level" is used to insert tab-stops when a nested list is encountered.
       A fourth argument called "fh" is used to indicate the place to write the data to, the default is the screen."""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
            print(each_item, file=fh)
