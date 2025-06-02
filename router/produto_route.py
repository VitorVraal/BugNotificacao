from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from controller.produtos_controller.produtos_controller import (
    insert_produto_controller,
    update_produto_controller,
    search_produto_controller,
    delete_produto_controller,
    list_produto_estoque
)

router = APIRouter()

class Produto(BaseModel):
    nome_produto: str
    preco_produto: float  
    desc_produto: str

class Estoque(BaseModel):
    tipo_estoque: str
    qtde_estoque: int

class ProdutoUpdate(BaseModel):
    nome_produto: str
    preco_produto: float  
    desc_produto: str
    tipo_estoque: str
    qtde_estoque: int
    tipo_atualizacao: int 

class ProdutoDelete(BaseModel):
    nome_produto: str

@router.post("/produto", status_code=201)
def cadastrar_produto_router(produto: Produto, estoque: Estoque):
    try:
        insert_produto_controller(
            produto.nome_produto,
            produto.preco_produto,
            produto.desc_produto,
            estoque.tipo_estoque,
            estoque.qtde_estoque
        )
        return {"message": "Produto e estoque cadastrados com sucesso!"}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/produto/{id}")
def search_produto_router(id: int):
    produto_data = search_produto_controller(id)
    if produto_data:
        return {"message": "Produto localizado", "data": produto_data}
    else:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado com essa ID.")

@router.get("/produto", status_code=200, summary="Lista todos os produtos disponíveis")
def list_produto_router():
    produtos_data = list_produto_estoque()
    if produtos_data:
        return {"message": "Produtos listados com sucesso!", "data": produtos_data}
    else:
        return {"message": "Nenhum produto encontrado.", "data": []}

@router.delete("/produto/{id}", status_code=200, summary="Excluir produto pelo ID")
def excluir_produto_router(id: int):
    result = delete_produto_controller(id)
    if result[0]:  # Excluído com sucesso
        return {"message": f"Produto com ID '{id}' excluído com sucesso."}
    else:
        raise HTTPException(status_code=404, detail=result[1])

@router.put("/produto", status_code=200, summary="Atualizar produto")
def atualizar_produto_router(produto: ProdutoUpdate):
    result = update_produto_controller(
        produto.nome_produto,
        produto.preco_produto,
        produto.desc_produto,
        produto.tipo_estoque,
        produto.qtde_estoque,
        produto.tipo_atualizacao
    )
    if result[0]:
        return {"message": "Produto atualizado com sucesso."}
    else:
        raise HTTPException(status_code=400, detail=result[1])