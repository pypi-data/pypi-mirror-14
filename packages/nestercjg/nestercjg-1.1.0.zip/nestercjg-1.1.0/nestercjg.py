"""This is the "nestercjg.py" module, and it prvides one function called
print_lol() which prints lists that may or may not include nested lists"""
def print_lol(the_list, indent):
        """This function takes a positional argument called "the_list", which
        is any Python list (of, possibly, nested lists), and a second argument
	"indent" to indicate number of tabs to be used to indent each sub-list.
	Each data item in the provided list is (recursively) printed to the 
	screen on its own line"""
        for each_item in the_list:
                if isinstance(each_item, list):
                        if indent == 0:
                                print_lol(each_item, 0)
                        else:
                                print_lol(each_item, indent+1)
                else:
                        for num in range(indent):
                                print("\t", end='')
                        print(each_item)
