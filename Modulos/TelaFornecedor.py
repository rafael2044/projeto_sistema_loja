from customtkinter import CTkToplevel, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkFont, CTkImage, CTkScrollableFrame, CTkCheckBox
from tkinter.ttk import Treeview, Scrollbar
from DAO.fornecedorDAO import fornecedorDAO
from Popup.MensagemAlerta import MensagemAlerta
from Popup.DialogoSimNao import DialogoSimNao
from DAL.fornecedorDAL import Fornecedor
from PIL import Image
from Imagens.img import img_pesquisa, img_atualizar, img_excluir, img_editar, img_cadastrar

class TelaFornecedor(CTkToplevel):
    
    def __init__(self, master=None):
        CTkToplevel.__init__(self, master=master, takefocus=True)
        self.master = master
        self.after(100, self.lift)
        self.title('Fornecedores')
        self.telaCadastrarFornecedor = None
        self.telaEditarFornecedor = None
        self.fornecedores = None
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        
    def centralizar_janela(self):
        
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        HEIGHT = int(W_HEIGHT * 0.60)
        WEIDTH = int(W_WEIDTH * 0.75)
        
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
        
        self.f_fornecedor = CTkScrollableFrame(self, corner_radius=20)
        self.f_fornecedor.grid_columnconfigure(0, weight=0)
        self.f_fornecedor.grid_columnconfigure(1, weight=5)
        self.f_fornecedor.grid_columnconfigure(2, weight=2)
        self.f_fornecedor.grid_columnconfigure(3, weight=2)
        self.f_fornecedor.grid_columnconfigure(4, weight=5)
        self.f_fornecedor.grid_columnconfigure(5, weight=5)
        self.f_fornecedor.grid_columnconfigure(6, weight=0)
        self.f_fornecedor.grid_columnconfigure(7, weight=0)
        
        
        self.pesquisa = CTkEntry(self, placeholder_text='Nome do fornecedor', width=150,height=40, font=self.font_entry)
        
        self.pesquisa.grid(column=0, row=0, padx=10, pady=10, sticky='we')
        f_bts_top.grid(column=1, columnspan=2, row=0, sticky='e')
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_pesquisa), size=(32,32)), width=75,height=40).pack(side='left', padx=(5,5))
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_atualizar), size=(32,32)), width=75,height=40).pack(side='left', padx=(5,10))
        CTkButton(f_bts_top, text='Cadastrar', image=CTkImage(Image.open(img_cadastrar), size=(32,32)), command=self.abrir_telaCadastrarFornecedor, compound='left',
                  font=self.font_button).pack(side='left', padx=(5,10))
        
        self.f_fornecedor.grid(column=0, row=1, columnspan=2, sticky='wsen', padx=(10,0), ipadx=20, ipady=20)
        self.carregar_fornecedores()
             
    def carregar_fornecedores(self):
        [x.destroy() for x in self.f_fornecedor.winfo_children()]
        CTkLabel(self.f_fornecedor, text='ID').grid(column=0, row=0)
        CTkLabel(self.f_fornecedor, text='NOME').grid(column=1, row=0)
        CTkLabel(self.f_fornecedor, text='CNPJ').grid(column=2, row=0)
        CTkLabel(self.f_fornecedor, text='CPF').grid(column=3, row=0)
        CTkLabel(self.f_fornecedor, text='ENREDEÇO').grid(column=4, row=0)
        CTkLabel(self.f_fornecedor, text='TELEFONE').grid(column=5, row=0)
        self.fornecedores = fornecedorDAO().select_all_fornecedores()
        rows = len(self.fornecedores)
        for l in range(rows):
            CTkLabel(self.f_fornecedor, text=self.fornecedores[l].id).grid(column=0, row=l+1)
            CTkLabel(self.f_fornecedor, text=self.fornecedores[l].nome).grid(column=1, row=l+1)
            CTkLabel(self.f_fornecedor, text=self.fornecedores[l].get_cnpj()).grid(column=2, row=l+1)
            CTkLabel(self.f_fornecedor, text=self.fornecedores[l].get_cpf()).grid(column=3, row=l+1)
            CTkLabel(self.f_fornecedor, text=self.fornecedores[l].endereco).grid(column=4, row=l+1)
            CTkLabel(self.f_fornecedor, text=self.fornecedores[l].get_telefone()).grid(column=5, row=l+1)
            CTkButton(self.f_fornecedor, text='', image=CTkImage(Image.open(img_editar), size=(32,32)), width=70, 
                      command=lambda x=l: self.abrir_telaEditarFornecedor(self.fornecedores[x])).grid(column=6, row=l+1, padx=10)
            CTkButton(self.f_fornecedor, text='',image=CTkImage(Image.open(img_excluir), size=(32,32)), width=70, 
                      command=lambda y = l: self.deletar_fornecedor(self.fornecedores[y])).grid(column=7, row=l+1, padx=10)
        
    def deletar_fornecedor(self, fornecedor):
        op = DialogoSimNao('Alerta', f'Deseja Excluir o fornecedor {fornecedor.nome}?')
        if op.opcao:
            fornecedorDAO().delete_fornecedor(fornecedor)   
            self.carregar_fornecedores()
    
    def abrir_telaEditarFornecedor(self, fornecedor):
        if self.telaEditarFornecedor is None or not self.telaEditarFornecedor.winfo_exists():
            self.telaEditarFornecedor = EditarFornecedor(self, fornecedor)
            self.telaEditarFornecedor.transient(self)
    def abrir_telaCadastrarFornecedor(self):
        if self.telaCadastrarFornecedor is None or not self.telaCadastrarFornecedor.winfo_exists():
            self.telaCadastrarFornecedor = CadastrarFornecedor(self)
            self.telaCadastrarFornecedor.transient(self)
        
