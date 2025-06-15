from fastapi import APIRouter
from controller.produtos_controller.produtos_controller import get_notificacoes_estoque_controller

router = APIRouter()

@router.get("/notificacoes/estoque")
def notificacoes_estoque():
    sucesso, resultado = get_notificacoes_estoque_controller()
    if sucesso:
        return {"notificacoes": resultado}
    else:
        return {"erro": resultado}

