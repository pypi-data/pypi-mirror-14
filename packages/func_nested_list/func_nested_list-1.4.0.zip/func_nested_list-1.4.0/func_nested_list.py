def print_lol(the_list,indent=False,level=0,df=sys.stdout):
 for each_item in the_list:
  if isinstance(each_item,list):
   print_lol(each_item,indent,level+1,df)
  else:
   if indent:
    for num in range(level):
     print('\t', end='',file=df)
   print(each_item,file=df)
   
