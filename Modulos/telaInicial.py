from customtkinter import CTk, CTkImage, CTkButton, CTkFrame, CTkFont
from Modulos.TelaFornecedor import TelaFornecedor
from Modulos.TelaFuncionario import TelaFuncionario
from Imagens.img import img_venda, img_estoque, img_produto, img_fornecedor, img_funcionario, img_cliente
from PIL import Image


class TelaInicial(CTk):
    def __init__(self):
        CTk.__init__(self)
        self.title('Sistema')
        self.tela_fornecedor = None
        self.tela_funcionario = None
        self.centralizar_janela()
        self.carregar_widgets()
        
    def centralizar_janela(self):
        HEIGHT = int(self.winfo_screenheight()/ 1.30)
        WEIDTH = int(self.winfo_screenwidth() / 1.20)
        
        W_HEIGHT = self.winfo_screenheight()
        W_WEIDTH = self.winfo_screenwidth()
        
        X = (W_WEIDTH - WEIDTH)//2
        Y = (W_HEIGHT - HEIGHT)//2
        
        self.minsize(WEIDTH, HEIGHT)
        self.geometry(f'{WEIDTH}x{HEIGHT}+{X}+{Y}') 
        self.after(0, lambda:self.wm_state('zoomed'))
        
    def carregar_widgets(self):
        font_button = CTkFont('Consolas', 18, 'bold')
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        
        f_menu = CTkFrame(self)
        
        bt_venda = CTkButton(f_menu,text='Venda', compound='top', image=CTkImage(Image.open(img_venda), size=(64,64)), font=font_button)
        bt_estoque = CTkButton(f_menu, text='Estoque', compound='top', image=CTkImage(Image.open(img_estoque), size=(64,64)), font=font_button)
        bt_produto = CTkButton(f_menu, text='Produto', compound='top', image=CTkImage(Image.open(img_produto), size=(64,64)), font=font_button)
        bt_fornecedor = CTkButton(f_menu, text='Fornecedor', compound='top', image=CTkImage(Image.open(img_fornecedor), size=(64,64)), font=font_button,
                                  command=self.abrir_tela_fornecedor)
        bt_funcionario = CTkButton(f_menu, text='Funcionario',compound='top', image=CTkImage(Image.open(img_funcionario), size=(64,64)), font=font_button, 
                                   command=self.abrir_tela_funcionario)
        bt_cliente = CTkButton(f_menu, text='Cliente',compound='top', image=CTkImage(Image.open(img_cliente), size=(64,64)), font=font_button)
        

        f_menu.grid(column=0, columnspan=2, row=0, sticky='nswe')
        bt_venda.pack(side='left', padx=(5,0), pady=5)
        bt_estoque.pack(side='left', padx=(20,0), pady=5)
        bt_produto.pack(side='left', padx=(20,0), pady=5)
        bt_fornecedor.pack(side='left', padx=(20,0), pady=5)
        bt_funcionario.pack(side='left', padx=(20,0), pady=5)
        bt_cliente.pack(side='left', padx=(20,0), pady=5)
        
    def abrir_tela_fornecedor(self):
        if self.tela_fornecedor is None or not self.tela_fornecedor.winfo_exists():
            self.tela_fornecedor = TelaFornecedor(self)
            self.tela_fornecedor.transient(self)
    def abrir_tela_funcionario(self):
        if self.tela_funcionario is None or not self.tela_funcionario.winfo_exists():
            self.tela_funcionario = TelaFuncionario(self)
            self.tela_funcionario.transient(self)