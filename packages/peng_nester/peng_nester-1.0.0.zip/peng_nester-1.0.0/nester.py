'''这个模块用来处理多重嵌套列表结构的元素单个输出
'''

def print_lol(the_list):
	"""此函数用来判断元素是否为列表，并把列表拆分为单独的元素输出"""
	for list2 in the_list:
		if(isinstance(list2,list)):
			print_lol(list2)
		else:
			print(list2)

