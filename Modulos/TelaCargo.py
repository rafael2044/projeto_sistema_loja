from customtkinter import CTkToplevel, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkFont, CTkImage, CTkScrollableFrame
from DAO.cargoDAO import cargoDAO
from Popup.MensagemAlerta import MensagemAlerta
from Popup.DialogoSimNao import DialogoSimNao
from DAL.cargoDAL import Cargo
from PIL import Image
from Imagens.img import img_pesquisa, img_atualizar, img_excluir, img_editar, img_cadastrar

class TelaCargo(CTkToplevel):
    
    def __init__(self, master=None):
        CTkToplevel.__init__(self, master=master, takefocus=True)
        self.master = master
        self.after(100, self.lift)
        self.title('Cargos')
        self.telaCadastrarCargo = None
        self.telaEditarCargo = None
        self.fornecedores = None
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        
    def centralizar_janela(self):
        
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        HEIGHT = int(W_HEIGHT * 0.45)
        WEIDTH = int(W_WEIDTH * 0.30)
        
        X = int((W_WEIDTH - WEIDTH)//2)
        Y = int((W_HEIGHT - HEIGHT)//4.5)
        
        self.geometry(f'{WEIDTH}x{HEIGHT}+{X}+{Y}+')
        
    def carregar_widgets(self):
        self.font_label = CTkFont('Segoe UI', size=18, weight='bold')
        self.font_entry = CTkFont('Segoe UI', size=16)
        self.font_button = CTkFont('Segoe UI', size=18, weight='bold')
        
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        
        
        f_bts_top = CTkFrame(self, corner_radius=25, fg_color='transparent')
        
        self.f_cargo = CTkScrollableFrame(self, corner_radius=20)
        self.f_cargo.grid_columnconfigure(0, weight=0)
        self.f_cargo.grid_columnconfigure(1, weight=5)
        self.f_cargo.grid_columnconfigure(2, weight=2)
        self.f_cargo.grid_columnconfigure(3, weight=2)
        
        self.pesquisa = CTkEntry(self, placeholder_text='Nome do cargo', width=150,height=40, font=self.font_entry)
        
        self.pesquisa.grid(column=0, row=0, padx=10, pady=10, sticky='we')
        f_bts_top.grid(column=1, columnspan=2, row=0, sticky='e')
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_pesquisa), size=(32,32)), width=75,height=40).pack(side='left', padx=(5,5))
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_atualizar), size=(32,32)), width=75,height=40).pack(side='left', padx=(5,10))
        CTkButton(f_bts_top, text='Cadastrar', image=CTkImage(Image.open(img_cadastrar), size=(32,32)), command=self.abrir_telaCadastrarCargo, compound='left',
                  font=self.font_button).pack(side='left', padx=(5,10))
        
        self.f_cargo.grid(column=0, row=1, columnspan=2, sticky='wsen', padx=(10,0), ipadx=20, ipady=20)
        self.carregar_cargos()
             
    def carregar_cargos(self):
        [x.destroy() for x in self.f_cargo.winfo_children()]
        CTkLabel(self.f_cargo, text='ID').grid(column=0, row=0)
        CTkLabel(self.f_cargo, text='NOME').grid(column=1, row=0)
        self.cargos = cargoDAO().select_all_cargos()
        rows = len(self.cargos)
        for l in range(rows):
            CTkLabel(self.f_cargo, text=self.cargos[l].id).grid(column=0, row=l+1)
            CTkLabel(self.f_cargo, text=self.cargos[l].nome).grid(column=1, row=l+1)
            CTkButton(self.f_cargo, text='', image=CTkImage(Image.open(img_editar), size=(32,32)), width=70, 
                      command=lambda x=l: self.abrir_telaEditarCargo(self.cargos[x])).grid(column=2, row=l+1, padx=10)
            CTkButton(self.f_cargo, text='',image=CTkImage(Image.open(img_excluir), size=(32,32)), width=70, 
                      command=lambda y = l: self.deletar_cargo(self.cargos[y])).grid(column=3, row=l+1, padx=10)
        
    def deletar_cargo(self, cargo):
        op = DialogoSimNao('Alerta', f'Deseja Excluir o cargo {cargo.nome}?')
        if op.opcao:
            cargoDAO().delete_cargo(cargo)   
            self.carregar_cargos()
            self.master.carregar_cargos()
    
    def abrir_telaEditarCargo(self, cargo):
        if self.telaEditarCargo is None or not self.telaEditarCargo.winfo_exists():
            self.telaEditarCargo = EditarCargo(self, cargo)
            self.telaEditarCargo.transient(self)
    def abrir_telaCadastrarCargo(self):
        if self.telaCadastrarCargo is None or not self.telaCadastrarCargo.winfo_exists():
            self.telaCadastrarCargo = CadastrarCargo(self)
            self.telaCadastrarCargo.transient(self)
        
