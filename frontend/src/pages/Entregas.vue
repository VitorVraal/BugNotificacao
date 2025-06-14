<template>
  <div class="container mx-auto px-4 py-6">
    <!-- Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
      <div class="bg-blue-100 p-4 rounded-2xl flex items-center justify-between">
        <div>
          <h3 class="text-sm text-gray-600">Entrega Pendentes</h3>
          <p class="text-2xl font-bold">{{ stats.pendingDeliveries }}</p>
        </div>
        <TruckIcon class="h-8 w-8 text-blue-500" />
      </div>

      <div class="bg-green-100 p-4 rounded-2xl flex items-center justify-between">
        <div>
          <h3 class="text-sm text-gray-600">Previstas para Hoje</h3>
          <p class="text-2xl font-bold">{{ stats.scheduledToday }}</p>
        </div>
        <CalendarIcon class="h-8 w-8 text-green-500" />
      </div>

      <div class="bg-purple-100 p-4 rounded-2xl flex items-center justify-between">
        <div>
          <h3 class="text-sm text-gray-600">Entregas nessa Semana</h3>
          <p class="text-2xl font-bold">{{ stats.scheduledThisWeek }}</p>
        </div>
        <CubeIcon class="h-8 w-8 text-purple-500" />
      </div>
    </div>

    <!-- Filtros e Busca -->
    <div class="bg-white rounded-lg shadow p-4 mb-6">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="relative">
          <SearchIcon class="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por nota fiscal ou fornecedor..."
            class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-300"
          />
        </div>

        <div>
          <select
            v-model="selectedStatus"
            class="w-full px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-300"
          >
            <option value="">Status</option>
            <option v-for="status in statusOptions" :key="status" :value="status">
              {{ status }}
            </option>
          </select>
        </div>

        <div>
          <input
            v-model="dateFrom"
            type="date"
            class="w-full px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-300"
          />
        </div>

        <div>
          <input
            v-model="dateTo"
            type="date"
            class="w-full px-3 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-300"
          />
        </div>
      </div>
    </div>

    <!-- Tabela de Entregas -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-lg font-semibold">Entregas Pendentes</h2>
        <p class="text-sm text-gray-600">Confirme as entregas quando chegarem</p>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                ID/Cliente
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Endereço
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Data Prevista
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Transportadora
              </th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="delivery in paginatedDeliveries" :key="delivery.id" class="hover:bg-gray-50">
              <td class="px-4 py-4">
                <div>
                  <div class="font-medium text-gray-900">#{{ delivery.id }}</div>
                  <div class="text-sm text-gray-500">{{ delivery.client }}</div>
                </div>
              </td>
              <td class="px-4 py-4 text-sm text-gray-500">
                {{ delivery.address }}
              </td>
              <td class="px-4 py-4 text-sm text-gray-500">
                {{ delivery.expectedDate }}
              </td>
              <td class="px-4 py-4">
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getStatusClass(delivery.status)"
                >
                  {{ delivery.status }}
                </span>
              </td>
              <td class="px-4 py-4 text-sm text-gray-500">
                {{ delivery.carrier || '-' }}
              </td>
              <td class="px-4 py-4 text-sm text-right space-x-2">
                <button
                  @click="viewDelivery(delivery)"
                  class="text-purple-600 hover:text-purple-900"
                >
                  Visualizar
                </button>
                <button
                  @click="editDelivery(delivery)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  Editar
                </button>
                <button
                  @click="handleCancelDelivery(delivery)"
                  class="text-red-600 hover:text-red-900"
                >
                  Cancelar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Paginação -->
      <div class="px-4 py-3 border-t border-gray-200">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4">
          <div class="flex items-center gap-2">
            <span class="text-sm text-gray-700">Itens por página:</span>
            <select
              v-model="itemsPerPage"
              class="border rounded px-2 py-1 text-sm"
            >
              <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <div class="flex justify-center gap-2">
            <button
              v-for="page in totalPages"
              :key="page"
              @click="currentPage = page"
              class="px-3 py-1 rounded"
              :class="currentPage === page ? 'bg-purple-500 text-white' : 'text-gray-700 hover:bg-gray-100'"
            >
              {{ page }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Detalhes -->
    <DeliveryDetailsModal
      v-if="showDetailsModal"
      :delivery="selectedDelivery"
      @close="showDetailsModal = false"
    />

    <!-- Modal de Edição -->
    <EditDeliveryModal
      v-if="showEditModal"
      :delivery="selectedDelivery"
      :statusOptions="statusOptions"
      @close="showEditModal = false"
      @save="handleSaveEdit"
    />

    <Toast :toasts="toasts" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  TruckIcon,
  CalendarIcon,
  CubeIcon,
  SearchIcon
} from '@heroicons/vue/outline'
import { useDeliveryStats } from '@/composables/useDeliveryStats'
import { useDeliveries } from '@/composables/useDeliveries' // Add this import
import DeliveryDetailsModal from '@/components/ui/Entregas/DeliveryDetailsModal.vue'
import EditDeliveryModal from '@/components/ui/Entregas/EditDeliveryModal.vue'
import Toast from '@/components/ui/Entregas/Toast.vue'

