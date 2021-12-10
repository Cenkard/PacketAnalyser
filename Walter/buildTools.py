from pa import *
from structure import *
from outils import *

def dnsType(chaine):
	err=0
	
	if(chaine=="0001"):
		typ = "IPv4 adress (A)"
	elif(chaine=="0005"):
		typ = "CNAME"
	elif(chaine=="0002"):
		typ = "Name of the authoritative server (NS)"
	elif(chaine=="000F" or chaine=="000f"):
		typ = "Name of the mail server (MX)" 
	elif(chaine=="000C" or chaine=="000c"):
		typ = "PTR (pointer)" 
	else:
		typ = "Error: no query type recognised"
		err=1
	typ = typ+" ("+chaine+")"

	return typ,err

def creerQuery(data,numQ):
	queries = data
	querTab = []
	cpt=0
	i = 0
	while(cpt < numQ and i+4<len(data)):
		while(queries[i:i+4] != "0001" and i+4<len(queries)):
			i += 1
		typ,err = dnsType(queries[i-4:i])
		if(err== 1):
			i+=4
		name = queries[i-8:i-4]
		typeQ,err = dnsType(queries[i-4:i])
		name = queries[:i-4]
		ind=0
		ascii_lab=""
		while(ind+2<len(name)):
			if(name[ind:ind+2] in ["01","02","03","04","05","06","07","08","09","0A","0a","0B","0b","0C","0c","0D","0d","0E","0e","0F","0f"]):
				if(ind<2):
					pass;
				else:
					ascii_lab = ascii_lab+"."
			elif((ConvHexDec(name[ind:ind+2])>=65 and ConvHexDec(name[ind:ind+2])<=122) or (ConvHexDec(name[ind:ind+2])>=48 and ConvHexDec(name[ind:ind+2])<=57)):
				ascii_lab = ascii_lab + bytearray.fromhex(name[ind:ind+2]).decode()
			ind=ind+2
		typeQ,err = dnsType(queries[i-4:i])

		if(queries[i:i+4]=="0001"):
			classe = "Classe : Internet"
			classe = classe+" ("+queries[i:i+4]+")"
		else:
			classe = "Error: no query class recognised"

		querTab.append(dnsQueries(name,ascii_lab,typeQ,classe))
		cpt += 1
		i=i+4

	resteQ = queries[i:]

	return querTab,resteQ	#retourne un tableau contenant toutes les queries repertoriees (en fonction du nombre annonce) et le reste de la trame

def creerA(data,numA):		#retourne un tableau contenant toutes les answers/authority/addition (dependant de l appel) repertoriees (en fonction du nombre annonce) et le reste de la trame"""
	paquet = data
	ansTab = []
	typ=""
	cpt=0
	i = 0
	j = 4
	while(cpt < numA):
		while(paquet[i:j] != "0001" and j<len(paquet)):

			i += 1
			j += 1
		typ,err = dnsType(paquet[i-4:j-4])

		if(err== 1):
			i+=4
			j+=4

		name = paquet[i-8:i-4]
		typeA,err = dnsType(paquet[i-4:i])

		if(paquet[i:j]=="0001"):
			classe = "Internet"
		else:
			classe = "Error: no query class recognised"
		classe = classe+" ("+paquet[i:j]+")"

		ttl = paquet[j:j+8]
		j+=8
		rdata_length = paquet[j:j+4]
		j+=4

		data = paquet[j:j+ConvHexDec(rdata_length)*2]
		j= j+ ConvHexDec(rdata_length)*2
		ansTab.append(dnsAnswers(name,typeA,classe,ttl,rdata_length,data))
		cpt += 1
		i=j
		j=i+4

	resteA = paquet[j:]
	return ansTab,resteA

def loadDnsAAAbis(tab,dataDns,trame,length):
	labelTab = searchLabel(trame)
	tabA=[]
	for paquet in tab:
		tmp_paq = paquet
		tmp_paq.name,tmp_paq.ascii_name = restoreData(paquet.name,trame)
		if("(A)" not in paquet.typeA):
			dat,asc_dat = restoreData(paquet.data,trame)
			tmp_paq.data = dat
			tmp_paq.ascii_data = asc_dat

		tabA.append(tmp_paq)
	return tabA