class CadastrarCargo(CTkToplevel):
    def __init__(self, master):
        CTkToplevel.__init__(self, master=master)
        self.master = master
        self.after(100, self.lift)
        self.title('Cadastrar Cargos')
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        
    def centralizar_janela(self):
        
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        HEIGHT = 300
        WEIDTH = int(W_WEIDTH * 0.30)
        
        X = int((W_WEIDTH - WEIDTH)//2)
        Y = int((W_HEIGHT - HEIGHT)//4.5)
        
        self.geometry(f'{WEIDTH}x{HEIGHT}+{X}+{Y}+')
    
    def carregar_widgets(self):
        self.font_label_titulo = CTkFont('Segoe UI', size=18, weight='bold')
        self.font_label_subtitulo = CTkFont('Segoe UI', size=16)
        self.font_label_infor = CTkFont('Segoe UI', size=15, weight='normal')
        self.font_entry = CTkFont('Segoe UI', size=16)
        self.font_button = CTkFont('Segoe UI', size=18, weight='bold')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
    
        
        self.nome = CTkEntry(self, placeholder_text='Digite o nome do cargo...', font=self.font_entry, height=40)
        
        CTkLabel(self, text='CADASTRAR CARGO', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=0, columnspan=2)
        CTkLabel(self, text='Preencha os dados abaixo.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', column=0, row=1, columnspan=2)
        CTkLabel(self, text='Nome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=2, columnspan=2)
        self.nome.grid(padx=10, sticky='we', column=0, row=3)
        CTkLabel(self, text='* -> Campo obrigatorio.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', pady=10, column=0, row=4, columnspan=2)    
        CTkButton(self, text='Cadastrar', image = CTkImage(Image.open(img_cadastrar)),compound='left',
                  font=self.font_button, command=self.cadastrar_cargo, height=40).grid(padx=10, sticky='w', pady=10, column=0, row=5)
        
    def cadastrar_cargo(self):
        nome = self.nome.get()
        if nome:
            match cargoDAO().insert_cargo(Cargo(0, nome)):
                case 1: 
                    MensagemAlerta('Sucesso', 'Cargo Cadastrado com sucesso!')
                    self.master.carregar_cargos()
                    self.master.master.carregar_cargos()
                case 2:
                    MensagemAlerta('Erro', 'O Cargo já está cadastrado no sistema!')
                case 3:
                    MensagemAlerta('Falha no sistema', 'Aconteceu um erro ao tentar cadastrar Cargo!')
        else:
            MensagemAlerta('Aviso', 'Os campos obrigatorios precisam se preenchidos!')
            
    
        
class EditarCargo(CTkToplevel):
    def __init__(self, master, cargo: Cargo):
        CTkToplevel.__init__(self)
        self.master =master
        self.cargo = cargo
        self.after(100, self.lift)
        self.title('Editar Cargo')
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        
    def centralizar_janela(self):
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        HEIGHT = 400
        WEIDTH = int(W_WEIDTH * 0.30)
        
        X = int(self.master.winfo_x() + WEIDTH//2)
        Y = self.master.winfo_y()
        
        self.geometry(f'{WEIDTH}x{HEIGHT}+{X}+{Y}+')
        
    def carregar_widgets(self):
        self.font_label_titulo = CTkFont('Segoe UI', size=18, weight='bold')
        self.font_label_subtitulo = CTkFont('Segoe UI', size=16)
        self.font_label_infor = CTkFont('Segoe UI', size=15, weight='normal')
        self.font_entry = CTkFont('Segoe UI', size=16)
        self.font_button = CTkFont('Segoe UI', size=18, weight='bold')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
    
        self.id = CTkEntry(self, placeholder_text='ID do cargo...', font=self.font_entry, height=40)
        
        self.nome = CTkEntry(self, placeholder_text='Digite o nome do Cargo...', font=self.font_entry, height=40)

        f_buttons = CTkFrame(self, fg_color='transparent')
        
        CTkLabel(self, text='EDITAR CARGo', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=0, columnspan=2)
        CTkLabel(self, text='Altere os campos que estão habilitados..', font=self.font_label_subtitulo).grid(padx=10, sticky='w', column=0, row=1, columnspan=2)
        CTkLabel(self, text='ID', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=2, columnspan=2)
        self.id.grid(padx=10, sticky='w', column=0, row=3)
        CTkLabel(self, text='Nome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=4, columnspan=2)
        self.nome.grid(padx=10, sticky='we', column=0, row=5)
        CTkLabel(self, text='* -> Campo obrigatorio.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', pady=10, column=0, row=6, columnspan=2)    
        f_buttons.grid(padx=10, sticky='wesn', column=0, row=7, columnspan=2)
        
        CTkButton(f_buttons, text='Salvar Alterações', font=self.font_button, height=40, command=self.salvar_alterecoes).pack(anchor='w', padx=10, pady=20, side='left')
        CTkButton(f_buttons, text='Cancelar', font=self.font_button, height=40, command=self.destroy).pack(anchor='w', padx=10, pady=20, side='left')

        self.carregar_dados()
        
    def carregar_dados(self):
        self.id.insert(0, self.cargo.id)
        self.nome.insert(0, self.cargo.nome)
        
        self.id.configure(state='disabled')
            
    def salvar_alterecoes(self):
        if self.nome.get():
            self.cargo.nome = self.nome.get()
            if cargoDAO().atualizar_cargo(self.cargo):
                MensagemAlerta('Sucesso!', 'Alteraçõoes realizadas com sucesso!')
                self.master.carregar_cargos()
                self.master.master.carregar_cargos()
            else:
                MensagemAlerta('Erro!', 'Aconteceu um erro ao realizar alteracões!')
        else:
            MensagemAlerta('Aviso', 'Preencha todos os campos obrigatorios disponiveis!')
        self.master.carregar_cargos()
        self.destroy()
    