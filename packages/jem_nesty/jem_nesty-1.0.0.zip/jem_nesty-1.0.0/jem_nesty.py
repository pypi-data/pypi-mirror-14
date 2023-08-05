""" This Nesty module contains the print_lol function which lets you display
the data in list and inner lists of the list"""

def print_lol(arg1):
        """This print_lol function takes a list in and checks for
        lists with in lists and processes the inner list by calling the same
        function recursively and if it is not an inner list then it simple prints
        the data"""
        for each_item in arg1:
                if isinstance(each_item,list):
                        print_lol(each_item)
                else:
                        print(each_item)
