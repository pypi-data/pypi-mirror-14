'''
Created on Mar 13, 2016

@author: casi
'''

"""
 Head First module for printing lists
"""
def print_lol (the_list):
# use for to recursivly print all lists in a list
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)