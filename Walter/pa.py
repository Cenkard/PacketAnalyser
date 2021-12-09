import math as m
import sys
from outils import *
#----------------------------------------------Convertisseurs
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
		while (res[i]=='0' and i<l):
			i=i+1;
	return res

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

#---------------------------------------------- Netoyage texte 

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

	#prendre les octets hexadecimaux qui peuvent etre texte ou pas
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
		tempi=i
		verif, i, res = VerifierOffset(FichierTemp, i, TailleOffset) #Verif = si ligne valide (correspond a offset), i= ligne de prochain offset valide, res = ligne validee sans texte ou ligne invalide
		TrameValide = []

		#ajout trame
		while (verif!=0):
			trame.append(res)
			if (verif == -1):
				TrameValide.append("Erreur dans trame ({}), verifier ligne : ".format(len(Fichier)+1)+str(tempi+1))

			tempi= i

			verif, i, res = VerifierOffset(FichierTemp, i, TailleOffset)

		#Gestion de la derniere ligne de la trame
		res = DerLigne(res)
		trame.append(res+" {}".format(tempi+1))
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


def creerTabTrame(fichier,tab): #recupere les trames valides sous forme de string contenant tous les hexadecimaux a la suite
	i=0
	j=0
	trameValide = []
	tabTrame = []
	tab2 = tab
	while(i<len(tab)):
		if(tab[i]==[]):
			trameValide.append(fichier[i])
		i+=1

	for trame in trameValide:
		tabTrame.append("")
		for ligne in trame:
			i=0
			ligneCopy = ""
			while(ligne[i]!=' '):
				i=i+1
			i=i+1
			ligneCopy = ''.join(str(item) for item in ligne[i:])
			tabTrame[j] = tabTrame[j]+ligneCopy
		j=j+1

	#Gestion de la derniere ligne de chaque trame
	l = len(tabTrame)
	for i in range(l):
		longueurTrameChiffre = 28+ConvHexDec(tabTrame[i][32:36])*2
		vraiLongueurTrameChiffre = len(tabTrame[i][:-2])
		if (vraiLongueurTrameChiffre>=longueurTrameChiffre):
			tabTrame[i] = tabTrame[i][:longueurTrameChiffre]
		else:
			trame = tabTrame[i]
			k = len(trame)-1
			while (trame[k]!=" "):
				k=k-1
			erreur = "Erreur trame ({}), ligne ({})".format(i, tabTrame[i][k+1:])
			tab2[i].append(erreur)
			tabTrame.pop(i)
			#print(erreur)
			
	return tabTrame
 

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
	return addrIP[:-1]	

def RecordRoute(trame, j):
	lrr = ConvHexDec(trame[j+2: j+4]) #longueur en octets
	Pointer = ConvHexDec(trame[j+4:j+6])
	L= [] #liste de textes a inserer L[0] = ligne de nom, L[1] = type, L[2] = longueur, L[3] = pointeur
	L.append("IP Option - Record Route ({} bytes)\n".format(lrr))
	contenu = "Type: 7\nLength: {}\nPointer: {}\n".format(lrr, Pointer)
	finOp = j+lrr*2-1 #indice du dernier chiffre hexadecimal de cette option
	i = j+6
	cpt= 0
	Pointer = (Pointer-4)/4
	while (i<=finOp):
		addrIP = LecteurIpAdresse(trame, i)
		if (addrIP == "0.0.0.0"):
			contenu = contenu + "Empty Route: "+addrIP+"\n"
		else:
			contenu = contenu + "Recorded Route: "+addrIP+"\n"
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
	L.append("IP Option - Time Stamp ({} bytes)\n".format(lts))
	Pointer = ConvHexDec(trame[j+4:j+6])
	OverflowBin = ConvHexBin(trame[j+6])
	OverflowDec = ConvHexDec(trame[j+6])
	Flag = ConvHexBin(trame[j+7])

	contenu = "Type: 68\nLength: {}\nPointer: {}\n{} .... = Overflow: {}\n.... {} = Flag: {}\n".format(lts, Pointer, OverflowBin, OverflowDec, Flag, FlagTextTimeStamp(Flag))

	i = j+8
	cpt = 0

	if (Flag=="0000"):
		while (i<=finOp):
			nb = str(ConvHexDec(trame[i:i+8]))
			contenu = contenu +"Time Stamp: "+ nb+"\n"
			i = i +8

	elif (Flag == "0001" or Flag=="0011"):
		while (i<=finOp):
			addrIP = LecteurIpAdresse(trame, i)
			i = i + 8
			nb = str(ConvHexDec(trame[i:i+8]))
			i=i+8

			if (addrIP=="0.0.0.0"):
				contenu=contenu+"Address: -\nTime Stamp: {}\n".format(nb)
			else:
				contenu=contenu+"Address: {}\nTime Stamp: {}\n".format(addrIP, nb)

	L.append(contenu)
	return i, L

