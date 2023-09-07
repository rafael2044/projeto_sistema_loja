from DAO.db import DataBase
from DAL.funcionarioDAL import Funcionario
from DAO.cargoDAO import cargoDAO
class funcionarioDAO(DataBase):
    def __init__(self):
        DataBase.__init__(self)
        
    def insert_funcionario(self, funcionario:Funcionario):
        '''1 - funcionario inserido com sucesso
           2 - funcionario já existe
           3 - Erro no banco de dados
           '''
        try:
            self.cursor()
            if not self.funcionario_existe(funcionario):
                sql = f'''INSERT INTO funcionario (nome_funcionario,sobrenome_funcionario, cpf_funcionario, telefone_funcionario, id_cargo) VALUES (?,?,?,?,?);'''
                self.cur.execute(sql,(funcionario.nome, funcionario.sobrenome, funcionario.cpf, funcionario.telefone, funcionario.get_cargo_id()))
                self.con.commit()
                return 1
            return 2
        except Exception as e:
            print(f'Erro ao inserir funcionario: {e}')
            return 3
        finally:
            self.desconectar()
    
    def delete_funcionario(self, funcionario:Funcionario):
        try:
            self.cursor()
            sql = "DELETE FROM funcionario WHERE id_funcionario = ?"
            self.cur.execute(sql, (funcionario.id, ))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao deletar funcionario: {e}')
        finally:
            self.desconectar
  
    def atualizar_funcionario(self, funcionario:Funcionario):
        try:
            self.cursor()
            sql = "UPDATE funcionario SET nome_funcionario = ?, sobrenome_funcionario= ?, telefone_funcionario = ?, id_cargo = ? WHERE id_funcionario = ?"
            self.cur.execute(sql, (funcionario.nome, funcionario.sobrenome,funcionario.telefone,funcionario.get_cargo_id(), funcionario.id))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao atualizar funcionario: {e}')
        finally:
            self.desconectar
  
    def select_all_funcionarios(self):
        try:
            self.cursor()
            sql = '''SELECT * FROM funcionario'''
            return [Funcionario(x[0], x[1], x[2], x[3], x[4], cargoDAO().select_cargo_id(x[5])) for x in self.cur.execute(sql).fetchall()]
        except Exception as e:
            print(f'Erro query select all funcionarioes: {e}')
        finally:
            self.desconectar()
    
    def select_id_funcionario(self, id:int):
        try:
            self.cursor()
            sql = '''SELECT * FROM funcionario WHERE id_funcionario = ?'''
            result = self.cur.execute(sql, (id, )).fetchall()
            if result:
                return Funcionario(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], cargoDAO().select_cargo_id(result[0][5]))
        except Exception as e:
            print(f'Erro query select all funcionarioes: {e}')
        finally:
            self.desconectar()
    def select_funcionario_cpf(self, funcionario:Funcionario):
        try:
            self.cursor()
            sql = '''SELECT * FROM funcionario WHERE cpf_funcionario = ?;'''
            return self.cur.execute(sql, (funcionario.cpf,)).fetchone()
        except Exception as e:
            print(f'Erro query select funcionario: {e}')
            self.desconectar()
        
    def select_like_funcionario(self, nome:str):
        try:
            self.cursor()
            if nome:
                sql = '''SELECT * FROM funcionario WHERE nome_funcionario LIKE ?;'''
                return [Funcionario(x[0], x[1], x[2], x[3], x[4], cargoDAO().select_cargo_id(x[5])) for x in self.cur.execute(sql, (nome+'%', )).fetchall()]
        except Exception as e:
            print(f'Erro query select like funcionario: {e}')
        finally:
            self.desconectar    
    
    def funcionario_existe(self, funcionario : Funcionario ):
        if self.select_funcionario_cpf(funcionario):
            return True
        return False