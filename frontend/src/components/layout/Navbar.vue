<template>
  <header class="bg-white border-b border-gray-200 h-16 flex items-center px-6">
    <h1 class="text-xl md:text-2xl font-bold truncate">{{ title }}</h1>

    <div class="flex items-center ml-auto gap-4">
      <!-- Notificações -->
      <div class="relative">
        <button
          @click.stop="toggleNotifications"
          class="relative flex items-center justify-center h-10 w-10 hover:bg-gray-100 rounded-full transition-colors"
        >
          <BellIcon class="h-6 w-6 text-gray-600" />
          <span
            v-if="unreadCount > 0"
            class="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center text-xs text-white bg-red-500 rounded-full"
          >
            {{ unreadCount }}
          </span>
        </button>

        <Transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div
            v-if="showNotifications"
            class="fixed sm:absolute right-4 left-4 sm:left-auto sm:right-0 mt-2 sm:w-80 bg-white rounded-lg shadow-lg py-1 z-50 max-h-[80vh] sm:max-h-[calc(100vh-80px)] overflow-y-auto"
            style="top: 3.5rem"
            @click.stop
          >
            <div
              class="px-4 py-2 border-b border-gray-100 flex justify-between items-center"
            >
              <h3 class="font-semibold">Notificações</h3>
              <button
                @click="markAllAsRead"
                class="text-sm text-purple-600 hover:text-purple-800"
              >
                Marcar todas como lidas
              </button>
            </div>

            <div class="max-h-96 overflow-y-auto">
              <div
                v-for="notification in notifications"
                :key="notification.id"
                class="px-4 py-3 hover:bg-gray-50 cursor-pointer"
                :class="{ 'bg-purple-50': !notification.read }"
              >
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
                    <p class="font-medium">{{ notification.title }}</p>
                    <p class="text-sm text-gray-600">
                      {{ notification.message }}
                    </p>
                    <p class="text-xs text-gray-500 mt-1">
                      {{ notification.date }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <div class="px-4 py-2 border-t border-gray-100">
              <router-link
                to="/notificacoes"
                class="text-sm text-purple-600 hover:text-purple-800"
              >
                Ver todas as notificações
              </router-link>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Botão de Logout-->
      <button
        @click="handleLogout"
        class="flex items-center justify-center h-10 w-10 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors"
        title="Sair"
      >
        <LogoutIcon class="h-6 w-6" />
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  BellIcon,
  LogoutIcon,
  ExclamationIcon,
  ClockIcon,
  CheckCircleIcon,
} from "@heroicons/vue/outline";
import { useAuth } from "@/composables/useAuth";
import { useNotifications } from "@/composables/useNotifications";

const route = useRoute();
const router = useRouter();
const { logout } = useAuth();
const { notifications, unreadCount, markAllAsRead } = useNotifications();
const showNotifications = ref(false);
const showMobileSearch = ref(false);

const title = computed(() => {
  return route.meta.title || "Dashboard";
});

const handleLogout = () => {
  logout();
  router.push("/login");
};

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value;
};

const toggleMobileSearch = () => {
  showMobileSearch.value = !showMobileSearch.value;
};

const getNotificationIcon = (type) => {
  const icons = {
    "baixo-estoque": ExclamationIcon,
    validade: ClockIcon,
    entrega: CheckCircleIcon,
  };
  return icons[type];
};

const handleClickOutside = (event) => {
  const notificationButton = event.target.closest("button");
  const notificationDropdown = event.target.closest(".absolute.right-0");
  const searchButton = event.target.closest("[data-search-toggle]");
  const searchBar = event.target.closest("[data-search-bar]");

  if (!notificationButton && !notificationDropdown) {
    showNotifications.value = false;
  }

  if (!searchButton && !searchBar) {
    showMobileSearch.value = false;
  }
};

const handleResize = () => {
  if (window.innerWidth >= 768) {
    showMobileSearch.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
  window.removeEventListener("resize", handleResize);
});
</script>
