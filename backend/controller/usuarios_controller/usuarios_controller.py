# Importa todas as funções de gerenciamento de usuário do seu módulo 'usuarios_model'.
# São elas: cadastrar_usuario, excluir_usuario_id, alterar_usuario, listar_usuarios, fazer_login.
from model.usuarios_model.usuarios_model import (cadastrar_usuario, excluir_usuario_id, alterar_usuario, listar_usuarios, fazer_login)
from utils.auth import criar_token # Importa a função para criar tokens de autenticação.

def criar_usuario_controller(email_usuario, senha_usuario):
    """
    Função: Controla a criação de um novo usuário.
    Recebe parâmetros: **email_usuario**, **senha_usuario**.
    """
    return cadastrar_usuario(email_usuario, senha_usuario)

def listar_usuarios_controller():
    """
    Função: Controla a listagem de todos os usuários.
    Recebe parâmetros: Nenhum.
    Simplesmente chama a função que busca todos os usuários no banco.
    """
    return listar_usuarios()

def deletar_usuario_controller(id_usuario):
    """
    Função: Controla a exclusão de um usuário.
    Recebe parâmetros: **id_usuario**.
    Pega o ID do usuário e passa para a função que o remove do banco.
    """
    return excluir_usuario_id(id_usuario)

def atualizar_usuario_controller(id_usuario,email_usuario, senha_usuario):
    """
    Função: Controla a atualização dos dados de um usuário.
    Recebe parâmetros: **id_usuario**, **email_usuario**, **senha_usuario**.
    Pega o ID e os novos dados e passa para a função que atualiza no banco.
    
    """
    return alterar_usuario(id_usuario,email_usuario, senha_usuario)

def fazer_login_controller(email_usuario, senha_usuario):
    """
    Função: Controla o processo de login do usuário e a criação de token de acesso.
    Recebe parâmetros: **email_usuario**, **senha_usuario**.
    
    Verifica as credenciais e, se o login for válido, cria um token de acesso para o usuário.
    """
    usuario = fazer_login(email_usuario, senha_usuario) # Tenta fazer o login no banco.


    # Se o login for bem-sucedido e a resposta contiver os dados do usuário:
    if usuario and "user" in usuario:
        dados = {
            "sub": str(usuario["user"]["id"]), # O ID do usuário (como string) para o token.
            "email_usuario": usuario["user"]["email"] # O email do usuário para o token.
        }
        token = criar_token(dados) # Cria o token de autenticação com os dados do usuário.
        return {
            "access_token": token, # O token de acesso gerado.
            "token_type": "bearer", # O tipo do token (padrão para tokens de acesso).
            "usuario": dados  # Os dados do usuário incluídos no token.
        }
    return None # Retorna None se o login falhar ou as credenciais forem inválidas.


