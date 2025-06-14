import { ref, onMounted, onUnmounted } from 'vue'

export function useNotificationStats() {
  const stats = ref({
    unreadCount: 0,
    scheduledToday: 0,
    scheduledThisWeek: 0
  })

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/notifications/stats')
      const data = await response.json()
      updateStats(data)
    } catch (error) {
      console.error('Erro ao buscar estatísticas:', error)
    }
  }

  const updateStats = (data) => {
    stats.value = {
      unreadCount: data.unreadCount,
      scheduledToday: data.scheduledToday,
      scheduledThisWeek: data.scheduledThisWeek
    }
  }

  let ws = null

  const initializeWebSocket = () => {
    ws = new WebSocket('seu_websocket_url')

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.type === 'NOTIFICATION_STATS_UPDATE') {
        updateStats(data)
      }
    }

    ws.onclose = () => {
      // Tenta reconectar após 5 segundos
      setTimeout(initializeWebSocket, 5000)
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