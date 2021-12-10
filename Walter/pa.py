import math as m
import sys
from outils import *

#----------------------------------------------Convertisseurs

def toAscii(data): #convertisseur de hex en ascii
	i=0
	ascii_data="" #notre reseultat final
	while(i+2<=len(data)):
		if(data[i:i+2] in ["01","02","03","04","05","06","07","08","09","0A","0a","0B","0b","0C","0c","0D","0d","0E","0e","0F","0f"]): #liste qui permet de reconnaitre un point a condition qu'on ne soit pas au debut de data (deux premiers chiffres hexadecimaux)
			if(i<2):
				pass;
			else:
				ascii_data = ascii_data+"."
		elif((ConvHexDec(data[i:i+2])>=65 and ConvHexDec(data[i:i+2])<=122) or (ConvHexDec(data[i:i+2])>=48 and ConvHexDec(data[i:i+2])<=57)): #si c'est pas un point 
			ascii_data = ascii_data + bytearray.fromhex(data[i:i+2]).decode() #on le decode directement de hex a ascii
		i=i+2
	return ascii_data

def ConvHexDec(nb): #convertit un nombre hexadecimal en decimal
	nombre = SupprimerEspace(nb) #on supprime les espaces inutiles

	l= len(nombre)
	res = 0
	for i in range(0, l): #on itere sur les chiffres hex
		n = ord(nombre[i].capitalize()) #on capitalise tout pour etre compatible avec majiscule et miniscule 
		if (n>=48 and n<=57): #si c'est un nombre 
			n = n-48 #on le transforme en nombre int en faisant -48 (48 est la valeur decimal pour coder le string du nombre 0, 49 pour code 1 etc...)
		elif (n>=65 and n<=70):  #si c'est une lettre (de A a F)
			n = n-55 #on fait -55 car A==65, pour retrouver 10 de meme, F=70, donc 70-55=15
		else:
			raise ValueError #sinon il y a une erreur
		res= res + n*(16**(l-1-i)) #on multiplie le chiffre n hexadecimal convertit en decimal par son poids (son coef 16)
	return res 


def ConvBinDec(nombre): #convertit un nombre binaire en decimal
	l = len(nombre) 
	res =0
	for i in range(0, l): #on itere sur les chiffres binaires
		n = ord(nombre[i].capitalize())-48; #Capitalisation non necessaire, on fait -48 pour retrouver nombre decimal 0 ou 1 
		if (n!=0 and n!=1): #on peut que trouver 0 ou 1
			raise ValueError #sinon il y a une erreur
		else:
			res = res + n*(2**(l-1-i)) #on multiplie le nombre binaire 0 ou 1 par son poids (coef 2)
	return res


def ConvHexBin(nombre): #convertit un nombre hexadecimal en binaire
	d = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101', '6':'0110', '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B':'1011', 'C':'1100', 'D':'1101', 'E':'1110', 'F':'1111'} #liste qui defini chiffres de bases en binaires
	l = len(nombre)
	res = ''
	for i in range(0, l): #pour chaque hex
		n = nombre[i].capitalize() #compatibilite capital et miniscule
		if (not(ord(n)>=48 and ord(n)<=57) and not(ord(n)>=65 and ord(n)<=70)): #si ce n'est pas un chiffre hex
			raise ValueError #erreur
		res = res + d[n] #sinon on ajoute version binaire au resultat
	return res

def ConvDecHex(nombre):  #convertit un nombre decimal en hex
	dic = {0:"0", 1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"A",11:"B",12:"C",13:"D",14:"E",15:"F"} #definition de chiffres de base
	lim= 0
	res = ""
	#determiner lim, tel que lim est le plus grand possible et nombre/(d^lim)>=1. En fait cherche le plus plus grand coef de 16 dans notre nombre pour savoir coder le nombre hex sur combien de chiffre
	while (nombre/(16**lim)>=1):
		lim= lim+1
	lim = lim-1
	while (nombre>0): #coder notre par division sucessives du plus gros au plus petit coef de 16
		ch = nombre / (16**lim)
		nombre = nombre - ch*(16**lim)
		res = res+dic[ch]
		lim = lim-1
	return res

#---------------------------------------------- Netoyage texte 

def FormatIndiceOffset0(FichierTemp, i): #prend en rentrer Fichier et ligne i dans le fichier 
	#Elle cherche le debut d'une trame: retourne le couple (offset, i) ou offset est l'offset nul indiquant le format des offset de cette trame et i est la ligne ou se trouve cet offset
	l = len(FichierTemp)
	while (i<l): #tant qu' on a pas depasser la taille du fichier
		ligne = FichierTemp[i] #on lit la ligne i
		try:
			if (ligne[0:3]=="000"): #d'apres l'enonce du projet, l'offset est code sur plus de 2 chiffres donc au minimum sur 3 chiffres
				j=3
				while(ligne[j]=="0"): #on determine longueur de offset nul
					j=j+1
				if (ligne[j]==" "):
					return ligne[:j], i #on retourne couple
				i=i+1
			else:
				i=i+1
		except IndexError as e: #gestion erreur en cas de index our of rance, on continue a chercher
			print(str(e)+" FormatIndiceOffset")
			i=i+1
	return -1, -1



def SupprimerEspace(element): #fonction qui elimine espaces dans un string
	res = ""
	for el in element:
		if (el!=" "):
			res = res+el
	return res


def DerLigne(DerLigne): #renvoie la derniere ligne sans autres elements que les nombre et les chiffres hexadecimaux, des qu'on trouve autre chose on s'arrette
	LigneValide= -1
	DL = ""
	
	l= len(DerLigne)
	i = 0

	#prendre le offset
	while (DerLigne[i]!=" "):
		DL = DL + DerLigne[i]
		i = i+1
	DL = DL + " "

	#prendre les octets hexadecimaux qui peuvent etre texte ou pas
	for j in range(i+1, l):
		n = ord(DerLigne[j].capitalize()) #insensibilite capital/minscule
		if ((n>=48 and n<=57) or (n>=65 and n<=70)): #par defintion du chiffre hex
			DL = DL+DerLigne[j]
		elif (DerLigne[i]!=" "):
			return DL
	return DL

