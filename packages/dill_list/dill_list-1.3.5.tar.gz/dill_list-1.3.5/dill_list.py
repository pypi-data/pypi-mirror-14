""" This is a function that performs recursive call on multi level arrays """

import sys

def print_lol(the_list,indent=False,level=0,fh=sys.stdout):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,fh)
		else:
			try:
				if indent:
					for each_indent in range(level):
						print("\t",end='', file=fh)
				print(each_item,file=fh)
			except IOError as err:
				print("File could not be open due to: " + str(err))
