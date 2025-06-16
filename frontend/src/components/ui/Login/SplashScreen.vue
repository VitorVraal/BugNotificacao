<template>
    <div class="relative h-screen w-screen">
      <div class="dashboard-container" :class="{ 'fade-in': startFade }">
        <DefaultLayout>
          <Dashboard />
        </DefaultLayout>
      </div>
  
      <div
        class="splash-screen"
        :class="{ 'fade-out': startFade }"
        @animationend="$emit('transitionComplete')"
      >
        <div class="text-center">
          <img
            src="@/assets/logo_animada.svg"
            alt="Logo"
            class="h-[20rem] w-[20rem] mx-auto mb-4 svg-black"
          />
          <h1 class="text-4xl font-bold text-gray-800">Mini Mercado Ideal</h1>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import DefaultLayout from "@/components/layout/DefaultLayout.vue";
  import Dashboard from "@/pages/Dashboard.vue";
  
  const startFade = ref(false);
  
  onMounted(() => {
    setTimeout(() => {
      startFade.value = true;
    }, 6000);
  });
  
  defineEmits(["transitionComplete"]);
  </script>
  
  <style scoped>
  .splash-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgb(216 180 254);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
    opacity: 1;
    transition: opacity 1.5s ease-in-out;
  }
  
  .dashboard-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    z-index: 1;
    transition: opacity 1.5s ease-in-out;
  }
  
  .fade-in {
    opacity: 1;
  }
  
  .fade-out {
    opacity: 0;
    pointer-events: none;
  }
  
  .svg-black {
    filter: brightness(0);
  }
  </style>
  