def FauxFormatOffset(ligne, TailleOffset): #Fonction qui prend une ligne du fichier et la taille de l'offset de la trame associe a cette ligne (celui de l'offset nul)
	#renvoit si le format d'un offset est faux, sinon renvoit l'offset et sa version decimale
	offset = ""
	i = 0
	while (ligne[i]!=" " and ligne[i]!="\n"): #tant qu'on est dans l'offset (on  a pas rencontre d'espaces ni de \n), on prend l'offset
		offset = offset+ligne[i]
		i=i+1
	if (len(offset)!= TailleOffset): #il est faux si les tailles different
		raise ValueError
	offsetDec = ConvHexDec(offset) #si l'offset est inconvertissable en hexadecimal il est aussi incorrecte, cette fonction raise error en cas d'erreur
	return offset, offsetDec #si l'offset est coherent on le retourne, pour verifier s il est plus grand que l'offset avant lui, pour le reconnaitre comme un vrai offset

def LigneSansTexteEvid(ligne): #Pour une ligne donnee: enleve tout le texte qui n'est pas sous la forme d'octets (n'enleve pas le texte competement) et envoie ligne sans espaces hormis celui entre offset et octets
	CptChiffreCons= 0 #compre le nombre de chiffres consecutives
	CptEspaceCons = 0 #compte le nombre d'espace consecutifs
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
	while ((i < l) and CptEspaceCons<2 and CptChiffreCons<3): #tant qu'on est pas a la fin de la ligne, et tant que le nombre d'espace consecutifs est < 2, et le nombre de chiffres consecutifs <3
		if (ligne[i] == " "): #si on a un espace 
			if (CptChiffreCons==1): #Si on a compter que un chiffre hexadecimal avant cet espace, 
				return res[:-1] #on retourne la ligne jusqu'a avant ce chiffre hexadecimal, car on aurait du compter 2 chiffres hexadecimaux (condition un octet delimite par un espace)
			CptChiffreCons = 0 #sinon on continue a chercher donc on reset le compteur de chiffres consecutifs
			CptEspaceCons = CptEspaceCons+1 #on augmente le nombre d espace consecutifs de 1 car on a rencontre un espace
		else: #si on a un chiffre
			CptEspaceCons = 0 #on reset notre compteur de espaces consecutifs
			if (CptChiffreCons<2): #si on a rencontre moins de 2 chiffres jusqu a present
				res = res + ligne[i] #on ajoute le chiffre qu'on vient de rencontrer
			CptChiffreCons = CptChiffreCons +1 #on augmente le compteur de chiffres consecutifs rencontre
		i=i+1
	if (CptChiffreCons==3): #a effacer si besoin
		return res[:-2]
	return res

def DebutTrame(ligne): #prend en entree une ligne du fichier
	#retourne si cette ligne commence par un offset nul, indiquant ainsi qu'on est au debut d'une trame
	if (ligne[0]=="0" and ligne[1]=="0" and ligne[2]=="0"): #offset nul commence par trois 0 au minimum d'apres enonce projet
		i=3
		while (ligne[i]!=" "): #si c'est pas un espace 
			if (ligne[i]!="0"): #alors ca ne peut pas etre different de 0 pour que ca soit un offset valide
				return False
			i = i+1
	else:
		return False 
	return True #si on continu a trouver des 0 jusqu'a l'espace, c'est un offset valide


def VerifierOffset(FichierTemp, j, TailleOffset): #fonction qui prend un fichier (une listes des lignes du fichier), l'indice d'une ligne j et la taille de l'offset associe a cette ligne j
	#Fonction retourne un triplet (n, i, ligne): si [n=0 => nouvelle trame ; 1-> ligne j valide ; -1 =>ligne j invalide] ; i est la nouvelle ligne de la trame debutant par un offset valide ;  ligne et la ligne j debarassee du tout texte
	lf = len(FichierTemp)

	#on initialise variables utiles
	ligne = FichierTemp[j]
	LigneAVerif =  LigneSansTexteEvid(ligne) #on se debarasse du texte evident (mais en garde texte sous forme d'octets)
	ll = (len(LigneAVerif) - TailleOffset -1)/2 #on divise par deux parce que la taille est en nombrer d octets = 2 chiffres, on fait -1 pout l'espace laisse entre l offset et le message
	OffsetPres = LigneAVerif[:TailleOffset] #on prend offset de la ligne presente
	OffsetPresDec = ConvHexDec(OffsetPres) #on transforme cet offset nombre hex (pour ensuite le comparer a l'offset suivant afin de determiner un offset suivant valide)

	#chercher offset suivant valide
	i = j+1
	while (i < lf): #tant qu'on a pas attaint la fin du fichier
		LigneValide = 1

		try:
			if (DebutTrame(FichierTemp[i])): #si on detecte une nouvelle trame, on retourne 0 pour l'indiquer, l'indice i de cette nouvelle trame et LigneAVerif qui est la derniere ligne de la trame presente
				return 0, i, LigneAVerif
			Offset, OffsetDec = FauxFormatOffset(FichierTemp[i], TailleOffset) #si faux format raise ValueError, sinon on recupere offset et sa valeur en decimal

			if (OffsetDec>OffsetPresDec): #On a trouve un bon offset (qui est superieur a l'offset present), on peut verifier LigneAVerif (la ligne presente)
				LigneValide = -1 #on part du principe qu'elle est invalide
				longueur = OffsetDec-OffsetPresDec #on determine sa longueur en theorie en fonction de l'offset present (de la ligne presente) et l'offset suivant valide trouve
				if (ll >= longueur): #si la ligne presente est de longueur superieur, on efface les ocetets textes additionnels
					LigneAVerif = LigneAVerif[:TailleOffset+longueur*2+1] #longueur*2 car taille est en nombrer d'octets = 2 chiffres, +1 pour compter espace entre offset et message
					LigneValide = ConvHexDec(SupprimerEspace(LigneAVerif)) # verifie si c'est uniquement des octets hexadecimaux (sans texte)
					return 1, i, LigneAVerif #si tout est verifie on retourne qu'elle est valide (1), l'indice i de la prochaine ligne a verifier avec l'offset valide et on retourne Ligne presente debarasse du texte
				else: #si longueur ligne presente est inferieure a celle precise 
					return -1, i, LigneAVerif #elle est invalide
			i = i+1 #si pas d'offset valide trouve encore on continue a chercher 


		except (ValueError, IndexError) as e: 
			if (LigneValide==-1): #si la conversion en hex de la ligne presente etait un echec, alors qu'on a trouve un offset suivant correcte, ca signifie que la ligne est incomplete
				return -1, i, LigneAVerif #retour ligne invalide
			i=i+1 #sinon exception causee par offset invalide ce qui est normal on continue a chercher

	return 0, i, LigneAVerif #si on atteint fin fichier, on atteint fin de fichier on retourne quand meme derniere ligne de la derniere trame


