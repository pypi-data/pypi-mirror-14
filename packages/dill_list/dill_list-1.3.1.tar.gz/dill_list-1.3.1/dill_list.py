""" This is a function that performs recursive call on multi level arrays """

def print_lol(the_list,indent=False,level=0,input=sys.stdout):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1,input)
		else:
			try:
				with open("print_lol.txt",'w+') as input:
					if indent:
						for each_indent in range(level):
							print("\t",end='', file=input)
					print(each_item,file=input)
			except IOError as err:
				print("File could not be open due to: " + str(err))
