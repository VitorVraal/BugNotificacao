<template>
    <button
      @click="$emit('toggle')"
      class="lg:hidden p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-purple-500"
    >
      <MenuIcon v-if="!isOpen" class="h-6 w-6" />
      <XIcon v-else class="h-6 w-6" />
    </button>
  </template>
  
  <script setup>
  import { MenuIcon, XIcon } from '@heroicons/vue/outline';
  
  defineProps({
    isOpen: {
      type: Boolean,
      default: false
    }
  });
  
  defineEmits(['toggle']);
  </script>