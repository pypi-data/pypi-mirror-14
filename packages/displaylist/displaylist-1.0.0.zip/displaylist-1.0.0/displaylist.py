def display(a_list):
    for each_element in a_list:
        if isinstance(each_element,list):
            display(each_element)
        else:
            print each_element
