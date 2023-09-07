from DAL.funcionarioDAL import Funcionario
class Usuario:
    def __init__(self, id:int, nome:str, senha:str, reset_senha:int, funcionario:Funcionario):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.reset_senha = reset_senha
        self.funcionario = funcionario
        
    def get_funcionario_id(self):
        return self.funcionario.id
    
    def get_nome_completo(self):
        return f'{self.funcionario.nome} {self.funcionario.sobrenome}'
    