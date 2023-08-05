#This module can be used to print all the items present in a nested list"""
def print_lol(the_list):
#This function takes each item from the given list and checks if the list has an inner list and if it does happen to have a list within a list it calls itself again and checks if the item is a list if its not a list then it will print the item'''
 for each_item in the_list:
  if isinstance(each_item,list):
   print_lol(each_item)
  else:
   print(each_item)
   
