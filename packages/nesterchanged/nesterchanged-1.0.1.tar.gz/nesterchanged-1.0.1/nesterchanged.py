def print_lol(the_list, indent=false, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent=false, level+1)

        else:

            for tab_stop in range(level+1):
                print("\t", end=' ')
            print(each_item)
                

      
            
                  
            
            
