from DAL.cargoDAL import Cargo
class Funcionario:
    def __init__(self, id:int, nome:str, sobrenome:str, cpf:str, telefone:str, cargo: Cargo):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.cpf = cpf
        self.telefone = telefone
        self.cargo = cargo
        
    def get_cpf(self):
        return '{}{}{}.{}{}{}.{}{}{}-{}{}'.format(*self.cpf) if len(self.cpf)==11 else ''
    
    def get_telefone(self):
        return '({}{}) {}{}{}{}-{}{}{}{}'.format(*self.telefone) if len(self.telefone)==10 else ''
    
    def get_cargo_nome(self):
        return self.cargo.nome

    def get_cargo_id(self):
        return self.cargo.id