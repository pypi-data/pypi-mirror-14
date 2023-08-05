"""xj’s fiest python"""
def print_lol(the_list,indent=False,num=0):
#item hanshu
	for each_flick in the_list:
	       if isinstance(each_flick,list):
		       print_lol(each_flick,indent,num+1)
	       else:
                       if indent:
		       for tab_stop in range(num):
			       print("\t",end="")
		       print(each_flick)
		       
		       


		       




