<template>
  <div class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 transition-opacity" @click="$emit('close')">
        <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
      </div>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <form @submit.prevent="handleSubmit">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">
              Editar Entrega #{{ delivery.id }}
            </h3>

            <div class="space-y-4">
              <!-- Status -->
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Status
                </label>
                <select
                  v-model="form.status"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                >
                  <option v-for="status in statusOptions" :key="status" :value="status">
                    {{ status }}
                  </option>
                </select>
              </div>

              <!-- Data Prevista -->
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Data Prevista
                </label>
                <input
                  type="date"
                  v-model="form.expectedDate"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                />
              </div>

              <!-- Transportadora -->
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Transportadora
                </label>
                <input
                  type="text"
                  v-model="form.carrier"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                />
              </div>

              <!-- Observações -->
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Observações
                </label>
                <textarea
                  v-model="form.notes"
                  rows="3"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
                ></textarea>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="submit"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Salvar
            </button>
            <button
              type="button"
              @click="$emit('close')"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  delivery: {
    type: Object,
    required: true
  },
  statusOptions: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['close', 'save'])

const form = ref({
  status: props.delivery.status,
  expectedDate: props.delivery.expectedDate.split('/').reverse().join('-'),
  carrier: props.delivery.carrier,
  notes: props.delivery.notes
})

const handleSubmit = () => {
  emit('save', {
    ...props.delivery,
    ...form.value,
    expectedDate: form.value.expectedDate.split('-').reverse().join('/')
  })
}
</script>