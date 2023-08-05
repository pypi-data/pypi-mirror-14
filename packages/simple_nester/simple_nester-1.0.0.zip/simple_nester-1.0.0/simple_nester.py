"""This is the 'simple_nester.py' module and it provides one function called print_lol()
which prints lists that may or may not include nested lists."""
def print_lol(the_list):
    """This function takes one positional argument called 'the list', which is any
        python list (of - possibly - nested lists). Each data item in the provided
        list is (recursively) printed to the screen on it's own line."""
    for each_flick in the_list:
        if isinstance(each_flick, list):
            print_lol(each_flick)
        else:
            print(each_flick)
