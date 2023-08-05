def print_lol (SomeList) :
	for item in SomeList:
		if(isinstance(item, list)):
			print_lol(item)
		else:
			print(item)
