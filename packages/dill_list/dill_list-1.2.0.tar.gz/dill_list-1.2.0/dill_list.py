""" This is a function that performs recursive call on multi level arrays """

def print_lol(the_list,level=0):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for each_indent in range(level):
				print("\t",end='')
			print(each_item)
