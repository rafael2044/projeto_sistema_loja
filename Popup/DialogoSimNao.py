from customtkinter import CTkToplevel, CTkLabel, CTkButton, CTkFrame, CTkFont

class DialogoSimNao(CTkToplevel):
    def __init__(self, titulo, mensagem):
        CTkToplevel.__init__(self)
        self.title(titulo)
        self.center_window()
        self.resizable(False,False)
        self.mensagem = mensagem
        self.opcao = 0
        
        self.carregar_widgets()
        self.wait_visibility()
        self.grab_set()
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        self.wait_window(self)
        
    def center_window(self):
        self.HEIGHT = 100
        self.WEIDTH = 450
        
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        X = (W_WEIDTH - self.WEIDTH)//2
        Y = (W_HEIGHT - self.HEIGHT)//2
        
        self.geometry(f'{self.WEIDTH}x{self.HEIGHT}+{X}+{Y}+') 
        
    def carregar_widgets(self):
        self.font_label = CTkFont('Segoe UI', size=15, weight='bold')
        CTkLabel(self, text=self.mensagem, font=self.font_label, wraplength=self.WEIDTH).pack(padx=10, pady=5, anchor='center')
        frame = CTkFrame(self, fg_color='transparent')
        frame.pack(padx=0, pady=10)
        CTkButton(frame, text='Sim', command=self.opcao_sim, width=100, font=self.font_label).pack(padx=10, anchor='center', side='left')
        CTkButton(frame, text='Não', command=self.opcao_nao, width=100, font=self.font_label).pack(padx=10, anchor='center')
        
    def opcao_sim(self):
        self.opcao = 1
        self.close()
    def opcao_nao(self):
        self.opcao = 0
        self.close()

    def close(self, event=None):
        self.destroy()
