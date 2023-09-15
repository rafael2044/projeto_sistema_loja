from customtkinter import CTkToplevel, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkFont, CTkImage, CTkScrollableFrame, CTkComboBox
from tkinter.ttk import Treeview, Scrollbar
from DAO.funcionarioDAO import funcionarioDAO
from DAO.cargoDAO import cargoDAO
from Modulos.TelaCargo import TelaCargo
from Modulos.TelaUsuario import TelaUsuario
from Popup.MensagemAlerta import MensagemAlerta
from Popup.DialogoSimNao import DialogoSimNao
from DAL.funcionarioDAL import Funcionario
from PIL import Image
from Imagens.img import img_pesquisa, img_atualizar, img_excluir, img_editar, img_cadastrar, img_usuario

class TelaFuncionario(CTkToplevel):
    
    def __init__(self, master=None):
        CTkToplevel.__init__(self, master=master, takefocus=True)
        self.master = master
        self.after(100, self.lift)
        self.title('Funcionarios')
        self.telaCadastrarFuncionario = None
        self.telaEditarFuncionario = None
        self.telaUsuario = None
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
        self.font_tabela_coluna = CTkFont('Segoe UI', size=17, weight='bold')
        self.font_tabela_linha = CTkFont('Segoe UI', size=15)
        self.font_entry = CTkFont('Segoe UI', size=16)
        self.font_button = CTkFont('Segoe UI', size=18, weight='bold')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        
        
        f_bts_top = CTkFrame(self, corner_radius=25, fg_color='transparent')
        
        self.f_funcionario = CTkScrollableFrame(self, corner_radius=20)
        self.f_funcionario.grid_columnconfigure(0, weight=1)
        self.f_funcionario.grid_columnconfigure(1, weight=3)
        self.f_funcionario.grid_columnconfigure(2, weight=5)
        self.f_funcionario.grid_columnconfigure(3, weight=3)
        self.f_funcionario.grid_columnconfigure(4, weight=4)
        self.f_funcionario.grid_columnconfigure(5, weight=5)
        self.f_funcionario.grid_columnconfigure(6, weight=0)
        self.f_funcionario.grid_columnconfigure(7, weight=0)

        
        
        self.pesquisa = CTkEntry(self, placeholder_text='Nome do Funcionario', width=150,height=40, font=self.font_entry)
        
        self.pesquisa.grid(column=0, row=0, padx=10, pady=10, sticky='we')
        f_bts_top.grid(column=1, columnspan=2, row=0, sticky='wesn')
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_pesquisa), size=(32,32)), width=75,height=40).pack(side='left', padx=(5,5))
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_atualizar), size=(32,32)), width=75,height=40).pack(side='left', padx=(5,10))
        CTkButton(f_bts_top, text='Cadastrar', image=CTkImage(Image.open(img_cadastrar), size=(32,32)), command=self.abrir_telaCadastrarFuncionario, compound='left',
                  font=self.font_button).pack(side='left', padx=(5,10))
        CTkButton(f_bts_top, text='Usuario', image=CTkImage(Image.open(img_usuario), size=(32,32)), command=self.abrir_telaUsuario, compound='left',
                  font=self.font_button).pack(side='left', padx=(5,10))
        
        self.f_funcionario.grid(column=0, row=1, columnspan=3, sticky='wsen', padx=(10,0), ipadx=20, ipady=20)
        self.carregar_funcionarios()
             
    def carregar_funcionarios(self):
        [x.destroy() for x in self.f_funcionario.winfo_children()]
        self.funcionarios = funcionarioDAO().select_all_funcionarios()
        rows = len(self.funcionarios)
        CTkLabel(self.f_funcionario, text='ID', font=self.font_tabela_coluna).grid(column=0, row=0, pady=0, padx=0)
        CTkLabel(self.f_funcionario, text='NOME', font=self.font_tabela_coluna).grid(column=1, row=0, pady=0,padx=0)
        CTkLabel(self.f_funcionario, text='SOBRENOME', font=self.font_tabela_coluna).grid(column=2, row=0, pady=0, padx=0)
        CTkLabel(self.f_funcionario, text='CPF', font=self.font_tabela_coluna).grid(column=3, row=0, pady=0, padx=0)
        CTkLabel(self.f_funcionario, text='CARGO', font=self.font_tabela_coluna).grid(column=4, row=0, pady=0, padx=0)
        CTkLabel(self.f_funcionario, text='TELEFONE', font=self.font_tabela_coluna).grid(column=5, row=0, pady=0, padx=0)
        CTkFrame(self.f_funcionario, bg_color='white', height=1).grid(column=0, columnspan=6, row=0, sticky='wes')
        CTkFrame(self.f_funcionario, bg_color='white', height=1).grid(column=0, columnspan=6, row=0, sticky='wen')
        
        for l in range(rows):
            CTkLabel(self.f_funcionario, text=self.funcionarios[l].id, font=self.font_tabela_linha).grid(column=0, row=l+1)
            CTkLabel(self.f_funcionario, text=self.funcionarios[l].nome, font=self.font_tabela_linha).grid(column=1, row=l+1)
            CTkLabel(self.f_funcionario, text=self.funcionarios[l].sobrenome, font=self.font_tabela_linha).grid(column=2, row=l+1)
            CTkLabel(self.f_funcionario, text=self.funcionarios[l].get_cpf(), font=self.font_tabela_linha).grid(column=3, row=l+1)
            CTkLabel(self.f_funcionario, text=self.funcionarios[l].get_cargo_nome(), font=self.font_tabela_linha).grid(column=4, row=l+1)
            CTkLabel(self.f_funcionario, text=self.funcionarios[l].get_telefone(), font=self.font_tabela_linha).grid(column=5, row=l+1)
            CTkButton(self.f_funcionario, text='', image=CTkImage(Image.open(img_editar), size=(32,32)), width=70, 
                      command=lambda x=l: self.abrir_telaEditarFuncionario(self.funcionarios[x])).grid(column=6, row=l+1, padx=10, pady=5)
            CTkButton(self.f_funcionario, text='',image=CTkImage(Image.open(img_excluir), size=(32,32)), width=70, 
                      command=lambda y = l: self.deletar_funcionario(self.funcionarios[y])).grid(column=7, row=l+1, padx=10, pady=5)
            

    def deletar_funcionario(self, funcionario):
        op = DialogoSimNao('Alerta', f'Deseja Excluir o funcionario {funcionario.nome}?')
        if op.opcao:
            funcionarioDAO().delete_funcionario(funcionario)   
            self.carregar_funcionarios()
    
    def abrir_telaEditarFuncionario(self, funcionario):
        if self.telaEditarFuncionario is None or not self.telaEditarFuncionario.winfo_exists():
            self.telaEditarFuncionario = EditarFuncionario(self, funcionario)
            self.telaEditarFuncionario.transient(self)
    def abrir_telaCadastrarFuncionario(self):
        if self.telaCadastrarFuncionario is None or not self.telaCadastrarFuncionario.winfo_exists():
            self.telaCadastrarFuncionario = CadastrarFuncionario(self)
            self.telaCadastrarFuncionario.transient(self)
            
    def abrir_telaUsuario(self):
        if self.telaUsuario is None or not self.telaUsuario.winfo_exists():
            self.telaUsuario = TelaUsuario(self)
            self.telaUsuario.transient(self)
        
