import math as m


def ConvHexDec(nombre):
	l= len(nombre)
	res = 0
	for i in range(0, l):
		n = ord(nombre[i].capitalize())
		if (n>=48 and n<=57):
			n = n-48
		elif (n>=65 and n<=70): 
			n = n-55
		else:
			return "Erreur"
		res= res + n*(16**(l-1-i))
	return res


def ConvBinDec(nombre):
	l = len(nombre)
	res =0
	for i in range(0, l):
		n = ord(nombre[i].capitalize())-48;
		if (n!=0 and n!=1):
			return "Erreur"
		else:
			res = res + n*(2**(l-1-i))
	return res


def ConvHexBin(nombre):
	d = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101', '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011', 'C':'1100', 'D':'1101', 'E':'1110', 'F':'1111'}
	l = len(nombre)
	res = ''
	for i in range(0, l):
		n = nombre[i].capitalize()
		if (not(ord(n)>=48 and ord(n)<=57) and not(ord(n)>=65 and ord(n)<=70)):
			return 'Erreur'
		res = res + d[n]

	i=0#eleminer les 0 du debut
	if (res!=''):
		while (res[i]=='0'):
			i=i+1;
	return res[i:]


print(ConvHexDec('123afb'))
print(ConvHexBin('123afb'))
print(ConvBinDec(ConvHexBin('123afb')))


