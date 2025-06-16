<template>
  <div class="flex h-screen">
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 transition-opacity lg:hidden"
      @click="toggleSidebar"
    ></div>

    <!-- Sidebar -->
    <aside
      :class="{
        'translate-x-0': isSidebarOpen,
        '-translate-x-full': !isSidebarOpen,
      }"
      class="fixed inset-y-0 left-0 z-50 w-64 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:relative"
    >
      <Sidebar />
    </aside>

    <div class="flex-1 flex flex-col min-w-0">
      <header class="sticky top-0 z-40 bg-white border-b border-gray-200">
        <div class="flex items-center h-16">
          <HamburgerButton
            :is-open="isSidebarOpen"
            @toggle="toggleSidebar"
            class="lg:hidden px-4"
          />
          <div class="flex-1">
            <Navbar />
          </div>
        </div>
      </header>

      <main class="flex-1 p-6 bg-gray-50 overflow-y-auto">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import Navbar from "@/components/layout/Navbar.vue";
import HamburgerButton from "@/components/Layout/HamburgerButton.vue";

const isSidebarOpen = ref(false);

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};
</script>