def  LooseSourceRoute(trame, j):
	lsr = ConvHexDec(trame[j+2: j+4]) #longueur en octets
	Pointer = ConvHexDec(trame[j+4:j+6])
	L= [] #liste de textes a inserer L[0] = ligne de nom, L[1] = type, L[2] = longueur, L[3] = pointeur
	L.append("IP Option - Loose Source Route ({} bytes)\n".format(lsr))
	contenu = "Type: 131\nLength: {}\nPointer: {}\n".format(lsr, Pointer)
	finOp = j+lsr*2-1 #indice du dernier chiffre hexadecimal de cette option
	i = j+6
	cpt= 0
	Pointer = (Pointer-4)/4
	while (i<=finOp):
		addrIP = LecteurIpAdresse(trame, i)
		if (i!=finOp-7):
			contenu = contenu + "Source Route: "+addrIP+"\n"
		else:
			contenu = contenu + "Destination: "+addrIP+"\n"
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
	L.append("IP Option - Strict Source Route ({} bytes)\n".format(lss))
	contenu = "Type: 137\nLength: {}\nPointer: {}\n".format(lss, Pointer)
	finOp = j+lss*2-1 #indice du dernier chiffre hexadecimal de cette option
	i = j+6
	cpt= 0
	Pointer = (Pointer-4)/4
	while (i<=finOp):
		addrIP = LecteurIpAdresse(trame, i)
		if (i!=finOp-7):
			contenu = contenu + "Source Route: "+addrIP+"\n"
		else:
			contenu = contenu + "Destination: "+addrIP+"\n"
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
				i, op= finOps+1, ["IP Option - End of Option List (EOL)\n", "Type: 0\n"]
			elif (typ==1):
				i, op = i+2, ["IP Option - No-Operation (NOP)\n", "Type: 1\n"]
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
				if (op!= "Erreur, option non reconnue"):
					cpt = 0
				res.append(op)

	if (mod==0):
		return res, LongOp*2

	return ListOpEnText(res), LongOp*2

#----------------------------------------------------------------------------------------- DHCP
def messageDHCP(nb):
	nbDec = ConvHexDec(nb)
	if (nbDec==1):
		return "Message type: Boot Request ({})".format(nbDec)
	elif (nbDec==2):
		return "Message type: Boot Reply ({})".format(nbDec)
	return "Message type: unknown"
	

def hardwareDHCP(code):
	nbDec = ConvHexDec(code)
	dico = {0: 'NET/ROM pseudo (reserved)', 1: 'Ethernet (10Mb)', 2: 'Experimental Ethernet (3Mb)', 3: 'Amateur Radio AX.25', 4: 'Proteon ProNET Token Ring', 5: 'Chaos', 6: 'IEEE 802 Networks', 7: 'ARCNET', 8: 'Hyperchannel', 9: 'Lanstar', 10: 'Autonet Short Address', 11: 'LocalTalk', 12: 'LocalNet (IBM PCNet or SYTEK LocalNET)', 13: 'Ultra link', 14: 'SMDS', 15: 'Frame Relay', 16: 'Asynchronous Transmission Mode (ATM)', 17: 'HDLC', 18: 'Fibre Channel', 19: 'Asynchronous Transmission Mode (ATM)', 20: 'Serial Line', 21: 'Asynchronous Transmission Mode (ATM)', 22: 'MIL-STD-188-220', 23: 'Metricom', 24: 'IEEE 1394.1995', 25: 'MAPOS', 26: 'Twinaxial', 27: 'EUI-64', 28: 'HIPARP', 29: 'IP and ARP over ISO 7816-3', 30: 'ARPSec', 31: 'IPsec tunnel', 32: 'InfiniBand (TM)', 33: 'TIA-102 Project 25 Common Air Interface (CAI)', 34: 'Wiegand Interface', 35: 'Pure IP', 36: 'HW_EXP1', 37: 'HFI', 38: 'Unassigned', 256: 'HW_EXP2', 257: 'AEthernet', 258: 'Unassigned', 42: 'Reserved'}
	if ((nbDec>37 and nbDec<256) or (nbDec>257 and nbDec<65535)):
		return dico[38]+" (0x{})".format(code)
	elif (nbDec in dico):
		return dico[nbDec]+" (0x{})".format(code)
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
	if (octets[0:20]=="00000000000000000000"):
		return "\tServer host name not given"
	else:
		nouvOctets = octets[:2]
		octets = octets[2:]
		i=0
		while(i!=126 and octets[i]!=0):
			nouvOctets= nouvOctets+el
			i=i+1
		return "\tServer host name: "+nouvOctets #il suffit de transformet ca en ascii si necessaire

