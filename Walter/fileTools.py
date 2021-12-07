from pa import *
from structure import *
from outils import *
from buildTools import *

def afficherTrameTease(trame):
	if(trame.data.protocol == "11"):
		print(str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type))
	else:
		print(str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type))

def afficherTrameDetail(listTrame):
	#ClearFicherTrame()
	with open("Trame_File", "w") as f:
		for trame in listTrame:
			f.write("#########	TRAME "+str(trame.id)+" #########\n")
			if(str(trame.destination) == "ff:ff:ff:ff:ff:ff"):
				f.write("Destination MAC : "+str(trame.destination)+" (broadcast)\n")
			else:
				f.write("Destination MAC : "+str(trame.destination)+"\n")

			f.write("Source MAC : "+str(trame.source)+"\n")
			f.write("Type : IPv4 (0x"+(trame.typ)+")\n")

			if(trame.typ=="0800"):
				dataEth = trame.data
				f.write("Internet Protocol Version 4 (""):\n")	
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
								#f.write("\t\t(ASCII): "+bytearray.fromhex(query.name[:len(query.name)-2]).decode()+"\n")
								f.write("\t\t"+query.typeQ+"\n")
								f.write("\t\tClasse : "+query.classe+"\n")
						if(ConvHexDec(dataUDP.answerRRs) != 0):
							f.write("\tAnswers : ("+str(len(dataUDP.answers))+")\n")
							for answer in dataUDP.answers:
								f.write("\t\tName : "+answer.name+"\n")
								#f.write("\t\t(ASCII): "+bytearray.fromhex(answer.name[:len(answer.name)-2]).decode()+"\n")
								f.write("\t\t"+answer.typeA+"\n")
								f.write("\t\tClasse : "+answer.classe+"\n")
								f.write("\t\tTTL : "+answer.ttl+"\n")
								f.write("\t\tDonnees : "+answer.data+"\n")
						if(ConvHexDec(dataUDP.authRRs) != 0):
							f.write("\tAuthorities : ("+str(len(dataUDP.authority))+")\n")
							for authority in dataUDP.authority:
								f.write("\t\tName : "+authority.name+"\n")
								#f.write("\t\t(ASCII): "+bytearray.fromhex(authority.name[:len(authority.name)-2]).decode()+"\n")
								f.write("\t\t"+authority.typeA+"\n")
								f.write("\t\tClasse : "+authority.classe+"\n")
								f.write("\t\tTTL : "+authority.ttl+"\n")
								f.write("\t\tDonnees : "+authority.data+"\n")
						if(ConvHexDec(dataUDP.answerRRs) != 0):
							f.write("\tAdditions : ("+str(len(dataUDP.addition))+")\n")
							for addition in dataUDP.addition:
								f.write("\t\tName : "+addition.name+"\n")
								#f.write("\t\t(ASCII): "+bytearray.fromhex(addition.name[:len(addition.name)-2]).decode()+"\n")
								f.write("\t\t"+addition.typeA+"\n")
								f.write("\t\tClasse : "+addition.classe+"\n")
								f.write("\t\tTTL : "+addition.ttl+"\n")
								f.write("\t\tDonnees : "+addition.data+"\n")

					elif(dataIP.data.type == "DHCP"):
						dataUDP = dataIP.data
						f.write("Dinamic Host Configuration Protocol : ("+dataUDP.type+")\n")
						f.write("\tMessage type : "+str(ConvHexDec(dataUDP.bootRq))+"	(0x"+dataUDP.bootRq+")\n")
						f.write("\tChecksum : 0x"+dataIP.checksum+" [validation disabled]\n")
						
					else:
						f.write("\nData not identified...\n")
						f.write(str(dataIP))

				f.write("\n\n")

Fichier, tab = TextCleanerTrame("trame.txt")
listTrame = creerTrame(Fichier,tab)
afficherTrameDetail(listTrame)
