from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.auth import pegar_usuario, security # Função para pegar o usuário autenticado (segurança).
from controller.produtos_controller.produtos_controller import (
    get_notificacoes_estoque_controller
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