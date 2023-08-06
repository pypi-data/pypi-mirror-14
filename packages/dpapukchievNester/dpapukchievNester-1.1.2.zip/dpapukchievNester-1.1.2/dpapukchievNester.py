'''This is the “nester.py" module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists.'''
def print_lol(the_list,indent = False,level=0):
    '''This function takes a positional argument called “the_list", which is any
Python list (of, possibly, nested lists). Each data item in the provided list
is (recursively) printed to the screen on its own line with the level indentation (optional).'''
    for each_item in the_list:
        if isinstance(each_item, list):
            if indent:
                print_lol(each_item,True,level+1)
            else:
                print_lol(each_item,False)
        else:
            if indent:
                for tab_stop in range(level):
                    print("-", end='')
            print(each_item)