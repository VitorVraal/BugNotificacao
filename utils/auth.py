from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

SECRET_KEY = "g464g6f84gg84x64gfdxgg8h486h468ty46h8t4t8f4g6d4g8f68dgf46gd8f4"
ALGORITHM = "HS256"
EXPIRE_DAYS = 7

app = FastAPI()

security = HTTPBearer()  # Define o esquema Bearer token

def criar_token(dados: dict):
    dados_copy = dados.copy()
    expiracao = datetime.utcnow() + timedelta(days=EXPIRE_DAYS)
    dados_copy.update({"exp": expiracao})
    return jwt.encode(dados_copy, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# Função para extrair e validar o token do header Authorization
def pegar_usuario(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials  # token puro extraído do header
    payload = verificar_token(token)
    if payload is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
