"""This is the nester.py comment"""

def print_lol( the_list, tab_level=0 ):
    """This is the print_lol comment. A second argument called "level" is used to insert tab-stops when a nested list is encountered"""
    
    for each_item in the_list:
        if isinstance( each_item, list ):
            print_lol( each_item, tab_level+1 )
        else:
            for tab_stop in range( tab_level ):
                print '\t',;
            print( each_item )
