# This is the nester module, simply 
# for studying the upload onto PyPI and 
# how to use it inside own computer.

def print_lol(the_list, level):
    # This function is for printing all 
    # items inside a list, even the items 
    # in nested lists.
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
		    print ("\t", end ='')
            print(each_item)
