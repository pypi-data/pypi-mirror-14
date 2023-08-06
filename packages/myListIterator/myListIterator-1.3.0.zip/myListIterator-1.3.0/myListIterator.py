#This is the nester.py module, and it provides one funtion called
#print_lol() which prints lists that may or may not include nested lists.

def print_lol(the_list,indent=False,level=0):
    
        for each_item in the_list:
            
            #This funtion takes a positional argument called "the_list", which is any
            #Python list (of, possibly, nested lists). Each data item in the provided list
            #is (recursively) printed to the screenon its own line.
            
                if(isinstance(each_item,list)):
                        print_lol(each_item,indent,level+1)
                else:
                        if(indent):
                                for num in range(level):
                                        print('\t', end="")
                        print(each_item)

                                

