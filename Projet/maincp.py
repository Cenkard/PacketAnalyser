"""
Fichier contenant la classe qui instancie la fenetre graphique du programme
Utilisation de la librairie Tkinter de Python pour l'interface
"""
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from fileTools import *

TK_SILENCE_DEPRECATION=1

class App:
    def __init__(self):     #initialisation de la fenetre graphique
        self.win = Tk()
        self.win.geometry("1080x720")
        s = ttk.Style()
        s.theme_use('clam')

        self.indic = Label(self.win, text="Choisissez le fichier a analyser", font=("Courrier",20))
        self.indic.pack()

        self.button = Button(self.win, text='Open', command=self.UploadAction)
        self.button.pack()

        self.listTrame = []
        self.analyse_tree = ttk.Treeview(self.win)

        self.activ=0
        
        self.win.mainloop()
        
    def onClick(self, event):
        self.hide_analyse()
        item = self.tree.identify('item',event.x,event.y)
        values = self.tree.item(item, "values")
        i=0
        while(i<len(self.listTrame)):
            trame=self.listTrame[i]
            if(values[0]==str(trame.id)):
                self.show_analyse(trame)
                break
            i+=1

    def hide_analyse(self):
        if(self.activ==1):
            self.analyse_tree.delete()
            self.analyse_tree.destroy()
            self.activ=0

    def show_analyse(self,trame):
        if(self.activ==0):
            self.analyse_tree = ttk.Treeview(self.win)
            self.analyse(trame)
            self.analyse_tree.pack(expand=YES,fill=BOTH,anchor='w')
            self.activ=1

    def UploadAction(self, event=None):
        filename = filedialog.askopenfilename()
        print("\n\n\n")
        print('Selected: '+filename)
        if(filename[-3:] != "txt"):
            self.wrongForm = Label(self.win, text="Le fichier doit etre au format .txt", font=("Courrier",20))
            self.wrongForm.pack()
        else:
            print("\n")
            self.listTrame, self.tab_erreur = ecrireTrameDetail(filename)
            print("\n\n")
            for el in self.tab_erreur:
                for el2 in el:
                    print(el2)
            
            label_trames = Label(self.win, text="Liste des trames", font=("Courrier", 20),anchor="nw")
            label_trames.pack(anchor='w')
            self.showList()

    def GestionProtocol(self, trame):
        #print(trame.data.type)
        if (trame.data.type!="Donnee non identifiee"):
            if (trame.data.data.type!="Donnee non identifiee"):
                if (trame.data.data.data.type!="Donnee non identifiee"):
                    return trame.data.data.data.type
                else:
                    return trame.data.data.type
            else:
                return trame.data.type
        return trame.type


    def showList(self):
        self.tree = ttk.Treeview(self.win, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings')
        self.tree.pack(expand=YES, fill=BOTH)
        self.tree.column("# 1", anchor=CENTER,width="50",stretch=NO)
        self.tree.heading("# 1", text="ID")
        self.tree.column("# 2", anchor=CENTER,width="100",stretch=YES)
        self.tree.heading("# 2", text="Source")
        self.tree.column("# 3", anchor=CENTER,width="100",stretch=YES)
        self.tree.heading("# 3", text="Destination")
        self.tree.column("# 4", anchor=CENTER,width="50",stretch=YES)
        self.tree.heading("# 4", text="Protocol")
        self.tree.column("# 5", anchor=CENTER,width="50",stretch=YES)
        self.tree.heading("# 5", text="Length")

        for trame in self.listTrame:
            self.tree.insert('', 'end', text=str(trame.id), values=(trame.id, trame.data.sourceIP, trame.data.destinationIP, self.GestionProtocol(trame), trame.length))
        self.tree.bind("<Button-1>",self.onClick)

    def analyse(self,trame):
        if(trame.typ=="0800"):
            dataIP = trame.data
            if(dataIP.protocol=="11"):
                dataUDP = dataIP.data
                if(dataUDP.data.type == "DNS"):
                    dataDNS = dataUDP.data
                    #-------    DNS       --------
                    if(ConvHexDec(dataDNS.answerRRs)==0):
                        self.analyse_tree.insert('','0','item5',text="Domain Name System "+dataDNS.query[0].dnsType+" Src: "+str(ConvHexDec(dataUDP.sourcePortNum))+" , Dst: "+str(ConvHexDec(dataUDP.destPortNum)))
                    else:
                        self.analyse_tree.insert('','0','item5',text="Domain Name System "+dataDNS.answers[0].dnsType+" Src: "+str(ConvHexDec(dataUDP.sourcePortNum))+" , Dst: "+str(ConvHexDec(dataUDP.destPortNum)))
                    
                    self.analyse_tree.insert('item5','end','trandID',text="Transaction ID : 0x"+dataDNS.transID)
                    self.analyse_tree.insert('item5','end','dnsFlags',text="Flags : 0x"+str(ConvHexDec(dataDNS.flags)))
                    fragFlags = ConvHexBin(dataDNS.flags)
                    self.analyse_tree.insert('dnsFlags','end','fq',text=str(fragFlags[0])+"... .... .... .... = Message is ")
                    self.analyse_tree.insert('dnsFlags','end','fopc',text='.'+str(fragFlags[1:4])+' '+str(fragFlags[4])+'... .... .... = opcode')
                    self.analyse_tree.insert('dnsFlags','end','fauth',text='.... .'+str(fragFlags[5])+".. .... .... = Authoritative")
                    self.analyse_tree.insert('dnsFlags','end','ftrunc',text='.... ..'+str(fragFlags[6])+". .... .... = Truncated")
                    self.analyse_tree.insert('dnsFlags','end','frecd',text='.... ...'+str(fragFlags[7])+" .... .... = Recursion desired")
                    self.analyse_tree.insert('dnsFlags','end','freca',text='.... .... '+str(fragFlags[8])+"... .... = Recursion available")
                    self.analyse_tree.insert('dnsFlags','end','fz',text='.... .... .'+str(fragFlags[9])+".. .... = Z")
                    self.analyse_tree.insert('dnsFlags','end','faa',text='.... .... ..'+str(fragFlags[10])+". .... = Answer authenticated")
                    self.analyse_tree.insert('dnsFlags','end','fna',text='.... .... ...'+str(fragFlags[11])+" .... = None-authenticated data")
                    self.analyse_tree.insert('dnsFlags','end','frepc',text='.... .... ....'+str(fragFlags[12:])+" = Reply code")
                    self.analyse_tree.insert('item5','end','questions',text="Questions :  "+str(ConvHexDec(dataDNS.questions))+" 0x"+dataDNS.questions+")")
                    self.analyse_tree.insert('item5','end','answerRRs',text="Answer RRs :  "+str(ConvHexDec(dataDNS.answerRRs))+" 0x"+dataDNS.answerRRs+")")
                    self.analyse_tree.insert('item5','end','authRRs',text="Authority RRs :  "+str(ConvHexDec(dataDNS.authRRs))+" 0x"+dataDNS.authRRs+")")
                    self.analyse_tree.insert('item5','end','addRRs',text="Additional RRs :  "+str(ConvHexDec(dataDNS.addRRs))+" 0x"+dataDNS.addRRs+")")
                    self.analyse_tree.insert('item5','end','Queries',text="Queries")
                    for query in dataDNS.query:
                        i=0
                        self.analyse_tree.insert('Queries','end','nameQ{}'.format(i),text=query.ascii_name+": Type "+query.typeQ+" Classe "+query.classe)
                        self.analyse_tree.insert('nameQ{}'.format(i),'end','nameq{}'.format(i),text="Name :  "+query.ascii_name)
                        self.analyse_tree.insert('nameQ{}'.format(i),'end','typeq{}'.format(i),text="Type :  "+query.typeQ)    
                        self.analyse_tree.insert('nameQ{}'.format(i),'end','classeq{}'.format(i),text=query.classe)
                        i+=1
                    if(ConvHexDec(dataDNS.answerRRs)!=0):
                        self.analyse_tree.insert('item5','end','Answers',text="Answers ")
                        i=0
                        for answer in dataDNS.answers:
                            self.analyse_tree.insert('Answers','end','nameAns{}'.format(i),text=answer.ascii_name+": Type "+answer.typeA+" Classe "+answer.classe)
                            self.analyse_tree.insert('nameAns{}'.format(i),'end','nameans{}'.format(i),text="Name :  "+answer.ascii_name)
                            self.analyse_tree.insert('nameAns{}'.format(i),'end','typeans{}'.format(i),text="Type :  "+answer.typeA)    
                            self.analyse_tree.insert('nameAns{}'.format(i),'end','classeans{}'.format(i),text=answer.classe)
                            self.analyse_tree.insert('nameAns{}'.format(i),'end','ttlans{}'.format(i),text="Time To Live "+str(ConvHexDec(answer.ttl))+" (0x"+answer.ttl+")")
                            self.analyse_tree.insert('nameAns{}'.format(i),'end','rdataans{}'.format(i),text="Data length : "+str(ConvHexDec(answer.rdata_length))+" (0x"+answer.rdata_length+")")
                            self.analyse_tree.insert('nameAns{}'.format(i),'end','dataans{}'.format(i),text="Data : "+answer.data)
                            self.analyse_tree.insert('nameAns{}'.format(i),'end','ascii_dataans{}'.format(i),text="(Ascii) : "+answer.ascii_data)
                            i+=1
                    if(ConvHexDec(dataDNS.authRRs)!=0):
                        self.analyse_tree.insert('item5','end','Authorities',text="Authorities ")
                        i=0
                        for authority in dataDNS.authority:
                            self.analyse_tree.insert('Authorities','end','nameAuth{}'.format(i),text=authority.ascii_name+": Type "+authority.typeA+" Classe "+authority.classe)
                            self.analyse_tree.insert('nameAuth{}'.format(i),'end','nameauth{}'.format(i),text="Name :  "+authority.ascii_name)
                            self.analyse_tree.insert('nameAuth{}'.format(i),'end','typeauth{}'.format(i),text="Type :  "+authority.typeA)    
                            self.analyse_tree.insert('nameAuth{}'.format(i),'end','classeauth{}'.format(i),text=authority.classe)
                            self.analyse_tree.insert('nameAuth{}'.format(i),'end','ttlauth{}'.format(i),text="Time To Live "+str(ConvHexDec(authority.ttl))+" (0x"+authority.ttl+")")
                            self.analyse_tree.insert('nameAuth{}'.format(i),'end','rdataauth{}'.format(i),text="Data length : "+str(ConvHexDec(authority.rdata_length))+" (0x"+authority.rdata_length+")")
                            self.analyse_tree.insert('nameAuth{}'.format(i),'end','dataauth{}'.format(i),text="Data : "+authority.ascii_data)
                            self.analyse_tree.insert('nameAuth{}'.format(i),'end','ascii_dataauth{}'.format(i),text="(Ascii) : "+authority.ascii_data)
                            i+=1
                    if(ConvHexDec(dataDNS.addRRs)!=0):
                        self.analyse_tree.insert('item5','end','Additions',text="Additions ")
                        i=0
                        for addition in dataDNS.addition:
                            self.analyse_tree.insert('Additions','end','nameAdd{}'.format(i),text=addition.ascii_name+": Type "+addition.typeA+" Classe "+addition.classe)
                            self.analyse_tree.insert('nameAdd{}'.format(i),'end','nameadd{}'.format(i),text="Name :  "+addition.ascii_name)
                            self.analyse_tree.insert('nameAdd{}'.format(i),'end','typeadd{}'.format(i),text="Type :  "+addition.typeA)    
                            self.analyse_tree.insert('nameAdd{}'.format(i),'end','classeadd{}'.format(i),text=addition.classe)
                            self.analyse_tree.insert('nameAdd{}'.format(i),'end','ttladd{}'.format(i),text="Time To Live "+str(ConvHexDec(addition.ttl))+" (0x"+addition.ttl+")")
                            self.analyse_tree.insert('nameAdd{}'.format(i),'end','rdataadd{}'.format(i),text="Data length : "+str(ConvHexDec(addition.rdata_length))+" (0x"+addition.rdata_length+")")
                            self.analyse_tree.insert('nameAdd{}'.format(i),'end','dataadd{}'.format(i),text="Data : "+addition.ascii_data)
                            self.analyse_tree.insert('nameAdd{}'.format(i),'end','ascii_dataadd{}'.format(i),text="(Ascii) : "+addition.ascii_data)
                            i+=1
                
                elif(dataUDP.data.type == "DHCP"):
                    #-------    DHCP       --------
                    dataDHCP = dataUDP.data
                    self.analyse_tree.insert('','0','item5',text="Dynamic Host Control Protocol")
                    self.analyse_tree.insert('item5','end','mt',text=messageDHCP(dataDHCP.bootRq))
                    self.analyse_tree.insert('item5','end','hardType',text="Hardware type: "+hardwareDHCP(dataDHCP.hardType))
                    self.analyse_tree.insert('item5','end','hardAddLength',text="Hardware address length: 0x"+dataDHCP.hardAddLength+" ("+str(ConvHexDec(dataDHCP.hardAddLength))+")")
                    self.analyse_tree.insert('item5','end','hops',text="Hops: 0x"+dataDHCP.hops+" ("+str(ConvHexDec(dataDHCP.hops))+")")
                    self.analyse_tree.insert('item5','end','transID',text="Transaction ID: 0x"+dataDHCP.transID)
                    self.analyse_tree.insert('item5','end','secColl',text="Seconds elapsed: 0x"+dataDHCP.secColl+" ("+str(ConvHexDec(dataDHCP.secColl))+")")
                    self.analyse_tree.insert('item5','end','bootpFlags',text="Bootp flags: "+BootpFlags(dataDHCP.bootpFlags))
                    ipAddrH, ipAddr = LecteurIpAdresse(dataDHCP.clientIP, 0)
                    self.analyse_tree.insert('item5','end','clientIP',text="Client IP address: 0x"+ipAddrH+" ("+ipAddr+")")
                    ipAddrH, ipAddr = LecteurIpAdresse(dataDHCP.yourIP, 0)
                    self.analyse_tree.insert('item5','end','yourIP',text="Your (client) IP address: 0x"+ipAddrH+" ("+ipAddr+")")
                    ipAddrH, ipAddr = LecteurIpAdresse(dataDHCP.serverIP, 0)
                    self.analyse_tree.insert('item5','end','serverIP',text="Next Server IP address: 0x"+ipAddrH+" ("+ipAddr+")")
                    ipAddrH, ipAddr = LecteurIpAdresse(dataDHCP.gatewayIP, 0)
                    self.analyse_tree.insert('item5','end','gatewayIP',text="Relay agent IP address: 0x"+ipAddrH+" ("+ipAddr+")")
                    self.analyse_tree.insert('item5','end','clientMAC',text=ClientMAC(dataDHCP.clientMAC))
                    self.analyse_tree.insert('item5','end','serverName',text=ServerHostName(dataDHCP.serverName))
                    self.analyse_tree.insert('item5','end','bootFileName',text=BootFileName(dataDHCP.bootFileName))
                    self.analyse_tree.insert('item5','end','magicCookie',text="Magic Cookie: "+MagicCookie(dataDHCP.magicCookie))
                    self.analyse_tree.insert('item5','end','options',text=optionDHCP(dataDHCP.options, 1))
                        
                else:
                    self.analyse_tree.insert('','0','item5',text="Data not identified")
                     
                #-------    UDP       --------
                self.analyse_tree.insert('','0','item4',text="User Datagram Protocol, Src: "+str(ConvHexDec(dataUDP.sourcePortNum))+" , Dst: "+str(ConvHexDec(dataUDP.destPortNum)))
                self.analyse_tree.insert('item4','end','sourcePort',text="Source Port : "+str(ConvHexDec(dataUDP.sourcePortNum))+" (0x"+dataUDP.sourcePortNum+')')
                self.analyse_tree.insert('item4','end','destPort',text="Destination Port : "+str(ConvHexDec(dataUDP.destPortNum))+" (0x"+dataUDP.destPortNum+')')
                self.analyse_tree.insert('item4','end','length',text="Length : "+str(ConvHexDec(dataUDP.length))+" (0x"+dataUDP.length+')')
                self.analyse_tree.insert('item4','end','checksum',text="Checksum : (0x"+dataIP.headerChecksum+") [unverified]")       
                
            #-------    IPv4       --------
            self.analyse_tree.insert('','0','item3',text="Internet Protocol Version 4, Src: "+trame.data.sourceIP+" , Dst: "+trame.data.destinationIP)
            self.analyse_tree.insert('item3','end','vers',text="Version : "+str(ConvHexDec(dataIP.version))+" (0x"+dataIP.version+')')
            self.analyse_tree.insert('item3','end','IHL',text="Header length : "+str(ConvHexDec(dataIP.IHL))+" (0x"+dataIP.IHL+')')
            self.analyse_tree.insert('item3','end','totalLengthL',text="Total length : "+str(ConvHexDec(dataIP.totalLength))+" (0x"+dataIP.totalLength+')')
            self.analyse_tree.insert('item3','end','Identification',text="Identification : (0x"+dataIP.identification+') ('+str(ConvHexDec(dataIP.identification))+')')
            self.analyse_tree.insert('item3','end','flags',text="Flags : 0x"+str(ConvHexDec(dataIP.fragOffset)))
            self.analyse_tree.insert('flags','end','res',text=str(dataIP.flags[0])+"... .... .... .... = Reserved bit")
            self.analyse_tree.insert('flags','end','df',text='.'+str(dataIP.flags[1])+".. .... .... .... = Don't fragment")
            self.analyse_tree.insert('flags','end','mf',text='..'+str(dataIP.flags[2])+". .... .... .... = More fragments")
            self.analyse_tree.insert('item3','end','ttl',text="Time To Live : "+str(ConvHexDec(dataIP.TTL))+" (0x"+dataIP.TTL+")")
            
            if(dataIP.data.type=="UDP"):
                self.analyse_tree.insert('item3','end','proto',text="Protocol : UDP (0x"+dataIP.protocol+")")
            elif(dataIP.data.type=="ICMP"):
                self.analyse_tree.insert('item3','end','proto',text="Protocol : ICMP (0x"+dataIP.protocol+")")
            else:
                self.analyse_tree.insert('item3','end','proto',text="Protocol : Non reconnu (0x"+dataIP.protocol+")")
            self.analyse_tree.insert('item3','end','headchecksum',text="Header checksum : (0x"+dataIP.headerChecksum+") [unverified]")       
            self.analyse_tree.insert('item3','end','sourceIP',text="Source : "+dataIP.sourceIP)
            self.analyse_tree.insert('item3','end','destinationIP',text="Destination : "+dataIP.destinationIP)
        
        else:
            self.analyse_tree.insert('item3','end','dataUnknown',text="Data type not identified")
        
        #-------    Ethernet       --------
        self.analyse_tree.insert('','0','item2',text="Ethernet II, Src: "+trame.source+" , Dst: "+trame.destination)
        self.analyse_tree.insert('item2','end','src',text="Source : "+trame.source)
        self.analyse_tree.insert('item2','end','dst',text="Destination : "+trame.destination)
        self.analyse_tree.insert('item2','end','type',text="Type : "+trame.type)

        self.analyse_tree.insert('','0','item1',text="Frame {}".format(trame.id))

def main(args):
    App()

App()
