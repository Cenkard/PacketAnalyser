from pa import *

"""
Fichier repertoriant les differentes classes utiles pour la conception des trames
"""

class Trame: #Classe Trame contenant les champs d une trame Ethernet, le champs data etant IP
	def __init__(self,id,destination=None,source=None,typ=None,data=None):
		self.id = id
		self.type="Ethernet"
		if(destination!=None):
			self.destination = destination[:2]+":"+destination[2:4]+":"+destination[4:6]+":"+destination[6:8]+":"+destination[8:10]+":"+destination[10:12]
		else:
			self.destination = destination

		if(source!=None):	
			self.source = source[:2]+":"+source[2:4]+":"+source[4:6]+":"+source[6:8]+":"+source[8:10]+":"+source[10:12]
		else:
			self.source = source

		self.typ = typ
		self.data = data

class DataIP: #Classe DataIP contenant les champs d'un paquet IP et le champs data etant le segment UDP
	def __init__(self,version=None,IHL=None,TOS=None,totalLength=None,identification=None,flags=None,fragOffset=None,TTL=None,
				protocol=None,headerChecksum=None,destinationIP=None,sourceIP=None,options=None,data=None):
		self.type="Datagrame IP"
		self.version = version
		self.IHL = IHL
		self.TOS = TOS

		self.totalLength = totalLength

		self.identification = identification
		self.flags = flags
		self.fragOffset = fragOffset[:4]+" "+fragOffset[4:8]+" "+fragOffset[8:]

		self.TTL = TTL
		self.protocol = protocol
		self.headerChecksum = headerChecksum

		if(destinationIP!=None):	
			self.destinationIP = str(ConvHexDec(destinationIP[:2]))+"."+str(ConvHexDec(destinationIP[2:4]))+"."+str(ConvHexDec(destinationIP[4:6]))+"."+str(ConvHexDec(destinationIP[6:8]))
		else:
			self.destinationIP = destinationIP
		
		if(sourceIP!=None):	
			self.sourceIP = str(ConvHexDec(sourceIP[:2]))+"."+str(ConvHexDec(sourceIP[2:4]))+"."+str(ConvHexDec(sourceIP[4:6]))+"."+str(ConvHexDec(sourceIP[6:8]))
		else:
			self.sourceIP = sourceIP

		self.options = options

		self.data = data	

class ICMP:	#Classe ICMP contenant l'entete ICMP
	def __init__(self,checksum=None,identifier=None,sequenceNumber=None,optionalData=None):
		self.type="ICMP"
		self.checksum
		self.identifier
		self.sequenceNumber
		self.optionalData	

class UDP: #Classe UDP contenant les champs d'un segment UDP et le champs data etant ou DHCP ou DNS
	def __init__(self,sourcePortNum=None,destPortNum=None,length=None,checksum=None,data=None):
		self.type = "UDP"
		self.sourcePortNum = sourcePortNum
		self.destPortNum = destPortNum
		self.length = length
		self.checksum = checksum
		self.data = data

class DNS: #Classe DNS contenant l'entete DNS et les diffrents champs data de DNS
	def __init__(self,transID=None,flags=None,questions=None,answerRRs=None,authRRs=None,addRRs=None,query=None,answers=None,authority=None,addition=None):
		self.type="DNS"
		self.transID = transID
		self.flags = flags
		fragFlags = ConvHexBin(flags)

		self.questions = questions
		self.answerRRs = answerRRs
		self.authRRs = authRRs
		self.addRRs = addRRs

		self.query = query
		self.answers = answers
		self.authority = authority
		self.addition = addition

class dnsQueries: #Classe dnsQueries contenant les champs de la section queries
	def __init__(self,name=None,ascii_name="",typeQ=None,classe=None):
		self.dnsType = "(query)"
		self.name = name
		self.ascii_name=ascii_name
		self.name_length = len(name)
		self.typeQ = typeQ
		if(typeQ=="CNAME"):
			self.label_length = name[:2]
			self.label = name[2:len(name)-2]

		self.classe = classe

class dnsAnswers: #Classe dnsAnswers propre au paquet Answer/Authority/Addition qui ont la meme structure donc on les representent tous par la meme classe
	def __init__(self,name,typeA,classe,ttl=None,rdata_length=None,data=None,ascii_name="None",ascii_data="None"):
		self.dnsType = "(response)"
		self.name = name
		self.ascii_name = ascii_name
		self.nameLength = len(name)
		self.typeA = typeA
		self.classe = classe
		self.ttl = ttl
		self.rdata_length = rdata_length
		self.ascii_data=ascii_data
		if(rdata_length!=0):
			if("(A)" in typeA):
				self.data = str(ConvHexDec(data[:2]))+"."+str(ConvHexDec(data[2:4]))+"."+str(ConvHexDec(data[4:6]))+"."+str(ConvHexDec(data[6:8]))
			else:
				self.data = data
		
class DHCP:	#Classe DHCP contenant les champs de DHCP et les options
	def __init__(self,bootRq,hardType,hardAddLength,hops,transID,secColl,bootpFlags,clientIP,yourIP,serverIP,gatewayIP, clientMAC, serverName,bootFileName,magicCookie,options):
		self.type="DHCP"
		self.bootRq = bootRq
		self.hardType = hardType
		self.hardAddLength = hardAddLength
		self.hops = hops
		self.transID = transID
		self.secColl = secColl
		self.bootpFlags = bootpFlags
		self.clientIP = clientIP
		self.yourIP = yourIP
		self.serverIP = serverIP
		self.gatewayIP = gatewayIP
		self.clientMAC = clientMAC
		self.serverName = serverName
		self.bootFileName = bootFileName
		self.magicCookie = magicCookie
		self.options = options

class noneTypeData: #Classe noneTypeData qui sert si un des paquets n'est pas identifie
		def __init__(self,data,type):
			self.type = type
			self.data = data
			self.poids = len(data)/2