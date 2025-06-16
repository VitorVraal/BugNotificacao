from fastapi import APIRouter, HTTPException
from controller.dashboard_controller.dashboard_controller import buscar_estatisticas_dashboard

router = APIRouter()

@router.get("/api/dashboard/stats")
def get_dashboard_stats():
    try:
        resultado = buscar_estatisticas_dashboard()
        print("Resultado retornado para o front:", resultado)
        return resultado
    except Exception as e:
        print("Erro ao buscar estatísticas:", str(e))
        raise HTTPException(status_code=500, detail="Erro ao buscar estatísticas do dashboard")