from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from mysql.connector import Error
from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol
from model.produtos_model.modules_produtos_model.pdf_reader import read_pdf
from model.produtos_model.modules_produtos_model.email_data_extractor import read_email_data, baixar_anexos_pdf

def CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO):
    try:
        qtde_estoque_int = int(QTDE_ESTOQUE)
    except ValueError:
        print(f"Valor inválido para QTDE_ESTOQUE: {QTDE_ESTOQUE}")
        return False, 'QTDE_ESTOQUE inválido'    
    
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL CADASTRAR_PRODUTO_ESTOQUE(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO)
        print("Valores enviados para procedure:", values)
        cursor.execute(command, values)
        conn.commit()
        return True, 'sucesso'
    except Exception as e:
        print(f"Erro ao inserir produto: {e}")
        return False, 'fracassado'
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()


def LISTAR_PRODUTOS():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("LISTAR_PRODUTOS")   
        produtos = []
        for result in cursor.stored_results():
            produtos.extend(result.fetchall())

        cursor.close()
        conn.close()
        return produtos
    except Error as error:
        print(f"Erro ao listar produtos: {error}")
        return []
# print(LISTAR_PRODUTOS())

def PROCURAR_PRODUTO_NOME(NOME_PRODUTO):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL PROCURAR_PRODUTO_NOME(%s)"
        values = (NOME_PRODUTO,)
        cursor.execute(command, values)
        resultados = cursor.fetchall()
        return True, resultados
    except Exception as e:
        return False, f"Erro ao procurar produto por nome: {e}"
    finally:
        if cursor:
            cursor.close()
        if db:
            conn.close()



def ATUALIZAR_PRODUTO(
    p_id_estoque_upd=None, p_categoria_estoque_upd=None, p_qtde_estoque_upd=None,     
    p_id_produto_upd=None, p_nome_produto_upd=None, p_preco_produto_upd=None,    
    p_desc_produto_upd=None, p_numero_nf_produto_upd=None,
    p_validade_produto_upd=None, p_fornecedor_produto_upd=None,
    p_qtd_minima_produto_upd=None
):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    if conn is None:
        print(f"Erro de conexão: {msg}")
        return False, f"Falha na conexão: {msg}"
    try:
        cursor = conn.cursor()
        command = "CALL ATUALIZAR_ESTOQUE_PRODUTO(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            p_id_estoque_upd,
            p_categoria_estoque_upd,
            p_qtde_estoque_upd,
            p_id_produto_upd,
            p_nome_produto_upd,
            p_preco_produto_upd,
            p_desc_produto_upd,
            p_numero_nf_produto_upd,
            p_validade_produto_upd,
            p_fornecedor_produto_upd,
            p_qtd_minima_produto_upd
        )
        cursor.execute(command, values)
        conn.commit()
        return True, 'sucesso'
    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        return False, 'fracassado'
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


#area de teste
# sucesso, msg = ATUALIZAR_PRODUTO(
#     p_id_estoque_upd=2, # ID do estoque
#     # p_tipo_estoque_upd="Estoqe Principal Novo", 
#     p_tipo_estoque_upd="Estoque Principal Novo", 


#     p_qtde_estoque_upd=500 
# )
# # Todo os outros parâmetros de produto ficarão como None
# sucesso, msg = ATUALIZAR_PRODUTO(
#     p_id_produto_upd=2,# ID do produto que você quer atualizar
#     p_nome_produto_upd="Cadeira Gamer PRO",
#     p_preco_produto_upd=799.99,
#     p_desc_produto_upd="Cadeira ergonômica com ajuste total",
#     p_numero_nf_produto_upd="NF-CADEIRA-002"
# )
# print(f"Resultado atualização produto: {msg}")
# print(f"Resultado atualização estoque: {msg}")



def EXCLUIR_PRODUTO_GERAL(ID_ESTOQUE):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "CALL EXCLUIR_ESTOQUE_PRODUTOS(%s)"
        values = (ID_ESTOQUE,)
        cursor.execute(command, values)
        conn.commit()
        print(f"ESTOQUE '{ID_ESTOQUE}' excluído com sucesso")
        return True, 'ESTOQUE excluído'
    except Exception as e:
        print(f"Erro ao remover ESTOQUE: {e}")
        return False, str(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def coleta_de_dados_email():
    try:
        if read_email_data():
            emitente, nome_produto, tipo_produto, descricao_produto, qtde_produto, preco_produto_float, numero_nota = read_pdf()
            try:
                CADASTRAR_PRODUTO_ESTOQUE(nome_produto, preco_produto_float, descricao_produto, tipo_produto, qtde_produto, numero_nota )
            except Error as err:
                print(f'{err}')
        else:
            print('n')
    except:
        print("erro ao buscar no email")
        
def diminuir_estoque(produto_id: int, quantidade: int):
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        command = "UPDATE ESTOQUE SET QTDE_ESTOQUE = QTDE_ESTOQUE - %s WHERE ID_ESTOQUE = (SELECT FK_ID_ESTOQUE FROM PRODUTOS WHERE ID_PRODUTO = %s)"
        cursor.execute(command, (quantidade, produto_id))
        conn.commit()
        return True, "Estoque atualizado"
    except Exception as e:
        return False, f"Erro ao atualizar estoque: {e}"
    finally:
        cursor.close()
        conn.close()