class CadastrarFuncionario(CTkToplevel):
    def __init__(self, master):
        CTkToplevel.__init__(self, master=master)
        self.master = master
        self.after(100, self.lift)
        self.title('Cadastrar Funcionarios')
        self.telaCargo = None
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
        
    
        self.nome = CTkEntry(self, placeholder_text='Digite o nome do Funcionario...', font=self.font_entry, height=40)

        self.sobrenome = CTkEntry(self, placeholder_text='Digite o sobreme do Funcionario...', font=self.font_entry, height=40)

        self.cpf = CTkEntry(self, placeholder_text='Digite o cpf do Funcionario...', font=self.font_entry, height=40)
        
        self.cargo = CTkComboBox(self, font=self.font_entry,values=[''] , height=40, state='readonly')
        
        self.telefone = CTkEntry(self, width=200, font=self.font_entry, placeholder_text='Digite o Telefone do Funcionario...', height=40)
        
        CTkLabel(self, text='CADASTRAR FUNCIONARIO', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=0, columnspan=2)
        CTkLabel(self, text='Preencha os dados abaixo.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', column=0, row=1, columnspan=2)
        CTkLabel(self, text='Nome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=2, columnspan=2)
        self.nome.grid(padx=10, sticky='we', column=0, row=3)
        CTkLabel(self, text='sobrenome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=4, columnspan=2)
        self.sobrenome.grid(padx=10, sticky='we', column=0, row=5)
        CTkLabel(self, text='CPF*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=6, columnspan=2)
        self.cpf.grid(padx=10, sticky='we', column=0, row=7)
        CTkLabel(self, text='Cargo*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=8, columnspan=2)
        self.cargo.grid(padx=10, sticky='we', column=0, row=9)
        CTkButton(self, text='+', font=self.font_button, width=50, command=self.abrir_telaCargo).grid(column=1, row=9)
        CTkLabel(self, text='Telefone', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=10, columnspan=2)
        self.telefone.grid(padx=10, sticky='we', column=0, row=11)
        CTkLabel(self, text='* -> Campo obrigatorio.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', pady=10, column=0, row=12, columnspan=2)    
        CTkButton(self, text='Cadastrar', image = CTkImage(Image.open(img_cadastrar)),compound='left',
                  font=self.font_button, command=self.cadastrar_funcionario, height=40).grid(padx=10, sticky='w', pady=10, column=0, row=13)
        
        self.carregar_cargos()
    def carregar_cargos(self):
        self.cargos = cargoDAO().select_all_cargos()
        self.cargo.configure(values=[x.nome for x in self.cargos])
        if self.cargos:
            self.cargo.set(self.cargos[0].nome)
    
    def cadastrar_funcionario(self):
        nome = self.nome.get()
        sobrenome = self.sobrenome.get()
        cpf = self.cpf.get()
        cargo = list(filter(lambda x: x.nome == self.cargo.get(), self.cargos))[0]
        telefone = self.telefone.get()
        if nome and sobrenome and cpf and cargo:
            match funcionarioDAO().insert_funcionario(Funcionario(0, nome, sobrenome, cpf, telefone, cargo)):
                case 1: 
                    MensagemAlerta('Sucesso', 'Funcionario Cadastrado com sucesso!')
                    self.master.carregar_funcionarios()
                case 2:
                    MensagemAlerta('Erro', 'O funcionario já está cadastrado no sistema!')
                case 3:
                    MensagemAlerta('Falha no sistema', 'Aconteceu um erro ao tentar cadastrar fornecedor!')
        else:
            MensagemAlerta('Aviso', 'Os campos obrigatorios precisam se preenchidos!')
            
    def abrir_telaCargo(self):
        if self.telaCargo is None or not self.telaCargo.winfo_exists():
            self.telaCargo = TelaCargo(self)
            self.telaCargo.transient(self)
    
        
class EditarFuncionario(CTkToplevel):
    def __init__(self, master, funcionario: Funcionario):
        CTkToplevel.__init__(self)
        self.master =master
        self.funcionario = funcionario
        self.after(100, self.lift)
        self.title('Editar Funcionario')
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
        self.carregar_cargos()
        self.font_label_titulo = CTkFont('Segoe UI', size=18, weight='bold')
        self.font_label_subtitulo = CTkFont('Segoe UI', size=16)
        self.font_label_infor = CTkFont('Segoe UI', size=15, weight='normal')
        self.font_entry = CTkFont('Segoe UI', size=16)
        self.font_button = CTkFont('Segoe UI', size=18, weight='bold')
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        
        self.id = CTkEntry(self, placeholder_text='ID do Funcionario...', font=self.font_entry, height=40)
        self.nome = CTkEntry(self, placeholder_text='Digite o nome do Funcionario...', font=self.font_entry, height=40)

        self.sobrenome = CTkEntry(self, placeholder_text='Digite o sobreme do Funcionario...', font=self.font_entry, height=40)

        self.cpf = CTkEntry(self, placeholder_text='Digite o cpf do Funcionario...', font=self.font_entry, height=40)
        
        self.cargo = CTkComboBox(self, font=self.font_entry,values=[x.nome for x in self.cargos] , height=40)
        
        self.telefone = CTkEntry(self, width=200, font=self.font_entry, placeholder_text='Digite o Telefone do Funcionario...', height=40)
        
        f_buttons = CTkFrame(self, fg_color='transparent')
        CTkLabel(self, text='CADASTRAR FUNCIONARIO', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=0, columnspan=2)
        CTkLabel(self, text='Preencha os dados abaixo.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', column=0, row=1, columnspan=2)
        CTkLabel(self, text='ID', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=2, columnspan=2)
        self.id.grid(padx=10, sticky='we', column=0, row=3)
        CTkLabel(self, text='Nome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=4, columnspan=2)
        self.nome.grid(padx=10, sticky='we', column=0, row=5)
        CTkLabel(self, text='sobrenome*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=6, columnspan=2)
        self.sobrenome.grid(padx=10, sticky='we', column=0, row=7)
        CTkLabel(self, text='CPF*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=8, columnspan=2)
        self.cpf.grid(padx=10, sticky='we', column=0, row=9)
        CTkLabel(self, text='Cargo*', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=10, columnspan=2)
        self.cargo.grid(padx=10, sticky='we', column=0, row=11)
        CTkLabel(self, text='Telefone', font=self.font_label_titulo).grid(padx=10, sticky='w', pady=10, column=0, row=12, columnspan=2)
        self.telefone.grid(padx=10, sticky='we', column=0, row=13)
        CTkLabel(self, text='* -> Campo obrigatorio.', font=self.font_label_subtitulo).grid(padx=10, sticky='w', pady=10, column=0, row=14, columnspan=2)    
        f_buttons.grid(padx=10, sticky='wesn', column=0, row=15, columnspan=2)
        
        CTkButton(f_buttons, text='Salvar Alterações', font=self.font_button, height=40, command=self.salvar_alterecoes).pack(anchor='w', padx=10, pady=20, side='left')
        CTkButton(f_buttons, text='Cancelar', font=self.font_button, height=40, command=self.destroy).pack(anchor='w', padx=10, pady=20, side='left')

        self.carregar_dados()
       
    def carregar_cargos(self):
        self.cargos = cargoDAO().select_all_cargos()    
        
    def carregar_dados(self):
        self.id.insert(0, self.funcionario.id)
        self.nome.insert(0, self.funcionario.nome)
        self.sobrenome.insert(0, self.funcionario.sobrenome)
        self.cpf.insert(0, self.funcionario.get_cpf())
        self.cargo.set(self.funcionario.get_cargo_nome())
        self.telefone.insert(0, self.funcionario.get_telefone())
        
        self.id.configure(state='disabled')
        self.cpf.configure(state='disabled')
            
    def salvar_alterecoes(self):
        if self.nome.get() and self.sobrenome and self.cargo.get():
            self.funcionario.nome = self.nome.get()
            self.funcionario.cargo = list(filter(lambda x: x.nome == self.cargo.get(), self.cargos))[0]
            self.funcionario.telefone = self.telefone.get()
            if funcionarioDAO().atualizar_funcionario(self.funcionario):
                MensagemAlerta('Sucesso!', 'Alteraçõoes realizadas com sucesso!')
            else:
                MensagemAlerta('Erro!', 'Aconteceu um erro ao realizar alteracões!')
        else:
            MensagemAlerta('Aviso', 'Preencha todos os campos obrigatorios disponiveis!')
        self.master.carregar_funcionarios()
        self.destroy()
    