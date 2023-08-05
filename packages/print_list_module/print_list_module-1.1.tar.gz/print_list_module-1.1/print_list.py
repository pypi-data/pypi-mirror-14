"""This is the module to print list items"""


def print_nested_list(the_list,indentlevel):
        """This print_nested_list function takes one arguments that should be a list to print each item
        second argument is indent level"""
        
        for each_inner_list in the_list:
                if isinstance(each_inner_list,list):                           
                        print_nested_list(each_inner_list,indentlevel+1)
                else:
                        for indent in range(indentlevel):
                                print("\t", end='') 
                        print(each_inner_list)


		
