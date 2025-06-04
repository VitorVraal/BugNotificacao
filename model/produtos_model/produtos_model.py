import mysql.connector
from mysql.connector import Error

def conectar():
    return mysql.connector.connect(host='localhost', user='root', password='', database='db')

def CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE):
    db = conectar()

    try:
        cursor = db.cursor()
        command = "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s)"
        values = (NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE)
        cursor.execute(command, values)
        db.commit()
        return True, 'sucesso'
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
        return False, 'fracassado'
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def LISTAR_PRODUTOS():
    try:
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("LISTAR_PRODUTOS")
        
        produtos = []
        for result in cursor.stored_results():
            produtos.extend(result.fetchall())

        cursor.close()
        conn.close()
        return produtos
    except mysql.connector.Error as error:
        return []



def PROCURAR_PRODUTO_ID(ID_PRODUTO):
    db = conectar()

    try:
        cursor = db.cursor()
        command = "CALL PROCURAR_PRODUTO_ID(%s)"
        values = (ID_PRODUTO,)
        cursor.execute(command, values)
        resultados = cursor.fetchall()
        return True, resultados
    except Exception as e:
        return False, f"Erro ao procurar produto: {e}"
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def ATUALIZAR_PRODUTO(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO):
    db = conectar()

    try:
        cursor = db.cursor()
        command = "CALL ATUALIZAR_PRODUTO(%s, %s, %s, %s, %s, %s)"
        values = (NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO)
        cursor.execute(command, values)
        db.commit()
        return True, 'sucesso'

    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        return False, 'fracassado'

    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if db:
            db.close()

def EXCLUIR_PRODUTO_GERAL(ID_PRODUTO):
    db = conectar()

    try:
        cursor = db.cursor()
        command = "CALL EXCLUIR_PRODUTO_GERAL(%s)"
        values = (ID_PRODUTO,)
        cursor.execute(command, values)
        db.commit()
        print(f"Produto '{ID_PRODUTO}' excluído com sucesso")
        return True, 'produto excluído'
    
    except Exception as e:
        print(f"Erro ao remover produto: {e}")
        return False, 'fracassado'
    
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

