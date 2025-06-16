<template>
  <div class="mb-4 bg-white p-4 rounded shadow">
    <h2 class="text-lg font-semibold mb-2 flex items-center gap-2">
      <SearchIcon class="w-5 h-5 text-gray-600" />
      Procurar Produto
    </h2>
    <input
      :value="modelValue"
      @input="onInput"
      type="text"
      @keyup.enter="onEnter"
      placeholder="Procurar Produtos por Nome"
      class="w-full p-2 border rounded mb-2"
    />
  </div>
</template>

<script setup>
import { SearchIcon } from '@heroicons/vue/outline'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue', 'search'])

function onInput(event) {
  emit('update:modelValue', event.target.value)
  emit('search', event.target.value)  // Aqui você emite o termo para o pai buscar no backend
}

function onEnter() {
  // opcional: se quiser buscar só ao pressionar enter, pode usar só essa função
  emit('search', props.modelValue)
}
</script>

