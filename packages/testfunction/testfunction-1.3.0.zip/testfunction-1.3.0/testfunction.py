"""这是testfunction.py模块，提供了一个名为print_lol（）的函数,
用来打印列表，其中包含或不包含嵌套列表"""

def print_lol(the_list,indent=False,level=0):
	"""这个函数有一个位置参数，名为the_list,可以用于任何Python列表，包含或
	不包含嵌套列表均可，所提供列表中的各个数据项会递归地打印到屏幕上，而且各占一行"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t",end='')
			print(each_item)


