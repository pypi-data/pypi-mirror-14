def print_name(the_list):
	for Num in the_list:
		if isinstance (Num,list):
		       print_name(Num)
		else:
			print(Num)