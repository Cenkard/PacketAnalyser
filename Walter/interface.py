"""
from tkinter import * 
from tkinter import ttk
from buildTools import *
from fileTools import *

Fichier, tab = TextCleanerTrame("trame.txt")
listTrame = creerTrame(Fichier,tab)
afficherTrameDetail(listTrame)

app = Tk()
app.title("Analyseur de trames") 
app.geometry("720x480")
titre = ttk.Label(app, text="Liste des trames trouvees").pack


frame_analyse = Frame(app)
analyses_titre = ttk.Label(frame_analyse, text ="Analyses").pack()
analyses = ttk.Treeview(frame_analyse)
analyses.pack()
frame_analyse.pack()  

analyses.insert('', '1', 'item2', 
                text ='Computer Science')
analyses.insert('', '2', 'item3', 
                text ='GATE papers')
analyses.insert('', 'end', 'item4',
                text ='Programming Languages')
 
analyses.insert('item2', 'end', 'Algorithm', 
                text ='Algorithm')  
analyses.insert('item2', 'end', 'Data structure', 
                text ='Data structure') 
analyses.insert('item3', 'end', '2018 paper', 
                text ='2018 paper')  
analyses.insert('item3', 'end', '2019 paper', 
                text ='2019 paper')
analyses.insert('item4', 'end', 'Python', 
                text ='Python')
analyses.insert('item4', 'end', 'Java', 
                text ='Java')

app.mainloop()

"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from buildTools import *
from fileTools import *

# creer la fenetre
window = Tk()
window.title("Analyseur de trame")
window.geometry("720x480")
window.config(background='#349eeb')

def UploadAction(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    Fichier, tab = TextCleanerTrame(filename)
    listTrame = creerTrame(Fichier,tab)
    afficherTrameDetail(listTrame)

    list_trames = Listbox(window,width=300)
    list_trames.pack(anchor="nw")
    for trame in listTrame:
        if(trame.data.protocol == "11"):
            list_trames.insert(END,str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type)+" | "+str(trame.data.data.data.type))
        else:
            list_trames.insert(END,str(trame.id)+" : "+str(trame.data.destinationIP)+" | "+str(trame.data.sourceIP)+" | "+str(trame.data.data.type))

button = Button(window, text='Open', command=UploadAction)
button.pack()

label_trames = Label(window, text="Liste des trames", font=("Courrier", 30), bg="#349eeb")
label_trames.pack()

# affichage
window.mainloop()
