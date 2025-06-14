<template>
  <div 
    :class="['p-4 rounded-2xl shadow cursor-pointer transition-all hover:shadow-md', color]"
    @click="$emit('click')"
  >
    <div class="flex items-center mb-3">
      <component :is="icon" class="h-6 w-6 mr-2" />
      <h3 class="text-lg font-semibold">{{ title }}</h3>
    </div>
    <p class="text-sm text-gray-600">{{ description }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  description: String,
  color: String,
  icon: [Object, String, Function], // <-- Aqui está o fix
});

defineEmits(['click']);
</script>