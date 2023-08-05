"""This is the standard way to include a multipe-line comment in you code"""

def print_lol(the_list):
    """
    'the_list' is the arguments, 'the_list' can be anyone,however the string or
    list or object
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else :
            print(each_item)
            
