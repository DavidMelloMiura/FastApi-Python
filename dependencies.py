from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from main import oath2_schema


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        # return session
        yield session # yield retona valor mas não encerra a execução como o return faz
    finally: # Independente se der erro ou não nas linhas acima o finally encerrará a session
        session.close()
    
    # Dessa forma retorna a session e logo após fecha a session
    
    

def verificar_token(token: str = Depends(oath2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Acesso Negado, Verifique a validade do token")
    # verificar de o token é valido
    # estrair o ID do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario


# header
# OAuth2 - Enviado no header
# Access-token: Bearer numerotoken