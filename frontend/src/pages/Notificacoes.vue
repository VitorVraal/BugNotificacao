<template>
  <div class="container mx-auto px-4 py-6">
    <!-- Cards estatísticos -->
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
      <div class="lg:col-span-2">
        <!-- Filtros -->
        <div class="mb-4 sm:mb-6 overflow-x-auto">
          <div class="flex space-x-2 min-w-max pb-2">
            <button
              v-for="filter in filters"
              :key="filter.name"
              @click="currentFilter = filter.value"
              class="px-3 sm:px-4 py-2 rounded-lg text-sm whitespace-nowrap"
              :class="
                currentFilter === filter.value
                  ? 'bg-purple-100 text-purple-700'
                  : 'bg-gray-100'
              "
            >
              {{ filter.name }}
            </button>
          </div>
        </div>

        <!-- Lista de notificações -->
        <div class="bg-white rounded-xl shadow">
          <div
            class="p-3 sm:p-4 border-b border-gray-100 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2"
          >
            <h2 class="font-semibold">Todas as Notificações</h2>
            <button
              @click="markAllAsRead"
              class="text-sm text-purple-600 hover:text-purple-800"
            >
              Marcar todas como lidas
            </button>
          </div>
          <div class="divide-y">
            <div
              v-for="notification in filteredNotifications"
              :key="notification.id"
              class="p-3 sm:p-4 hover:bg-gray-50 relative group"
              :class="{
                'bg-purple-50': !notification.read,
                'opacity-75': notification.read,
              }"
            >
              <div
                v-if="!notification.read"
                class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-12 bg-purple-500 rounded-r"
              ></div>

              <div class="flex items-start justify-between">
                <div class="flex items-start space-x-3">
                  <div
                    class="p-2 rounded-full"
                    :class="{
                      'bg-yellow-100': notification.type === 'baixo-estoque',
                      'bg-red-100': notification.type === 'validade',
                      'bg-green-100': notification.type === 'entrega',
                    }"
                  >
                    <component
                      :is="getNotificationIcon(notification.type)"
                      class="h-5 w-5"
                      :class="{
                        'text-yellow-600':
                          notification.type === 'baixo-estoque',
                        'text-red-600': notification.type === 'validade',
                        'text-green-600': notification.type === 'entrega',
                      }"
                    />
                  </div>
                  <div>
                    <p
                      class="font-medium"
                      :class="
                        !notification.read ? 'text-gray-900' : 'text-gray-700'
                      "
                    >
                      {{ notification.title }}
                    </p>
                    <p
                      class="text-sm"
                      :class="
                        !notification.read ? 'text-gray-600' : 'text-gray-500'
                      "
                    >
                      {{ notification.message }}
                    </p>
                    <p class="text-xs text-gray-500 mt-1">
                      {{ notification.date }}
                    </p>
                  </div>
                </div>

                <button
                  v-if="!notification.read"
                  @click="markAsRead(notification.id)"
                  class="opacity-0 group-hover:opacity-100 transition-opacity duration-200 p-2 hover:bg-gray-100 rounded-full"
                  title="Marcar como lida"
                >
                  <CheckIcon class="h-5 w-5 text-purple-600" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
        </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import {
  TruckIcon,
  CalendarIcon,
  CubeIcon,
  ExclamationIcon,
  ClockIcon,
  CheckCircleIcon,
  CheckIcon,
} from "@heroicons/vue/outline";
import { useNotifications } from "@/composables/useNotifications";
import { useNotificationStats } from "@/composables/useNotificationStats";
import { useNotificationSettings } from '@/composables/useNotificationSettings'

const { stats } = useNotificationStats();

const { notifications, unreadCount, markAllAsRead, clearAll, markAsRead, fetchNotifications } =
  useNotifications();

const {
  notificationTypes,
  settings,
  updateNotificationType,
  saveSettings
} = useNotificationSettings()

const currentFilter = ref("all");

const filters = [
  { name: "Tudo", value: "all" },
  { name: "Baixo Estoque", value: "baixo-estoque" },
  { name: "Validade", value: "validade" },
];

const filteredNotifications = computed(() => {
  if (currentFilter.value === "all") return notifications.value;
  return notifications.value.filter((n) => n.type === currentFilter.value);
});

const getNotificationIcon = (type) => {
  const icons = {
    "baixo-estoque": ExclamationIcon,
    validade: ClockIcon,
    entrega: CheckCircleIcon,
  };
  return icons[type];
};

// Função para salvar as configurações
const handleSaveSettings = async () => {
  const { success, error } = await saveSettings()
  if (success) {
    console.log('Configurações salvas com sucesso!')
  } else {
    console.error('Erro ao salvar configurações:', error)
  }
}

onMounted(async () => {
  await fetchNotifications();

  const uniqueNotifications = [];
  const seenIds = new Set();

  notifications.value.forEach((n) => {
    if (!seenIds.has(n.id)) {
      seenIds.add(n.id);
      uniqueNotifications.push(n);
    }
  });

  notifications.value = uniqueNotifications;

  setInterval(async () => {
    await fetchNotifications();

    const updated = [];
    const ids = new Set();

    notifications.value.forEach((n) => {
      if (!ids.has(n.id)) {
        ids.add(n.id);
        updated.push(n);
      }
    });

    notifications.value = updated;
  }, 86400000);
});


</script>