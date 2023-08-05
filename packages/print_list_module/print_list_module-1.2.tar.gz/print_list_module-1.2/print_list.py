		
"""This is the module to print list items"""


def print_nested_list(the_list,indent=False,indentlevel=0):
        """This print_nested_list function takes one arguments that should be a list to print each item
        second argument is whether to on or off the indent and third argument is indent count
        first argument=required
        second and third argument=optional
        """
        
        for each_inner_list in the_list:
                if isinstance(each_inner_list,list):                           
                        print_nested_list(each_inner_list,indent,indentlevel+1)
                else:
                        if indent:
                                for indentcount in range(indentlevel):
                                        print("\t", end='') 
                        print(each_inner_list)

		
