import { ref, onMounted, onUnmounted } from 'vue'

export function useDeliveryStats() {
  const stats = ref({
    pendingDeliveries: 0,
    scheduledToday: 0,
    scheduledThisWeek: 0
  })

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/deliveries/stats')
      const data = await response.json()
      updateStats(data)
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
    }
  }

  const updateStats = (data) => {
    stats.value = {
      pendingDeliveries: data.pendingDeliveries,
      scheduledToday: data.scheduledToday,
      scheduledThisWeek: data.scheduledThisWeek
    }
  }

  let ws = null

  const initializeWebSocket = () => {
    ws = new WebSocket('seu_websocket_url')

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'DELIVERY_STATS_UPDATE') {
        updateStats(data)
      }
    }

    ws.onclose = () => {
      setTimeout(initializeWebSocket, 5000) 
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }

  onMounted(() => {
    fetchStats()
    initializeWebSocket()
  })

  onUnmounted(() => {
    if (ws) ws.close()
  })

  return {
    stats,
    fetchStats
  }
}