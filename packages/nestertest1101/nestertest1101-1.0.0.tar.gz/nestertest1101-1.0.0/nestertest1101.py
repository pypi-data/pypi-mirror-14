"""This is nester py modules, provide a function, Print_lol by name."""
"""This function print out all items that are included in List if Nested list 
exist """
def print_lol(the_list):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item) #recursively!
		else:
			print(each_item)