def BootFileName(octets):#trans?
	if (octets[0:20]=="00000000000000000000"):
		return "\tBoot file name not given"
	else:
		nouvOctets = octets[:2]
		octets = octets[2:]
		i=0
		while(i!=126 and octets[i]!=0):
			nouvOctets= nouvOctets+el
			i=i+1
		return "\tBoot file name: "+nouvOctets #il suffit de transformet ca en ascii si necessaire

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
	op = ["Option: ({}) Router Option".format(3)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: {}\n".format(l)
	while (i <= FinOp):
		addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"Router preference {}: ".format(cpt)+addrIP+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption6(options, j):
	i = j
	op = ["Option: ({}) Domain Name Server Option".format(6)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: {}\n".format(l)
	while (i <= FinOp):
		addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"DNS server preference {}: ".format(cpt)+addrIP+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption4(options, j): 
	i = j
	op = ["Option: ({}) Time Server Option".format(4)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: {}\n".format(l)
	while (i <= FinOp):
		addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"Time Server Option preference {}: ".format(cpt)+addrIP+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption12(options, j): #trans?
	i = j
	op = ["Option: ({}) Host Name Option".format(12)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: {}\n".format(l)

	nom= "Host Name: "
	octets = ""
	while (i<=FinOp and options[i:i+2]!="00"):
		octets = octets+options[i:i+2]
		i=i+2
	nom = nom + octets + "\n" #transforme octets en ascii si necessaire
	contenu = contenu+nom
	op.append(contenu)
	return FinOp+1, op

def DHCPoption15(options, j): #trans?
	i = j
	op = ["Option: ({}) Domain Name".format(15)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: {}\n".format(l)

	nom= "Domain Name: "
	octets = ""
	while (i<=FinOp and options[i:i+2]!="00"):
		octets = octets+options[i:i+2]
		i=i+2
	nom = nom + octets + "\n" #transforme octets en ascii si necessaire
	contenu = contenu+nom
	op.append(contenu)
	return FinOp+1, op

def DHCPoption42(options, j):
	i = j
	op = ["Option: ({}) Network Time Protocol Servers Option".format(42)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: {}\n".format(l)
	while (i <= FinOp):
		addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"Network Time Protocol Server preference {}: ".format(cpt)+addrIP+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption48(options, j):
	i = j
	op = ["Option: ({}) X Window System Font Server Option".format(48)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	cpt = 1
	i=i+4
	contenu = contenu+"Length: {}\n".format(l)
	while (i <= FinOp):
		addrIP = LecteurIpAdresse(options, i)
		contenu= contenu+"X Window System Font Server Option preference {}: ".format(cpt)+addrIP+"\n"
		cpt= cpt+1
		i=i+8
	op.append(contenu)
	return i, op

def DHCPoption61(options, j): #transformation ascii non necessaire
	i = j
	op = ["Option: ({}) Client-identifier".format(61)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	contenu = contenu+"Length: {}\nHardware type: {}\n".format(l, hardwareDHCP(options[i+4:i+6]))
	i = i+6

	nom= "Client-identifier: "
	octets = ""
	while (i<=FinOp and options[i:i+2]!="00"):
		octets = octets+options[i:i+2]+":"
		i=i+2
	nom = nom + octets[:-1] + "\n" #transforme octets en ascii si necessaire
	contenu = contenu+nom
	op.append(contenu)
	return FinOp+1, op


def DHCPoption60(options, j): #trans?
	i = j
	op = ["Option: ({}) Vendor class identifier".format(60)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: {}\n".format(l)

	nom= "Vendor class identifier: "
	octets = ""
	while (i<=FinOp and options[i:i+2]!="00"):
		octets = octets+options[i:i+2]
		i=i+2
	nom = nom + octets + "\n" #transforme octets en ascii si necessaire
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
	op = ["Option: ({}) Parameter Request List".format(55)]
	contenu = ""
	l = ConvHexDec(options[i+2:i+4])
	FinOp = i+4+l*2-1
	i = i+4
	contenu = contenu+"Length: {}\n".format(l)
	while (i<=FinOp):
		octet = options[i:i+2]
		nb = ConvHexDec(octet)
		contenu = contenu+"Parameter Request List Item: ({}) {}\n".format(nb, nomOpDHCP(nb))
		i=i+2
	op.append(contenu)
	return FinOp+1, op

def messageTypeDHCP(nb):
	nbDec = ConvHexDec(nb)
	if (nbDec==1):
		return "DHCP: Discover ({})".format(nbDec)
	elif (nbDec==2):
		return "DHCP: Offer ({})".format(nbDec)
	elif (nbDec==3):
		return "DHCP: Request ({})".format(nbDec)
	elif (nbDec==4):
		return "DHCP: Decline ({})".format(nbDec)
	elif (nbDec==5):
		return "DHCP: ACK ({})".format(nbDec)
	elif (nbDec==6):
		return "DHCP: NAK ({})".format(nbDec)
	elif (nbDec==7):
		return "DHCP: Release ({})".format(nbDec)
	elif (nbDec==8):
		return "DHCP: Inform ({})".format(nbDec)
	else:
		return "Unknown code".format(nbDec)

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
				SubMask = LecteurIpAdresse(options, i+4)
				i, op = i+12, ["Option: ({}) Subnet Mask ({})".format(typ, SubMask), "Length: {}\nSubnet Mask: {}\n".format(l, SubMask)]
			elif (typ==3):
				i, op = DHCPoption3(options, i)
			elif (typ==6):
				i, op = DHCPoption6(options, i)
			elif (typ==51):
				l = ConvHexDec(options[i+2:i+4])
				LeaseTime = ConvHexDec(options[i+4:i+12])
				i, op = i+12, ["Option: ({}) IP Address Lease Time".format(typ), "Length: {}\nIP Address Lease Time: ({}) seconds\n".format(l, LeaseTime)]
			elif (typ==2):
				l = ConvHexDec(options[i+2:i+4])
				TimeOffset = ConvHexBin(options[i+4:i+12])
				i, op = i+12, ["Option: ({}) Time Offset".format(typ), "Length: {}\nTime Offset: ({}) seconds\n".format(l, TimeOffset)]
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
				i, op = i+6, ["Option: ({}) DHCP Message Type".format(typ), "Length: {}\n{}\n".format(1, messageTypeDHCP(options[i+4:i+6]))]
			elif (typ==50):
				i, op = i+12, ["Option: ({}) Requested IP Address".format(typ), "Length: {}\nRequested IP Address: {}\n".format(1,LecteurIpAdresse(options[i+4:i+12], 0))]
			elif (typ==255):
				i, op = i+2, ["Option: ({}) End".format(typ), "Option End: {}\n".format(typ)]
			elif (typ==59):
				l = ConvHexDec(options[i+2:i+4])
				RebindTime = ConvHexDec(options[i+4:i+12])
				i, op = i+12, ["Option: ({}) Rebinding Time Value".format(typ), "Length: {}\nRebinding Time Value: ({}) seconds\n".format(l, RebindTime)]
			elif (typ==54):
				i, op = i+12, ["Option: ({}) DHCP Server Identifier".format(typ), "Length: {}\nDHCP Server Identifier: {}\n".format(4, LecteurIpAdresse(options[i+4:i+12], 0))]
			elif (typ==0):
				i, op = DHCPoptionPad(options, i)
			elif (typ==58):
				l = ConvHexDec(options[i+2:i+4])
				RenewalTime = ConvHexDec(options[i+4:i+12])
				i, op = i+12,["Option: ({}) Renewal Time Value".format(typ), "Length: {}\nRenewal Time Value: ({}) seconds\n".format(l, RenewalTime)]
			else:
				i, op = i+2, ["Erreur, option non reconnue {}".format(typ), "Unknown"]
				cpt = cpt+1


			if (op!= ["Erreur, option non reconnue {}".format(typ), "Unknown"] or cpt==1):#gestion de plusieurs octets d option inconnue
				if (op!= "Erreur, option non reconnue"):
					cpt = 0
				res.append(op)
	#print(res)

	if (mod==0):
		return res
	return ListOpDHCPEnText(res)


#Fichier, tab = TextCleanerTrame("trame.txt")
#listTrame, tab= creerTabTrame(Fichier,tab)
#print(listTrame)
#fichier, tab = TextCleanerTrame("test 2.txt")
#fichier = creerTabTrame(fichier, tab)
#AfficherDim2(fichier)




