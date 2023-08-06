""" This module nester.py() contains function to act on nested lists """

def print_nested_list(input_list,level=0,indent=False):
	for item in input_list:
		if isinstance(item,list):
			if indent==True:
				print_nested_list(item,level+1,True)
			else:
				print_nested_list(item,level,False)
		else:
			for i in range(level):
				print('\t',end='')
			print (item)