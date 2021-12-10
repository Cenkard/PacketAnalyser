from pa import *
from structure import *
from outils import *
from buildTools import *

def afficherTrameTease(listTrame):
	for trame in listTrame:
		if(trame.data.protocol == "11"):
			print(str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type)+" | "+str(trame.data.data.data.type))
		else:
			print(str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type))

def afficherTrameDetail(listTrame):
	#ClearFicherTrame()
	with open("Trame_File", "w") as f:
		for trame in listTrame:
			f.write("--------------- TRAME "+str(trame.id)+" ----------------\n")
			f.write("----------------------------------------\n")

			f.write("Paquet ethernet de ... bytes\n\n")
			f.write("Ethernet :\n")
			if(str(trame.destination) == "ff:ff:ff:ff:ff:ff"):
				f.write("\tDestination MAC : "+str(trame.destination)+" (broadcast)\n")
			else:
				f.write("\tDestination MAC : "+str(trame.destination)+"\n")

			f.write("\tSource MAC : "+str(trame.source)+"\n")
			f.write("\tType : IPv4 (0x"+(trame.typ)+")\n")

			if(trame.typ=="0800"):
				dataEth = trame.data
				f.write("Internet Protocol Version 4 :\n")	
				f.write("\tVersion : "+str(ConvHexDec(dataEth.version))+" (0x"+ConvHexBin(dataEth.version)+")\n")
				f.write("\tIHL : "+(dataEth.IHL)+" (0x"+ConvHexBin(dataEth.IHL)+")\n")
				f.write("\tTotal Length : "+str(ConvHexDec(dataEth.totalLength))+"	(0x"+dataEth.totalLength+")\n")
				f.write("\tIdentification : 0x"+(dataEth.identification)+ " ("+str(ConvHexDec(dataEth.identification))+")\n")	
				f.write("\tTOS : "+str(ConvHexDec(dataEth.TOS))+"	(0x"+dataEth.TOS+")\n")
				f.write("\tFlags : 0x"+dataEth.flags+""+str(ConvHexDec(dataEth.fragOffset))+"\n")
				if(len(dataEth.flags)!=0):
					f.write("\t	"+str(dataEth.flags[0])+"... .... .... .... : Reserved bite\n")
					f.write("\t	."+str(dataEth.flags[1])+".. .... .... .... : Don't fragment\n")
					f.write("\t	.."+str(dataEth.flags[2])+". .... .... .... : More fragment\n")
					
					f.write("\t	...0 "+dataEth.fragOffset+" = Fragment offset: "+str(ConvHexDec(dataEth.fragOffset))+"\n")
				
				f.write("\tTime to live : "+str(ConvHexDec(dataEth.TTL))+"	(0x"+dataEth.TTL+")\n")
				f.write("\tProtocol : "+dataEth.data.type+" ("+str(ConvHexDec(dataEth.protocol))+")	(Ox"+dataEth.protocol+")\n")
				f.write("\tChecksum : 0x"+dataEth.headerChecksum+" [validation disabled]\n")
				f.write("\tDestination IP : "+str(dataEth.destinationIP)+"\n")
				f.write("\tSource IP : "+str(dataEth.sourceIP)+"\n")
				if (dataEth.options!=None):
					f.write(dataEth.options) #------------------------------

				if(dataEth.data.type == "ICMP"):
					dataIP = trame.data
					f.write("Internet Control Message Protocol :\n")	
					f.write("\tType : "+str(ConvHexDec(dataIP.type))+" ("+ConvHexBin(dataIP.type)+")\n")
					f.write("\tIHL : "+(dataIP.IHL)+" ("+ConvHexBin(dataIP.IHL)+")\n")
					f.write("\tTotal Length : "+str(ConvHexDec(dataIP.totalLength))+"	(0x"+dataIP.totalLength+")\n")
					f.write("\tIdentification : 0x"+(dataIP.identification)+ " ("+str(ConvHexDec(dataIP.identification))+")\n")	
					f.write("\tTOS : "+str(ConvHexDec(dataIP.TOS))+"	(0x"+dataIP.TOS+")\n")
					f.write("\tFlags : 0x"+dataIP.flags+""+str(ConvHexDec(dataIP.fragOffset))+"\n")
					if(len(dataIP.flags)!=0):
						f.write("	"+str(dataIP.flags[0])+"... .... .... .... : Reserved bite\n")
						f.write("	."+str(dataIP.flags[1])+".. .... .... .... : Don't fragment\n")
						f.write("	.."+str(dataIP.flags[2])+". .... .... .... : More fragment\n")
						
						f.write("	...0 "+dataIP.fragOffset+" = Fragment offset: "+str(ConvHexDec(dataIP.fragOffset))+"\n")
					f.write("Time to live : "+str(ConvHexDec(dataIP.TTL))+"	(0x"+dataIP.TTL+")\n")
					f.write("Protocol : "+dataIP.data.type+" ("+str(ConvHexDec(dataIP.protocol))+")	(Ox"+dataIP.protocol+")\n")
					f.write("Checksum : Ox"+dataIP.headerChecksum+" [validation disabled]\n")
					f.write("Destination IP : "+str(dataIP.destinationIP)+"\n")
					f.write("Source IP : "+str(dataIP.sourceIP)+"\n")

				if(dataEth.data.type == "UDP"):
					dataIP = dataEth.data
					f.write("User Datagram Protocol :\n")	
					f.write("\tSource Port  : "+str(ConvHexDec(dataIP.sourcePortNum))+" (0x"+dataIP.sourcePortNum+")\n")
					f.write("\tDestination Port : "+str(ConvHexDec(dataIP.destPortNum))+" (0x"+dataIP.destPortNum+")\n")
					f.write("\tLength : "+str(ConvHexDec(dataIP.length))+"	(0x"+dataIP.length+")\n")
					f.write("\tChecksum : 0x"+dataIP.checksum+" [validation disabled]\n")
				
					if(dataIP.data.type == "DNS"):
						dataUDP = dataIP.data
						f.write("Domain Name System : ("+dataUDP.type+")\n")
						f.write("\tTransaction ID : "+str(ConvHexDec(dataUDP.transID))+"	(0x"+dataUDP.transID+")\n")
						f.write("\tFlags : "+dataUDP.flags+"\n")
						f.write("\tQuestion : "+str(ConvHexDec(dataUDP.questions))+"	(0x"+dataUDP.questions+")\n")
						f.write("\tAnswer RRs : "+str(ConvHexDec(dataUDP.answerRRs))+"	(0x"+dataUDP.answerRRs+")\n")
						f.write("\tAuthority RRs : "+str(ConvHexDec(dataUDP.authRRs))+"	(0x"+dataUDP.authRRs+")\n")
						f.write("\tAdditional RRs : "+str(ConvHexDec(dataUDP.addRRs))+"	(0x"+dataUDP.addRRs+")\n")
						if(ConvHexDec(dataUDP.questions) != 0):
							f.write("\tQueries : ("+str(len(dataUDP.query))+")\n")
							for query in dataUDP.query:
								f.write("\t\tName : "+query.name+"\n")
								f.write("\t\t(ASCII): "+query.ascii_name+"\n")
								f.write("\t\tType : "+query.typeQ+"\n")
								f.write("\t\t"+query.classe+"\n")
						if(ConvHexDec(dataUDP.answerRRs) != 0):
							f.write("\tAnswers : ("+str(len(dataUDP.answers))+")\n")
							for answer in dataUDP.answers:
								f.write("\t\tName : "+answer.name+"\n")
								f.write("\t\t(ASCII): "+answer.ascii_name+"\n")
								f.write("\t\t"+answer.typeA+"\n")
								f.write("\t\tClasse : "+answer.classe+"\n")
								f.write("\t\tTTL : "+answer.ttl+"\n")
								f.write("\t\tRdata_length : "+str(ConvHexDec(answer.rdata_length))+" (0x"+answer.rdata_length+")\n")
								f.write("\t\tDonnees: "+answer.data+"\n")
								f.write("\t\t(ASCII): "+answer.ascii_data+"\n")
								f.write("\t\t\t----\n")
						if(ConvHexDec(dataUDP.authRRs) != 0):
							f.write("\tAuthorities : ("+str(len(dataUDP.authority))+")\n")
							for authority in dataUDP.authority:
								f.write("\t\tName : "+authority.name+"\n")
								f.write("\t\t(ASCII): "+authority.ascii_name+"\n")
								f.write("\t\t"+authority.typeA+"\n")
								f.write("\t\tClasse : "+authority.classe+"\n")
								f.write("\t\tTTL : "+authority.ttl+"\n")
								f.write("\t\tRdata_length : "+str(ConvHexDec(authority.rdata_length))+" (0x"+authority.rdata_length+")\n")
								f.write("\t\tDonnees : "+authority.data+"\n")
								f.write("\t\t(ASCII): "+authority.ascii_data+"\n")
								f.write("\t\t----\n")
						if(ConvHexDec(dataUDP.addRRs) != 0):
							f.write("\tAdditions : ("+str(len(dataUDP.addition))+")\n")
							for addition in dataUDP.addition:
								f.write("\t\tName : "+addition.name+"\n")
								f.write("\t\t(ASCII): "+addition.ascii_name+"\n")
								#f.write("\t\t(ASCII): "+bytearray.fromhex(addition.name[:len(addition.name)-2]).decode()+"\n")
								f.write("\t\t"+addition.typeA+"\n")
								f.write("\t\tClasse : "+addition.classe+"\n")
								f.write("\t\tTTL : "+addition.ttl+"\n")
								f.write("\t\tRdata_length : "+str(ConvHexDec(addition.rdata_length))+" (0x"+addition.rdata_length+")\n")
								f.write("\t\tDonnees : "+addition.data+"\n")
								f.write("\t\t(ASCII): "+addition.ascii_data+"\n")
								f.write("\t\t----\n")
					
					elif(dataIP.data.type == "DHCP"):
						dataUDP = dataIP.data
						f.write("Dynamic Host Configuration Protocol\n")
						f.write("\t"+messageDHCP(dataIP.data.bootRq)+"\n")
						f.write("\tHardware type: "+hardwareDHCP(dataIP.data.hardType)+"\n")
						f.write("\tHardware address length: 0x"+dataIP.data.hardAddLength+" ("+str(ConvHexDec(dataIP.data.hardAddLength))+")"+"\n")
						f.write("\tHops: 0x"+dataIP.data.hops+" ("+str(ConvHexDec(dataIP.data.hops))+")"+"\n")
						f.write("\tTransaction ID: 0x"+dataIP.data.transID+"\n")
						f.write("\tSeconds elapsed: 0x"+dataIP.data.secColl+" ("+str(ConvHexDec(dataIP.data.secColl))+")"+"\n")
						f.write("\tBootp flags: "+BootpFlags(dataIP.data.bootpFlags)+"\n") #retourne texte selon broadcast ou unicast
						ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.clientIP, 0)
						f.write("\tClient IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n")
						ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.yourIP, 0)
						f.write("\tYour (client) IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n")
						ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.serverIP, 0)
						f.write("\tNext Server IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n")
						ipAddrH, ipAddr = LecteurIpAdresse(dataIP.data.gatewayIP, 0)
						f.write("\tRelay agent IP address: 0x"+ipAddrH+" ("+ipAddr+")"+"\n")
						f.write(ClientMAC(dataIP.data.clientMAC)+"\n") #retourne MAC selon si ca existe ou pas
						f.write(ServerHostName(dataIP.data.serverName)+"\n")#retourne le nom selon s'il existe ou pas
						f.write(BootFileName(dataIP.data.bootFileName)+"\n") #retourne le nom du bootfile selon s'il est donne ou pas
						f.write("\tMagic Cookie: "+MagicCookie(dataIP.data.magicCookie)+"\n")
						f.write(optionDHCP(dataIP.data.options, 1)+"\n")
					else:
						f.write("\n\tUDP data not identified...\n")
						f.write("\tUDP data known : DNS, DHCP\n")		
				
				else:
					f.write("\n\tError: IP datagrame not identified...\n")
					f.write("\tIP protocol known : ICMP, UDP\n")
			
			else:
				f.write("\nEthernet data not identified...\n")
				f.write("\nEthernet data type known : IPv4\n")

			f.write("\n\n")

	print("Les trames suivantes ont bien ete chargees !\n")
	afficherTrameTease(listTrame)

def loadTrameFile(fichier):
	with open("Trame_File", "r") as f:
		for ligne in f:
			ligne = ligne[:-1]
			print(ligne)

Fichier, tab = TextCleanerTrame("test.txt")
afficherTrameDetail(creerTrame(Fichier,tab))

