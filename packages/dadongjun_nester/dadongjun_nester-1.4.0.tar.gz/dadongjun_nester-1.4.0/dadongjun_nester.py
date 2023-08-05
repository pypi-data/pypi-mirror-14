"""This is the dadongjun_nester.py module, it provides one function called
print_lol(), which prints lists that may or may not include nested lists."""
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """This function takes a positional argument called the_list, which is
    any Python list (or nested lists). Each data in the provide list is printed
    to the screen on its own line.
    A second argument called indent controls whether or not True to switch on.
    A third argument called level (which defaults to 0) is used to insert
    tab_stops when a nested list is encountered.
    A fourth argument has the default value sys.stdout"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
            print(each_item, file=fh)