const { stats } = useDeliveryStats()

// Estados
const searchQuery = ref('')
const selectedStatus = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const showDetailsModal = ref(false)
const showEditModal = ref(false)
const selectedDelivery = ref(null)

// Opções
const itemsPerPageOptions = [10, 20, 50]
const statusOptions = ['Pendente', 'Em rota', 'Entregue', 'Atrasada']

// Dados mockados (substituir pelos dados do backend)
const deliveries = ref([
  {
    id: 1,
    client: 'Mercado Central',
    address: 'Rua Principal, 123',
    expectedDate: '02/04/2025',
    status: 'Pendente',
    carrier: 'Transportadora XYZ',
    items: [
      { name: 'Arroz', quantity: 10 },
      { name: 'Feijão', quantity: 5 }
    ],
    totalWeight: '50kg',
    history: [
      { date: '01/04/2025', status: 'Pedido Criado' }
    ],
    notes: 'Entregar no período da manhã'
  },
])

const filteredDeliveries = computed(() => {
  let result = deliveries.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(d => 
      d.client.toLowerCase().includes(query) ||
      d.id.toString().includes(query) ||
      d.status.toLowerCase().includes(query)
    )
  }

  if (selectedStatus.value) {
    result = result.filter(d => d.status === selectedStatus.value)
  }

  if (dateFrom.value && dateTo.value) {
    result = result.filter(d => {
      const date = new Date(d.expectedDate.split('/').reverse().join('-'))
      return date >= new Date(dateFrom.value) && date <= new Date(dateTo.value)
    })
  }

  return result
})

const paginatedDeliveries = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredDeliveries.value.slice(start, start + itemsPerPage.value)
})

const totalPages = computed(() => 
  Math.ceil(filteredDeliveries.value.length / itemsPerPage.value)
)

// Métodos
const getStatusClass = (status) => {
  const classes = {
    'Pendente': 'bg-yellow-100 text-yellow-800',
    'Em rota': 'bg-blue-100 text-blue-800',
    'Entregue': 'bg-green-100 text-green-800',
    'Atrasada': 'bg-red-100 text-red-800'
  }
  return classes[status]
}

const viewDelivery = (delivery) => {
  selectedDelivery.value = delivery
  showDetailsModal.value = true
}

const { updateDelivery, cancelDelivery } = useDeliveries()

const editDelivery = (delivery) => {
  selectedDelivery.value = delivery
  showEditModal.value = true
}

const toasts = ref([])

const showToast = (message, type = 'success') => {
  const id = Date.now()
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(toast => toast.id !== id)
  }, 3000)
}

const handleSaveEdit = async (updatedDelivery) => {
  try {
    const { success, error } = await updateDelivery(updatedDelivery.id, updatedDelivery)
    
    if (success) {
      deliveries.value = deliveries.value.map(d => 
        d.id === updatedDelivery.id ? updatedDelivery : d
      )
      showEditModal.value = false
      showToast('Entrega atualizada com sucesso!')
    } else {
      throw new Error(error)
    }
  } catch (error) {
    console.error('Erro ao salvar edição:', error)
    showToast('Erro ao atualizar entrega', 'error')
  }
}

const handleCancelDelivery = async (delivery) => {
  if (confirm(`Deseja cancelar a entrega #${delivery.id}?`)) {
    try {
      const { success, error } = await cancelDelivery(delivery.id)
      
      if (success) {
        deliveries.value = deliveries.value.map(d => 
          d.id === delivery.id ? { ...d, status: 'Cancelada' } : d
        )
        showToast('Entrega cancelada com sucesso!')
      } else {
        throw new Error(error)
      }
    } catch (error) {
      console.error('Erro ao cancelar entrega:', error)
      showToast('Erro ao cancelar entrega', 'error')
    }
  }
}
</script>