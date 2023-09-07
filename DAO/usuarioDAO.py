from DAO.db import DataBase
from DAL.funcionarioDAL import Funcionario
from DAO.funcionarioDAO import funcionarioDAO
from DAO.cargoDAO import cargoDAO
from DAL.usuarioDAL import Usuario
from hashlib import sha256
class usuarioDAO(DataBase):
    def __init__(self):
        DataBase.__init__(self)
        
    def insert_usuario(self, usuario:Usuario):
        '''1 - usuario inserido com sucesso
           2 - usuario já existe
           3 - Erro no banco de dados
           '''
        try:
            self.cursor()
            if not self.usuario_existe(usuario):
                sql = f'''INSERT INTO usuario (nome_usuario,senha_usuario, reset_senha, id_funcionario) VALUES (?,?,?,?);'''
                self.cur.execute(sql,(usuario.nome, sha256(usuario.senha.encode()).hexdigest(), usuario.reset_senha, usuario.get_funcionario_id()))
                self.con.commit()
                return 1
            return 2
        except Exception as e:
            print(f'Erro ao inserir usuario: {e}')
            return 3
        finally:
            self.desconectar()
    
    def delete_usuario(self, usuario: Usuario):
        try:
            self.cursor()
            sql = "DELETE FROM usuario WHERE id_usuario = ?"
            self.cur.execute(sql, (usuario.id, ))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao deletar usuario: {e}')
        finally:
            self.desconectar
  
    def resetar_senha(self, usuario: Usuario):
        try:
            self.cursor()
            sql = "UPDATE usuario SET senha_usuario= ? WHERE id_usuario = ?"
            self.cur.execute(sql, (usuario.senha, usuario.id))
            self.con.commit()
            return True
        except Exception as e:
            print(f'Erro ao atualizar usuario: {e}')
        finally:
            self.desconectar
  
    def select_all_usuarios(self):
        try:
            self.cursor()
            sql = '''SELECT * FROM usuario'''
            return [Usuario(x[0], x[1], x[2], x[3], funcionarioDAO().select_id_funcionario(x[4])) for x in self.cur.execute(sql).fetchall()]
        except Exception as e:
            print(f'Erro query select all usuarioes: {e}')
        finally:
            self.desconectar()
            
    def select_all_funcionarios_nao_cadastrados(self):
        try:
            self.cursor()
            sql = '''SELECT * FROM funcionario AS f
                     WHERE f.id_funcionario NOT IN (SELECT id_funcionario FROM usuario);'''
            result = self.cur.execute(sql).fetchall()
            if result:
                return [Funcionario(x[0], x[1], x[2], x[3], x[4], cargoDAO().select_cargo_id(x[5])) for x in result]
        except Exception as e:
            print(f'Erro query select all usuarioes: {e}')
        finally:
            self.desconectar()    
            
    def select_usuario_nome(self, usuario: Usuario):
        try:
            self.cursor()
            sql = '''SELECT * FROM usuario WHERE nome_usuario = ?;'''
            return self.cur.execute(sql, (usuario.nome,)).fetchone()
        except Exception as e:
            print(f'Erro query select usuario: {e}')
            self.desconectar()
        
    def select_like_usuario(self, nome:str):
        try:
            self.cursor()
            if nome:
                sql = '''SELECT * FROM usuario WHERE nome_usuario LIKE ?;'''
                return [Usuario(x[0], x[1], x[2], x[3], x[4], funcionarioDAO().select_id_funcionario(x[5])) for x in self.cur.execute(sql, (nome+'%', )).fetchall()]
        except Exception as e:
            print(f'Erro query select like usuario: {e}')
        finally:
            self.desconectar    
    
    def usuario_existe(self, usuario : Usuario ):
        if self.select_usuario_nome(usuario):
            return True
        return False