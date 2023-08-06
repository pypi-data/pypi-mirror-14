def printMovie(movieList,indent=False,level=0):
	"""This is a note"""
	for item in movieList:
		if isinstance(item,list):
			printMovie(item,indent,level+1)
		else:
			if indent:
				for tab in range(level):
					print("\t",end='')
			print(item)
