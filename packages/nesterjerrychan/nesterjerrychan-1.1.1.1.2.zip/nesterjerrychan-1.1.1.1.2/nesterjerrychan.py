

def print_lol(the_list,number):
    for each_item in the_list:
        if isinstance (each_item,list):
            print_lol(each_item,number+1)
        else:
             for tab_stop in range(number):
                 print ("\t",end='')
             print(each_item)




