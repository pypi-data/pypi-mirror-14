"""This is the dadongjun_nester.py module, and it provides one function called print_lol() which prints lists that may or may not include nested lists."""
def print_lol(the_list, level):
	"""This function takes a positional argument called the_list, which is any Python list 		(or possibly, nested lists). Each data in the provide list is (recurively) printed to 		the screen on its own line. A second argument called level is used to insert tab_stop 		when a nested list is encountered."""
	for each_item in the_list:
		if isinstance(each_item, list):	#each_list is list, invoke(call) print_lol()
			print_lol(each_item, level+1)	#recursion
		else:				#each_list is not a list, print()
			for tab_stop in range(level):
				print("\t", end='')
			print(each_item)
