from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]
    
    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):
    id_usuario: int
    
    class Config:
        from_attributes = True
    
    
class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True
    

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    
    class Config:
        from_attributes = True

# Personalizar os dados que vão aparecer
class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    
    class Config:
        from_attributes = True
    
    

# Pydantic - Força a tipagem de dados
# class UsuarioSchema - Padrão de informações que quero que seja enviado para o sistema

# É adicionado no Swagger como deve ser enviado as informações
# Quando clica em Try it out para testar, basta apenas editar as informações
# Dessa forma evita erro e fica na documentação como deve ser os dados