try:
    from datetime import datetime
    from tkinter import Label,Button,Text,Scrollbar,Entry,Tk,Toplevel,END,N,S,E,W
    from tkinter import ttk,messagebox
    import socket,threading,ipaddress,re,pickle,string
    import caesar,vigenere,onetimepad,playfair,hill,des,des3,aes
except:
    print("Por favor instale todas as dependências antes de usar o programa.")
    exit(0)

class Application():
    '''Classe principal'''
    def __init__(self, root):
        '''Construtor da classe, recebe a janela como parâmetro'''
        self.root = root
        self.initComponents()
        threading._start_new_thread(self.waitForMessage,())

    def start(self):
        '''Inicia a aplicação'''
        self.root.mainloop()
        
    def initComponents(self):
        '''Inicizalização dos componentes principais da janela'''
        self.root.title("CriptoMaster 3000")
        
        for pos in range(0,7,2):
            self.root.grid_columnconfigure(pos,minsize=10)
        
        Label(self.root,text="CriptoMaster 3000",font=('Times',50),borderwidth=3).grid(row=0,column=1,columnspan=5,sticky=W+E)
        
        Label(self.root,text="Instruções:\n"
            +"1. Escreva a sua mensagem no campo de texto abaixo\n"
            +"2. Escolha a opção de cifra desejada\n"
            +"3. Escolha o modo de encriptação (somente DES, DES3 e AES)\n"
            +"4. Insira a chave de encriptação (regras no botão abaixo da chave)\n"
            +"5. Pressione \'Cifrar\' ou \'Decifrar\'\n"
            +"6. Insira o endereço IP do destinatário ao lado do botão 'Enviar'\n"
            +"6.1. Deixe este campo em branco para enviar em modo broadcast\n"
            +"7. Pressione \'Enviar\' para enviar a mensagem\n",font=('Times',16),borderwidth=3).grid(row=1,column=1,columnspan=5)
        
        self.algorithms = {0:"Caesar", 1:"Vigenère", 2:"One-time pad", 3:"Playflair", 4:"Hill", 5:"DES", 6:"DES3", 7:"AES"}
        self.txtAlgorithms = []
        for k in self.algorithms:
            self.txtAlgorithms.append(self.algorithms[k])

        self.modes = {'ECB - Eletronic Codebook':1, 'CBC - Cipher Block Chaining':2 ,'CFB - Cipher Feedback':3, 'OFB - Output Feedback':5, 'CTR - Counter':6}
        self.txtModes = []        
        for k in self.modes:
            self.txtModes.append(k)

        self.methods = [{0:caesar.encrypt, 1:vigenere.encrypt, 2:onetimepad.encrypt, 3:playfair.encrypt, 4:hill.encrypt, 5:des.encrypt, 6:des3.encrypt, 7:aes.encrypt},
                        {0:caesar.decrypt, 1:vigenere.decrypt, 2:onetimepad.decrypt, 3:playfair.decrypt, 4:hill.decrypt, 5:des.decrypt, 6:des3.decrypt, 7:aes.decrypt}]

        Label(self.root,text="Mensagem a ser enviada (somente uma linha): ").grid(row=3,column=1,columnspan=3,sticky="W")

        self.txtMessage = Text(self.root,borderwidth=3,height=3)
        self.txtMessage.grid(row=4,column=1,columnspan=5)

        self.root.grid_rowconfigure(5,minsize=10)   

        Label(self.root,text="Console: ").grid(row=6,column=1,sticky='W')

        self.txtConsole = Text(self.root,height=5,state='disabled')
        self.txtConsole.grid(row=7,column=1,columnspan=5)
        self.txtConsoleScroll = Scrollbar(self.root, orient="vertical", command=self.txtConsole.yview)
        self.txtConsoleScroll.grid(row=7,column=6,sticky='nsew')
        self.txtConsole.configure(yscrollcommand=self.txtConsoleScroll.set)
        
        self.root.grid_rowconfigure(8,minsize=10)   

        Label(self.root,text="Cifra",font=('Times',12)).grid(row=9,column=1)

        self.cbCifra = ttk.Combobox(self.root,values=self.txtAlgorithms,state="readonly")
        self.cbCifra.grid(row=10,column=1)
        self.cbCifra.current(0)

        Label(self.root,text="Modo de Operação",font=('Times',12)).grid(row=9,column=3)

        self.cbMode = ttk.Combobox(self.root,values=self.txtModes,state="readonly")
        self.cbMode.grid(row=10,column=3)
        self.cbMode.current(0)

        Label(self.root,text="Chave",font=('Times',12)).grid(row=9,column=5)

        self.entryKey = Entry(self.root)
        self.entryKey.grid(row=10,column=5)

        self.root.grid_rowconfigure(11,minsize=20)

        self.btnCifra = Button(self.root,text="Cifrar",command= lambda : self.cipher(0))
        self.btnCifra.grid(row=12,column=1,padx=20,sticky='W')

        self.btnDecifra = Button(self.root,text="Decifrar",command= lambda : self.cipher(1))
        self.btnDecifra.grid(row=12,column=1,padx=20,sticky='E')

        self.entryIP = Entry(self.root, width=14)
        self.entryIP.grid(row=12,column=3, padx=5, sticky='W')

        self.btnEnvia = Button(self.root,text="Enviar",command=self.findServer)
        self.btnEnvia.grid(row=12,column=3, padx=5, sticky='E')

        self.btnInfoKeys = Button(self.root, text="Regras da Chave",command=self.showKeyTips)
        self.btnInfoKeys.grid(row=12,column=5)

        self.root.grid_rowconfigure(14,minsize=20)

    def waitForMessage(self):
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv.bind(('0.0.0.0', 8080))
        serv.listen(5)
        while True:
            conn, addr = serv.accept()
            while True:
                data_arr = conn.recv(4096)
                if not data_arr: break
                # Single-Machine mode
                elif addr[0] == self.getOwnIP(): break
                data = pickle.loads(data_arr)
                msg = data[0].decode()
                cipher = int(data[1])
                mode = int(data[2])
                key = data[3].decode()
                self.txtMessage.delete('0.0',END)
                self.txtMessage.insert(END,msg)
                self.writeLog(msg + " recebido de " + addr[0])
                self.cbCifra.current(cipher)
                self.cbMode.current(mode)
                self.entryKey.delete(0,END)
                self.entryKey.insert(END,key)
            conn.close()
        pass

    def findServer(self):
        try:
            ip = self.entryIP.get()
            if not ip:
                #broadcast mode
                splittedIP = self.getOwnIP().split('.')
                for addr in range(0,256):
                    serverIP = splittedIP[0] + '.' + splittedIP[1] + '.' + splittedIP[2] + '.' + str(addr)
                    threading._start_new_thread(self.sendMessage,(serverIP,))
            else:
                #single message mode
                socket.inet_aton(ip)
                threading._start_new_thread(self.sendMessage,(ip,))
        except:
            messagebox.showerror("Erro no endereço IP","Endereço inválido!\n\nPor favor, verifique se o endereço está correto.")


        
    def getOwnIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]

    def sendMessage(self,ip):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((ip, 8080))
            data = [self.txtMessage.get('0.0',END).splitlines()[0].encode(), self.cbCifra.current(), self.cbMode.current(), self.entryKey.get().encode()]
            data_string = pickle.dumps(data)
            client.send(data_string)
        except:
            pass
        finally:
            client.close()

    def cipher(self,encryptOrDecrypt):
        if ((re.search("^[A-Za-z ]*$",self.txtMessage.get(0.0,END).splitlines()[0]) and encryptOrDecrypt == 0) or encryptOrDecrypt == 1):
            if(self.validateKey()):
                msg = self.txtMessage.get('0.0',END).splitlines()[0]
                cipher = self.methods[encryptOrDecrypt].get(self.cbCifra.current()) 
                cipherText = cipher(msg,self.entryKey.get(),self.modes.get(self.cbMode.get()))
                self.txtMessage.delete('0.0',END)
                self.txtMessage.insert(END,cipherText)
                msg += ' foi '  + ('encriptado' if encryptOrDecrypt == 0 else 'decriptado') + ' para ' + cipherText + ((' no modo ' + (self.cbMode.get()[:3])) if self.cbCifra.current() > 4 else '')
                self.writeLog(msg)
            else:
                messagebox.showerror("Erro na chave","Chave inválida!\n\nPor favor, verifique as regras.")
        else:
            messagebox.showerror("Erro na mensagem","Mensagem inválida!\n\nPor favor, verifique que contém somente letras e espaços.")
    def validateKey(self):
        key = self.entryKey.get()
        if (self.cbCifra.current() == 0):
            try:
                key = int(key)
                return key in range(0,26)
            except:
                return False
        elif (self.cbCifra.current() == 1):
            return re.search("^[A-Za-z0-9]*$",key)
        elif (self.cbCifra.current() == 2):
            return self.special_match(key)
        elif (self.cbCifra.current() == 3):
            return key.isalpha()
        elif (self.cbCifra.current() == 4):
            try:
                key = int(key)
                return True
            except:
                return False
        elif (self.cbCifra.current() == 5):
            return re.search("^[A-Za-z0-9]*$",key) and (len(key) == 8)
        elif (self.cbCifra.current() == 6):
            return re.search("^[A-Za-z0-9]*$",key) and (len(key) == 16 or len(key) == 24)
        elif (self.cbCifra.current() == 7):
            return re.search("^[A-Za-z0-9]*$",key) and (len(key) == 16 or len(key) == 24 or len(key) == 32)

    def special_match(self,str, search=re.compile(r'[^0-1.]').search):
        return not bool(search(str))

    def writeLog(self,message):
        message += " às " + (str(datetime.now().time())[:8]) + "\n"
        self.txtConsole.configure(state='normal')
        self.txtConsole.insert(END,message)
        self.txtConsole.see("end")
        self.txtConsole.configure(state='disabled')

    def showKeyTips(self):
        win = Toplevel()
        win.title('Regras da Chave')
        win.geometry("600x550")
        info = str("\nREGRAS PARA A CHAVE DE ENCRIPTAÇÃO/DECRIPTAÇÃO\n\n\n" 
            +"1. Para Ceaser é a quantidade de Shift (inteiro natural < 26).\n\n"
            +"2. Para Vigenère são letras e números (L&N).\n\n"
            +"3. Para One-time Pad são 0s e 1s.\n\n"
            +"4. Para Playfair são somente letras.\n\n"
            +"5. Para Hill, será um valor inteiro N\n"
            +"    tal que x = 3^N formará a matriz: \n"
            +"        X  0  0\n"
            +"        0  X  0\n"
            +"        0  0  X\n"
            +"6. Para DES a chave deve ter exatos 8 caracteres (L&N).\n\n"
            +"7. Para DES a chave deve ter exatos 16 ou 24 caracteres (L&N).\n\n"
            +"8. Para AES a chave deve ter exatos 16, 24 ou 32 caracteres (L&N).\n\n")
        Label(win, text=info,font=('Times',16), justify='left', anchor=W).pack()

#inicialização do programa
if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.start()