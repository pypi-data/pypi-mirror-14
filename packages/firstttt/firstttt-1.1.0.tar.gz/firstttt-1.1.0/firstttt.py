"""xj’s fiest python"""
def print_lol(the_list,num):
#item hanshu
	for each_flick in the_list:
	       if isinstance(each_flick,list):
		       print_lol(each_flick,num+1)
	       else:
		       for tab_stop in range(num):
			       print("\t",end="")
		       print(each_flick)
		       
		       


		       




