from customtkinter import CTkToplevel, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkFont, CTkImage, CTkScrollableFrame, CTkComboBox
from tkinter.ttk import Treeview, Scrollbar
from DAO.usuarioDAO import usuarioDAO
from DAO.funcionarioDAO import funcionarioDAO
from Popup.MensagemAlerta import MensagemAlerta
from Popup.DialogoSimNao import DialogoSimNao
from DAL.usuarioDAL import Usuario
from PIL import Image
from Imagens.img import img_pesquisa, img_atualizar, img_excluir, img_editar, img_cadastrar, img_usuario


class TelaUsuario(CTkToplevel):

    def __init__(self, master=None):
        CTkToplevel.__init__(self, master=master, takefocus=True)
        self.master = master
        self.after(100, self.lift)
        self.title('Usuarios')
        self.telaCadastrarUsuario = None
        self.telaEditarUsuario = None
        self.fornecedores = None
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def centralizar_janela(self):

        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()

        HEIGHT = int(W_HEIGHT * 0.45)
        WEIDTH = int(W_WEIDTH * 0.50)

        X = int((W_WEIDTH - WEIDTH)//2)
        Y = int((W_HEIGHT - HEIGHT)//4.5)

        self.geometry(f'{WEIDTH}x{HEIGHT}+{X}+{Y}+')

    def carregar_widgets(self):
        self.font_label = CTkFont('Segoe UI', size=18, weight='bold')
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

        self.f_usuario = CTkScrollableFrame(self, corner_radius=20)
        self.f_usuario.grid_columnconfigure(0, weight=0)
        self.f_usuario.grid_columnconfigure(1, weight=3)
        self.f_usuario.grid_columnconfigure(2, weight=5)
        self.f_usuario.grid_columnconfigure(3, weight=5)
        self.f_usuario.grid_columnconfigure(4, weight=0)

        self.pesquisa = CTkEntry(
            self, placeholder_text='Nome do Usuario', width=150, height=40, font=self.font_entry)

        self.pesquisa.grid(column=0, row=0, padx=10, pady=10, sticky='we')
        f_bts_top.grid(column=1, columnspan=2, row=0, sticky='wesn')
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_pesquisa), size=(
            32, 32)), width=75, height=40).pack(side='left', padx=(5, 5))
        CTkButton(f_bts_top, text='', image=CTkImage(Image.open(img_atualizar), size=(
            32, 32)), width=75, height=40).pack(side='left', padx=(5, 10))
        CTkButton(f_bts_top, text='Cadastrar', image=CTkImage(Image.open(img_cadastrar), size=(32, 32)), command=self.abrir_telaCadastrarUsuario, compound='left',
                  font=self.font_button).pack(side='left', padx=(5, 10))

        self.f_usuario.grid(column=0, row=1, columnspan=3,
                            sticky='wsen', padx=(10, 0), ipadx=20, ipady=20)
        self.carregar_usuarios()

    def carregar_usuarios(self):
        [x.destroy() for x in self.f_usuario.winfo_children()]
        CTkLabel(self.f_usuario, text='ID').grid(column=0, row=0)
        CTkLabel(self.f_usuario, text='NOME DE USUARIO').grid(column=1, row=0)
        CTkLabel(self.f_usuario, text='NOME COMPLETO').grid(column=2, row=0)
        CTkLabel(self.f_usuario, text='CARGO').grid(column=3, row=0)
        self.usuarios = usuarioDAO().select_all_usuarios()
        rows = len(self.usuarios)
        for l in range(rows):
            CTkLabel(self.f_usuario, text=self.usuarios[l].id).grid(
                column=0, row=l+1)
            CTkLabel(self.f_usuario, text=self.usuarios[l].nome).grid(
                column=1, row=l+1)
            CTkLabel(self.f_usuario, text=self.usuarios[l].get_nome_completo()).grid(
                column=2, row=l+1)
            CTkLabel(self.f_usuario, text=self.usuarios[l].funcionario.get_cargo_nome()).grid(
                column=3, row=l+1)
            CTkButton(self.f_usuario, text='', image=CTkImage(Image.open(img_excluir), size=(32, 32)), width=70,
                      command=lambda y=l: self.deletar_usuario(self.usuarios[y])).grid(column=4, row=l+1, padx=10)

    def deletar_usuario(self, usuario):
        op = DialogoSimNao(
            'Alerta', f'Deseja Excluir o Usuario {usuario.nome}?')
        if op.opcao:
            usuarioDAO().delete_usuario(usuario)
            self.carregar_usuarios()

    def abrir_telaCadastrarUsuario(self):
        if self.telaCadastrarUsuario is None or not self.telaCadastrarUsuario.winfo_exists():
            self.telaCadastrarUsuario = CadastrarUsuario(self)
            self.telaCadastrarUsuario.transient(self)


