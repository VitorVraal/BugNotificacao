<template>
  <div class="container mx-auto px-4 py-6">
    <!-- Cards estatísticos -->
    <div
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8"
    >
      <div
        class="bg-blue-100 p-4 sm:p-6 rounded-2xl flex justify-between items-center"
      >
        <div>
          <h3 class="text-sm sm:text-base font-semibold">
            Notificações Não Lidas
          </h3>
          <p class="text-xl sm:text-2xl font-bold">{{ stats.unreadCount }}</p>
        </div>
        <TruckIcon class="h-6 w-6 sm:h-8 sm:w-8" />
      </div>

      <div
        class="bg-green-100 p-4 sm:p-6 rounded-2xl flex justify-between items-center"
      >
        <div>
          <h3 class="text-sm sm:text-base font-semibold">
            Previstas para Hoje
          </h3>
          <p class="text-xl sm:text-2xl font-bold">
            {{ stats.scheduledToday }}
          </p>
        </div>
        <CalendarIcon class="h-6 w-6 sm:h-8 sm:w-8" />
      </div>

      <div
        class="bg-purple-100 p-4 sm:p-6 rounded-2xl flex justify-between items-center"
      >
        <div>
          <h3 class="text-sm sm:text-base font-semibold">
            Entregas nessa Semana
          </h3>
          <p class="text-xl sm:text-2xl font-bold">
            {{ stats.scheduledThisWeek }}
          </p>
        </div>
        <CubeIcon class="h-6 w-6 sm:h-8 sm:w-8" />
      </div>
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

      <!-- Configuração das Notificações -->
      <div class="bg-white rounded-xl shadow p-4 sm:p-6 h-fit">
        <div class="mb-4 sm:mb-6">
          <h3 class="text-base sm:text-lg font-semibold">
            Configuração das Notificações
          </h3>
        </div>

        <div class="space-y-4 sm:space-y-6">
          <!-- Tipos de notificações -->
          <div>
            <h4 class="font-medium mb-3 sm:mb-4">Tipos de notificações</h4>
            <div class="space-y-3 sm:space-y-4">
              <div
                v-for="type in notificationTypes"
                :key="type.id"
                class="flex items-center justify-between"
              >
                <span class="text-sm sm:text-base text-gray-700">{{ type.name }}</span>
                <button
                  class="w-10 sm:w-12 h-5 sm:h-6 rounded-full p-1 transition-colors duration-200 ease-in-out"
                  :class="type.enabled ? 'bg-purple-600' : 'bg-gray-200'"
                  @click="updateNotificationType(type.id, !type.enabled)"
                >
                  <div
                    class="w-3 sm:w-4 h-3 sm:h-4 rounded-full bg-white transition-transform duration-200 ease-in-out"
                    :class="type.enabled ? 'transform translate-x-5 sm:translate-x-6' : ''"
                  ></div>
                </button>
              </div>
            </div>
          </div>

          <!-- Configuração de Validade/Baixo Estoque -->
          <div>
            <h4 class="font-medium mb-3 sm:mb-4">
              Configuração de Validade/Baixo Estoque
            </h4>
            <div class="space-y-3 sm:space-y-4">
              <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
                <span class="text-sm sm:text-base text-gray-700">
                  Limite Mínimo de Estoque
                </span>
                <select
                  v-model="settings.minStockLimit"
                  class="border rounded-md px-2 py-1 text-sm sm:text-base"
                >
                  <option value="10">10%</option>
                  <option value="15">15%</option>
                  <option value="25">25%</option>
                </select>
              </div>
              <div class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4">
                <span class="text-sm sm:text-base text-gray-700">
                  Alerta de validade
                </span>
                <select
                  v-model="settings.expiryAlertDays"
                  class="border rounded-md px-2 py-1 text-sm sm:text-base"
                >
                  <option value="3">3 dias</option>
                  <option value="5">5 dias</option>
                  <option value="7">7 dias</option>
                </select>
              </div>
            </div>
          </div>

          <button
            @click="handleSaveSettings"
            class="w-full bg-purple-500 text-white py-2 rounded-lg hover:bg-purple-600 text-sm sm:text-base"
          >
            Salvar
          </button>
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
  { name: "Entregas", value: "entrega" },
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

onMounted(() => {
  fetchNotifications();
  setInterval(fetchNotifications, 10000); // a cada 10s
});

</script>