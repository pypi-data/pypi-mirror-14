"""This is a new modules from jds
haha ,is that cool?"""
def print_lol(the_list,level):
  for loop in the_list:
    if(isinstance(loop,list)):
      print_lol(loop,level+1)
    else:
      for num in range(level):
               print("\t",end='')        
      print(loop)
