import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import json

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.send_json({
                "type": "NOTIFICATION_STATS_UPDATE",
                "unreadCount": 5,
                "scheduledToday": 1,
                "scheduledThisWeek": 4
            })
            await asyncio.sleep(30)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("🔌 WebSocket desconectado.")

@router.websocket("/ws/dashboard")
async def websocket_dashboard(websocket: WebSocket):
    """
    Função: Lida com a conexão WebSocket para o dashboard.
    Recebe parâmetros:websocket (WebSocket): O objeto WebSocket que representa a conexão com o cliente.
    Detalhes:
    - Aceita a conexão WebSocket.
    - Entra em um loop infinito para enviar atualizações de dados do dashboard a cada 30 segundos.
    - Se o cliente desconectar, imprime uma mensagem.
    """
    await websocket.accept() # espera e a ceita a conexão WebSocket que veio do cliente.
    try:
        while True: # Loop que mantém a conexão aberta e envia dados.
            await websocket.send_json({ # Envia dados no formato JSON para o cliente.
                "type": "DASHBOARD_STATS_UPDATE", # Tipo da mensagem, para o cliente saber o que é.
                "totalProducts": 130,  # Exemplo: total de produtos.
                "lowStockProducts": 5, # Exemplo: produtos com estoque baixo.
                "pendingDeliveries": 10, # Exemplo: entregas pendentes.
                "productOutput": 50, # Exemplo: saída de produtos.
                "totalProductsTrend": "+7%", # Exemplo: tendência do total de produtos.
                "lowStockProductsTrend": "-1%", # Exemplo: tendência de estoque baixo.
                "pendingDeliveriesTrend": "+2%", # Exemplo: tendência de entregas pendentes.
                "productOutputTrend": "+4%",  # Exemplo: tendência de saída de produtos.
            })
            await asyncio.sleep(30)  # Pausa a execução por 30 segundos antes de enviar a próxima atualização.
    except WebSocketDisconnect: # Captura a exceção se o cliente desconectar do WebSocket.
        print("🔌 WebSocket desconectado.")
