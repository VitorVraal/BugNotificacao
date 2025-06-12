import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            await websocket.send_json({
                "type": "DASHBOARD_STATS_UPDATE",
                "totalProducts": 130,
                "lowStockProducts": 5,
                "pendingDeliveries": 10,
                "productOutput": 50,
                "totalProductsTrend": "+7%",
                "lowStockProductsTrend": "-1%",
                "pendingDeliveriesTrend": "+2%",
                "productOutputTrend": "+4%",
            })
            await asyncio.sleep(30)  # Atualiza a cada 30 segundos
    except WebSocketDisconnect:
        print("🔌 WebSocket desconectado.")
