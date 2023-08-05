def print_lol(the_list, level):
	for each_list in the_list:
		if isinstance(each_list, list):
			print_lol(each_list)
		else:
                        for tab_stop in range(level):
                                print ("\t")
			print (each_list)
			
