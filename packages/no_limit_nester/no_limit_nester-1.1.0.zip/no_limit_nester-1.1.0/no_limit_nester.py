""" This module nester.py() contains function to act on nested lists """

def print_nested_list(input_list,level):
	for item in input_list:
		if isinstance(item,list):
			print_nested_list(item,level+1)
		else:
			for i in range(level):
				print('\t',end='')
			print (item)