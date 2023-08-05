"""This is the print module and it provides a function called print_lol() which prints lists which may or may not contain nested lists."""


def print_lol(the_list):
	""" this is the function implementation of print_lol()
	it takes as ag=rgument the list and checks for any nested lists using
	the BIF isinstance(name , type)."""
	for each_item in the_list:
		if isinstance(each_item,the_list):
			print_lol(each_item)
		else:
			print (each_item)

