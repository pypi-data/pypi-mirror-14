"""This is the "list_sweep.py" module. It provides one fuction called 'list_sweep' which prints lists that may or may not contain inner lists."""

def list_sweep(any_list, level):

	"""This function takes a positional arguement called "any_list", which is any Python list (which may include inner lists). Each data item within the list, and its inner list(s), respectively, is printed, recursively, to the screen on its own line. In addition, a secondary arguement allows for the inner lists to be printed with a tab space relative to its range position within the lists."""

	for each_item in any_list:
		if isinstance(each_item, list):
			list_sweep(each_item, level+1)
		else:
			for tab_stop in range(level):
				print("\t", end ='')
			print(each_item)

