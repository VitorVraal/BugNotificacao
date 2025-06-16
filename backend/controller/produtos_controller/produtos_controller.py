from model.produtos_model.notificacao_model import VERIFICAR_NOTIFICACOES_ESTOQUE, get_notificacoes_estoque_controller, marcar_como_lida_controller
from model.produtos_model.produtos_model import (
    CADASTRAR_PRODUTO_ESTOQUE,
    PROCURAR_PRODUTO_NOME,
    ATUALIZAR_PRODUTO,
    EXCLUIR_PRODUTO_GERAL,
    LISTAR_PRODUTOS,
    coleta_de_dados_email
)
#importa funções do arquivo produtos_model (model->produtos_model->produtos_model)

def insert_produto_controller(NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO
                              ):
    """
    Função de inserir produtos:
    parâmentros usados:
    NOME_PRODUTO, 
    CATEGORIA_ESTOQUE, 
    DESC_PRODUTO, 
    QTDE_ESTOQUE,                        
    PRECO_PRODUTO, 
    QTD_MINIMA_PRODUTO, 
    VALIDADE_PRODUTO, 
    NUMERO_NF_PRODUTO, 
    FORNECEDOR_PRODUTO
    """

    """
        Chama CADASTRAR_PRODUTO_ESTOQUE do arquivo model_produtos e aplica o parâmetros recebidos na função insert_produto_controller
    """
    return CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO)

def delete_produto_estoque_controller(id_estoque: int):
    # validation, resultado = PROCURAR_PRODUTO_ID(id_produto)
    # if validation:
    #     return EXCLUIR_PRODUTO_GERAL(id_produto)
    # else:
    #     return (False, resultado)
    """
    Controla a exclusão de um item de estoque.
    Simplesmente chama a função principal de exclusão no banco por meio da função "EXCLUIR_PRODUTO_GERAL" presente no arquivo model_produtos.
    """
    return EXCLUIR_PRODUTO_GERAL(id_estoque)
    


def update_produto_controller(
    id_estoque,
    categoria_estoque,
    qtde_estoque,
    id_produto,
    nome_produto,
    preco_produto,
    desc_produto,
    numero_nf_produto,
    validade_produto,
    fornecedor_produto,
    qtd_minima_produto
):
    """
    Controla a atualização de um produto ou seu estoque.
    Valida os IDs e converte tipos antes de chamar a função de atualização do banco.
    """
    # Validação básica: ID do estoque e do produto são obrigatórios para atualizar.
    if not id_estoque or not id_produto:
        return False, "ID do estoque e do produto são obrigatórios"
    
    try:
        # Chama a função principal de atualização, convertendo tipos quando necessário.
        return ATUALIZAR_PRODUTO(
            p_id_estoque_upd=int(id_estoque),
            p_categoria_estoque_upd=categoria_estoque,
            p_qtde_estoque_upd=int(qtde_estoque) if qtde_estoque is not None else None,
            p_id_produto_upd=int(id_produto),
            p_nome_produto_upd=nome_produto,
            p_preco_produto_upd=float(preco_produto) if preco_produto is not None else None,
            p_desc_produto_upd=desc_produto,
            p_numero_nf_produto_upd=numero_nf_produto,
            p_validade_produto_upd=validade_produto,
            p_fornecedor_produto_upd=fornecedor_produto,
            p_qtd_minima_produto_upd=int(qtd_minima_produto) if qtd_minima_produto is not None else None
        )
    except Exception as e:
        # Captura erros durante a conversão de tipo ou na atualização.
        return False, str(e)

# print(update_produto_controller(2, "teste novo estoque", 2000))


def search_produto_name_controller(nome):
    """
    Controla a busca de produtos por nome.
    Chama a função de busca no banco e formata os resultados para serem mais legíveis.
    """
    success, resultados = PROCURAR_PRODUTO_NOME(nome)
    if not success:
        return [] # Retorna lista vazia se a busca falhar.

    produtos = [] 
    for row in resultados: # Percorre os resultados do banco (que vêm como tuplas).
        # Mapeia os resultados da tupla para um dicionário mais fácil de usar.

        produtos.append({
            "id_produto": row[0],
            "nome_produto": row[1],
            "preco_produto": row[2],
            "desc_produto": row[3],
            "numero_nf_produto": row[4],
            "validade_produto": row[5],
            "fornecedor_produto": row[6],
            "qtd_minima_produto": row[7],
            "id_estoque": row[8],
            "categoria_estoque": row[9],
            "qtde_estoque": row[10]
        })

    return produtos # Retorna a lista de produtos formatada.



def list_produto_estoque():
    """
    Controla a listagem de todos os produtos no estoque.
    Simplesmente chama a função principal de listagem no banco.
    """
        
    """
    Delega a listagem para a função do banco por meio da função "LISTAR_PRODUTOS" do presente no arquivo model_produtos.. 
    """
    return LISTAR_PRODUTOS() 

def iniciar_coleta_email_controller():
    """
    Controla o início do processo de coleta de dados de e-mails (ex: notas fiscais).
    Chama a função que lida com a lógica de leitura de e-mails e PDFs.
    """
    return coleta_de_dados_email() # Delega a coleta para a função principal.



