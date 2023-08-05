"""This is the "nester.py" module and it provides one function called print_lol()
    which prints lists that may or may not include nested lists, The second arg named 'level' is used to insert tab to the nestde list"""

def print_lol(the_list, indent = False ,level = 0):
    """This function takes one positional argument called "the list", which
        is any Python list(of - possibly - nested lists). Each data item in the
        provided list is (recursively) printed to the screen on it's own line"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,indent, level + 1)
        else:
            if indent:
	        for tab_stop in range(level):
                    print("\t", end=' ')
            print(each_item)

