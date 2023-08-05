"""This is a new modules from jds
haha ,is that cool?"""
def print_lol(the_list):
  for loop in the_list:
    if(isinstance(loop,list)):
      print_lol(loop)
    else:
      print(loop)