def TextCleanerTrame(NomFichier): #Prend en entre un fichier contennat des trames a lire
	#renvoit couple (Fichier, TramesValides): Fichier represente un tableau de trames sans texte et TramesValides 
	FichierTemp=[]
	Fichier = []
	TramesValides = []

	#Lire toutes les lignes du fichier
	with open (NomFichier, "r") as f: #transforme fichier en liste de lignes
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
		tempi=i
		verif, i, res = VerifierOffset(FichierTemp, i, TailleOffset) #Verif = si ligne valide (correspond a offset), i= ligne de prochain offset valide, res = ligne validee sans texte ou ligne invalide
		TrameValide = []

		#ajout trame
		while (verif!=0):
			trame.append(res)
			if (verif == -1): #si ligne invalide, sauvegarder ligne erreur
				TrameValide.append("Erreur dans trame ({}), verifier ligne : ".format(len(Fichier)+1)+str(tempi+1))

			tempi= i

			verif, i, res = VerifierOffset(FichierTemp, i, TailleOffset) #verifie ligne presente et trouver ligne suivante (ayant offset valide)

		#Gestion de la derniere ligne de la trame
		res = DerLigne(res)
		trame.append(res+" {}".format(tempi+1)) #on rajoute numero de la ligne de la derniere ligne de cette trame car on va la perdre apres (on va l'enlever plus tard)
		Fichier.append(trame) #on ajoute trame

		#indiquer si trame est valide
		TramesValides.append(TrameValide) #TrameValides contient une liste d'erreurs par trame, si cette liste est vide, la trame est valide sinon elle est incorrecte

	return Fichier, TramesValides

def EnleverOffset(Fichier): #prend en entre un fichier (liste de lignes du fichier), lignes valides et sans textes
	#Retourne les lignes sans offset
	l = len(Fichier)
	for i in range(l): #pour chaque trame
		ll = len(Fichier[i])
		TailleOffset = 0
		k=0

		while (Fichier[i][0][k]!=" "): #determiner taille offset de la trame presente
			TailleOffset = TailleOffset+1
			k=k+1 
		for j in range(ll):#pour chaque ligne enleve offset
			Fichier[i][j] = Fichier[i][j][TailleOffset+1:]
	return Fichier


#--------------------------------------------------------------------------------------- Options IP
def ListOpEnText(L):  #Fonction intermediaire pour le mode texte en optionIP
	res2= L[0]
	l = len(L)
	for i in range(1, l):
		res2 = res2+"\t\t"+L[i][0]
		L2 = L[i][1].split("\n")
		L2 = L2[:-1] #ignorer dernier element vide
		for el in L2:
			res2=res2+"\t\t\t"+el+"\n"
	return res2

def LecteurIpAdresse(trame, i): #Fonction intermediaire pour lire IP (ne pas oublie de faire i=i+8 au retour)
	fin = i+8
	addrIP = ""
	while (i<fin):
		nb = ConvHexDec(trame[i:i+2])
		addrIP = addrIP + str(nb) + "."
		i=i+2
	return trame[i-8:i], addrIP[:-1]

def RecordRoute(trame, j):
	lrr = ConvHexDec(trame[j+2: j+4]) #longueur en octets
	Pointer = ConvHexDec(trame[j+4:j+6])
	L= [] #liste de textes a inserer L[0] = ligne de nom, L[1] = type, L[2] = longueur, L[3] = pointeur
	L.append("IP Option {} ({})- Record Route ({} bytes)\n".format("0x"+trame[j: j+2],ConvHexDec(trame[j: j+2]),  lrr))
	contenu = "Type: {} (7)\nLength: {} ({})\nPointer: {} ({})\n".format(trame[j:j+2], trame[j+2:j+4], lrr, trame[j+4:j+6], Pointer)
	finOp = j+lrr*2-1 #indice du dernier chiffre hexadecimal de cette option
	i = j+6
	cpt= 0
	Pointer = (Pointer-4)/4
	while (i<=finOp):
		addrIPH, addrIP = LecteurIpAdresse(trame, i)
		if (addrIP == "0.0.0.0"):
			contenu = contenu + "Empty Route: "+"0x"+addrIPH+" ("+addrIP+")"+"\n"
		else:
			contenu = contenu + "Recorded Route: "+"0x"+addrIPH+" ("+addrIP+")"+"\n"
		i = i+8

		#gestion pointer
		if (Pointer<(lrr-3)/4 and cpt==Pointer):
			contenu = contenu[:-1]+"  <- (next)\n"
		cpt=cpt+1
	L.append(contenu)
	return i, L


