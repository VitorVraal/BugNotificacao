import { ref, computed } from "vue";
import { useNotificationSettings } from "./useNotificationSettings";
import api from "@/services/api";

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
      const token = localStorage.getItem('token');

      if (!token) {
        console.error("Token de autenticação não encontrado");
        return;
      }

      const expiryDays = settings.value.expiryAlertDays || 3;
      const minStock = settings.value.minStockLimit || 10;

      const response = await api.get('/notificacoes/estoque', {
        params: {
          limite_baixo: minStock,
          dias_validade: expiryDays
        },
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log('Resposta da API:', response.data);

      if (!response.data?.notificacoes) {
        console.error("Resposta não contém 'notificacoes'");
        return;
      }

      const novasNotificacoes = response.data.notificacoes.map((n) => ({
        id: n.id || `${n.type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        title: n.title || (n.type === 'baixo-estoque'
          ? 'Estoque Baixo'
          : n.type === 'validade'
            ? 'Validade Próxima'
            : 'Notificação'),
        message: n.message || 'Nova notificação disponível',
        type: n.type || 'info',
        read: false,
        date: new Date().toLocaleString('pt-BR'),
        priority: n.type === 'validade' ? 1 : 2
      }));

      const idsExistentes = new Set(notifications.value.map(n => n.id));
      const notificacoesUnicas = novasNotificacoes.filter(n => !idsExistentes.has(n.id));

      notifications.value = [
        ...notificacoesUnicas,
        ...notifications.value.filter(n => !n.read)
      ]
        .sort((a, b) => {
          if (a.priority !== b.priority) return a.priority - b.priority;
          return new Date(b.date) - new Date(a.date);
        })
        .slice(0, 50);

    } catch (error) {
      console.error("Erro ao buscar notificações:", error);

      if (notifications.value.length === 0) {
        notifications.value = [{
          id: 'error_fallback',
          title: 'Erro de Conexão',
          message: 'Não foi possível carregar as notificações',
          type: 'error',
          read: false,
          date: new Date().toLocaleString('pt-BR')
        }];
      }
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