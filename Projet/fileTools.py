from pa import *
from structure import *
from outils import *
from buildTools import *

def afficherTrameTease(listTrame):#entres: list d instances de trames
	#Affiche pour chaque trame une breve description
	for trame in listTrame:
		if(trame.data.protocol == "11"):
			print(str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type)+" | "+str(trame.data.data.data.type))
		else:
			print(str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type))
	print("")

def enregistrerTrameDetail(Fichier): #entre: un fichier contenant des trames
	#Retourne: un triplet, le remier element est L qui est une liste de triplet indiquand l'id, la taille et le contenu de chaque trame. Le 2eme elementt est listTrame qui est une liste des trames en format texte et le 3eme element est tab_erreur qui contien les erreur des trames erronnes

	#Initialisation de base
	fichier, tab = TextCleanerTrame(Fichier)
	listTrame,tab_erreur = creerTrame(fichier, tab)
	print("Les trames suivantes ont bien ete chargees !\n")
	afficherTrameTease(listTrame)
	L= []
	for trame in listTrame: #pour chaque trame 
		#Traite entete ethernet
		res = ""
		res=res+"Ethernet :\n"
		if(str(trame.destination) == "ff:ff:ff:ff:ff:ff"):
			res=res+"\tDestination MAC : "+str(trame.destination)+" (broadcast)\n"
		else:
			res=res+"\tDestination MAC : "+str(trame.destination)+"\n"

		res=res+"\tSource MAC : "+str(trame.source)+"\n"
		res=res+"\tType : IPv4 (0x"+(trame.typ)+")\n"

		if(trame.typ=="0800"):
			#Traite entete IP
			dataEth = trame.data
			res=res+"Internet Protocol Version 4 :\n"
			res=res+"\tVersion : "+str(ConvHexDec(dataEth.version))+" (0x"+ConvHexBin(dataEth.version)+")\n"
			res=res+"\tIHL : "+(dataEth.IHL)+" (0x"+ConvHexBin(dataEth.IHL)+")\n"
			res=res+"\tTotal Length : "+str(ConvHexDec(dataEth.totalLength))+"	(0x"+dataEth.totalLength+")\n"
			res=res+"\tIdentification : 0x"+(dataEth.identification)+ " ("+str(ConvHexDec(dataEth.identification))+")\n"
			res=res+"\tTOS : "+str(ConvHexDec(dataEth.TOS))+"	(0x"+dataEth.TOS+")\n"
			res=res+"\tFlags : 0x"+dataEth.flags+""+str(ConvHexDec(dataEth.fragOffset))+"\n"
			if(len(dataEth.flags)!=0):
				res=res+"\t	"+str(dataEth.flags[0])+"... .... .... .... : Reserved bite\n"
				res=res+"\t	."+str(dataEth.flags[1])+".. .... .... .... : Don't fragment\n"
				res=res+"\t	.."+str(dataEth.flags[2])+". .... .... .... : More fragment\n"
				
				res=res+"\t	...0 "+dataEth.fragOffset+" = Fragment offset: "+str(ConvHexDec(dataEth.fragOffset))+"\n"
			
			res=res+"\tTime to live : "+str(ConvHexDec(dataEth.TTL))+"	(0x"+dataEth.TTL+")\n"
			res=res+"\tProtocol : "+dataEth.data.type+" ("+str(ConvHexDec(dataEth.protocol))+")	(Ox"+dataEth.protocol+")\n"
			res=res+"\tChecksum : 0x"+dataEth.headerChecksum+" [validation disabled]\n"
			res=res+"\tDestination IP : "+str(dataEth.destinationIP)+"\n"
			res=res+"\tSource IP : "+str(dataEth.sourceIP)+"\n"
			if (dataEth.options!=None):
				res=res+dataEth.options #------------------------------

			if(dataEth.data.type == "ICMP"):
				res=res+("Internet Control Message Protocol :\n")	
				res=res+("\tICMP data not known\n")		
		
			elif(dataEth.data.type == "UDP"):
				#Traite couche transport UDP
				dataIP = dataEth.data
				res=res+"User Datagram Protocol :\n"
				res=res+"\tSource Port  : "+str(ConvHexDec(dataIP.sourcePortNum))+" (0x"+dataIP.sourcePortNum+")\n"
				res=res+"\tDestination Port : "+str(ConvHexDec(dataIP.destPortNum))+" (0x"+dataIP.destPortNum+")\n"
				res=res+"\tLength : "+str(ConvHexDec(dataIP.length))+"	(0x"+dataIP.length+")\n"
				res=res+"\tChecksum : 0x"+dataIP.checksum+" [validation disabled]\n"
			
				if(dataIP.data.type == "DNS"):
					#Traite couche data DNS
					dataUDP = dataIP.data
					res=res+"Domain Name System : ("+dataUDP.type+")\n"
					res=res+"\tTransaction ID : "+str(ConvHexDec(dataUDP.transID))+"	(0x"+dataUDP.transID+")\n"
					res=res+"\tFlags : "+dataUDP.flags+"\n"
					res=res+"\tQuestion : "+str(ConvHexDec(dataUDP.questions))+"	(0x"+dataUDP.questions+")\n"
					res=res+"\tAnswer RRs : "+str(ConvHexDec(dataUDP.answerRRs))+"	(0x"+dataUDP.answerRRs+")\n"
					res=res+"\tAuthority RRs : "+str(ConvHexDec(dataUDP.authRRs))+"	(0x"+dataUDP.authRRs+")\n"
					res=res+"\tAdditional RRs : "+str(ConvHexDec(dataUDP.addRRs))+"	(0x"+dataUDP.addRRs+")\n"
					if(ConvHexDec(dataUDP.questions) != 0):
						res=res+"\tQueries : ("+str(len(dataUDP.query))+")\n"
						for query in dataUDP.query:
							res=res+"\t\tName : "+query.name+"\n"
							res=res+"\t\t(ASCII): "+query.ascii_name+"\n"
							res=res+"\t\tType : "+query.typeQ+"\n"
							res=res+"\t\t"+query.classe+"\n"
					if(ConvHexDec(dataUDP.answerRRs) != 0):
						res=res+("\tAnswers : ("+str(len(dataUDP.answers))+")\n")
						for answer in dataUDP.answers:
							res=res+"\t\tName : "+answer.name+"\n"
							res=res+"\t\t(ASCII): "+answer.ascii_name+"\n"
							res=res+"\t\t"+answer.typeA+"\n"
							res=res+"\t\tClasse : "+answer.classe+"\n"
							res=res+"\t\tTTL : "+answer.ttl+"\n"
							res=res+"\t\tRdata_length : "+str(ConvHexDec(answer.rdata_length))+" (0x"+answer.rdata_length+")\n"
							res=res+"\t\tDonnees: "+answer.data+"\n"
							res=res+"\t\t(ASCII): "+answer.ascii_data+"\n"
							res=res+"\t\t\t----\n"
					if(ConvHexDec(dataUDP.authRRs) != 0):
						res=res+"\tAuthorities : ("+str(len(dataUDP.authority))+")\n"
						for authority in dataUDP.authority:
							res=res+"\t\tName : "+authority.name+"\n"
							res=res+"\t\t(ASCII): "+authority.ascii_name+"\n"
							res=res+"\t\t"+authority.typeA+"\n"
							res=res+"\t\tClasse : "+authority.classe+"\n"
							res=res+"\t\tTTL : "+authority.ttl+"\n"
							res=res+"\t\tRdata_length : "+str(ConvHexDec(authority.rdata_length))+" (0x"+authority.rdata_length+")\n"
							res=res+"\t\tDonnees : "+authority.data+"\n"
							res=res+"\t\t(ASCII): "+authority.ascii_data+"\n"
							res=res+"\t\t----\n"
					if(ConvHexDec(dataUDP.addRRs) != 0):
						f.write("\tAdditions : ("+str(len(dataUDP.addition))+")\n")
						for addition in dataUDP.addition:
							res=res+"\t\tName : "+addition.name+"\n"
							res=res+"\t\t(ASCII): "+addition.ascii_name+"\n"
							#f.write("\t\t(ASCII): "+bytearray.fromhex(addition.name[:len(addition.name)-2]).decode()+"\n")
							res=res+"\t\t"+addition.typeA+"\n"
							res=res+"\t\tClasse : "+addition.classe+"\n"
							res=res+"\t\tTTL : "+addition.ttl+"\n"
							res=res+"\t\tRdata_length : "+str(ConvHexDec(addition.rdata_length))+" (0x"+addition.rdata_length+")\n"
							res=res+"\t\tDonnees : "+addition.data+"\n"
							res=res+"\t\t(ASCII): "+addition.ascii_data+"\n"
							res=res+"\t\t----\n"
				
				elif(dataIP.data.type == "DHCP"):
					#Traite couche data DHCP
					dataUDP = dataIP.data
					res=res+"Dynamic Host Configuration Protocol:\n"
					res=res+"\t"+messageDHCP(dataIP.data.bootRq)+"\n"
					res=res+"\tHardware type: "+hardwareDHCP(dataIP.data.hardType)+"\n"
					res=res+"\tHardware address length: 0x"+dataIP.data.hardAddLength+" ("+str(ConvHexDec(dataIP.data.hardAddLength))+")"+"\n"
					res=res+"\tHops: 0x"+dataIP.data.hops+" ("+str(ConvHexDec(dataIP.data.hops))+")"+"\n"
					res=res+"\tTransaction ID: 0x"+dataIP.data.transID+"\n"
					res=res+"\tSeconds elapsed: 0x"+dataIP.data.secColl+" ("+str(ConvHexDec(dataIP.data.secColl))+")"+"\n"
					res=res+"\tBootp flags: "+BootpFlags(dataIP.data.bootpFlags)+"\n" #retourne texte selon broadcast ou unicast
					ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.clientIP, 0)
					res=res+"\tClient IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n"
					ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.yourIP, 0)
					res=res+"\tYour (client) IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n"
					ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.serverIP, 0)
					res=res+"\tNext Server IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n"
					ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.gatewayIP, 0)
					res=res+"\tRelay agent IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n"
					res=res+ClientMAC(dataIP.data.clientMAC)+"\n" #retourne MAC selon si ca existe ou pas
					res=res+ServerHostName(dataIP.data.serverName)+"\n"#retourne le nom selon s'il existe ou pas
					res=res+BootFileName(dataIP.data.bootFileName)+"\n" #retourne le nom du bootfile selon s'il est donne ou pas
					res=res+"\tMagic Cookie: "+MagicCookie(dataIP.data.magicCookie)+"\n"
					res=res+optionDHCP(dataIP.data.options, 1)+"\n"
				else:
					res=res+"\tUDP data not identified...\n"
					res=res+"\tUDP data known : DNS, DHCP\n"
			
			else:
				res=res+"\tError: IP datagrame not identified...\n"
				res=res+"\tIP protocol known : ICMP, UDP\n"
		
		else:
			res=res+"Ethernet data not identified...\n"
			res=res+"Ethernet data type known : IPv4\n"


		L.append((14+ConvHexDec(dataEth.totalLength), str(trame.id), res))
	return L,listTrame,tab_erreur

def ecrireTrameDetail(Fichier): #entre: fichier de trames
	#Retourne: un couple (listTrame, tab_erreur) ou listTrame est une liste des trames en format instance et tab_erreur une liste des erreur par trame 
	#Cette fonction creer aussi un fichier avec les trames lues
	#ClearFicherTrame()
	listTrame=[]
	with open("Trame_File", "w") as f:
		L,listTrame,tab_erreur = enregistrerTrameDetail(Fichier)
		for l, ident, el in L:
			f.write("--------------- TRAME "+ident+" ----------------\n")
			f.write("----------------------------------------\n")
			f.write("Paquet ethernet de {} bytes\n\n".format(l))
			f.write(el)
			f.write("\n\n")
	return listTrame,tab_erreur
def afficherTrameDetail(Fichier): #entre: fichier de trames
	#Retourne: rien
	#Cette fonction affiche sur la console les trames lues
	L,listTrame,tab_erreur = enregistrerTrameDetail(Fichier)
	for l, ident, el in L:
		print("--------------- TRAME "+ident+" ----------------")
		print("----------------------------------------")
		print("Trame ethernet de {} bytes\n".format(l))
		print(el)
		print("\n\n")

ecrireTrameDetail("trame.txt")		
