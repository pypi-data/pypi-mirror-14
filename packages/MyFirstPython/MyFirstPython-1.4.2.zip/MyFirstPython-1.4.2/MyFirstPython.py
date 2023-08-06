import sys
def printMovie(movieList,indent=False,level=0,fh=sys.stdout):
    """This is a note"""
    for item in movieList:
        if isinstance(item,list):
            printMovie(item,indent,level+1,fh)
        else:
            if indent:
                for tab in range(level):
                    print("\t",end='',file=fh)
            print(item,file=fh)
