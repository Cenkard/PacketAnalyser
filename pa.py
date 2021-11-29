import math as m
import sys
from outils import *

def ConvHexDec(nb):
	nombre = SupprimerEspace(nb)

	l= len(nombre)
	res = 0
	for i in range(0, l):
		n = ord(nombre[i].capitalize())
		if (n>=48 and n<=57):
			n = n-48
		elif (n>=65 and n<=70): 
			n = n-55
		else:
			raise ValueError
		res= res + n*(16**(l-1-i))
	return res


def ConvBinDec(nombre):
	l = len(nombre)
	res =0
	for i in range(0, l):
		n = ord(nombre[i].capitalize())-48;
		if (n!=0 and n!=1):
			raise ValueError
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
			raise ValueError
		res = res + d[n]

	i=0#eleminer les 0 du debut
	if (res!=''):
		while (res[i]=='0'):
			i=i+1;
	return res[i:]

def ConvDecHex(nombre):
	dic = {0:"0", 1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"A",11:"B",12:"C",13:"D",14:"E",15:"F"}
	lim= 0
	res = ""
	#determiner lim, tel que lim est le plus grand possible et nombre/(d^lim)>=1
	while (nombre/(16**lim)>=1):
		lim= lim+1
	lim = lim-1
	while (nombre>0):
		ch = nombre / (16**lim)
		nombre = nombre - ch*(16**lim)
		res = res+dic[ch]
		lim = lim-1
	return res



def FormatIndiceOffset0(FichierTemp, i):#prend en rentrer Fichier et retourne offset nul suivante
	l = len(FichierTemp)
	while (i<l):
		ligne = FichierTemp[i]
		try:
			if (ligne[0:3]=="000"):
				j=3
				while(ligne[j]=="0"):
					j=j+1
				if (ligne[j]==" "):
					return ligne[:j], i
				i=i+1
			else:
				i=i+1
		except IndexError as e:
			print(str(e)+" FormatIndiceOffset")
			i=i+1
	return -1, -1



def SupprimerEspace(element):
	res = ""
	for el in element:
		if (el!=" "):
			res = res+el
	return res


def DerLigne(DerLigne): #renvoie DerLigne sans texte
	LigneValide= -1
	DL = ""
	
	l= len(DerLigne)
	i = 0

	#prendre le offset
	while (DerLigne[i]!=" "):
		DL = DL + DerLigne[i]
		i = i+1
	DL = DL + " "

	#prendre les octets non textes
	for j in range(i+1, l):
		n = ord(DerLigne[j].capitalize())
		if ((n>=48 and n<=57) or (n>=65 and n<=70)):
			DL = DL+DerLigne[j]
		elif (DerLigne[i]!=" "):
			return DL
	return DL

def FauxFormatOffset(ligne, TailleOffset): #renvoit si le format d'un offset et faux, sinon renvoit l'offset valide et sa version decimale
	offset = ""
	i = 0
	while (ligne[i]!=" " and ligne[i]!="\n"):
		offset = offset+ligne[i]
		i=i+1
	if (len(offset)!= TailleOffset):
		raise ValueError
	offsetDec = ConvHexDec(offset)
	return offset, offsetDec

def LigneSansTexteEvid(ligne): #enleve tout le texte qui n'est pas sous la forme d'octets et envoie ligne sans espaces hormis celui entre offset et octets
	CptChiffreCons= 0
	CptEspaceCons = 0
	i = 0
	res = ""
	l = len(ligne)
	if (ligne[-1] == "\n"):
		l=l-1

	#ajouter offset
	while (ligne[i]!=" "):
		res = res+ligne[i]
		i=i+1
	res = res+" " #ajouter espace entre offset et reste

	#i = indice debut message
	while (ligne[i]==" "):
		i=i+1

	#ajouter octets 
	while ((i < l) and CptEspaceCons<2 and CptChiffreCons<3):
		if (ligne[i] == " "):
			if (CptChiffreCons==1):
				return res[:-1]
			CptChiffreCons = 0
			CptEspaceCons = CptEspaceCons+1
		else:
			CptEspaceCons = 0
			if (CptChiffreCons<2):
				res = res + ligne[i]
			CptChiffreCons = CptChiffreCons +1
		i=i+1
	if (CptChiffreCons==3): #a effacer si besoin
		return res[:-2]
	return res

def DebutTrame(ligne): #PEUT CHANCHER EN FONCTION REPONSE DU PROF (est-ce que l'offset est fixe dans toutes les trames?)
	if (ligne[0]=="0" and ligne[1]=="0"):
		i=2
		while (ligne[i]!=" "):
			if (ligne[i]!="0"):
				return False
			i = i+1
	else:
		return False
	return True


