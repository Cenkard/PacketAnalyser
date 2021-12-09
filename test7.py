def ClearSpace(el):
	res = ""
	for e in el:
		if (e!=" "):
			res = res+e
	return res

with open("test.txt", "r") as f:
	dico = {}
	for line in f:
		L= line.split("	")
		print(L)
		num, nom = int(ClearSpace(L[0])), ClearSpace(L[1][:-1])
		dico[num] = nom

	print("")
	print("")
	print(dico)


#147-149, 102-107, 162-174, 178-207, 214-219
#224-254 Reserved (Private Use)