def FlagTextTimeStamp(Flag): #fonction intermediaire pour les flag de TimeStamp
	if (Flag == "0000"):
		return "Time stamps only (0x0)"
	elif (Flag == "0001"):
		return "Time stamp and address (0x1)"
	elif (Flag== "0011"):
		return "Time stamp and address prespecified"

def TimeStamp(trame, j):
	lts = ConvHexDec(trame[j+2: j+4]) #longueur en octets
	finOp = j+lts*2-1 #indice du dernier chiffre hexadecimal de cette option
	L= [] #liste de textes a inserer L[0] = ligne de nom, L[1] = type, L[2] = longueur, L[3] = pointeur
	L.append("IP Option 0x{} ({})- Time Stamp ({} bytes)\n".format(trame[j: j+2],ConvHexDec(trame[j: j+2]), lts))
	Pointer = ConvHexDec(trame[j+4:j+6])
	OverflowBin = ConvHexBin(trame[j+6])
	OverflowDec = ConvHexDec(trame[j+6])
	Flag = ConvHexBin(trame[j+7])

	contenu = "Type: 0x{} (68)\nLength: 0x{} ({})\nPointer: 0x{} ({})\n{} .... = Overflow: {}\n.... {} = Flag: {}\n".format(trame[j: j+2], trame[j+2:j+4], lts,trame[j+4:j+6], Pointer, OverflowBin, OverflowDec, Flag, FlagTextTimeStamp(Flag))

	i = j+8
	cpt = 0

	if (Flag=="0000"):
		while (i<=finOp):
			nb = str(ConvHexDec(trame[i:i+8]))
			contenu = contenu +"Time Stamp: 0x"+trame[i:i+8]+" ("+nb+")"+"\n"
			i = i+8

	elif (Flag == "0001" or Flag=="0011"):
		while (i<=finOp):
			addrIPH, addrIP = LecteurIpAdresse(trame, i)
			i = i+8
			nb = str(ConvHexDec(trame[i:i+8]))
			i= i+8

			if (addrIP=="0.0.0.0"):
				contenu=contenu+"Address: - 0x{}\nTime Stamp: 0x{} ({})\n".format(addrIPH, trame[i-8:i], nb)
			else:
				contenu=contenu+"Address: 0x{} ({})\nTime Stamp: 0x{} ({})\n".format(addrIPH, addrIP, trame[i-8:i], nb)

	L.append(contenu)
	return i, L

def  LooseSourceRoute(trame, j):
	lsr = ConvHexDec(trame[j+2: j+4]) #longueur en octets
	Pointer = ConvHexDec(trame[j+4:j+6])
	L= [] #liste de textes a inserer L[0] = ligne de nom, L[1] = type, L[2] = longueur, L[3] = pointeur
	L.append("IP Option 0x{} ({}) - Loose Source Route ({} bytes)\n".format(trame[j:j+2],ConvHexDec(trame[j: j+2]), lsr))
	contenu = "Type: 0x{} (131)\nLength: 0x{} ({})\nPointer: 0x{} ({})\n".format(trame[j:j+2],trame[j+2:j+4], lsr,trame[j+4:j+6], Pointer)
	finOp = j+lsr*2-1 #indice du dernier chiffre hexadecimal de cette option
	i = j+6
	cpt= 0
	Pointer = (Pointer-4)/4
	while (i<=finOp):
		addrIPH, addrIP = LecteurIpAdresse(trame, i)
		if (i!=finOp-7):
			contenu = contenu + "Source Route: 0x"+addrIPH+" ("+addrIP+")"+"\n"
		else:
			contenu = contenu + "Destination: 0x"+addrIPH+" ("+addrIP+")"+"\n"
		i = i+8

		#gestion pointer
		if (Pointer<(lsr-3)/4-1 and cpt==Pointer):
			contenu = contenu[:-1]+"  <- (next)\n"
		cpt=cpt+1
	L.append(contenu)
	return i, L
	
def StrictSourceRoute(trame, j):
	lss = ConvHexDec(trame[j+2: j+4]) #longueur en octets
	Pointer = ConvHexDec(trame[j+4:j+6])
	L= [] #liste de textes a inserer L[0] = ligne de nom, L[1] = type, L[2] = longueur, L[3] = pointeur
	L.append("IP Option 0x{} ({})- Strict Source Route ({} bytes)\n".format(trame[j:j+2],ConvHexDec(trame[j: j+2]),lss))
	contenu = "Type: 0x{} (137)\nLength: 0x{} ({})\nPointer: 0x{} ({})\n".format(trame[j:j+2], trame[j+2:j+4], lss, trame[j+4:j+6], Pointer)
	finOp = j+lss*2-1 #indice du dernier chiffre hexadecimal de cette option
	i = j+6
	cpt= 0
	Pointer = (Pointer-4)/4
	while (i<=finOp):
		addrIPH, addrIP = LecteurIpAdresse(trame, i)
		if (i!=finOp-7):
			contenu = contenu + "Source Route: 0x"+addrIPH+" ("+addrIP+")"+"\n"
		else:
			contenu = contenu + "Destination: 0x"+addrIPH+" ("+addrIP+")"+"\n"
		i = i+8

		#gestion pointer
		if (Pointer<(lss-3)/4-1 and cpt==Pointer):
			contenu = contenu[:-1]+"  <- (next)\n"
		cpt=cpt+1
	L.append(contenu)
	return i, L

