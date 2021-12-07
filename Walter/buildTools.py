from pa import *
from structure import *
from outils import *

def dnsType(chaine):
	err=0
	if(chaine=="0001"):
		typ = "IPv4 adress (A)"
	if(chaine=="000C" or chaine=="000c"):
		typ = "IPv6 adress (AAAA)"
	elif(chaine=="0005"):
		typ = "CNAME"
	elif(chaine=="0002"):
		typ = "Name of the authoritative server (NS)"
	elif(chaine=="000F" or chaine=="000f"):
		typ = "Name of the mail server (MX)" 
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
	j = 4
	while(cpt < numQ and j<len(data)):
		i = 0
		j = 4
		while(queries[i:j] != "0001" ):
			i += 1
			j += 1
		name = queries[:i-4]
		typeQ,err = dnsType(queries[i-4:i])

		if(queries[i:j]=="0001"):
			classe = "Internet"
		else:
			classe = "Error: no query class recognised"

		classe = classe+" ("+queries[i:j]+")"

		querTab.append(dnsQueries(name,typeQ,classe))
		cpt += 1

	resteQ = queries[j:]

	return querTab,resteQ	#retourne un tableau contenant toutes les queries répertoriees (en fonction du nombre annonce) et le reste de la trame

def creerA(data,numA):		#retourne un tableau contenant toutes les answers/authority/addition (dependant de l'appel) répertoriees (en fonction du nombre annonce) et le reste de la trame
	paquet = data
	ansTab = []
	str=""
	cpt=0
	i = 0
	j = 4
	while(cpt < numA):
		while(paquet[i:j] != "0001" and j<len(paquet)):
			i += 1
			j += 1
		str,err = dnsType(paquet[i-4:j-4])
		if(err== 1):
			i+=4
			j+=4
		name = paquet[:i-4]
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
		print(ConvHexDec(rdata_length))

		data = paquet[j:j+ConvHexDec(rdata_length)*2]
		j+=ConvHexDec(rdata_length)*2
		ansTab.append(dnsAnswers(name,typeA,classe,ttl,rdata_length,data))
		cpt += 1


	resteA = paquet[j:]
	print(resteA)
	return ansTab,resteA

def loadDnsAAA(tab,dataDns):
	for paquet in tab:
		if("CNAME" in paquet.typeA or "NS" in paquet.typeA or "MX" in paquet.typeA):
			if(paquet.nameLength==4):
				pointer = ConvHexDec(paquet.name[1:])*2
				pointer = pointer-24
				print("pointer paquet :"+str(pointer))
				paquet.name = dataDns.query[0].name[pointer:len(dataDns.query[0].name)]
			if(ConvHexDec(paquet.rdata_length)==4):
				pointer = ConvHexDec(paquet.data[1:])*2
				pointer = pointer-24
				print("pointer paquet :"+str(pointer))
				paquet.data = dataDns.query[0].name[pointer:len(dataDns.query[0].name)]
			elif(ConvHexDec(paquet.rdata_length)>4):
				i=0
				j=2
				while(j<=len(paquet.data)):
					if(paquet.data[i:j]=="c0"):
						pointer = ConvHexDec(paquet.data[i+1:j+2])*2
						pointer = pointer-24
						print("pointer paquet :"+str(pointer))
						paquet.data = dataDns.query[0].name[pointer:len(dataDns.query[0].name)]
						i+=2
						j+=2
					i+=2
					j+=2
	return tab

def creerDNS(trame):	#cree le paquet dns
	dataDns = DNS(trame[:4],trame[4:8],trame[8:12],trame[12:16],trame[16:20],trame[20:24])
	queries = trame[24:]
	dataDns.query,resteQ = creerQuery(queries,ConvHexDec(dataDns.questions))
	if(len(resteQ) != 0):
		ansTab,reste = creerA(resteQ,ConvHexDec(dataDns.answerRRs))
		ansTab = loadDnsAAA(ansTab,dataDns)
		dataDns.answers = ansTab
		authTab,reste = creerA(reste,ConvHexDec(dataDns.authRRs))
		authTab = loadDnsAAA(authTab,dataDns)
		dataDns.authority = authTab
		addTab,reste = creerA(reste,ConvHexDec(dataDns.addRRs))
		addTab = loadDnsAAA(addTab,dataDns)
		dataDns.addition = addTab
	return dataDns

def creerDHCP(dhcpData):	#cree le paquet DHCP
	dataDHCP = DHCP(dhcpData[:2],dhcpData[2:4],dhcpData[4:6],dhcpData[6:8],dhcpData[8:16],dhcpData[16:20],dhcpData[20:24],dhcpData[24:32],dhcpData[32:40],dhcpData[40:48],dhcpData[48:60],dhcpData[60:80],dhcpData[80:208],dhcpData[208:464],dhcpData[464:472],dhcpData[472:])
	return dataDHCP

def creerTabTrame(fichier,tab): #recupere les trames valides sous forme de string contenant tous les hexadecimaux a la suite
	i=0
	j=0
	trameValide = []
	tabTrame = []
	while(i<len(tab)):
		if(tab[i]==1):
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
