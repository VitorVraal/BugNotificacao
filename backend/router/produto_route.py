from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from utils.auth import pegar_usuario
from controller.produtos_controller.produtos_controller import (
    insert_produto_controller,
    update_produto_controller,
    search_produto_name_controller,
    delete_produto_estoque_controller,
    list_produto_estoque,
    iniciar_coleta_email_controller,
)
from model.produtos_model.produtos_model import diminuir_estoque


router = APIRouter()

class Produto(BaseModel):
    nome_produto: str
    preco_produto: float  
    desc_produto: str
    numero_nf_produto:str
    validade_produto: date
    fornecedor_produto: str
    qtd_minima_produto: int

class Estoque(BaseModel):
    id_estoque: Optional[int] = None
    categoria_estoque: str
    qtde_estoque: int
    
class ProdutoEstoque(BaseModel):
    produto: Produto
    estoque: Estoque    

class ProdutoUpdate(BaseModel):
    id_produto: int
    nome_produto: str
    preco_produto: float = Field(default=0.0)
    desc_produto: str = Field(default="")
    numero_nf_produto: str = Field(default="")
    validade_produto: date
    fornecedor_produto: str
    qtd_minima_produto: int

class EstoqueUpdate(BaseModel):
    id_estoque: int
    qtde_estoque: int
    categoria_estoque: str
    
class EstoqueCheckout(BaseModel):
    id_produto: int
    qtde_estoque: int

class ProdutoEstoqueUpdate(BaseModel):
    produto: ProdutoUpdate
    estoque: EstoqueUpdate

class ProdutoDelete(BaseModel):
    nome_produto: str

@router.post("/produto", status_code=201)
def cadastrar_produto_router(dados: ProdutoEstoque, usuario=Depends(pegar_usuario)):
    try:
        # Verifique se o produto já existe
        produtos = list_produto_estoque()
        if any(p['NOME_PRODUTO'].lower() == dados.produto.nome_produto.lower() for p in produtos):
            raise HTTPException(
                status_code=400,
                detail="Produto já cadastrado. Use a função de atualização para modificar."
            )
            
        success, message = insert_produto_controller(
            dados.produto.nome_produto,
            dados.estoque.categoria_estoque,
            dados.produto.desc_produto,
            dados.estoque.qtde_estoque,
            dados.produto.preco_produto,
            dados.produto.qtd_minima_produto,
            dados.produto.validade_produto,
            dados.produto.numero_nf_produto,
            dados.produto.fornecedor_produto,
        )
        
        if not success:
            raise HTTPException(status_code=400, detail=message)
            
        return {"message": "Produto cadastrado com sucesso!"}
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/produto/nome/{nome}")
def search_produto_nome_router(nome: str, usuario=Depends(pegar_usuario)):
    produto_data = search_produto_name_controller(nome)
    if produto_data:
        return {
            "message": "Produtos encontrados",
            "data": produto_data 
        }
    else:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado com esse nome.")

@router.get("/produto", response_model=List[dict])
#def list_produto_router():
def list_produto_router(usuario=Depends(pegar_usuario)):
        return list_produto_estoque()


@router.delete("/produto/{id}", status_code=200, summary="Excluir produto pelo ID")
def excluir_produto_router(id: int, usuario=Depends(pegar_usuario)):
    result = delete_produto_estoque_controller(id)
    if result[0]:  # Excluído com sucesso
        return {"message": f"Produto com ID '{id}' excluído com sucesso."}
    else:
        raise HTTPException(status_code=404, detail=result[1])

@router.put("/produto")
def atualizar_produto_router(dados: ProdutoEstoqueUpdate, usuario=Depends(pegar_usuario)):
    try:
        success, message = update_produto_controller(
            dados.estoque.id_estoque,
            dados.estoque.categoria_estoque,
            dados.estoque.qtde_estoque,
            dados.produto.id_produto,
            dados.produto.nome_produto,
            dados.produto.preco_produto,
            dados.produto.desc_produto,
            dados.produto.numero_nf_produto,
            dados.produto.validade_produto,
            dados.produto.fornecedor_produto,
            dados.produto.qtd_minima_produto
        )
        
        if not success:
            raise HTTPException(status_code=400, detail=message)
            
        return {"message": "Produto atualizado com sucesso."}
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

@router.get("/coleta-email", summary="Coleta dados de e-mails do Gmail com anexos PDF")
def coleta_email_router(usuario=Depends(pegar_usuario)):
    try:
        result = iniciar_coleta_email_controller()
        return {"message": "Coleta de e-mail concluída", "resultado": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na coleta de e-mails: {e}")
    
@router.post("/estoque/atualizar")
def atualizar_estoque(dados: EstoqueCheckout, usuario=Depends(pegar_usuario)):
    success, msg = diminuir_estoque(dados.id_produto, dados.qtde_estoque)
    if success:
        return {"message": "Estoque atualizado"}
    else:
        raise HTTPException(status_code=400, detail=msg)

@router.get("/produtos/total")
def get_total_produtos():
    db = conectar()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM PRODUTO")  # ou o nome correto da sua tabela
        total = cursor.fetchone()[0]
        return {"total": total}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()