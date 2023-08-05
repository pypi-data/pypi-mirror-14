def print_lol(the_list,level):
	''' 我是注释 '''
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for num in range(level):
				print(level)
			print(each_item)
