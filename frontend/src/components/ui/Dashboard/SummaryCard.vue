<template>
  <div
    :class="['p-4 rounded-2xl shadow cursor-pointer transition-all hover:shadow-md', color]"
    @click="$emit('click')"
  >
    <div class="flex flex-col items-center text-center">
      <div class="summary-card-icon p-2 rounded-full mb-2 bg-white">
        <component :is="icon" class="h-6 w-6" />
      </div>
      <h3 class="text-sm font-medium text-gray-600">{{ title }}</h3>
      <p class="text-2xl font-bold my-1">{{ value }}</p>
      <p
        v-if="change"
        class="text-xs"
        :class="changeColor"
      >
        {{ change }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  value: [String, Number],
  icon: [Object, String, Function], // <-- Aqui está o fix
  color: String,
  change: String
})

defineEmits(['click'])

const changeColor = computed(() =>
  props.change?.startsWith('+') ? 'text-green-600' : 'text-red-600'
)
</script>