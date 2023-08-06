"""This is the "nestercjg.py" module, and it provides one function called
print_lol() which prints lists that may or may not include nested lists"""
def print_lol(the_list, indent=False, level=0):
        """This function takes a positional argument called "the_list", which
        is any Python list (of, possibly, nested lists), and 2 optional
        arguments: "indent" which is a Boolean to indicate if indentation
        is required, and "level" to indicate number of tabs to be used to
        indent each sub-list. Each data item in the provided list is
        (recursively) printed to the screen on its own line"""
        for each_item in the_list:
                if isinstance(each_item, list):
                        print_lol(each_item, indent, level+1)
                else:
                        if indent == True:
                                for num in range(level):
                                        print("\t", end='')
                        print(each_item)