class CadastrarUsuario(CTkToplevel):
    def __init__(self, master):
        CTkToplevel.__init__(self, master=master)
        self.master = master
        self.after(100, self.lift)
        self.title('Cadastrar Usuarios')
        self.telaCargo = None
        self.centralizar_janela()
        self.carregar_widgets()
        self.protocol('WM_DELETE_WINDOW', self.destroy)

    def centralizar_janela(self):

        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()

        HEIGHT = 500
        WEIDTH = 350

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

        self.funcionario = CTkComboBox(
            self, font=self.font_entry, values=[], height=40, width=300)

        self.nome = CTkEntry(self, placeholder_text='Digite o nome de Usuario...',
                             font=self.font_entry, height=40, width=300)

        self.senha = CTkEntry(self, placeholder_text='Digite a senha',
                              font=self.font_entry, height=40, width=300, show='*')

        CTkLabel(self, text='CADASTRAR USUARIO', font=self.font_label_titulo).grid(
            padx=10, sticky='w', pady=10, column=0, row=0, columnspan=2)
        CTkLabel(self, text='Selecione um funcionario e preencha os dados abaixo.',
                 font=self.font_label_subtitulo).grid(padx=10, sticky='w', column=0, row=1, columnspan=2)
        CTkLabel(self, text='Funcionario*', font=self.font_label_titulo).grid(padx=10,
                                                                              sticky='w', pady=10, column=0, row=2, columnspan=2)
        self.funcionario.grid(padx=10, sticky='w', column=0, row=3)
        CTkLabel(self, text='Nome de Usuario*', font=self.font_label_titulo).grid(
            padx=10, sticky='w', pady=10, column=0, row=4, columnspan=2)
        self.nome.grid(padx=10, sticky='w', column=0, row=5)
        CTkLabel(self, text='Senha*', font=self.font_label_titulo).grid(padx=10,
                                                                        sticky='w', pady=10, column=0, row=6, columnspan=2)
        self.senha.grid(padx=10, sticky='w', column=0, row=7)
        CTkLabel(self, text='* -> Campo obrigatorio.', font=self.font_label_subtitulo).grid(
            padx=10, sticky='w', pady=10, column=0, row=8, columnspan=2)
        CTkButton(self, text='Cadastrar', image=CTkImage(Image.open(img_cadastrar)), compound='left',
                  font=self.font_button, command=self.cadastrar_usuario, height=40).grid(padx=10, sticky='w', pady=10, column=0, row=9)

        self.carregar_funcionario()

    def carregar_funcionario(self):
        self.funcionarios = usuarioDAO().select_all_funcionarios_nao_cadastrados()
        if self.funcionarios:
            self.funcionario.configure(
                values=[f'{x.nome} {x.sobrenome}' for x in self.funcionarios])
            self.funcionario.set(
                f'{self.funcionarios[0].nome} {self.funcionarios[0].sobrenome}')
        else:
            self.funcionario.set('')

    def cadastrar_usuario(self):
        nome = self.nome.get()
        senha = self.senha.get()
        funcionario = self.funcionario.get()
        if nome and senha and funcionario:
            match usuarioDAO().insert_usuario(Usuario(0, nome, senha, 0, list(filter(lambda x: f'{x.nome} {x.sobrenome}' == funcionario, self.funcionarios))[0])):
                case 1:
                    MensagemAlerta(
                        'Sucesso', 'Usuario Cadastrado com sucesso!')
                    self.master.carregar_usuarios()
                    self.nome.delete(0, nome.rfind(nome[-1])+1)
                    self.senha.delete(0, senha.rfind(senha[-1])+1)
                    self.carregar_funcionario()
                case 2:
                    MensagemAlerta(
                        'Erro', 'O Usuario já está cadastrado no sistema!')
                case 3:
                    MensagemAlerta(
                        'Falha no sistema', 'Aconteceu um erro ao tentar cadastrar fornecedor!')
        else:
            MensagemAlerta(
                'Aviso', 'Os campos obrigatorios precisam se preenchidos!')
