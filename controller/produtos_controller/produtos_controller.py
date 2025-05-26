from model.produtos_model.produtos_model import CADASTRAR_PRODUTO_ESTOQUE, PROCURAR_PRODUTO_ID, ATUALIZAR_PRODUTO, EXCLUIR_PRODUTO_GERAL, LISTAR_PRODUTOS



def insert_produto_controller(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE):
    return CADASTRAR_PRODUTO_ESTOQUE(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_PRODUTO, QTDE_ESTOQUE)

insert_produto_controller('uva', 10.50, 'Uva verde', 'uva', 100)

def delete_produto_controller(NOME_PRODUTO):
    
    return EXCLUIR_PRODUTO_GERAL(NOME_PRODUTO)

def update_produto_estoque(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO):
    return ATUALIZAR_PRODUTO(NOME_PRODUTO, PRECO_PRODUTO, DESC_PRODUTO, TIPO_ESTOQUE, QTDE_ESTOQUE, TIPO_ATUALIZACAO)

def search_produto_estoque(ID_PRODUTO):
    return PROCURAR_PRODUTO_ID(ID_PRODUTO)


def list_produto_estoque():
    produtos = LISTAR_PRODUTOS()         
    return produtos


print(list_produto_estoque())