from model.produtos_model.produtos_model import (
    CADASTRAR_PRODUTO_ESTOQUE,
    PROCURAR_PRODUTO_ID,
    ATUALIZAR_PRODUTO,
    EXCLUIR_PRODUTO_GERAL,
    LISTAR_PRODUTOS,
    coleta_de_dados_email
)

def insert_produto_controller(NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO
                              ):
    return CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, CATEGORIA_ESTOQUE, DESC_PRODUTO, QTDE_ESTOQUE, 
                              PRECO_PRODUTO, QTD_MINIMA_PRODUTO, VALIDADE_PRODUTO, NUMERO_NF_PRODUTO, 
                              FORNECEDOR_PRODUTO)

def delete_produto_estoque_controller(id_estoque: int):
    # validation, resultado = PROCURAR_PRODUTO_ID(id_produto)
    # if validation:
    #     return EXCLUIR_PRODUTO_GERAL(id_produto)
    # else:
    #     return (False, resultado)
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
    # Validação básica
    if not id_estoque or not id_produto:
        return False, "ID do estoque e do produto são obrigatórios"
    
    try:
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
        return False, str(e)

# print(update_produto_controller(2, "teste novo estoque", 2000))


def search_produto_controller(ID_PRODUTO):
    validation, resultado = PROCURAR_PRODUTO_ID(ID_PRODUTO)
    return resultado  # Não há necessidade de condicional se ambos os caminhos retornam o mesmo valor


def list_produto_estoque():
    return LISTAR_PRODUTOS()

# Exemplo de teste (descomente para usar)
# print(search_produto_controller(1))


def iniciar_coleta_email_controller():
    return coleta_de_dados_email()
