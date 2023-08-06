# This is the nester module, simply 
# for studying the upload onto PyPI and 
# how to use it inside own computer.

def print_lol(the_list, indent=False, level=0):
    # This function is for printing all 
    # items inside a list, even the items 
    # in nested lists.
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print ("\t", end ='')
            print(each_item)