def restoreData(paquet,trame):
	labelTab = searchLabel(trame)
	listA=[]
	listRet=[]
	data=""
	ascii_data=""
	i=0
	while(i+4<=len(paquet)):
		listA.append((paquet[i:i+4],""))
		i=i+4
	i=0
	b=0
	while(i<len(listA)):
		for pointer,label,ascii_lab in labelTab:
			if(listA[i][0]==pointer):
				listRet.append((label,ascii_lab))
				b=1
		if(b==0):
			listRet.append(listA[i])
		else:
			b=0
		i+=1
	data = ''.join(str(hexa) for hexa,asc in listRet)
	i=0
	while(i+2<=len(data)):
		if(data[i:i+2] in ["01","02","03","04","05","06","07","08","09","0A","0a","0B","0b","0C","0c","0D","0d","0E","0e","0F","0f"]):
			if(i<2):
				pass;
			else:
				ascii_data = ascii_data+"."
		elif((ConvHexDec(data[i:i+2])>=65 and ConvHexDec(data[i:i+2])<=122) or (ConvHexDec(data[i:i+2])>=48 and ConvHexDec(data[i:i+2])<=57)):
			ascii_data = ascii_data + bytearray.fromhex(data[i:i+2]).decode()
		i=i+2

	return data,ascii_data

def searchLabel(paquet):
	label=[]
	i=0
	j=2
	tabP = []
	while(j<len(paquet)):
		if("c0" in paquet[i:j]):
			tabP.append(paquet[i:j+2])
			i+=2
			j+=2
		i+=2
		j+=2
	for pointer in tabP:
		pt_dec = ConvHexDec(pointer[1:])*2
		i=pt_dec
		lab=""
		ascii_lab=""
		while(paquet[i:i+2]!="00" and paquet[i:i+2]!="c0"):
			lab = lab + paquet[i:i+2]
			if(paquet[i:i+2] in ["01","02","03","04","05","06","07","08","09","0A","0a","0B","0b","0C","0c","0D","0d","0E","0e","0F","0f"]):
				if(i<pt_dec+2):
					pass;
				else:
					ascii_lab = ascii_lab+"."
			elif((ConvHexDec(paquet[i:i+2])>=65 and ConvHexDec(paquet[i:i+2])<=122) or (ConvHexDec(paquet[i:i+2])>=48 and ConvHexDec(paquet[i:i+2])<=57)):
				ascii_lab = ascii_lab + bytearray.fromhex(paquet[i:i+2]).decode("ASCII")
			i=i+2
		label.append((pointer,lab,ascii_lab))
	return label

def toAscii(data):
	i=0
	ascii_data=""
	while(i+2<=len(data)):
		if(data[i:i+2] in ["01","02","03","04","05","06","07","08","09","0A","0a","0B","0b","0C","0c","0D","0d","0E","0e","0F","0f"]):
			if(i<2):
				pass;
			else:
				ascii_data = ascii_data+"."
		elif((ConvHexDec(data[i:i+2])>=65 and ConvHexDec(data[i:i+2])<=122) or (ConvHexDec(data[i:i+2])>=48 and ConvHexDec(data[i:i+2])<=57)):
			ascii_data = ascii_data + bytearray.fromhex(data[i:i+2]).decode()
		i=i+2
	return ascii_data

def creerDNS(trame):	#cree le paquet dns
	dataDns = DNS(trame[:4],trame[4:8],trame[8:12],trame[12:16],trame[16:20],trame[20:24])
	queries = trame[24:]
	dataDns.query,resteQ = creerQuery(queries,ConvHexDec(dataDns.questions))
	if(len(resteQ)!= 0):
		ansTab,reste = creerA(resteQ,ConvHexDec(dataDns.answerRRs))
		ansTab = loadDnsAAAbis(ansTab,dataDns,trame,dataDns.answerRRs)
		dataDns.answers = ansTab
		authTab,reste = creerA(reste,ConvHexDec(dataDns.authRRs))
		authTab = loadDnsAAAbis(authTab,dataDns,trame,dataDns.authRRs)
		dataDns.authority = authTab
		addTab,reste = creerA(reste,ConvHexDec(dataDns.addRRs))
		addTab = loadDnsAAAbis(addTab,dataDns,trame,dataDns.addRRs)
		dataDns.addition = addTab
	return dataDns

