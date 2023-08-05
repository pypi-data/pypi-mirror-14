"""
module for list utilities
"""
def print_lol(the_list, indent=False, level=0):
    """input: list object. can contain nested list
    output: print item from all lists
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                for number_of_tabs in range(level):
                    print("\t", end='')
            print(each_item)

