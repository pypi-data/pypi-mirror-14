# coding:utf-8



"""
This is nester.py module whilud provide a function named print_log().
print_log could  print list which maybe include nested list

"""
def print_log(the_list,indent_flag=False,level=0):
    """
    :param the_list:
    :return: print each item in the_list
    """
    for list_item in the_list:
        if isinstance(list_item,list):
            print_log(list_item,indent_flag,level+1)
        else:
            if(indent_flag):
                for tap_stop in range(level):
                    print("\t")
            print(list_item)