def creerDHCP(dhcpData):	#cree le paquet DHCP -------------------------------------------------------------- modifie
	dataDHCP = DHCP(dhcpData[:2],dhcpData[2:4],dhcpData[4:6],dhcpData[6:8],dhcpData[8:16],dhcpData[16:20],dhcpData[20:24],dhcpData[24:32],dhcpData[32:40],dhcpData[40:48], dhcpData[48: 56], dhcpData[56:88],dhcpData[88:216],dhcpData[216:472], dhcpData[472: 480], dhcpData[480:])
	return dataDHCP
"""
def creerTabTrame(fichier,tab): #recupere les trames valides sous forme de string contenant tous les hexadecimaux a la suite
	i=0
	j=0
	trameValide = []
	tabTrame = []
	while(i<len(tab)):
		if(tab[i]==1):
			trameValide.append(fichier[i])
		i+=1
	print(trameValide)
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
	return tabTrame

def creerTrame(fichier,tab):	#cree l'entete ethernet en fonction du tableau de trames valides 
	cpt=0
	listTrame = []
	tabTrame = creerTabTrame(fichier,tab)
	for trame in tabTrame:
		cpt+=1
		newTrame = Trame(cpt,trame[:12],trame[12:24])
		newTrame.typ = trame[24:28]

		if(newTrame.typ == "0800"):			#verification du type datagrame IP
			tabFrag = ConvHexBin(trame[40:44])
			flags = tabFrag[:3]
			fragOffset = tabFrag[4:]
			dataEth = DataIP(trame[28:29],trame[29:30],trame[30:32],trame[32:36],trame[36:40],flags,fragOffset,sourceIP = trame[52:60],destinationIP = trame[60:68])
			
			dataEth.TTL = trame[44:46]
			dataEth.protocol = trame[46:48]
			dataEth.headerChecksum = trame[48:52]
			if(dataEth.protocol == "01"):						#attribution des donnees ICMP
				dataEth = ICMP(trame[68:70],trame[70:72],trame[72:76])

			elif(dataEth.protocol == "11"):					#attribution des donnees UDP
				dataIP = UDP(trame[68:72],trame[72:76])
				dataIP.length = trame[76:80]
				dataIP.checksum = trame[80:84]

				if(ConvHexDec(dataIP.sourcePortNum) == 67 or ConvHexDec(dataIP.sourcePortNum) == 68):	#attribution des donnees DHCP
					dataUDP = creerDHCP(trame[84:])

				elif(ConvHexDec(dataIP.sourcePortNum) == 53 or ConvHexDec(dataIP.destPortNum) == 53):
					dataUDP = creerDNS(trame[84:])
				else:
					dataUDP = noneTypeData(trame[84:],"Donnee UDP non identifiee")

				dataIP.data = dataUDP
			else:
				dataIP = noneTypeData(trame[68:],"Donnee non identifiee")

			dataEth.data = dataIP
		else:
			dataEth = noneTypeData(trame[28:],"Donnee non identifiee")

		newTrame.data = dataEth
		listTrame.append(newTrame)
	return listTrame

"""
def creerTabTrame(fichier,tab): #Prend en entre les trames, et un tableau indiquant validite des trames
	#retourne tabTrame2: tableau de trames, une trame = un string d'octets sans offset. Elle verifie aussi validite de chaque trame en calculant la taille totale de chaque trame
	i=0
	j=0
	trameValide = []
	tabTrame = []
	tab2 = tab
	while(i<len(tab)): #prendre les trames valides de bases (sans erreurs)
		if(tab[i]==[]):
			trameValide.append(fichier[i])
		i+=1

	for trame in trameValide: #transforme chque trame en un string d'octets
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

	#Gestion de la derniere ligne de chaque trame, donc verification de la taille de la trame
	l = len(tabTrame)
	tabTrame2 = []
	for i in range(l): #pour chaque trame s
		trame = tabTrame[i]
		k = len(trame)-1 
		while (trame[k]!=" "): #k va contenir la fin de la trame. Car j'ai sauvegarde dans trame[k+1:] le numero de ligne de la derniere ligne de cette trame 
			k=k-1
		longueurTrameChiffre = 28+ConvHexDec(trame[32:36])*2 #longueur en theorie en fonction de 14 + champs total length de IP
		vraiLongueurTrameChiffre = len(trame[:k]) #la veritable longueur de la trame, on enleve le numero de la derniere ligne a la fin, que j'ai ajoute dans la fonction TextCleanerTrame 
		if (vraiLongueurTrameChiffre>=longueurTrameChiffre):
			tabTrame2.append(trame[:longueurTrameChiffre])
		else:
			erreur = "Erreur trame ({}), ligne ({}), trame incomplete...".format(i, trame[k+1:]) #On renvoit derniere ligne de la trame car la trame est incomplete..
			tab2[i].append(erreur) #ajout erreur lie a la derniere ligne ou la taille totale
	return tabTrame2
 

