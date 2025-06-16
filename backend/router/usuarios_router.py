from fastapi import APIRouter, HTTPException, Request # Ferramentas do FastAPI para criar rotas, lidar com erros HTTP e requisitar.
from pydantic import BaseModel, EmailStr # Pydantic para criar modelos de dados e validar strings de e-mail.
from typing import List  # Para definir tipos como listas.


# Importa as funções de "controller" de usuários, que lidam com a lógica de negócio e o banco de dados.
from controller.usuarios_controller.usuarios_controller import (
    criar_usuario_controller,
    listar_usuarios_controller,
    deletar_usuario_controller,
    atualizar_usuario_controller,
    fazer_login_controller
)
from utils.auth import criar_token

# Cria um roteador do FastAPI. Ele agrupa rotas relacionadas a usuários.
router = APIRouter()



            # Modelos de Dados (Pydantic) um bom soldado, faz oq tem q fazer 
# Essas classes definem como os dados dos usuários devem parecer
# quando a API os recebe ou envia.
class Usuario(BaseModel):
    """
    Modelo: Representa os dados para "criar" um novo usuário.
    Atributos:
        email_usuario (EmailStr): O e-mail do usuário (validado como e-mail).
        senha_usuario (str): A senha do usuário.
    """
    email_usuario: EmailStr
    senha_usuario: str

class UsuarioUpdate(BaseModel):
    """
    Modelo: Representa os dados para "atualizar" um usuário existente.
    Atributos:
        id_usuario (int): O ID do usuário a ser atualizado.
        email_usuario (EmailStr): O novo e-mail do usuário (validado como e-mail).
        senha_usuario (str): A nova senha do usuário.
    """
    id_usuario: int
    email_usuario: EmailStr
    senha_usuario: str

class Login(BaseModel):
    """
    Modelo: Representa os dados para realizar o ""login".
    Atributos:
        email_usuario (EmailStr): O e-mail do usuário para login.
        senha_usuario (str): A senha do usuário para login.
    """
    email_usuario: EmailStr
    senha_usuario: str

@router.post("/usuarios", status_code=201)
def criar_usuario(usuario: Usuario):
    """
    Função: Cria um novo usuário no sistema.
    Recebe parâmetros:
        usuario (Usuario): Os dados do novo usuário (email e senha).
    Detalhes:
    - Chama a função `criar_usuario_controller` para fazer o cadastro.
    """
    try:
        criar_usuario_controller(
            usuario.email_usuario,
            usuario.senha_usuario
        )
        #Retorna uma mensagem de sucesso ou um erro HTTP 400 se algo der errado.
        return {"mensagem": "Usuário cadastrado com sucesso."}
    except Exception as e:
        # Se houver qualquer erro no processo de cadastro, retorna um erro HTTP 400.
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usuarios", response_model=List[dict])
def listar():
    """
    Função: Lista todos os usuários cadastrados no sistema.
    Recebe parâmetros: Nenhum.
    Detalhes:
    - Chama a função `listar_usuarios_controller` para buscar os usuários no banco.
    - Retorna uma lista de dicionários, onde cada dicionário representa um usuário.
    """
    return listar_usuarios_controller()

@router.delete("/usuarios/{id}")
def deletar_usuario(id: int):
    """
    Função: Deleta um usuário específico pelo ID.
    Recebe parâmetros:
        id (int): O ID do usuário a ser excluído.
    Detalhes:
    - Chama a função `deletar_usuario_controller` para remover o usuário do banco.
    - Retorna uma mensagem de sucesso.
    """
    deletar_usuario_controller(id)
    return {"mensagem": f"Usuário com ID {id} excluído com sucesso."}

@router.put("/usuarios")
def atualizar(usuario: UsuarioUpdate):
    """
    Função: Atualiza as informações (e-mail e senha) de um usuário existente.
    Recebe parâmetros:
        usuario (UsuarioUpdate): Os dados atualizados do usuário, incluindo o ID.
    Detalhes:
    - Chama a função `atualizar_usuario_controller` para aplicar as mudanças no banco.
    - Retorna uma mensagem de sucesso.
    """
    atualizar_usuario_controller(
        usuario.id_usuario,
        usuario.email_usuario,
        usuario.senha_usuario
    )
    return {"mensagem": f"Usuário com ID {usuario.id_usuario} atualizado com sucesso."}

@router.post("/login")
def login(dados: Login):
    """
    Função: Realiza o login de um usuário e, se as credenciais forem válidas, gera um token de acesso.
    Recebe parâmetros:
        dados (Login): As credenciais do usuário (e-mail e senha).
    Detalhes:
    - Chama a função `fazer_login_controller` para verificar as credenciais no banco.
    - Se o login for bem-sucedido, cria um token JWT (JSON Web Token) e o retorna.
    - Retorna um erro HTTP 401 (Não Autorizado) se as credenciais forem inválidas.
    """
    usuario = fazer_login_controller(dados.email_usuario, dados.senha_usuario)
    print("Usuário retornado:", usuario) # Log no terminal: mostra o que foi retornado da função de login.
    
    if not usuario:
        # Se a função de login não retornar um usuário válido, as credenciais são inválidas.
        raise HTTPException(status_code=401, detail="Credenciais inválidas.")
    
    # Verifique as chaves aqui:
    print("Chaves do usuário:", usuario.keys())
    

    # Cria um token de autenticação usando os dados do usuário.
    # Usa `.get()` com fallback para garantir que a chave exista, mesmo que o nome mude (ID_USUARIO ou id_usuario).
    token = criar_token({
        "id": usuario.get("ID_USUARIO") or usuario.get("id_usuario"),
        "email": usuario.get("EMAIL_USUARIO") or usuario.get("email_usuario")
    })
    return {"access_token": token, "token_type": "bearer"} # Retorna o token de acesso.
