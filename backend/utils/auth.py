from datetime import datetime, timedelta # Para trabalhar com datas e tempos.
from jose import JWTError, jwt # Biblioteca para lidar com JSON Web Tokens.
from fastapi import FastAPI, Depends, HTTPException, status, Security # Ferramentas do FastAPI para API, dependências, erros HTTP e segurança.
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials # Para implementar segurança baseada em token Bearer.
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED # Códigos de status HTTP para erros comuns de autenticação.


"""
SECRET_KEY: "CHAVE SECRETA": Usada para assinar e verificar tokens. Mantenha-a segura e não a exponha!
ALGORITHM: O algoritmo de criptografia usado para assinar o token (HMAC com SHA-256).
EXPIRE_DAYS: Quantos dias o token será válido a partir da sua criação.
"""
SECRET_KEY = "g464g6f84gg84x64gfdxgg8h486h468ty46h8t4t8f4g6d4g8f68dgf46gd8f4"
ALGORITHM = "HS256"
EXPIRE_DAYS = 7

app = FastAPI()

security = HTTPBearer()  # Define  esquema de segurança HTTP Bearer para ser usado nas rotas.

def criar_token(dados: dict):
    """
    Função: Cria um novo token JWT a partir de um dicionário de dados.
    Recebe parâmetros:
        dados (dict): Um dicionário contendo as informações que você quer guardar no token (ex: ID do usuário, e-mail).
    Detalhes:
    - Adiciona uma data de expiração ao token (7 dias a partir de agora).
    - Codifica os dados usando a chave secreta e o algoritmo definidos.
    - O token gerado pode ser usado para autenticar requisições futuras.
    """
    dados_copy = dados.copy() # Cria uma cópia dos dados para não modificar o dicionário original.
    expiracao = datetime.utcnow() + timedelta(days=EXPIRE_DAYS) # Calcula a data de expiração do token.
    dados_copy.update({"exp": expiracao}) # Adiciona a data de expiração aos dados do token.
    return jwt.encode(dados_copy, SECRET_KEY, algorithm=ALGORITHM) # Codifica os dados no token JWT.

def verificar_token(token: str):
    """
    Função: Verifica a validade de um token JWT.
    Recebe parâmetros:
        token (str): A string do token JWT a ser verificada.
    Detalhes:
    - Tenta decodificar o token usando a chave secreta e o algoritmo.
    - Se o token for válido e não estiver expirado, retorna o payload (os dados originais).
    - Se o token for inválido (corrompido, expirado, chave errada), retorna None.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # Decodifica o token.
        return payload
    except JWTError: # Captura qualquer erro relacionado ao JWT (token inválido, expirado, etc.).
        return None # Retorna None se o token for inválido.

# Função para extrair e validar o token do header Authorization
def pegar_usuario(credentials: HTTPAuthorizationCredentials = Security(security)):

    
    #apagar esse comentário: "Lá ele... pegar o usário? XDXD"


    """
    Função: Extrai e valida o token JWT do cabeçalho 'Authorization' de uma requisição HTTP.
    Recebe parâmetros:
        credentials (HTTPAuthorizationCredentials): Objeto que o FastAPI injeta, contendo as credenciais de autorização (o token Bearer).
    Detalhes:
    - Esta função é projetada para ser usada como uma **dependência** em rotas do FastAPI (com `Depends` ou `Security`).
    - Ela obtém o token do cabeçalho "Authorization: Bearer <token>".
    - Valida o token usando `verificar_token`.
    - Se o token for inválido ou ausente, levanta uma `HTTPException` (erro 401 Unauthorized), impedindo o acesso à rota.
    - Se o token for válido, retorna o payload (os dados do usuário contidos no token).
    """
    token = credentials.credentials  # token puro extraído do header
    payload = verificar_token(token) # Tenta verificar o token.
    if payload is None:   # Se o token for inválido (retornou None de verificar_token)
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"}, # Cabeçalho padrão para indicar o tipo de autenticação.
        )
    return payload # Retorna o payload do token se for válido.
