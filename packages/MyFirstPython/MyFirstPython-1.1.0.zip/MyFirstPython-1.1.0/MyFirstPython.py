def printMovie(movieList,level):
	"""This is a note"""
	for item in movieList:
		if isinstance(item,list):
			printMovie(item,level+1)
		else:
			for tab in range(level):
				print("\t",end='')
			print(item)
