"""This is a new modules from jds
haha ,is that cool?"""
def print_lol(the_list,indent=False,level=0):
  for loop in the_list:
    if(isinstance(loop,list)):
      print_lol(loop,indent,level+1)
    else:
      if indent:
        for num in range(level):
               print("\t",end='')        
      print(loop)
