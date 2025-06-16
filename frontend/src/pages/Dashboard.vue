<template>
  <div class="p-6 dashboard-container" :class="{ 'fade-in': onMounted }">
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6 items-stretch">
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
                  <span :class="getActivityTypeClass(item.tipo)" class="px-2 py-1 text-xs rounded-full">
                    {{ item.tipo }}
                  </span>
                </td>
                <td class="px-6 py-4">{{ item.descricao }}</td>
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

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
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

// Pesquisa e paginação
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = ref(10);
const itemsPerPageOptions = [10, 20, 50];

const activities = ref([]);

const fetchActivities = async () => {
  try {
    const response = await api.get("/api/dashboard/stats");
    console.log(response.data.data.atividades_recentes);
    activities.value = Array.isArray(response.data?.data?.atividades_recentes)
      ? response.data.data.atividades_recentes
      : [];
  } catch (error) {
    console.error("Erro ao buscar atividades:", error);
  }
};




// Filtro das atividades com base na pesquisa
const filteredActivities = computed(() => {
  if (!searchQuery.value) return activities.value;
  
  const query = searchQuery.value.toLowerCase();
  return activities.value.filter(item => 
    item.descricao.toLowerCase().includes(query) || // 
    item.tipo.toLowerCase().includes(query) ||      //
    String(item.value).toLowerCase().includes(query) || 
    item.time.toLowerCase().includes(query)
  );
});


const paginatedActivities = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredActivities.value.slice(start, end);
});

const totalPages = computed(() => {
  const length = filteredActivities.value?.length || 0;
  const perPage = itemsPerPage.value || 10;

  console.log('length:', length, 'perPage:', perPage);

  return Math.ceil(length / perPage);
});


const getActivityTypeClass = (tipo) => {
  const classes = {
    'Adição': 'bg-green-100 text-green-800',
    'Atualização': 'bg-blue-100 text-blue-800',
    'Alerta': 'bg-red-100 text-red-800',
    'Entrega': 'bg-purple-100 text-purple-800'
  };
  return classes[tipo] || 'bg-gray-100 text-gray-800';
};

onMounted(() => {
  fetchActivities();
});

</script>
