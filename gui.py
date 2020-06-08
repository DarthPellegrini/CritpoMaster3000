try:
    import logic
    from tkinter import *
    from tkinter import ttk,messagebox
except:
    print("Este programa requer Python 3.x e a biblioteca Python-Tk")
    exit(0)

class Application():
    '''Classe principal'''
    def __init__(self, root):
        '''Construtor da classe, recebe a janela como parâmetro'''
        self.root = root
        self.initComponents()

    def start(self):
        '''Inicia a aplicação'''
        self.root.mainloop()
        
    def initComponents(self):
        '''Inicizalização dos componentes principais da janela'''
        self.root.title("CriptoMaster 3000")
        
        for pos in range(0,7,2):
            self.root.grid_columnconfigure(pos,minsize=10)
        
        Label(self.root,text="CriptoMaster 3000",font=('Times',50),borderwidth=3).grid(row=0,column=1,columnspan=5,sticky=W+E)
        
        Label(self.root,text="Escreva a sua mensagem no campo de texto abaixo, \nescolha a opção de cifra/modo desejado e insira a chave, \npor fim, pressione cifrar ou decifrar.",font=('Times',18),borderwidth=3).grid(row=1,column=1,columnspan=5)
        
        self.algorithms = {0:"Caesar", 1:"Vigenère", 2:"One-time pad", 3:"Playflair", 4:"Hill", 5:"DES", 6:"3DES", 7:"AES"}
        self.txtAlgorithms = []

        for k in self.algorithms:
            self.txtAlgorithms.append(self.algorithms[k])

        self.modes = {1:'ECB - Eletronic Codebook', 2:'CBC - Cipher Block Chaining', 3:'CFB - Cipher Feedback', 4:'OFB - Output Feedback', 5:'CTR - Counter'}
        self.txtModes = []        

        for k in self.modes:
            self.txtModes.append(self.modes[k])

        self.txtField = Text(self.root,borderwidth=3,height=3)
        self.txtField.grid(row=3,column=1,columnspan=5)

        self.root.grid_rowconfigure(4,minsize=10)   

        Label(self.root,text="Cifra",font=('Times',12)).grid(row=5,column=1)

        self.cbCifra = ttk.Combobox(self.root,values=self.txtAlgorithms,state="readonly")
        self.cbCifra.grid(row=6,column=1)
        self.cbCifra.current(0)

        Label(self.root,text="Modo de Operação",font=('Times',12)).grid(row=5,column=3)

        self.cbCifra = ttk.Combobox(self.root,values=self.txtModes,state="readonly")
        self.cbCifra.grid(row=6,column=3)
        self.cbCifra.current(0)

        Label(self.root,text="Chave",font=('Times',12)).grid(row=5,column=5)

        self.entryKey = Entry(self.root)
        self.entryKey.grid(row=6,column=5)

        self.root.grid_rowconfigure(7,minsize=20)

        self.btnCifra = Button(self.root,text="Cifrar")
        self.btnCifra.grid(row=8,column=1)

        self.btnDecifra = Button(self.root,text="Decifrar")
        self.btnDecifra.grid(row=8,column=3)

        self.btnEnvia = Button(self.root,text="Enviar")
        self.btnEnvia.grid(row=8,column=5)

        self.root.grid_rowconfigure(9,minsize=20)


        

#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()