import { ref, computed } from "vue";
import { useNotificationSettings } from "./useNotificationSettings";
import api from "@/services/api"; // axios

const notifications = ref([]);

export function useNotifications() {
  const { settings, notificationTypes } = useNotificationSettings();

  const unreadCount = computed(() => {
    return notifications.value.filter((n) => !n.read).length;
  });

  const markAllAsRead = () => {
    notifications.value = notifications.value.map((n) => ({
      ...n,
      read: true,
    }));
  };

  const markAsRead = (notificationId) => {
    notifications.value = notifications.value.map((n) =>
      n.id === notificationId ? { ...n, read: true } : n
    );
  };

  const clearAll = () => {
    notifications.value = [];
  };

  const fetchNotifications = async () => {
    try {
      const response = await api.get('http://localhost:8000/notificacoes/estoque', {
        params: { limite_baixo: 10, limite_alto: 50 },
      });
      console.log('Resposta da API:', response.data);

      const notificacoes = response.data.notificacoes;

      if (!notificacoes) {
        console.error("Resposta não contém 'notificacoes'");
        return;
      }

      const lista = notificacoes.map((n) => ({
        id: n.id,
        title: n.title,
        message: n.message,
        type: n.type,
        read: false,
      }));

      notifications.value = lista;

    } catch (error) {
      console.error("Erro ao buscar notificações:", error);
    }
  };


  return {
    notifications,
    unreadCount,
    markAllAsRead,
    clearAll,
    markAsRead,
    fetchNotifications,
  };
}