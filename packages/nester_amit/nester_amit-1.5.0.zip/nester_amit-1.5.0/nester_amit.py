# This is the “nester_amit.py" module, and it provides one function called print_lol()
# which prints lists that may or may not include nested lists.


def print_lol(the_list, indent=False, level=0):
    # This function takes a positional argument called “the_list", which is any Python list (of, possibly, nested lists)
    # Each data item in the provided list is (recursively) printed to the screen on its own line.
    # Second argument called “level", which is optional, is used to insert tab-stops when a nested list is encountered.
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
                print(each_item)
            else:
                print(each_item)

muvis = [1,[2,[3,[4,[5,[6,7,8,[9,0]]]]]]]

print_lol(muvis,True,0)