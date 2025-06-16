from database.db_mysql import MySqlConnector
from database.db_model import DBModel
from model.produtos_model.produtos_model import inserir_atividade

VERIFICAR_NOTIFICACOES_ESTOQUE = """
SELECT 
    p.ID_PRODUTO,
    p.NOME_PRODUTO,
    e.QTDE_ESTOQUE,
    p.QTD_MINIMA_PRODUTO,
    p.VALIDADE_PRODUTO,
    DATEDIFF(p.VALIDADE_PRODUTO, CURDATE()) AS DIAS_PARA_VENCER
FROM PRODUTOS p
JOIN ESTOQUE e ON p.FK_ID_ESTOQUE = e.ID_ESTOQUE
WHERE e.QTDE_ESTOQUE <= p.QTD_MINIMA_PRODUTO
OR DATEDIFF(p.VALIDADE_PRODUTO, CURDATE()) <= %s
"""

def get_notificacoes_estoque_controller(user_id, limite_baixo=10, dias_validade=3):
    try:
        config = DBModel.get_dotenv()
        db = MySqlConnector(config)
        connection, msg = db.connection()

        if not connection:
            return False, f"Erro na conexão com o banco: {msg}"

        cursor = connection.cursor(dictionary=True)

        # Verificar notificações já lidas por este usuário
        cursor.execute(
            "SELECT ID_NOTIFICACAO FROM NOTIFICACOES_LIDAS WHERE ID_USUARIO = %s",
            (user_id,)
        )
        lidas = {row['ID_NOTIFICACAO'] for row in cursor.fetchall()}

        # Buscar produtos com estoque baixo
        cursor.callproc("LISTAR_PRODUTOS_ESTOQUE_BAIXO", [limite_baixo])
        produtos_baixo_estoque = list(cursor.stored_results())[0].fetchall()

        # Buscar produtos próximos da validade
        cursor.callproc("LISTAR_PRODUTOS_PROXIMOS_VALIDADE", [dias_validade])
        produtos_prox_validade = list(cursor.stored_results())[0].fetchall()

        notificacoes = []

        # Processar notificações de estoque baixo
        for produto in produtos_baixo_estoque:
            notif_id = f"estoque_{produto['ID_PRODUTO']}"
            if notif_id not in lidas:
                notificacoes.append({
                    "id": notif_id,
                    "title": "Estoque Baixo",
                    "message": f"Produto {produto['NOME_PRODUTO']} está com estoque baixo ({produto['QTDE_ESTOQUE']} unidades)",
                    "type": "baixo-estoque"
                })
                
                inserir_atividade(
                    tipo="Alerta",
                    descricao=f"Produto '{produto['NOME_PRODUTO']}' com estoque baixo ({produto['QTDE_ESTOQUE']} unidades).",
                    quantidade=produto['QTDE_ESTOQUE']
                )                

        # Processar notificações de validade
        for produto in produtos_prox_validade:
            notif_id = f"validade_{produto['ID_PRODUTO']}"
            if notif_id not in lidas:
                notificacoes.append({
                    "id": notif_id,
                    "title": "Validade Próxima",
                    "message": f"Produto {produto['NOME_PRODUTO']} vence em {produto['DIAS_PARA_VENCER']} dias ({produto['VALIDADE_PRODUTO']})",
                    "type": "validade"
                })
                
                inserir_atividade(
                    tipo="Alerta",
                    descricao=f"Produto '{produto['NOME_PRODUTO']}' vence em {produto['DIAS_PARA_VENCER']} dias.",
                    quantidade=0
                )            

        return True, notificacoes

    except Exception as e:
        return False, str(e)
    finally:
        if 'connection' in locals() and connection:
            connection.close()

def marcar_como_lida_controller(user_id, notificacao_id, produto_id):
    try:
        config = DBModel.get_dotenv()
        db = MySqlConnector(config)
        connection, msg = db.connection()

        if not connection:
            return False, f"Erro na conexão com o banco: {msg}"

        cursor = connection.cursor()

        # Verificar se o produto existe
        cursor.execute("SELECT ID_PRODUTO FROM PRODUTOS WHERE ID_PRODUTO = %s", (produto_id,))
        if not cursor.fetchone():
            return False, "Produto não encontrado"

        # Verificar se a notificação é válida
        if not (notificacao_id.startswith("estoque_") or notificacao_id.startswith("validade_")):
            return False, "Tipo de notificação inválido"

        # Marcar como lida
        cursor.execute(
            "INSERT INTO NOTIFICACOES_LIDAS (ID_NOTIFICACAO, ID_USUARIO) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE DATA_LEITURA = CURRENT_TIMESTAMP",
            (notificacao_id, user_id)
        )
        connection.commit()
        return True, "Notificação marcada como lida"

    except Exception as e:
        return False, str(e)
    finally:
        if 'connection' in locals() and connection:
            connection.close()