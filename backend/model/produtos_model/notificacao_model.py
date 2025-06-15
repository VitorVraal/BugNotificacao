from database.db_mysql import MySqlConnector  # Ferramenta que realmente faz a conexão com o MySQL.
from database.db_model import DBModel

def VERIFICAR_NOTIFICACOES_ESTOQUE():
    config = DBModel.get_dotenv()
    db = MySqlConnector(config)
    conn, msg = db.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT NOME_PRODUTO FROM PRODUTOS")
        nomes_produtos = cursor.fetchall()

        lista_notificacoes = []

        for (nome_produto,) in nomes_produtos:
            # Agora chama sem parâmetros extras, só o nome do produto
            cursor.callproc("NOTIFICACAO_FALTA_PRODUTO", [nome_produto])

            for result in cursor.stored_results():
                resultado = result.fetchone()
                if resultado and resultado[0]:
                    mensagem = resultado[0]

                    tipo = "baixo-estoque"
                    if "esgotado" in mensagem:
                        tipo = "baixo-estoque"
                    elif "normal" in mensagem:
                        tipo = "estoque-ok"
                    elif "ATENÇÃO" in mensagem or "ALERTA" in mensagem:
                        tipo = "baixo-estoque"

                    lista_notificacoes.append({
                        "id": nome_produto.lower().replace(" ", "_"),
                        "title": f"Produto: {nome_produto}",
                        "message": mensagem,
                        "type": tipo,
                        "read": False
                    })

        return (True, lista_notificacoes)

    except Exception as e:
        return (False, str(e))


