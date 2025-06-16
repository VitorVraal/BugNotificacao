from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from mysql.connector import Error
from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol

def cadastrar_usuario(EMAIL_USUARIO, SENHA_USUARIO):
    """
    Função de cadastrar usuario.
    Recebe parâmentros de email e senha para o cadastro no banco
    """


    """
    Pega as configurações do banco de um arquivo .env 
    Usando o método "get.dotenv" da classe localizada no arquivo "db_model" da pasta "database/db_model.py".
    """
    config = DBModel.get_dotenv() #Pega as configurações do banco
    db = MySqlConnector(config) # Cria o conector MySQL.
    conn, msg = db.connection() # Conecta ao banco.

    #Tenta realizar uma operação no banco
    try:
        cursor = conn.cursor()
        #Chama procedure de "cadastrar usuarios no banco de dados"
        command = "CALL CADASTRAR_USUARIO(%s, %s)"
        values = ( EMAIL_USUARIO, SENHA_USUARIO)#define valores da a serem aplicados no comando da procedure
        cursor.execute(command, values) #executa comando com os valores
        conn.commit() #realiza um commit para aplicar alterações no banco de dados
        return True #retorna True se funcionar
    except Exception as e: #caputra um erro caso não seja aplicada a alteração
        raise Exception(f"Erro ao cadastrar usuário: {e}") #menssagem de erro e seu erro 
    finally:
        #garante a finalização da sessão de e conexão com com banco 
        if cursor:
            cursor.close()
        if db:
            conn.close()

def excluir_usuario_id(ID_USUARIO):
    """
    Função de exclusão de usuario.
    Recebe Id do usuário à ser excluida
    """
    config = DBModel.get_dotenv() #Pega as configurações do banco
    db = MySqlConnector(config) # Cria o conector MySQL.
    conn, msg = db.connection() # Conecta ao banco.

    #Tenta realizar uma operação no banco
    try:
        cursor = conn.cursor()  # Prepara o "cursor" para enviar comandos SQL.
        command = "CALL EXCLUIR_USUARIO_ID(%s)" #prepara procedure presente no banco de dados para receber os valores e ser executado
        values = (ID_USUARIO,) #valores à serem aplicados nessa procedure de exclusão 
        """
        Obs:
        Em Python, a virgula presente após a varivel é o que faz com que o (ID_USUARIO,) 
        Seja reconhecido como uma tupla de um único elemento, e não apenas como um valor dentro de parênteses.
        """
        cursor.execute(command, values) #executa a procedure e os valores
        conn.commit() #commit para aplicar alterações
        return {"message": "Usuário excluído com sucesso."} #retorna menssagem de sucesso caso consiga excluir usuario
    except Exception as e:
        """
        qualquer erro que houver, cria e retorna um dicionário Python. 
        chave: erro, valor: menssagem de erro e seu erro
        """
        return {"error": f"Erro ao excluir usuário: {e}"} 
        
    finally:
        #garante finalização da sessão e sua conexão
        if cursor:
            cursor.close()
        if db:
            conn.close()

def alterar_usuario(ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO):
    """
    Função de alteração de usuário.
    Recebe como parâmentro "ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO" para realizar a alteração
    """
    config = DBModel.get_dotenv()  #Pega as configurações do banco
    db = MySqlConnector(config)# Cria o conector MySQL.
    conn, msg = db.connection()# Conecta ao banco.

    #Tenta realizar uma operação no banco
    try:
        cursor = conn.cursor() #cria um "cursor" para realizar procedimentos no banco de dados
        command = "CALL ALTERAR_USUARIO(%s, %s, %s)" #chama procedure de alterar usuarios
        values = (ID_USUARIO, EMAIL_USUARIO, SENHA_USUARIO) # define os valores à serem aplicados nos campos da procedure (" %s ")
        cursor.execute(command, values) # executa procedure com os valores definidos
        conn.commit()  #commit para aplicar alterações

        """
        Caso consiga executar e realiar o commit, cria e retorna um dicionário Python. 
        chave: message, valor: Usuário alterado com sucesso.
        """
        return {"message": "Usuário alterado com sucesso."} 
    except Exception as e:
        """
        qualquer erro que houver, cria e retorna um dicionário Python. 
        chave: error, valor: Erro ao alterar usuário: 
        """
        return {"error": f"Erro ao alterar usuário: {e}"}
    finally:
        #garante a finalização da sessão e da conexão com o banco de dados
        if cursor:
            cursor.fetchall()
            cursor.close()
        if conn:
            conn.close()

def listar_usuarios():
    """
    Função listar usuarios.
    Não recebe parâmetros de entrada.
    """
    config = DBModel.get_dotenv() # Pega as configurações do banco
    db = MySqlConnector(config)# Cria o conector MySQL.
    conn, msg = db.connection()# Conecta ao banco.
    
    #Tenta realizar uma operação no banco
    try:
        cursor = conn.cursor(dictionary=True) # Prepara o cursor para retornar resultados como dicionário.
        cursor.callproc("LISTAR_USUARIOS")
        
        usuarios = []
        for result in cursor.stored_results():
            usuarios.extend(result.fetchall())

        cursor.close()
        conn.close()
        return usuarios
    except Error as error:
        
        return []


def fazer_login(EMAIL_USUARIO, SENHA_USUARIO):

    """
    Função de realizar login no sistema
    Recebe como parâmetros: " EMAIL_USUARIO, SENHA_USUARIO "
    """
    config = DBModel.get_dotenv() # Pega as configurações do banco
    db = MySqlConnector(config) # Cria o conector MySQL.
    conn, msg = db.connection() # Conecta ao banco.

    #Tenta realizar uma operação no banco
    try:
        cursor = conn.cursor(dictionary=True) # Prepara o cursor para retornar resultados como dicionário.

        """
        Forma direta de executar a procedure de login no sistema.
        Aplicação dos parâmetros direto na procedure
        parâmetros -> procedure -> exec
        """
        cursor.execute("CALL FAZER_LOGIN(%s, %s)", (EMAIL_USUARIO, SENHA_USUARIO))  #executa procedure com seus valores(parâmetros)
        result = cursor.fetchone() #coleta resultado da procedure em um variável

        #verificação
        #Caso o resultado(results) e a menssagem de resposta seja devolvida da procedure seja igual a:
        # "Login realizado com sucesso!"
        if result and result.get("MENSAGEM") == "Login realizado com sucesso!":
            # Se o login deu certo, retorna um dicionário com o ID e e-mail do usuário.
            return {
                "user": {
                    "id": result["ID_USUARIO"],
                    "email": result["EMAIL_USUARIO"]
                }
            }
        else:
            # Se a mensagem não for de sucesso, o login é inválido.
            return None  # Login inválido

    except Exception as e:
        print(f"Erro ao fazer login: {e}")
        return None
    finally:
        # garante que o cursor e a conexão sejam sempre fechados.
        if cursor:
            cursor.close()
        if db:
            conn.close()

