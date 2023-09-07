from DAO.db import DataBase
from DAL.fornecedorDAL import Fornecedor
class fornecedorDAO(DataBase):
    def __init__(self):
        DataBase.__init__(self)
        
    def insert_fornecedor(self, fornecedor:Fornecedor):
        '''1 - Fornecedor inserido com sucesso
           2 - Fornecedor já existe
           3 - Erro no banco de dados
           '''
        try:
            self.cursor()
            if not self.fornecedor_existe(fornecedor):
                sql = f'''INSERT INTO fornecedor (nome_fornecedor, cnpj_fornecedor, cpf_fornecedor, endereco_fornecedor, telefone_fornecedor) VALUES (?,?,?,?,?);'''
                self.cur.execute(sql,(fornecedor.nome, fornecedor.cnpj, fornecedor.cpf, fornecedor.endereco, fornecedor.telefone))
                self.con.commit()
                return 1
            return 2
        except Exception as e:
            print(f'Erro ao inserir fornecedor: {e}')
            return 3
        finally:
            self.desconectar()
    
    def delete_fornecedor(self, fornecedor: Fornecedor):
        try:
            self.cursor()
            sql = "DELETE FROM fornecedor WHERE id_fornecedor = ?"
            self.cur.execute(sql, (fornecedor.id, ))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao deletar fornecedor: {e}')
        finally:
            self.desconectar
  
    def atualizar_fornecedor(self, fornecedor: Fornecedor):
        try:
            self.cursor()
            sql = "UPDATE fornecedor SET nome_fornecedor = ?, endereco_fornecedor= ?, telefone_fornecedor = ? WHERE id_fornecedor = ?"
            self.cur.execute(sql, (fornecedor.nome, fornecedor.endereco,fornecedor.telefone, fornecedor.id))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao atualizar fornecedor: {e}')
        finally:
            self.desconectar
  
    def select_all_fornecedores(self):
        try:
            self.cursor()
            sql = '''SELECT * FROM fornecedor'''
            return [Fornecedor(x[0], x[1], x[2], x[3], x[4], x[5]) for x in self.cur.execute(sql).fetchall()]
        except Exception as e:
            print(f'Erro query select all fornecedores: {e}')
        finally:
            self.desconectar()
            
    def select_fornecedor_cnpj(self, fornecedor: Fornecedor):
        try:
            self.cursor()
            sql = '''SELECT * FROM fornecedor WHERE cnpj_fornecedor = ? AND LENGTH(cnpj_fornecedor) != 0;'''
            return self.cur.execute(sql, (fornecedor.cnpj, )).fetchone()
        except Exception as e:
            print(f'Erro query select fornecedor: {e}')
            self.desconectar()
            
    def select_fornecedor_cpf(self, fornecedor: Fornecedor):
        try:
            self.cursor()
            sql = '''SELECT * FROM fornecedor WHERE cpf_fornecedor = ? AND LENGTH(cpf_fornecedor) != 0;'''
            return self.cur.execute(sql, (fornecedor.cpf,)).fetchone()
        except Exception as e:
            print(f'Erro query select fornecedor: {e}')
            self.desconectar()
        
    def select_like_fornecedor(self, nome:str):
        try:
            self.cursor()
            if nome:
                sql = '''SELECT * FROM fornecedor WHERE nome_fornecedor LIKE ?;'''
                return [Fornecedor(x[0], x[1], x[2], x[3], x[4], x[5]) for x in self.cur.execute(sql, (nome+'%', )).fetchall()]
        except Exception as e:
            print(f'Erro query select like fornecedor: {e}')
        finally:
            self.desconectar    
    
    def fornecedor_existe(self, fornecedor : Fornecedor ):
        if self.select_fornecedor_cnpj(fornecedor) or self.select_fornecedor_cpf(fornecedor):
            return True
        return False