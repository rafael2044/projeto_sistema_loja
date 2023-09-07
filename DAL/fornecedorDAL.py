class Fornecedor:
    def __init__(self, id:int, nome:str, cnpj:str, cpf:str, endereco:str, telefone:str):
        self.id = id
        self.nome = nome
        self.cnpj = cnpj
        self.cpf = cpf
        self.endereco = endereco
        self.telefone = telefone
        
    def get_cnpj(self):
        return '{}{}.{}{}{}.{}{}{}/{}{}{}{}-{}{}'.format(*self.cnpj) if len(self.cnpj)==14 else ''

    def get_cpf(self):
        return '{}{}{}.{}{}{}.{}{}{}-{}{}'.format(*self.cpf) if len(self.cpf)==11 else ''
    
    def get_telefone(self):
        return '({}{}) {}{}{}{}-{}{}{}{}'.format(*self.telefone) if len(self.telefone)==10 else ''