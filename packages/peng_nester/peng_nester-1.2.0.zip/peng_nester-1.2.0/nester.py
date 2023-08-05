'''这个模块用来处理多重嵌套列表结构的元素单个输出
'''

def print_lol(the_list,indent=False,level=0):
	"""此函数用来判断元素是否为列表，并把列表拆分为单独的元素输出"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1)
		else:
			if(indent):
				for tab_stop in range(level):
					print("\t",end='')
			print(each_item)

