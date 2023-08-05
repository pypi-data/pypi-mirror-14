"""This is the “nester.py" module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists."""
def print_lol(the_list, indent = false, level = 0, fh = sys.stdout):
    """This function takes a positional argument called “the_list", which is any
Python list (of, possibly, nested lists). Each data item in the provided list
is (recursively) printed to the screen on its own line."""
    for each_list in the_list:
         if isinstance(each_list, list):
            print_lol(each_list, indent, level + 1, fh)
         else:
             if indent:
                 for tab_stop in range(level):
                    print("\t", end = '', file = fh)
             print(each_list, file = fh)