class CadastrarFornecedor(CTkToplevel):
    def __init__(self, master):
        CTkToplevel.__init__(self, master=master)
        self.master = master
        self.after(100, self.lift)
        self.title('Cadastrar Fornecedor')
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        
    def centralizar_janela(self):
        
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        HEIGHT = 650
        WEIDTH = int(W_WEIDTH * 0.40)
        
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
        
    
        
        self.nome = CTkEntry(self, placeholder_text='Digite o nome do Fornecedor...', font=self.font_entry, height=40)

        self.cnpj = CTkEntry(self, placeholder_text='Digite o cnpj do Fornecedor...', font=self.font_entry, height=40)

        self.cpf = CTkEntry(self, placeholder_text='Digite o cpf do Fornecedor...', font=self.font_entry, height=40, state='disabled')
        
        self.endereco = CTkEntry(self, font=self.font_entry, placeholder_text='Digite o Endereço do fornecedor...', height=40)
        
        self.telefone = CTkEntry(self, width=200, font=self.font_entry, placeholder_text='Digite o Telefone do fornecedor...', height=40)
        
        CTkLabel(self, text='CADASTRAR FORNECEDOR', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=0, columnspan=2)
        CTkLabel(self, text='Preencha os dados abaixo.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', column=0, row=1, columnspan=2)
        CTkLabel(self, text='Nome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=2, columnspan=2)
        self.nome.grid(padx=10, sticky='we', column=0, row=3)
        CTkLabel(self, text='CNPJ*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=4, columnspan=2)
        self.cnpj.grid(padx=10, sticky='we', column=0, row=5)
        CTkCheckBox(self, command=self.nao_possui_cnpj, text='Não Possui').grid(column=1, row=5, sticky='w', padx=10, pady=10)
        CTkLabel(self, text='CPF*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=6, columnspan=2)
        self.cpf.grid(padx=10, sticky='we', column=0, row=7)
        CTkLabel(self, text='Endereço', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=8, columnspan=2)
        self.endereco.grid(padx=10, sticky='we', column=0, row=9)
        CTkLabel(self, text='Telefone', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=10, columnspan=2)
        self.telefone.grid(padx=10, sticky='we', column=0, row=11)
        CTkLabel(self, text='* -> Campo obrigatorio.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', pady=10, column=0, row=12, columnspan=2)    
        CTkButton(self, text='Cadastrar', image = CTkImage(Image.open(img_cadastrar)),compound='left',
                  font=self.font_button, command=self.cadastrar_fornecedor, height=40).grid(padx=10, sticky='w', pady=10, column=0, row=13)
        
    def nao_possui_cnpj(self):
        if self.cnpj.cget('state') == 'normal':
            self.cnpj.configure(placeholder_text='')
            self.cnpj.configure(state='disabled')
            self.cpf.configure(state='normal')
            self.cpf.configure(placeholder_text='Digite o cpf do Fornecedor...')
        else:
            self.cnpj.configure(state='normal')
            self.cnpj.configure(placeholder_text='Digite o cnpj do Fornecedor...')
            self.cpf.configure(placeholder_text='')
            self.cpf.configure(state='disabled')
    
    def cadastrar_fornecedor(self):
        nome = self.nome.get()
        cnpj = self.cnpj.get()
        cpf = self.cpf.get()
        endereco = self.endereco.get()
        telefone = self.telefone.get()
        if nome and (cnpj or cpf):
            match fornecedorDAO().insert_fornecedor(Fornecedor(0, nome, cnpj, cpf, endereco, telefone)):
                case 1: 
                    MensagemAlerta('Sucesso', 'Fornecedor Cadastrado com sucesso!')
                    self.master.carregar_fornecedores()
                case 2:
                    MensagemAlerta('Erro', 'O fornecedor já está cadastrado no sistema!')
                case 3:
                    MensagemAlerta('Falha no sistema', 'Aconteceu um erro ao tentar cadastrar fornecedor!')
        else:
            MensagemAlerta('Aviso', 'Os campos obrigatorios precisam se preenchidos!')
            
    
        
class EditarFornecedor(CTkToplevel):
    def __init__(self, master, fornecedor:Fornecedor):
        CTkToplevel.__init__(self)
        self.master =master
        self.fornecedor = fornecedor
        self.after(100, self.lift)
        self.title('Editar Fornecedor')
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        
    def centralizar_janela(self):
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        HEIGHT = 750
        WEIDTH = int(W_WEIDTH * 0.40)
        
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
        
    
        self.id = CTkEntry(self, placeholder_text='ID do fornecedor...', font=self.font_entry, height=40)
        
        self.nome = CTkEntry(self, placeholder_text='Digite o nome do Fornecedor...', font=self.font_entry, height=40)

        self.cnpj = CTkEntry(self, placeholder_text='Digite o cnpj do Fornecedor...', font=self.font_entry, height=40)

        self.cpf = CTkEntry(self, placeholder_text='Digite o cpf do Fornecedor...', font=self.font_entry, height=40, state='disabled')
        
        self.endereco = CTkEntry(self, font=self.font_entry, placeholder_text='Digite o Endereço do fornecedor...', height=40)
        
        self.telefone = CTkEntry(self, width=200, font=self.font_entry, placeholder_text='Digite o Telefone do fornecedor...', height=40)
        
        f_buttons = CTkFrame(self, fg_color='transparent')
        
        CTkLabel(self, text='EDITAR FORNECEDOR', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=0, columnspan=2)
        CTkLabel(self, text='Altere os campos que estão habilitados..', font=self.font_label_subtitulo).grid(padx=10, sticky='w', column=0, row=1, columnspan=2)
        CTkLabel(self, text='ID', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=2, columnspan=2)
        self.id.grid(padx=10, sticky='w', column=0, row=3)
        CTkLabel(self, text='Nome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=4, columnspan=2)
        self.nome.grid(padx=10, sticky='we', column=0, row=5)
        CTkLabel(self, text='CNPJ*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=6, columnspan=2)
        self.cnpj.grid(padx=10, sticky='we', column=0, row=7)
        CTkLabel(self, text='CPF*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=8, columnspan=2)
        self.cpf.grid(padx=10, sticky='we', column=0, row=9)
        CTkLabel(self, text='Endereço', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=10, columnspan=2)
        self.endereco.grid(padx=10, sticky='we', column=0, row=11)
        CTkLabel(self, text='Telefone', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=12, columnspan=2)
        self.telefone.grid(padx=10, sticky='we', column=0, row=13)
        CTkLabel(self, text='* -> Campo obrigatorio.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', pady=10, column=0, row=14, columnspan=2)    
        f_buttons.grid(padx=10, sticky='wesn', column=0, row=15, columnspan=2)
        
        CTkButton(f_buttons, text='Salvar Alterações', font=self.font_button, height=40, command=self.salvar_alterecoes).pack(anchor='w', padx=10, pady=20, side='left')
        CTkButton(f_buttons, text='Cancelar', font=self.font_button, height=40, command=self.destroy).pack(anchor='w', padx=10, pady=20, side='left')

        self.carregar_dados()
        
    def carregar_dados(self):
        self.id.insert(0, self.fornecedor.id)
        self.nome.insert(0, self.fornecedor.nome)
        self.cnpj.insert(0, self.fornecedor.get_cnpj())
        self.cpf.insert(0, self.fornecedor.get_cpf())
        self.endereco.insert(0, self.fornecedor.endereco)
        self.telefone.insert(0, self.fornecedor.get_telefone())
        
        self.id.configure(state='disabled')
        self.cnpj.configure(state='disabled')
        self.cpf.configure(state='disabled')
            
    def salvar_alterecoes(self):
        if self.nome.get():
            self.fornecedor.nome = self.nome.get()
            self.fornecedor.endereco = self.endereco.get()
            self.fornecedor.telefone = self.telefone.get()
            if fornecedorDAO().atualizar_fornecedor(self.fornecedor):
                MensagemAlerta('Sucesso!', 'Alteraçõoes realizadas com sucesso!')
            else:
                MensagemAlerta('Erro!', 'Aconteceu um erro ao realizar alteracões!')
        else:
            MensagemAlerta('Aviso', 'Preencha todos os campos obrigatorios disponiveis!')
        self.master.carregar_fornecedores()
        self.destroy()
    