def optionIP(trameTot,mod): #prend en entree une trame retourne ses options decodes #0,1,7,68, 131,137, mod = 0 retourne liste, sinon retourne texte
	cpt = 0
	trame = trameTot[28:] #on s'occupe que de la partie IP
	LongOp = ConvHexDec(trame[1])*4 - 20
	finOps = 40 + LongOp*2 -1 #indice du dernier chiffre hexadecimal d'option
	res = []
	res.append("\tOptions: ({} bytes)\n".format(LongOp)) # L[0] = ligne de titre options, a partir de L[1] on commences les differentes options, avec e.g. L[1][0] le titre et L[1][1] le contenu
	if (LongOp==0):
		return None, 0
	else:
		i = 40
		while (i<=finOps):
			typ = ConvHexDec(trame[i:i+2])
			op = ""
			if (typ==0):
				i, op= finOps+1, ["IP Option 0x{} ({})- End of Option List (EOL)\n".format(trame[i:i+2], ConvHexDec(trame[i: i+2])), "Type: 0x{} (0)\n".format(trame[i:i+2])]
			elif (typ==1):
				i, op = i+2, ["IP Option 0x{} ({})- No-Operation (NOP)\n".format(trame[i:i+2], ConvHexDec(trame[i: i+2])), "Type: 0x{} (1)\n".format(trame[i:i+2])]
			elif (typ==7):
				i, op = RecordRoute(trame, i)
			elif (typ==68):
				i, op = TimeStamp(trame, i)
			elif (typ==131):
				i, op = LooseSourceRoute(trame, i)
			elif (typ==137):
				i, op = StrictSourceRoute(trame, i)
			else:
				i, op = i+2, ["Erreur, option non reconnue", "Unknown"]
				cpt = cpt+1


			if (op!= ["Erreur, option non reconnue", "Unknown"] or cpt==1):#gestion de plusieurs octets d option inconnue
				if (op!= ["Erreur, option non reconnue", "Unknown"]):
					cpt = 0
				res.append(op)

	if (mod==0):
		return res, LongOp*2

	return ListOpEnText(res), LongOp*2

#----------------------------------------------------------------------------------------- DHCP
def messageDHCP(nb):
	nbDec = ConvHexDec(nb)
	if (nbDec==1):
		return "Message type: Boot Request 0x{} ({})".format(nb, nbDec)
	elif (nbDec==2):
		return "Message type: Boot Reply 0x{} ({})".format(nb, nbDec)
	return "Message type: unknown"
	

def hardwareDHCP(code):
	nbDec = ConvHexDec(code)
	dico = {0: 'NET/ROM pseudo (reserved)', 1: 'Ethernet (10Mb)', 2: 'Experimental Ethernet (3Mb)', 3: 'Amateur Radio AX.25', 4: 'Proteon ProNET Token Ring', 5: 'Chaos', 6: 'IEEE 802 Networks', 7: 'ARCNET', 8: 'Hyperchannel', 9: 'Lanstar', 10: 'Autonet Short Address', 11: 'LocalTalk', 12: 'LocalNet (IBM PCNet or SYTEK LocalNET)', 13: 'Ultra link', 14: 'SMDS', 15: 'Frame Relay', 16: 'Asynchronous Transmission Mode (ATM)', 17: 'HDLC', 18: 'Fibre Channel', 19: 'Asynchronous Transmission Mode (ATM)', 20: 'Serial Line', 21: 'Asynchronous Transmission Mode (ATM)', 22: 'MIL-STD-188-220', 23: 'Metricom', 24: 'IEEE 1394.1995', 25: 'MAPOS', 26: 'Twinaxial', 27: 'EUI-64', 28: 'HIPARP', 29: 'IP and ARP over ISO 7816-3', 30: 'ARPSec', 31: 'IPsec tunnel', 32: 'InfiniBand (TM)', 33: 'TIA-102 Project 25 Common Air Interface (CAI)', 34: 'Wiegand Interface', 35: 'Pure IP', 36: 'HW_EXP1', 37: 'HFI', 38: 'Unassigned', 256: 'HW_EXP2', 257: 'AEthernet', 258: 'Unassigned', 42: 'Reserved'}
	if ((nbDec>37 and nbDec<256) or (nbDec>257 and nbDec<65535)):
		return "0x{} ".format(code)+" ["+dico[38]+"]"
	elif (nbDec in dico):
		return "0x{} ".format(code)+" ["+dico[nbDec]+"]"
	return "Unknown (0x{})".format(code)


def BootpFlags(flag):
	if (flag=="0000"):
		return "0000 (unicast)"  
	elif (flag=="1000"):
		return "1000 (broadcast)"  
	return flag+" unknown"

def LecteurMAC(clMAC, i):
	fin = i+12
	addrMAC = ""
	while (i<fin):
		addrMAC = addrMAC + clMAC[i:i+2] + ":"
		i=i+2
	return addrMAC[:-1]	

def ClientMAC(mac):
	clientMAC = mac[:12]
	if (clientMAC!="000000000000"):
		return "\tClient MAC address: {}\n\tClient hardware address padding: {}".format(LecteurMAC(clientMAC,0), mac[12:])
	else:
		return "\tClient address not given"

def ServerHostName(octets): #trans?
	asci = toAscii(octets)
	if (asci == ""):
		return "\tServer host name not given"
	else:
		return "\tServer host name: 0x"+octets+" ("+asci+")" #il suffit de transformet ca en ascii si necessaire

def BootFileName(octets):#trans?
	asci = toAscii(octets)
	if (asci == ""):
		return "\tBoot file name not given"
	else:
		return "\tBoot file name: 0x"+octets+" ("+asci+")" #il suffit de transformet ca en ascii si necessaire

def MagicCookie(cookie):
	if (cookie=="63825363"):
		return "DHCP"
	else:
		return "Unknown"

