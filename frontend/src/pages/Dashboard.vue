<template>
  <div class="p-6 dashboard-container" :class="{ 'fade-in': mounted }">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <SummaryCard
        title="Total de Produtos"
        :value="dashboardStats.totalProducts"
        :icon="CubeIcon"
        color="bg-blue-100"
        :change="dashboardStats.totalProductsTrend"
        @click="navigateTo('/produtos')"
      />
      <SummaryCard
        title="Produtos em Baixo estoque"
        :value="dashboardStats.lowStockProducts"
        :icon="ExclamationIcon"
        color="bg-yellow-100"
        :change="dashboardStats.lowStockProductsTrend"
        @click="navigateTo('/estoque')"
      />
      <SummaryCard
        title="Entregas Pendentes"
        :value="dashboardStats.pendingDeliveries"
        :icon="TruckIcon"
        color="bg-orange-100"
        :change="dashboardStats.pendingDeliveriesTrend"
        @click="navigateTo('/entregas')"
      />
      <SummaryCard
        title="Saída de Produtos"
        :value="dashboardStats.productOutput"
        :icon="ArrowUpIcon"
        color="bg-green-100"
        :change="dashboardStats.productOutputTrend"
        @click="navigateTo('/checkout')"
      />
    </div>

    <div class="bg-white rounded-2xl shadow mb-6">
      <div class="p-6 border-b border-gray-200">
        <div class="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6">
          <h2 class="text-lg font-semibold">Atividade Recente</h2>
          
          <div class="relative w-full sm:w-96">
            <SearchIcon class="h-5 w-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Buscar por produto, tipo ou data..."
              class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-purple-300"
            />
          </div>
        </div>

        <!-- Tabela -->
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tipo
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Descrição
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Quantidade
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data/Hora
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="item in paginatedActivities" :key="item.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getActivityTypeClass(item.type)" class="px-2 py-1 text-xs rounded-full">
                    {{ item.type }}
                  </span>
                </td>
                <td class="px-6 py-4">{{ item.description }}</td>
                <td class="px-6 py-4">{{ item.value }}</td>
                <td class="px-6 py-4 text-gray-500">{{ item.time }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="flex flex-col sm:flex-row justify-between items-center gap-4 mt-6">
          <div class="flex items-center gap-2">
            <span class="text-sm text-gray-600">Itens por página:</span>
            <select
              v-model="itemsPerPage"
              class="border rounded-md px-2 py-1 text-sm"
              @change="currentPage = 1"
            >
              <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <div class="text-sm text-gray-600">
            Página {{ currentPage }} de {{ totalPages }}
            ({{ filteredActivities.length }} itens)
          </div>

          <div class="flex gap-2">
            <button
              v-for="page in totalPages"
              :key="page"
              @click="currentPage = page"
              class="px-3 py-1 rounded-md text-sm"
              :class="[
                currentPage === page
                  ? 'bg-purple-500 text-white'
                  : 'text-gray-700 hover:bg-gray-50 border border-gray-300'
              ]"
            >
              {{ page }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <ActionCard
        title="Adicionar novo Produto"
        description="Registrar novo item no estoque"
        color="bg-purple-200"
        :icon="PlusIcon"
        @click="navigateTo('/produtos')"
      />
      <ActionCard
        title="Atualizar Estoque"
        description="Ajustar quantidades"
        color="bg-blue-200"
        :icon="PencilIcon"
        @click="navigateTo('/estoque')"
      />
      <ActionCard
        title="Confirmar Entregas"
        description="Verificar entregas pendentes"
        color="bg-green-200"
        :icon="TruckIcon"
        @click="navigateTo('/entregas')"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { 
  CubeIcon,
  ExclamationIcon,
  TruckIcon,
  ArrowUpIcon,
  PlusIcon,
  PencilIcon,
  SearchIcon
} from "@heroicons/vue/outline";
import { useRouter } from "vue-router";
import { useDashboard } from "@/composables/useDashboard";
import SummaryCard from "../components/ui/Dashboard/SummaryCard.vue";
import ActionCard from "../components/ui/Dashboard/ActionCard.vue";
import api from "@/services/api";

const router = useRouter();
const { dashboardStats } = useDashboard();

const navigateTo = (path) => {
  router.push(path);
};

// Nova função para buscar os dados do dashboard (pelo menos totalProducts)
async function fetchDashboardStats() {
  try {
    const response = await api.get('/produtos/total');
    // Atualizando só o totalProducts, sem mexer nos outros
    dashboardStats.totalProducts = response.data.total || 0;
  } catch (error) {
    console.error('Erro ao buscar total de produtos:', error);
  }
}

// Chamar a busca ao montar o componente
onMounted(() => {
  fetchDashboardStats();
});

// Pesquisa e paginação
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const itemsPerPageOptions = [10, 20, 50];

//Implementar o backend aqui
const activities = ref([
  {
    id: 1,
    type: 'Adição',
    description: 'Margarina',
    value: '10 unidades',
    time: '10 minutos atrás'
  },
  {
    id: 2,
    type: 'Atualização',
    description: 'Biscoito Oreo',
    value: '-15 unidades',
    time: '25 minutos atrás'
  },
  {
    id: 3,
    type: 'Entrega',
    description: 'Coca-Cola pedido #447',
    value: '32 itens',
    time: '1 hora atrás'
  },
  {
    id: 4,
    type: 'Alerta',
    description: 'Ovos de Galinha Caipira',
    value: '2 unidades restantes',
    time: '1 dia atrás'
  }
]);

// Filtro das atividades com base na pesquisa
const filteredActivities = computed(() => {
  if (!searchQuery.value) return activities.value;
  
  const query = searchQuery.value.toLowerCase();
  return activities.value.filter(item => 
    item.description.toLowerCase().includes(query) ||
    item.type.toLowerCase().includes(query) ||
    item.value.toLowerCase().includes(query) ||
    item.time.toLowerCase().includes(query)
  );
});

const paginatedActivities = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredActivities.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredActivities.value.length / itemsPerPage.value);
});

const getActivityTypeClass = (type) => {
  const classes = {
    'Adição': 'bg-green-100 text-green-800',
    'Atualização': 'bg-blue-100 text-blue-800',
    'Alerta': 'bg-red-100 text-red-800',
    'Entrega': 'bg-purple-100 text-purple-800'
  };
  return classes[type] || 'bg-gray-100 text-gray-800';
};
</script>
