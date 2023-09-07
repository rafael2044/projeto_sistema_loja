import sqlite3
from pathlib import Path
class DataBase:
    def __init__(self):
        self.create_tables()
        
    def conexao(self):
        try:
            db_path = Path(Path(__file__).parent.parent, 'DB','BancoDeDados.db')
            self.con = sqlite3.connect(db_path)
        except Exception as e:
            print(f'Erro ao realizar conexao com banco de dados!')
            self.desconectar()
    
    def cursor(self):
        self.conexao()
        self.cur = self.con.cursor()
        
    def desconectar(self):
        self.con.close()
        
    def create_tables(self):
        try:
            self.cursor()
            
            sql_cargo = '''CREATE TABLE IF NOT EXISTS cargo (
                            id_cargo INTEGER NOT NULL,
                            nome_cargo VARCHAR(100) NOT NULL,
                            PRIMARY KEY(id_cargo)
                            );'''
            self.cur.execute(sql_cargo)
            
            sql_categoria = '''CREATE TABLE IF NOT EXISTS categoria (
                                id_categoria INTEGER NOT NULL,
                                nome_categoria VARCHAR(100) NOT NULL,
                                PRIMARY KEY(id_categoria)
                                );'''
            self.cur.execute(sql_categoria)  
            
            sql_cliente = '''CREATE TABLE IF NOT EXISTS cliente (
                                id_cliente INTEGER NOT NULL,
                                nome_cliente VARCHAR(30) NOT NULL,
                                sobrenome_cliente VARCHAR(80) NOT NULL,
                                cpf_cliente VARCHAR(11),
                                telefone_cliente VARCHAR(11),
                                PRIMARY KEY(id_cliente)
                                );
                                ''' 
            self.cur.execute(sql_cliente)
            
            sql_fornecedor = '''CREATE TABLE IF NOT EXISTS fornecedor (
                                    id_fornecedor INTEGER NOT NULL,
                                    nome_fornecedor VARCHAR(200) NOT NULL,
                                    cnpj_fornecedor VARCHAR(14),
                                    cpf_fornecedor VARCHAR(11),
                                    endereco_fornecedor VARCHAR(255),
                                    telefone_fornecedor VARCHAR(10),
                                    PRIMARY KEY(id_fornecedor)
                                    );'''
            self.cur.execute(sql_fornecedor)
            
            sql_funcionario = '''CREATE TABLE IF NOT EXISTS funcionario (
                id_funcionario INTEGER NOT NULL,
                nome_funcionario VARCHAR(30) NOT NULL,
                sobrenome_funcionario VARCHAR(80) NOT NULL,
                cpf_funcionario VARCHAR(11) NOT NULL,
                telefone_funcionario VARCHAR(11),
                id_cargo INTEGER,
                PRIMARY KEY(id_funcionario),
                FOREIGN KEY(id_cargo) REFERENCES cargo (id_cargo)
                );'''
            self.cur.execute(sql_funcionario)
            
            sql_usuario = '''CREATE TABLE IF NOT EXISTS usuario (
                                id_usuario INTEGER NOT NULL,
                                nome_usuario VARCHAR(30) NOT NULL,
                                senha_usuario VARCHAR(64) NOT NULL,
                                reset_senha INTEGER NOT NULL DEFAULT 0,
                                id_funcionario INTEGER,
                                PRIMARY KEY(id_usuario),
                                FOREIGN KEY(id_funcionario) REFERENCES funcionario (id_funcionario)
                                );'''
            self.cur.execute(sql_usuario)
            
            sql_produto = '''CREATE TABLE IF NOT EXISTS produto (
                                id_produto INTEGER NOT NULL,
                                cod_barra_produto VARCHAR(13) NOT NULL,
                                descrica_produto VARCHAR(200) NOT NULL,
                                id_categoria INTEGER NOT NULL,
                                id_fornecedor INTEGER NOT NULL,
                                valor_venda_produto REAL NOT NULL,
                                valor_custo_produto REAL NOT NULL,
                                PRIMARY KEY(id_produto),
                                FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria),
                                FOREIGN KEY (id_fornecedor) REFERENCES fornecedor (id_fornecedor)
                                );'''
            self.cur.execute(sql_produto)
                        
            sql_estoque = '''CREATE TABLE IF NOT EXISTS estoque (
                                id_estoque INTEGER NOT NULL,
                                id_produto INTEGER NOT NULL,
                                quant_min_estoque INTEGER NOT NULL,
                                quant_atual_estoque INTEGER NOT NULL,
                                quant_max_estoque INTEGER NOT NULL,
                                data_cadastro TEXT NOT NULL DEFAULT (strftime('%d/%m/%Y %H:%M:%S',datetime('now', 'localtime'))),
                                CHECK(quant_atual_estoque >= quant_min_estoque AND quant_atual_estoque <= quant_max_estoque),
                                PRIMARY KEY(id_estoque),
                                FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
                                );'''
            self.cur.execute(sql_estoque)
                                  
            sql_venda_total = '''CREATE TABLE IF NOT EXISTS venda_total (
                                    id_venda_total INTEGER NOT NULL,
                                    id_cliente INTEGER NOT NULL,
                                    id_funcionario INTEGER NOT NULL,
                                    valor_venda_total REAL NOT NULL,
                                    data_venda_total TEXT NOT NULL DEFAULT (strftime('%d/%m/%Y %H:%M:%S',datetime('now', 'localtime'))),
                                    PRIMARY KEY(id_venda_total),
                                    FOREIGN KEY(id_funcionario) REFERENCES funcionario (id_funcionario),
                                    FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
                                    );'''
            self.cur.execute(sql_venda_total)
            
            sql_venda_unitaria = '''CREATE TABLE IF NOT EXISTS venda_unitaria (
                                        id_venda_unitaria INTEGER NOT NULL,
                                        id_venda_total INTEGER NOT NULL,
                                        id_produto INTEGER NOT NULL,
                                        valor_venda_unitaria REAL NOT NULL,
                                        PRIMARY KEY(id_venda_unitaria),
                                        FOREIGN KEY(id_venda_total) REFERENCES venda_total (id_venda_total),
                                        FOREIGN KEY(id_produto) REFERENCES produto (id_produto)
                                        );'''
            self.cur.execute(sql_venda_unitaria)
            self.con.commit()
            
        except Exception as e:
            print(f'Erro ao criar tabelas: {e}')
        finally:
            self.desconectar()
            
DataBase()