#--------------------------------------------------------------------------------------- Options DHCP

def ListOpDHCPEnText(L):  #Fonction intermediaire pour le mode texte en optionIP
	l = len(L)
	res2 = ""
	for i in range(l):
		op = L[i]
		res2=res2+"\t"+op[0]+"\n"
		#print(op[1])
		L2 = op[1].split("\n")
		L2 = L2[:-1] #ignorer dernier element vide
		for el in L2:
			res2=res2+"\t\t"+el+"\n"
	return res2

def DHCPoption3(options, j):
	i = j
	op = ["Option {}: (0x{}) - Router Option".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)
	while (i <= FinOp):
		addrIPH, addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"Router preference {}: 0x".format(cpt)+addrIPH+" ("+addrIP+")"+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption6(options, j):
	i = j
	op = ["Option {}: (0x{}) Domain Name Server Option".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)
	while (i <= FinOp):
		addrIPH, addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"DNS server preference {}: 0x".format(cpt)+addrIPH+" ("+addrIP+")"+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	cpt= cpt+1
	i=i+8
	op.append(contenu)
	return i, op

def DHCPoption4(options, j): 
	i = j
	op = ["Option {}: (0x{}) Time Server Option".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)
	while (i <= FinOp):
		addrIPH, addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"Time Server Option preference {}: 0x".format(cpt)+addrIPH+" ("+addrIP+")"+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption12(options, j): 
	i = j
	op = ["Option {}: (0x{}) Host Name Option".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)

	nom= "Host Name: "
	octets = ""
	while (i<=FinOp):
		octets = octets+options[i]
		i=i+1
	octetsTemp = octets
	octets = toAscii(octets)
	if (octets==""):
		octets = "0x000....0 (Not given)"
	else:
		octets = "0x"+octetsTemp+" ("+octets+")"
	nom = nom + octets + "\n"
	contenu = contenu+nom
	op.append(contenu)
	return FinOp+1, op

def DHCPoption15(options, j): #trans?
	i = j
	op = ["Option {}: (0x{}) Domain Name".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)

	nom= "Domain Name: "
	octets = ""
	while (i<=FinOp):
		octets = octets+options[i]
		i=i+1
	octetsTemp = octets
	octets = toAscii(octets)
	if (octets==""):
		octets = "0x000....0 (Not given)"
	else:
		octets = "0x"+octetsTemp+" ("+octets+")"
	nom = nom + octets + "\n"
	contenu = contenu+nom
	op.append(contenu)
	return FinOp+1, op

