""" This Nesty module contains the print_lol function which lets you display
the data in list and inner lists of the list"""

def print_lol(arg1,indent='false',level=0):
        """This print_lol function takes a list in and checks for
        lists with in lists and processes the inner list by calling the same
        function recursively and if it is not an inner list then it simply
        prints the data. The inner list is tab indented when the second argument
        is provided"""
        for each_item in arg1:
                if isinstance(each_item,list):
                        print_lol(each_item,indent,level+1)
                else:
                        if indent == 'true':
                                for num in range(level):
                                        print('\t',end='')
                        print(each_item)
