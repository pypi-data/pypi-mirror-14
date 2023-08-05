"""
modole for list utilities
"""
def print_lol(the_list, indent_level):
    """input: list object. can contain nested list
    output: print item from all lists
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent_level + 1)
        else:
            for number_of_tabs in range(indent_level):
                print("\t", end='')
            print(each_item)