def DHCPoption42(options, j):
	i = j
	op = ["Option {}: (0x{}) Network Time Protocol Servers Option".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)
	while (i <= FinOp):
		addrIPH, addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"Network Time Protocol Server preference {}: 0x".format(cpt)+addrIPH+" ("+addrIP+")"+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption48(options, j):
	i = j
	op = ["Option {}: (0x{}) X Window System Font Server Option".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)
	while (i <= FinOp):
		addrIPH, addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"X Window System Font Server Option preference {}: 0x".format(cpt)+addrIPH+" ("+addrIP+")"+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption61(options, j): #transformation ascii non necessaire
	i = j
	op = ["Option {}: (0x{}) Client-identifier".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	contenu = contenu+"Length: 0x{} ({})\nHardware type: {}\n".format(options[j+2:j+4], l, hardwareDHCP(options[i+4:i+6]))
	i = i+6

	nom= "Client-identifier: "
	octets = ""
	while (i<=FinOp):
		octets = octets+options[i:i+2]+":"
		i=i+2
	if (octets[0:12]=="000000000000"):
		octets = "Not given"
	nom = nom + octets[:-1] + "\n" #transforme octets en ascii si necessaire
	contenu = contenu+nom
	op.append(contenu)
	return FinOp+1, op


def DHCPoption60(options, j): #trans?
	i = j
	op = ["Option {}: (0x{}) Vendor class identifier".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)

	nom= "Vendor class identifier: "
	octets = ""
	while (i<=FinOp):
		octets = octets+options[i:i+2]+":"
		i=i+2
	if (octets[0:12]=="000000000000"):
		octets = "Not given"
	nom = nom + octets[:-1] + "\n" #transforme octets en ascii si necessaire
	contenu = contenu+nom
	op.append(contenu)
	return FinOp+1, op

def DHCPoptionPad(options, j):
	i = j
	op = ["Padding: ", ""]
	FinOp = len(options)-1
	while (i<=FinOp):
		op[0] = op[0]+"00"
		i = i+2
	return i, op

def nomOpDHCP(nb):
	dico = {0: 'Pad', 1: 'SubnetMask', 2: 'TimeOffset', 3: 'Router', 4: 'TimeServer', 5: 'NameServer', 6: 'DomainServer', 7: 'LogServer', 8: 'QuotesServer', 9: 'LPRServer', 10: 'ImpressServer', 11: 'RLPServer', 12: 'Hostname', 13: 'BootFileSize', 14: 'MeritDumpFile', 15: 'DomainName', 16: 'SwapServer', 17: 'RootPath', 18: 'ExtensionFile', 19: 'ForwardOn/Off', 20: 'SrcRteOn/Off', 21: 'PolicyFilter', 22: 'MaxDGAssembly', 23: 'DefaultIPTTL', 24: 'MTUTimeout', 25: 'MTUPlateau', 26: 'MTUInterface', 27: 'MTUSubnet', 28: 'BroadcastAddress', 29: 'MaskDiscovery', 30: 'MaskSupplier', 31: 'RouterDiscovery', 32: 'RouterRequest', 33: 'StaticRoute', 34: 'Trailers', 35: 'ARPTimeout', 36: 'Ethernet', 37: 'DefaultTCPTTL', 38: 'KeepaliveTime', 39: 'KeepaliveData', 40: 'NISDomain', 41: 'NISServers', 42: 'NTPServers', 43: 'VendorSpecific', 44: 'NETBIOSNameSrv', 45: 'NETBIOSDistSrv', 46: 'NETBIOSNodeType', 47: 'NETBIOSScope', 48: 'XWindowFont', 49: 'XWindowManager', 50: 'AddressRequest', 51: 'AddressTime', 52: 'Overload', 53: 'DHCPMsgType', 54: 'DHCPServerId', 55: 'ParameterList', 56: 'DHCPMessage', 57: 'DHCPMaxMsgSize', 58: 'RenewalTime', 59: 'RebindingTime', 60: 'ClassId', 61: 'ClientId', 62: 'NetWare/IPDomain', 63: 'NetWare/IPOption', 64: 'NIS-Domain-Name', 65: 'NIS-Server-Addr', 66: 'Server-Name', 67: 'Bootfile-Name', 68: 'Home-Agent-Addrs', 69: 'SMTP-Server', 70: 'POP3-Server', 71: 'NNTP-Server', 72: 'WWW-Server', 73: 'Finger-Server', 74: 'IRC-Server', 75: 'StreetTalk-Server', 76: 'STDA-Server', 77: 'User-Class', 78: 'DirectoryAgent', 79: 'ServiceScope', 80: 'RapidCommit', 81: 'ClientFQDN', 82: 'RelayAgentInformation', 83: 'iSNS', 84: 'REMOVED/Unassigned', 85: 'NDSServers', 86: 'NDSTreeName', 87: 'NDSContext', 88: 'BCMCSControllerDomainNamelist', 89: 'BCMCSControllerIPv4addressoption', 90: 'Authentication', 91: 'client-last-transaction-timeoption', 92: 'associated-ipoption', 93: 'ClientSystem', 94: 'ClientNDI', 95: 'LDAP', 96: 'REMOVED/Unassigned', 97: 'UUID/GUID', 98: 'User-Auth', 99: 'GEOCONF_CIVIC', 100: 'PCode', 101: 'TCode', 108: 'REMOVED/Unassigned', 109: 'OPTION_DHCP4O6_S46_SADDR', 110: 'REMOVED/Unassigned', 111: 'Unassigned', 112: 'NetinfoAddress', 113: 'NetinfoTag', 114: 'URL', 115: 'REMOVED/Unassigned', 116: 'Auto-Config', 117: 'NameServiceSearch', 118: 'SubnetSelectionOption', 119: 'DomainSearch', 120: 'SIPServersDHCPOption', 121: 'ClasslessStaticRouteOption', 122: 'CCC', 123: 'GeoConfOption', 124: 'V-IVendorClass', 125: 'V-IVendor-SpecificInformation', 126: 'Removed/Unassigned', 127: 'Removed/Unassigned', 128: 'TFTPServerIPaddress(forIPPhonesoftwareload)', 129: 'CallServerIPaddress', 130: 'Discriminationstring(toidentifyvendor)', 131: 'RemotestatisticsserverIPaddress', 132: 'IEEE802.1QVLANID', 133: 'IEEE802.1D/pLayer2Priority', 134: 'DiffservCodePoint(DSCP)forVoIPsignallingandmediastreams', 135: 'HTTPProxyforphone-specificapplications', 136: 'OPTION_PANA_AGENT', 137: 'OPTION_V4_LOST', 138: 'OPTION_CAPWAP_AC_V4', 139: 'OPTION-IPv4_Address-MoS', 140: 'OPTION-IPv4_FQDN-MoS', 141: 'SIPUAConfigurationServiceDomains', 142: 'OPTION-IPv4_Address-ANDSF', 143: 'OPTION_V4_SZTP_REDIRECT', 144: 'GeoLoc', 145: 'FORCERENEW_NONCE_CAPABLE', 146: 'RDNSSSelection', 150: 'GRUBconfigurationpathname', 151: 'status-code', 152: 'base-time', 153: 'start-time-of-state', 154: 'query-start-time', 155: 'query-end-time', 156: 'dhcp-state', 157: 'data-source', 158: 'OPTION_V4_PCP_SERVER', 159: 'OPTION_V4_PORTPARAMS', 160: 'DHCPCaptive-Portal', 161: 'OPTION_MUD_URL_V4', 175: 'Etherboot(TentativelyAssigned\xe2\x80\x932005-06-23)', 176: 'IPTelephone(TentativelyAssigned\xe2\x80\x932005-06-23)', 177: 'PacketCableandCableHome(replacedby122)', 208: 'PXELINUXMagic', 209: 'ConfigurationFile', 210: 'PathPrefix', 211: 'RebootTime', 212: 'OPTION_6RD', 213: 'OPTION_V4_ACCESS_DOMAIN', 220: 'SubnetAllocationOption', 221: 'VirtualSubnetSelection(VSS)Option', 255: 'End', 257: 'Reserved(PrivateUse'}
	#224-254 Reserved (Private Use)
	if (nb>=224 and nb<=254):
		nb= 257
	if (nb not in dico):
		return "Unasigned"
	return dico[nb]
	 
def DHCPoption55(options, j):
	i = j
	op = ["Option {}: (0x{}) Parameter Request List".format(ConvHexDec(options[j:j+2]), options[j:j+2])]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: 0x{} ({})\n".format(options[j+2:j+4], l)
	while (i<=FinOp):
		octet = options[i:i+2]
		nb = ConvHexDec(octet)
		contenu = contenu+"Parameter Request List Item: 0x{} ({}/{})\n".format(octet, nb,nomOpDHCP(nb))
		i=i+2
	op.append(contenu)
	return FinOp+1, op

def messageTypeDHCP(nb):
	nbDec = ConvHexDec(nb)
	if (nbDec==1):
		return "DHCP: 0x{} ({}/Discover)".format(nb, nbDec)
	elif (nbDec==2):
		return "DHCP: 0x{} ({}/Offer)".format(nb, nbDec)
	elif (nbDec==3):
		return "DHCP: 0x{} ({}/Request)".format(nb, nbDec)
	elif (nbDec==4):
		return "DHCP: 0x{} ({}/Decline)".format(nb, nbDec)
	elif (nbDec==5):
		return "DHCP: 0x{} ({}/ACK)".format(nb, nbDec)
	elif (nbDec==6):
		return "DHCP: 0x{} ({}/NAK)".format(nb, nbDec)
	elif (nbDec==7):
		return "DHCP: 0x{} ({}/Release)".format(nb, nbDec)
	elif (nbDec==8):
		return "DHCP: 0x{} ({}/Inform)".format(nb, nbDec)
	else:
		return "Unknown code 0x{}".format(nb, nbDec)

def optionDHCP(options, mod):
	cpt = 0
	LongOp = len(options)
	finOps = len(options)-1
	res = []
	if (options == "0"*LongOp):
		return "\tPas d'options"
	elif (options[0:2]=="ff"):
		return "\tPas d'options"
	else:
		i= 0
		while (i<=finOps):
			typ = ConvHexDec(options[i:i+2])
			op = ""
			if (typ==1):
				l = ConvHexDec(options[i+2:i+4])
				SubMaskH, SubMask = LecteurIpAdresse(options, i+4)
				i, op = i+12, ["Option {}: (0x{}) Subnet Mask ({})".format(ConvHexDec(options[i:i+2]), options[i:i+2], SubMask), "Length: 0x{} ({})\nSubnet Mask: 0x{} ({})\n".format(options[i+2:i+4], l, SubMaskH, SubMask)]
			elif (typ==3):
				i, op = DHCPoption3(options, i)
			elif (typ==6):
				i, op = DHCPoption6(options, i)
			elif (typ==51):
				l = ConvHexDec(options[i+2:i+4])
				LeaseTime = ConvHexDec(options[i+4:i+12])
				i, op = i+12, ["Option {}: (0x{}) IP Address Lease Time".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Length: 0x{} ({})\nIP Address Lease Time: 0x{} ({} seconds)\n".format(options[i+2:i+4], l, options[i+4:i+12], LeaseTime)]
			elif (typ==2):
				l = ConvHexDec(options[i+2:i+4])
				TimeOffset = ConvHexBin(options[i+4:i+12])
				i, op = i+12, ["Option {}: (0x{}) Time Offset".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Length: 0x{} ({})\nTime Offset: 0x{} ({} seconds) \n".format(options[i+2:i+4], l, options[i+4:i+12], TimeOffset)]
			elif (typ==4):
				i, op = DHCPoption4(options, i)
			elif (typ==12):
				i, op = DHCPoption12(options, i)
			elif (typ==15):
				i, op = DHCPoption15(options, i)
			elif (typ==42):
				i, op = DHCPoption42(options, i)
			elif (typ==48):
				i, op = DHCPoption48(options, i)
			elif (typ==61):
				i, op = DHCPoption61(options, i)
			elif (typ==60):
				i, op = DHCPoption60(options, i)
			elif (typ==55):
				i, op = DHCPoption55(options, i)
			elif (typ==53):
				i, op = i+6, ["Option {}: (0x{}) DHCP Message Type".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Length: 0x{} ({})\n{}\n".format(options[i+2:i+4], 1, messageTypeDHCP(options[i+4:i+6]))]
			elif (typ==50):
				ipAddrH, ipAddr = LecteurIpAdresse(options[i+4:i+12], 0)
				i, op = i+12, ["Option {}: (0x{}) Requested IP Address".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Length: 0x{} ({})\nRequested IP Address: 0x{} ({})\n".format(options[i+2:i+4], 1,ipAddrH, ipAddr)] 
			elif (typ==255):
				i, op = i+2, ["Option {}: (0x{}) End".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Option End: 0x{} ({})\n".format(options[i:i+2], 255)]
			elif (typ==59):
				l = ConvHexDec(options[i+2:i+4])
				RebindTime = ConvHexDec(options[i+4:i+12])
				i, op = i+12, ["Option {}: (0x{}) Rebinding Time Value".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Length: 0x{} ({})\nRebinding Time Value: 0x{} ({} seconds)\n".format(options[i+2:i+4], l, options[i+4:i+12], RebindTime)]
			elif (typ==54):
				ipAddrH, ipAddr = LecteurIpAdresse(options[i+4:i+12], 0)
				i, op = i+12, ["Option {}: (0x{}) DHCP Server Identifier".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Length: 0x{} ({})\nDHCP Server Identifier: 0x{} ({})\n".format(options[i+2:i+4], 4, ipAddrH, ipAddr)]
			elif (typ==0):
				i, op = DHCPoptionPad(options, i)
			elif (typ==58):
				l = ConvHexDec(options[i+2:i+4])
				RenewalTime = ConvHexDec(options[i+4:i+12])
				i, op = i+12,["Option {}: (0x{}) Renewal Time Value".format(ConvHexDec(options[i:i+2]), options[i:i+2]), "Length: 0x{} ({})\nRenewal Time Value: 0x{} ({} seconds)\n".format(options[i+2:i+4], l, options[i+4:i+12], RenewalTime)]
			else:
				i, op = i+2, ["Erreur, option non reconnue {}".format(options[i:i+2])]
				cpt = cpt+1


			if (op[0][0:27]!= "Erreur, option non reconnue" or cpt==1):#gestion de plusieurs octets d option inconnue
				if (op[0][0:27]!= "Erreur, option non reconnue"):
					cpt = 0
				res.append(op)

	if (mod==0):
		return res
	return ListOpDHCPEnText(res)



