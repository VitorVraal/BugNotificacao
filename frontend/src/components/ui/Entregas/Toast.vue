<template>
  <div
    class="fixed bottom-4 right-4 z-50"
  >
    <TransitionGroup
      enter-active-class="transform transition duration-300 ease-out"
      enter-from-class="translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transform transition duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-2 opacity-0"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="mb-2 p-4 rounded-lg shadow-lg flex items-center space-x-2 min-w-[300px]"
        :class="{
          'bg-green-100 text-green-800': toast.type === 'success',
          'bg-red-100 text-red-800': toast.type === 'error'
        }"
      >
        <CheckCircleIcon
          v-if="toast.type === 'success'"
          class="h-5 w-5 text-green-500"
        />
        <ExclamationCircleIcon
          v-if="toast.type === 'error'"
          class="h-5 w-5 text-red-500"
        />
        <span>{{ toast.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { CheckCircleIcon, ExclamationCircleIcon } from '@heroicons/vue/solid'
import { ref, onUnmounted } from 'vue'

const props = defineProps({
  toasts: {
    type: Array,
    required: true
  }
})
</script>