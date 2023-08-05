def print_lol(the_list):
	for each_list in the_list:
		if isinstance(each_list, list):
			print_lol(each_list)
		else:
			print (each_list)
			
