def print_haha(the_list):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_haha(each_item)
		else:
			print(each_item)


