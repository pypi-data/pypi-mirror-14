
"""这是"shwanglb_nester.py"模块，该模块作用是打印列表"""
def print_lol(the_list):
	"""这个函数取一个位置参数，名为"the_list",这可以是任何Python列表"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:print(each_item)
		
