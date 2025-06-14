import { ref, computed } from 'vue'

export function useEstoque() {
  const stockStats = ref({
    totalProducts: 0,
    lowStockCount: 0,
    updateCount: 0
  })

  const fetchStockStats = async () => {
    try {
      // Substitua por chamada do back
      const response = await fetch('/api/stock/stats')
      const data = await response.json()
      
      stockStats.value = {
        totalProducts: data.totalProducts,
        lowStockCount: data.lowStockCount,
        updateCount: data.updateCount
      }
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
    }
  }

  // Função para atualizar em tempo real via WebSocket
  const initializeRealTimeUpdates = () => {
    const ws = new WebSocket('seu_websocket_url')

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'STOCK_STATS_UPDATE') {
        stockStats.value = {
          totalProducts: data.totalProducts,
          lowStockCount: data.lowStockCount,
          updateCount: data.updateCount
        }
      }
    }

    return ws
  }

  return {
    stockStats,
    fetchStockStats,
    initializeRealTimeUpdates
  }
}