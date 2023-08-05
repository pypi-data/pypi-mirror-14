 """this is "nester.py" module and it provide one function called print_lol()"""
'this is "nester.py" module and it provide one function called print_lol()'
 def print_lol(the_list):
	"""this is a function"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item)
		else:
			print(each_item)

			
