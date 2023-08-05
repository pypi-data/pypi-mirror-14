"""This is the 'simple_nester.py' module and it provides one function called print_lol()
which prints lists that may or may not include nested lists."""
def print_lol(the_list, indent=False, level=0):
    """This function takes one positional argument called 'the list', which is any
        python list (of - possibly - nested lists). Each data item in the provided
        list is (recursively) printed to the screen on it's own line.
        A second argument called 'indent' is used to invoke tab-stops or not.
        A Third argument called 'level' is used to insert tab-stops when a nested
        list is encounterd if the indent value True."""
    for each_flick in the_list:
        if isinstance(each_flick, list):
            print_lol(each_flick, indent, level + 1)
        else:
            if indent:
                print('\t'*level, end='')
            print(each_flick)

# if __name__ == '__main__':
#     cast = ['Palin', 'Cleese', 'Idle', 'Jones', 'Gilliam', 'Chapman']
#     cast.append(['Tom', 'Jerry'])
#     cast.append('Joy')
#     print_lol(cast, True)
    
