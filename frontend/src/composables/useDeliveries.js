import { ref } from 'vue'

export function useDeliveries() {
  const updateDelivery = async (deliveryId, updatedData) => {
    try {
      // Implementar no backend
      const response = await fetch(`/api/deliveries/${deliveryId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedData),
      });

      if (!response.ok) {
        throw new Error("Erro ao atualizar entrega");
      }

      return { success: true };
    } catch (error) {
      console.error('Erro ao atualizar entrega:', error)
      return { success: false, error }
    }
  }

  const cancelDelivery = async (deliveryId) => {
    try {
      // Implementar no backend 
      const response = await fetch(`/api/deliveries/${deliveryId}/cancel`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        throw new Error('Erro ao cancelar entrega')
      }

      return { success: true }
    } catch (error) {
      console.error('Erro ao cancelar entrega:', error)
      return { success: false, error }
    }
  }

  return {
    updateDelivery,
    cancelDelivery
  }
}