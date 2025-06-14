<template>
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6 border-b border-gray-200">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-lg font-semibold">
              Detalhes da Entrega #{{ delivery.id }}
            </h3>
            <p class="text-sm text-gray-600">{{ delivery.client }}</p>
          </div>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-500"
          >
            <XIcon class="h-6 w-6" />
          </button>
        </div>
      </div>

      <div class="p-6 space-y-6">
        <!-- Informações Básicas -->
        <div>
          <h4 class="font-medium mb-2">Informações da Entrega</h4>
          <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <dt class="text-sm text-gray-600">Endereço</dt>
              <dd>{{ delivery.address }}</dd>
            </div>
            <div>
              <dt class="text-sm text-gray-600">Data Prevista</dt>
              <dd>{{ delivery.expectedDate }}</dd>
            </div>
            <div>
              <dt class="text-sm text-gray-600">Status</dt>
              <dd>
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getStatusClass(delivery.status)"
                >
                  {{ delivery.status }}
                </span>
              </dd>
            </div>
            <div>
              <dt class="text-sm text-gray-600">Transportadora</dt>
              <dd>{{ delivery.carrier || '-' }}</dd>
            </div>
          </dl>
        </div>

        <!-- Produtos -->
        <div>
          <h4 class="font-medium mb-2">Produtos Incluídos</h4>
          <div class="border rounded-lg overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Produto
                  </th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">
                    Quantidade
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="item in delivery.items" :key="item.name">
                  <td class="px-4 py-3 text-sm">{{ item.name }}</td>
                  <td class="px-4 py-3 text-sm text-right">{{ item.quantity }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="text-sm text-gray-600 mt-2">
            Peso Total: {{ delivery.totalWeight }}
          </p>
        </div>

        <!-- Histórico -->
        <div>
          <h4 class="font-medium mb-2">Histórico de Status</h4>
          <div class="space-y-3">
            <div
              v-for="(event, index) in delivery.history"
              :key="index"
              class="flex gap-4"
            >
              <div class="w-24 text-sm text-gray-600">
                {{ event.date }}
              </div>
              <div class="flex-1 text-sm">
                {{ event.status }}
              </div>
            </div>
          </div>
        </div>

        <!-- Observações -->
        <div v-if="delivery.notes">
          <h4 class="font-medium mb-2">Observações</h4>
          <p class="text-sm text-gray-600">{{ delivery.notes }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { XIcon } from '@heroicons/vue/outline'

const props = defineProps({
  delivery: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])

const getStatusClass = (status) => {
  const classes = {
    'Pendente': 'bg-yellow-100 text-yellow-800',
    'Em rota': 'bg-blue-100 text-blue-800',
    'Entregue': 'bg-green-100 text-green-800',
    'Atrasada': 'bg-red-100 text-red-800'
  }
  return classes[status]
}
</script>