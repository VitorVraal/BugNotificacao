from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.auth import pegar_usuario, security # Função para pegar o usuário autenticado (segurança).
from controller.produtos_controller.produtos_controller import (
    get_notificacoes_estoque_controller,
    marcar_como_lida_controller
)

router = APIRouter()

router = APIRouter()

@router.get("/notificacoes/estoque")
async def notificacoes_estoque(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    limite_baixo: int = 10,
    dias_validade: int = 3
):
    usuario = pegar_usuario(credentials)
    sucesso, resultado = get_notificacoes_estoque_controller(
        usuario['id'], limite_baixo, dias_validade
    )
    if sucesso:
        return {"notificacoes": resultado}
    else:
        raise HTTPException(status_code=400, detail=resultado)

@router.post("/notificacoes/marcar-lida/{notificacao_id}")
async def marcar_notificacao_lida(
    notificacao_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        usuario = pegar_usuario(credentials)
        
        # Verificar formato do ID
        if not (notificacao_id.startswith("estoque_") or notificacao_id.startswith("validade_")):
            raise HTTPException(
                status_code=400,
                detail="Formato de ID de notificação inválido"
            )
            
        # Extrair ID do produto
        try:
            produto_id = int(notificacao_id.split("_")[1])
        except (IndexError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="ID de produto inválido na notificação"
            )
            
        sucesso, resultado = marcar_como_lida_controller(
            usuario['id'], notificacao_id, produto_id
        )
        
        if sucesso:
            return {"mensagem": resultado}
        else:
            raise HTTPException(status_code=400, detail=resultado)
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar notificação: {str(e)}"
        )