def creerTrame(fichier,tab):	#cree l'entete ethernet en fonction du tableau de trames valides, NE PAS OUBLIER DE AJOUTER DECALAGE OPTIONS IP #------------------------------------  options + decalage
	cpt=0
	listTrame = []
	tabTrame = creerTabTrame(fichier,tab)
	for trame in tabTrame:
		dataEth = ""
		dataIP = ""
		dataUDP = ""

		cpt+=1
		newTrame = Trame(cpt,trame[:12],trame[12:24])
		newTrame.typ = trame[24:28]

		if(newTrame.typ == "0800"):			#verification du type datagrame IP
			#print(trame[40:44])
			tabFrag = ConvHexBin(trame[40:44])
			flags = tabFrag[:3]
			fragOffset = tabFrag[4:]
			dataEth = DataIP(trame[28:29],trame[29:30],trame[30:32],trame[32:36],trame[36:40],flags,fragOffset,sourceIP = trame[52:60],destinationIP = trame[60:68])
			
			dataEth.TTL = trame[44:46]
			dataEth.protocol = trame[46:48]
			dataEth.headerChecksum = trame[48:52]
			dataEth.options, decalageIP = optionIP(trame, 1)

			if(dataEth.protocol == "11"):					#attribution des donnees UDP
				dataIP = UDP(trame[decalageIP+68:decalageIP+72],trame[decalageIP+72:decalageIP+76])
				dataIP.length = trame[decalageIP+76:decalageIP+80]
				dataIP.checksum = trame[decalageIP+80:decalageIP+84]

				if(ConvHexDec(dataIP.sourcePortNum) == 67 or ConvHexDec(dataIP.sourcePortNum) == 68 or ConvHexDec(dataIP.destPortNum) == 67 or ConvHexDec(dataIP.destPortNum)==68):	#attribution des donnees DHCP
					dataUDP = creerDHCP(trame[decalageIP+84:])

				elif(ConvHexDec(dataIP.sourcePortNum) == 53 or ConvHexDec(dataIP.destPortNum) == 53):
					
					dataUDP = creerDNS(trame[decalageIP+84:])
				else:
					dataUDP = noneTypeData(trame[decalageIP+84:],"Donnee UDP non identifiee")

				dataIP.data = dataUDP
			else:
				dataIP = noneTypeData(trame[decalageIP+68:],"Donnee non identifiee")

			dataEth.data = dataIP
		else:
			dataEth = noneTypeData(trame[28:],"Donnee non identifiee")

		newTrame.data = dataEth
		listTrame.append(newTrame)
	return listTrame



