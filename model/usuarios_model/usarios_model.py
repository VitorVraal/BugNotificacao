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

def listar_usarios():
    try: 
        db = conectar()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM usuario')
        usuario = cursor.fetchall()
        return usuario
    except Exception as e:
        print(f'Erro ao listar usuários: {e}')
        return []
    finally:
        if db.is_connected():
            db.close()

def buscar_usuario_por_email(email_usuario):
    try:
        db = conectar()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuario WHERE email_usuario = %s', (email_usuario,))
        usuario = cursor.fetchone()
        return usuario
    except Exception as e:
        print(f"Erro ao buscra usuário por email: {e}")
        return None
    finally:
        if db.is_connected():
            db.close()

def criar_usuario