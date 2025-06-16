from model.produtos_model.produtos_model import CONTAR_TOTAL_PRODUTOS, CONTAR_PRODUTOS_BAIXO_ESTOQUE, CONTAR_SAIDAS_PRODUTOS, inserir_atividade, buscar_atividades_recentes
from fastapi import HTTPException

def buscar_estatisticas_dashboard():
    total_ok, total = CONTAR_TOTAL_PRODUTOS()
    baixo_ok, baixo = CONTAR_PRODUTOS_BAIXO_ESTOQUE()
    saida_ok, saida = CONTAR_SAIDAS_PRODUTOS()

    if not total_ok or not baixo_ok or not saida_ok:
        return {
            "success": False,
            "message": f"Erro ao buscar estatísticas do dashboard: total_ok={total_ok}, total={total}, baixo_ok={baixo_ok}, baixo={baixo}, saida_ok={saida_ok}, saida={saida}"
        }

    atividades_ok, atividades = buscar_atividades_recentes()

    if not atividades_ok:
        return {
            "success": False,
            "message": f"Erro ao buscar atividades: {atividades}"
        }


    return {
        "success": True,
        "data": {
            "total_produtos": total,
            "produtos_baixo_estoque": baixo,
            "saida_produtos": saida,
            "atividades_recentes": atividades
        }
    }


def registrar_atividade_controller(tipo: str, descricao: str, quantidade: int = 0):
    sucesso, mensagem = inserir_atividade(tipo, descricao, quantidade)
    if not sucesso:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar atividade: {mensagem}")

def buscar_atividades_controller():
    atividades = buscar_atividades_recentes()
    return atividades
