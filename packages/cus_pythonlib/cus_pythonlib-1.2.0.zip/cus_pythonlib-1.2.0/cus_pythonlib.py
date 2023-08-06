"""print every element of a list, for nested list, go into it till find non-list element"""
def __printlist(listvar,tab=0):
	""" created by berwinsyu, referring to "head first python" """
	for l in listvar:
		if isinstance(l,list):
			__printlist(l,tab+1)
		else:
			for t in range(tab):
				print("\t"),
			print(l)
			
