import { ref } from 'vue'

export function useNotificationSettings() {
  const notificationTypes = ref([
    { id: 'baixo-estoque', name: 'Alerta de baixo Estoque', enabled: true },
    { id: 'entrega', name: 'Atualizações de Entrega', enabled: true },
    { id: 'validade', name: 'Alerta Validade', enabled: true },
  ])

  const settings = ref({
    minStockLimit: '10',
    expiryAlertDays: '3'
  })

  const updateNotificationType = (typeId, enabled) => {
    const type = notificationTypes.value.find(t => t.id === typeId)
    if (type) {
      type.enabled = enabled
    }
  }

  const saveSettings = async () => {
    try {
      // Aqui implementar o backend
      await fetch('http://localhost:8000/notification-settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          notificationTypes: notificationTypes.value,
          settings: settings.value
        })
      })
      
      return { success: true }
    } catch (error) {
      console.error('Erro ao salvar configurações:', error)
      return { success: false, error }
    }
  }

  return {
    notificationTypes,
    settings,
    updateNotificationType,
    saveSettings
  }
}