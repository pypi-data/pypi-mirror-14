"""This is the standard way to include a multipe-line comment in you code"""

def print_lol(the_list,level=0):
    """
    'the_list' is the arguments, 'the_list' can be anyone,however the string or
    list or object
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else :
            for num in range(level) :
            print(each_item)
            
