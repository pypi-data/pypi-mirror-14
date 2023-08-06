def printMovie(movieList):
	"""This is a note"""
	for item in movieList:
		if isinstance(item,list):
			printMovie(item)
		else:
			print(item)
