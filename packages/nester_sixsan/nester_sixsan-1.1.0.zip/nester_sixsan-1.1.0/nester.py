
"""This is a comment for "nester.py", the first module I've done with python,it provides a function
called print_lol() wich prints lists thay may include nested lists."""
def print_lol (the_list, level):
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item, level+1)
		else:
			for tab_stop in range(level):
				print ("\t")
			print(each_item)
