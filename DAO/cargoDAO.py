from DAO.db import DataBase
from DAL.cargoDAL import Cargo
class cargoDAO(DataBase):
    def __init__(self):
        DataBase.__init__(self)
        
    def insert_cargo(self, cargo: Cargo):
        '''1 - cargo inserido com sucesso
           2 - cargo já existe
           3 - Erro no banco de dados
           '''
        try:
            self.cursor()
            if not self.cargo_existe(cargo):
                sql = f'''INSERT INTO cargo (nome_cargo) VALUES (?);'''
                self.cur.execute(sql,(cargo.nome,))
                self.con.commit()
                return 1
            return 2
        except Exception as e:
            print(f'Erro ao inserir cargo: {e}')
            return 3
        finally:
            self.desconectar()
    
    def delete_cargo(self, cargo: Cargo):
        try:
            self.cursor()
            sql = "DELETE FROM cargo WHERE id_cargo = ?"
            self.cur.execute(sql, (cargo.id, ))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao deletar cargo: {e}')
        finally:
            self.desconectar
  
    def atualizar_cargo(self, cargo: Cargo):
        try:
            self.cursor()
            sql = "UPDATE cargo SET nome_cargo = ? WHERE id_cargo = ?"
            self.cur.execute(sql, (cargo.nome, cargo.id))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao atualizar cargo: {e}')
        finally:
            self.desconectar
  
    def select_all_cargos(self):
        try:
            self.cursor()
            sql = '''SELECT * FROM cargo'''
            return [Cargo(x[0], x[1]) for x in self.cur.execute(sql).fetchall()]
        except Exception as e:
            print(f'Erro query select all cargos: {e}')
        finally:
            self.desconectar()
    
    def select_cargo_id(self, id:int):
        try:
            self.cursor()
            sql = '''SELECT * FROM cargo WHERE id_cargo = ?'''
            result = self.cur.execute(sql, (id,)).fetchall()
            if result:
                return Cargo(result[0][0], result[0][1])
            return None
        except Exception as e:
            print(f'Erro query select cargo id: {e}')
        finally:
            self.desconectar()
    def select_cargo_nome(self, cargo: Cargo):
        try:
            self.cursor()
            sql = '''SELECT * FROM cargo WHERE nome_cargo = ?;'''
            return self.cur.execute(sql, (cargo.nome, )).fetchone()
        except Exception as e:
            print(f'Erro query select cargo: {e}')
            self.desconectar()
        
    def select_like_cargo(self, nome:str):
        try:
            self.cursor()
            if nome:
                sql = '''SELECT * FROM cargo WHERE nome_cargo LIKE ?;'''
                return [Cargo(x[0], x[1]) for x in self.cur.execute(sql, (nome+'%', )).fetchall()]
        except Exception as e:
            print(f'Erro query select like cargo: {e}')
        finally:
            self.desconectar    
    
    def cargo_existe(self, cargo : Cargo ):
        if self.select_cargo_nome(cargo):
            return True
        return False