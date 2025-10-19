from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# int() = Transformando em inteiro os minutos - Todas as variaveis são string

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt", "sha256_crypt"], deprecated="auto")
# oath2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")
oath2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

from routes_auth import router_auth
from routes_order import router_order

app.include_router(router_auth)
app.include_router(router_order)



# para rodar o nosso código, executar no terminal: uvicorn main:app --reload