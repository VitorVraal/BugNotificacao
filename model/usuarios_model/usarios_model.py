import mysql.connector

def conectar():
    return mysql.connector.connect(host='localhost', user='root', password='', database='db')

def criar_tabela():
    db = conectar()
    cursor = db.cursor()
    cursor.execute('''
    create table IF NOT EXISTS USUARIO(
	ID_USUARIO INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
    NOME_USUARIO VARCHAR(255),
    EMAIL_USUARIO VARCHAR(255) NOT NULL UNIQUE,
    SENHA_USUARIO VARCHAR(255) NOT NULL,
    TIPO_CONTA INT,
    DATA_CADASTRO DATE DEFAULT NULL,
    DATA_ATUALIZACAO DATE DEFAULT NULL,
    CONSTRAINT CHK_SENHA_TAMANHO CHECK (LENGTH(SENHA_USUARIO) >= 3),
    CONSTRAINT CHK_TIPO_CONTA CHECK (TIPO_CONTA IN (1, 2, 3))
    );        
    ''')
    db.commit()
    db.close()

def cadastrar_usuario(NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO, TIPO_CONTA):
    try:
        db = conectar()
        cursor = db.cursor()
        command = "CALL CADASTRAR_USUARIO(%s, %s, %s, %s)"
        values = (NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO, TIPO_CONTA)
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")
    finally:
        if db.is_connected():
            db.close()

def excluir_usuario_id(ID_USUARIO):
    try:
        db = conectar()
        cursor = db.cursor()
        command = "CALL EXCLUIR_USUARIO_ID(%s)"
        values = (ID_USUARIO,)
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
    finally:
        if db.is_connected():
            db.close()

def alterar_usuario(ID_USUARIO, NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO):
    try:
        db = conectar()
        cursor = db.cursor()
        command = "CALL ALTERAR_USUARIO(%s, %s, %s, %s)"
        values = (ID_USUARIO, NOME_USUARIO, EMAIL_USUARIO, SENHA_USUARIO)
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao alterar usuário: {e}")
    finally:
        if db.is_connected():
            db.close()

def listar_usarios():
    try:
        db = conectar()
        cursor = db.cursor()
        command = "CALL LISTAR_USUARIOS()"
        values = ()
        cursor.execute(command, values)
        db.commit()
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
    finally:
        if db.is_connected():
            db.close()

def fazer_login(EMAIL_USUARIO, SENHA_USUARIO):
    try:
        db = conectar()
        cursor = db.cursor()
        command = "CALL FAZER_LOGIN(%s, %s)"
        values = (EMAIL_USUARIO, SENHA_USUARIO)
        cursor.execute(command, values)
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Erro ao fazer login: {e}")
    finally:
        if db.is_connected():
            db.close()