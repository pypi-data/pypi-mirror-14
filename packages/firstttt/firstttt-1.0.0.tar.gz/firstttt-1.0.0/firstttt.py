"""xj’s fiest python"""
def print_lol(the_list):
#item hanshu
	for each_flick in the_list:
	       if isinstance(each_flick,list):
		       print_lol(each_flick)
	       else:
	               print(each_flick)




