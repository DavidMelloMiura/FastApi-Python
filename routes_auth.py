from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

router_auth = APIRouter(prefix="/auth", tags=["auth"])


# Criar Token
def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    # JWT
    # id_usuario
    # data_expiracao
    # token = f"fdartadaafga{id_usuario}"
    return jwt_codificado



def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario



@router_auth.get("/")
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "Voccê acessou a rota de autenticacao", "autenticado": False}



@router_auth.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
# async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):
   
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        #já existe um usuario com esse email
        # return {"Mensagem": "Já existe um usuário com esse email"}
        raise HTTPException(status_code=400, detail="Email do usuário ja cadastrado")
    else:
        # senha_segura = senha[:70].encode('utf-8')
        # senha_criptografada = bcrypt_context.hash(senha_segura)
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"Mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}




# login  -. email e senha -> tohen JWT (Json Web Token)
@router_auth.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    # usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
        # JWT Bearer
        # headers: {"Access-Token": "Bearer token"}
        
        
#  Logon por meio do form do FastAPI (Swagger) botão Authorize
# OAuth2PasswordBearer (OAuth2, password)
@router_auth.post("/login-form")
async def login_from(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    # usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
        # JWT Bearer
        # headers: {"Access-Token": "Bearer token"}
        
        
        
        
        
        
        
        
        
        
@router_auth.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    # verificar o token
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
        }