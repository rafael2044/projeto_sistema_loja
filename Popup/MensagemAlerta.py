from customtkinter import CTkToplevel, CTkLabel, CTkButton, CTkFont

class MensagemAlerta(CTkToplevel):
    def __init__(self, titulo, mensagem):
        CTkToplevel.__init__(self)
        self.title(titulo)
        self.center_window()
        self.resizable(False,False)
        self.mensagem = mensagem
        
        self.carregar_widgets()
    
        self.grab_set()
        self.wait_visibility()
        self.bind('<Return>', self.close)
        self.wait_window(self)
    def center_window(self):
        HEIGHT = 75
        WEIDTH = 350
        
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        X = (W_WEIDTH - WEIDTH)//2
        Y = (W_HEIGHT - HEIGHT)//2
        
        self.geometry(f'{WEIDTH}x{HEIGHT}+{X}+{Y}+') 
        
    def carregar_widgets(self):
        self.font_label = CTkFont('Segoe UI', size=15, weight='bold')

        CTkLabel(self, text=self.mensagem, font=self.font_label).pack(padx=10, pady=5, anchor='center')
        CTkButton(self, text='OK', command=self.destroy, width=100, font=self.font_label).pack(padx=10, anchor='center')
        
    def close(self, event):
        self.destroy()

    