"""------- TEST NON CONCLUANTS... ---------
def recreeTrame(trame,labelTab):
	i=0
	tab_tri = []
	trameRet=""
	l=len(trame)
	while(i<l):
		for pointer,label,ascii_lab in labelTab:
			if(trame[i:i+4] == pointer):
				trame = trame.replace(trame[i:i+4],label)
				tab_tri.append((i,i+len(label)))
		i+=1
	i=0
	l=len(trame)
	while(i<l):
		if(trame[i:i+2]=="c0"):
			return recreeTrame(trame,labelTab)
		i+=2
	return trame,tab_tri

def creerDNSbis(trame):	#cree le paquet dns
	dataDns = DNS(trame[:4],trame[4:8],trame[8:12],trame[12:16],trame[16:20],trame[20:24])
	trame, tab_tri = recreeTrame(trame,searchLabel(trame))
	dataDns.query,ind = creerQuery(trame[24:],ConvHexDec(dataDns.questions))
	ind = ind
	if(len(trame[ind:])!=0):
		print(trame[24:])
		ansTab,ind = creerAbis(trame[24:],ConvHexDec(dataDns.answerRRs),tab_tri,ind)
		dataDns.answers = ansTab
		authTab,ind = creerAbis(trame[24:],ConvHexDec(dataDns.authRRs),tab_tri,ind)
		authTab = loadDnsAAAbis(authTab,dataDns,trame,dataDns.authRRs)
		dataDns.authority = authTab
		addTab,ind = creerAbis(trame[24:],ConvHexDec(dataDns.addRRs),tab_tri,ind)
		addTab = loadDnsAAAbis(addTab,dataDns,trame,dataDns.addRRs)
		dataDns.addition = addTab
	return dataDns

def creerQuerybis(data,numQ):
	queries = data
	querTab = []
	cpt=0
	i = 0
	while(cpt < numQ and i+4<len(data)):
		while(queries[i:i+4] != "0001" and i+4<len(queries)):
			i += 1
		typ,err = dnsType(queries[i-4:i])
		if(err== 1):
			i+=4
		name = queries[i-8:i-4]
		typeQ,err = dnsType(queries[i-4:i])
		name = queries[:i-4]
		ind=0
		ascii_lab=""
		while(ind+2<len(name)):
			if(name[ind:ind+2] in ["01","02","03","04","05","06","07","08","09","0A","0a","0B","0b","0C","0c","0D","0d","0E","0e","0F","0f"]):
				if(ind<2):
					pass;
				else:
					ascii_lab = ascii_lab+"."
			elif((ConvHexDec(name[ind:ind+2])>=65 and ConvHexDec(name[ind:ind+2])<=122) or (ConvHexDec(name[ind:ind+2])>=48 and ConvHexDec(name[ind:ind+2])<=57)):
				ascii_lab = ascii_lab + bytearray.fromhex(name[ind:ind+2]).decode()
			ind=ind+2
		typeQ,err = dnsType(queries[i-4:i])

		if(queries[i:i+4]=="0001"):
			classe = "Classe : Internet"
			classe = classe+" ("+queries[i:i+4]+")"
		else:
			classe = "Error: no query class recognised"

		querTab.append(dnsQueries(name,ascii_lab,typeQ,classe))
		cpt += 1
		i=i+4

	return querTab,i

def creerAbis(data,numA,tab_tri,ind):		#retourne un tableau contenant toutes les answers/authority/addition (dependant de l appel) repertoriees (en fonction du nombre annonce) et le reste de la trame
	paquet = data
	ansTab = []
	typ=""
	cpt=0
	i = ind
	j = i+4
	while(cpt < numA):		
		while(paquet[i:j]!="0001"):
			i+=2
			j+=2
		name=paquet[ind:i-4]
		ascii_name=toAscii(name)
		print(name,ascii_name)

		typ,err = dnsType(paquet[i-4:j-4])
		if(err== 1):
			i+=4
			j+=4
		typeA,err = dnsType(paquet[i-4:i])
		print(typeA)

		if(paquet[i:j]=="0001"):
			classe = "Type : Internet"
			classe = classe+" ("+paquet[i:j]+")"
		else:
			classe = "Type : Error: no query class recognised"

		ttl = paquet[j:j+8]
		j+=8
		rdata_length = paquet[j:j+4]
		print(ttl,rdata_length)

		print(tab_tri)
		if("(A)" not in typeA):
			data_size = ConvHexDec(rdata_length)
			data=paquet[j+4:data_size]
			ascii_data = data
		else:	
			for(k,l)in tab_tri:
				print(j,k)
				if(j==k):
					data_size = l-ind+2
					data = paquet[j+4:data_size]
		
		print(data,ascii_data)
		ansTab.append(dnsAnswers(name,typeA,classe,ttl,rdata_length,data,ascii_name,ascii_data))
		cpt += 1
		i=j
		j=i+4

	return ansTab,j
"""
