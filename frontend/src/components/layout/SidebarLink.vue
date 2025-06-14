<template>
    <router-link 
      :to="to" 
      class="flex items-center text-gray-800 hover:text-black transition-colors" 
      :class="{ 'font-semibold': isActive }"
    >
      <component :is="iconComponent" class="h-6 w-6 mr-3" />
      <span class="text-lg">{{ text }}</span>
    </router-link>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  import { 
    ChartBarIcon, 
    CubeIcon, 
    CollectionIcon, 
    ShoppingCartIcon,
    TruckIcon,
    BellIcon
  } from '@heroicons/vue/outline';
  
  const route = useRoute();
  
  const props = defineProps({
    to: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: true
    }
  });
  
  const iconMap = {
    ChartBarIcon,
    CubeIcon,
    CollectionIcon,
    ShoppingCartIcon,
    TruckIcon,
    BellIcon
  };
  
  const iconComponent = computed(() => {
    return iconMap[props.icon];
  });
  
  const isActive = computed(() => {
    return route.path === props.to;
  });
  </script>