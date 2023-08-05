"""这是nester.py模块，提供了一个print_list函数，这个函数的作用是打印多层列表"""
def print_list (aaa):
	for x in aaa:
		if isinstance(x,list):
			print_list (x)
		else:
			print (x)
