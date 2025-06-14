import { ref, computed } from "vue";

const notifications = ref([
  {
    id: 1,
    type: "baixo-estoque",
    title: "Alerta de baixo Estoque",
    message: "Lorem (3 sobrando)",
    date: "02/04/2025",
    read: false,
  },
  {
    id: 2,
    type: "validade",
    title: "Alerta de Validade",
    message: "3 Produtos vão vencer daqui 2 dias",
    date: "02/04/2025",
    read: false,
  },
  {
    id: 3,
    type: "entrega",
    title: "Entrega Confirmada",
    message: "Entrega recebida e confirmada",
    date: "02/04/2025",
    read: false,
  },
]);

export function useNotifications() {
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

  const getNotifications = () => notifications.value;

  return {
    notifications,
    unreadCount,
    markAllAsRead,
    clearAll,
    markAsRead,
  };
}