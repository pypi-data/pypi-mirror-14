def display(a_list,level):
    for each_element in a_list:
        if isinstance(each_element,list):
            display(each_element,level+1)
        else:
            for tab in range(level):
                print "\t"
            print each_element