def VerifierOffset(FichierTemp, j, TailleOffset): #0 => nouvelle trame ; 1-> ligne valide ; -1 =>invalide
	lf = len(FichierTemp)

	ligne = FichierTemp[j]
	LigneAVerif =  LigneSansTexteEvid(ligne)
	ll = (len(LigneAVerif) - TailleOffset -1)/2 #on divise par deux parce que la taille est en nombrer d octets = 2 chiffres, on fait -1 pout l'espace laisse entre l offset et le message
	OffsetPres = LigneAVerif[:TailleOffset]
	OffsetPresDec = ConvHexDec(OffsetPres)

	#chercher offset valide
	i = j+1
	while (i < lf):
		LigneValide = 1

		try:
			if (DebutTrame(FichierTemp[i])):
				return 0, i, LigneAVerif
			Offset, OffsetDec = FauxFormatOffset(FichierTemp[i], TailleOffset) #si faux format raise ValueError, sinon retourne offset et sa valeur en decimal

			if (OffsetDec>OffsetPresDec): #On a trouve un bon offset, on peut verifier LigneAVerif
				LigneValide = -1
				longueur = OffsetDec-OffsetPresDec
				if (ll >= longueur):
					LigneAVerif = LigneAVerif[:TailleOffset+longueur*2+1] #longueur*2 car taille est en nombrer d'octets = 2 chiffres, +1 pour compter espace entre offset et message
					LigneValide = ConvHexDec(SupprimerEspace(LigneAVerif)) # verifie si c'est uniquement des octets (sans texte)
					return 1, i, LigneAVerif
				else:
					return -1, i, LigneAVerif
			i = i+1


		except (ValueError, IndexError) as e:
			if (LigneValide==-1):
				return -1, i, LigneAVerif
			i=i+1
			#if i<lf and not(DebutTrame(FichierTemp[i])):
			#	print("Erreur verifier offset ligne "+str(i))

	return 0, i, LigneAVerif


def TextCleanerTrame(NomFichier): #Enleve tout texte des trames et renovoie liste de trames
	FichierTemp=[]
	Fichier = []
	TramesValides = []

	#Lire toutes les lignes du fichier
	with open (NomFichier, "r") as f:
		FichierTemp = f.readlines()

	l = len(FichierTemp)	
	i = 0

	#stocker chaque trame du fichier dans une case
	while (i<l):
		#trame suivante
		Offset0, i = FormatIndiceOffset0(FichierTemp, i)
		TailleOffset = len(Offset0)

		#init trame
		trame = []
		res = ""
		verif, i, res = VerifierOffset(FichierTemp, i, TailleOffset) #Verif = si ligne valide (correspond a offset), i= ligne de prochain offset valide, res = ligne validee sans texte ou ligne invalide
		tempi=0
		TrameValide = []

		#ajout trame
		while (verif!=0):
			trame.append(res)
			if (verif == -1):
				TrameValide.append("Erreur dans trame, verifier ligne : "+str(tempi+1))

			tempi= i

			verif, i, res = VerifierOffset(FichierTemp, i, TailleOffset)

		#Gestion de la derniere ligne de la trame
		res = DerLigne(res)
		trame.append(res)
		Fichier.append(trame)

		#indiquer si trame est valide
		TramesValides.append(TrameValide)

	return Fichier, TramesValides

def EnleverOffset(Fichier):
	l = len(Fichier)
	for i in range(l):
		ll = len(Fichier[i])
		TailleOffset = 0
		k=0

		while (Fichier[i][0][k]!=" "):
			TailleOffset = TailleOffset+1
			k=k+1
		for j in range(ll):
			Fichier[i][j] = Fichier[i][j][TailleOffset+1:]
	return Fichier

"""
print(ConvHexDec('123afb'))
print(ConvHexBin('123afb'))
print(ConvBinDec(ConvHexBin('123afb')))

FichierTemp = []
with open ("trame.txt", "r") as f:
		FichierTemp = f.readlines()
Offset0, i = FormatIndiceOffset0(FichierTemp, 0)
print(Offset0, i)
TailleOffset = len(Offset0)
print(VerifierOffset(FichierTemp, i, TailleOffset))
"""

Fichier, tab = TextCleanerTrame("trame.txt")
AfficherDim2(Fichier)
print(tab)

AfficherDim2(EnleverOffset(Fichier))




