# Import the required libraries
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from fileTools import *

class App:
    def __init__(self):
        # Create an instance of tkinter frame
        self.win = Tk()
        # Set the size of the tkinter window
        self.win.geometry("1080x480")
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
        print('Selected: ', filename)
        if(filename[-3:] != "txt"):
            self.wrongForm = Label(self.win, text="Le fichier doit etre au format .txt", font=("Courrier",20))
            self.wrongForm.pack()
        else:
            Fichier, tab = TextCleanerTrame(filename)
            self.listTrame = creerTrame(Fichier,tab)
            ecrireTrameDetail(self.listTrame)
            
            label_trames = Label(self.win, text="Liste des trames", font=("Courrier", 20),anchor="nw")
            label_trames.pack(anchor='w')
            self.showList()

    def showList(self):
         # Add a Treeview widget
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
        self.tree.column("# 6", anchor=CENTER,width="50",stretch=YES)
        self.tree.heading("# 6", text="Info")

        for trame in self.listTrame:
            self.tree.insert('', 'end', text=str(trame.id), values=(trame.id, trame.data.sourceIP, trame.data.destinationIP, trame.data.data.type, "trame.length", "type udp"))
        self.tree.bind("<Button-1>",self.onClick)

    def analyse(self,trame):
        dataIP = trame.data
        dataUDP = dataIP.data
        if(dataUDP.type == "DNS"):
            dataDNS = dataUDP.data
            #-------    DNS       --------
            if(str(ConvHexDec(dataUDP.answerRRs))==0):
                self.analyse_tree.insert('','0','item5',text="Domain Name System "+dataDNS.query[0].dnsType+" Src: "+str(ConvHexDec(dataUDP.sourcePortNum))+" , Dst: "+str(ConvHexDec(dataUDP.destPortNum)))
            else:
                self.analyse_tree.insert('','0','item5',text="Domain Name System "+dataDNS.answer[0].dnsType+" Src: "+str(ConvHexDec(dataUDP.sourcePortNum))+" , Dst: "+str(ConvHexDec(dataUDP.destPortNum)))
            
            self.analyse_tree.insert('item5','end','sourcePort',text="Transaction ID : 0x"+dataDNS.transID)
            self.analyse_tree.insert('item3','end','flags',text="Flags : 0x"+str(ConvHexDec(dataDNS.flags)))
            self.analyse_tree.insert('flags','end','res',text=str(fragFlags[0])+"... .... .... .... = Message is ")
            self.analyse_tree.insert('flags','end','df',text='.'+str(fragFlags[0])+".. .... .... .... = Don't fragment")
            self.analyse_tree.insert('flags','end','mf',text='..'+str(fragFlags[0])+". .... .... .... = More fragments")
            self.analyse_tree.insert('flags','end','res',text=str(fragFlags[0])+"... .... .... .... = Reserved bit")
            self.analyse_tree.insert('flags','end','df',text='.'+str(fragFlags[0])+".. .... .... .... = Don't fragment")
            self.analyse_tree.insert('flags','end','mf',text='..'+str(fragFlags[0])+". .... .... .... = More fragments")
        
        else:
            #-------    DHCP       --------
            dataDHCP = dataUDP.data
            self.analyse_tree.insert('','0','item5',text="User Datagram Protocol, Src: "+str(ConvHexDec(dataUDP.sourcePortNum))+" , Dst: "+str(ConvHexDec(dataUDP.destPortNum)))
            self.analyse_tree.insert('item5','end','sourcePort',text="Source Port : "+str(ConvHexDec(dataUDP.sourcePortNum))+" (0x"+dataUDP.sourcePortNum+')')
            self.analyse_tree.insert('item5','end','destPort',text="Destination Port : "+str(ConvHexDec(dataUDP.destPortNum))+" (0x"+dataUDP.destPortNum+')')
            self.analyse_tree.insert('item5','end','IHL',text="Length : "+str(ConvHexDec(dataUDP.length))+" (0x"+dataUDP.length+')')
            self.analyse_tree.insert('item5','end','checksum',text="Checksum : (0x"+dataIP.headerChecksum+") [unverified]")
                  
        #-------    UDP       --------
        self.analyse_tree.insert('','0','item4',text="User Datagram Protocol, Src: "+str(ConvHexDec(dataUDP.sourcePortNum))+" , Dst: "+str(ConvHexDec(dataUDP.destPortNum)))
        self.analyse_tree.insert('item4','end','sourcePort',text="Source Port : "+str(ConvHexDec(dataUDP.sourcePortNum))+" (0x"+dataUDP.sourcePortNum+')')
        self.analyse_tree.insert('item4','end','destPort',text="Destination Port : "+str(ConvHexDec(dataUDP.destPortNum))+" (0x"+dataUDP.destPortNum+')')
        self.analyse_tree.insert('item4','end','IHL',text="Length : "+str(ConvHexDec(dataUDP.length))+" (0x"+dataUDP.length+')')
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
        
        #-------    Ethernet       --------
        self.analyse_tree.insert('','0','item2',text="Ethernet II, Src: "+trame.source+" , Dst: "+trame.destination)
        self.analyse_tree.insert('item2','end','src',text="Source : "+trame.source)
        self.analyse_tree.insert('item2','end','dst',text="Destination : "+trame.destination)
        self.analyse_tree.insert('item2','end','type',text="Type : "+trame.type)

        self.analyse_tree.insert('','0','item1',text="Frame {}".format(trame.id))

def main(args):
    app = App("trame.txt")

App()
