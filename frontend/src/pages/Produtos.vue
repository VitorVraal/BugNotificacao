<template>
  <div class="p-4 sm:p-6">
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4 sm:gap-6">
      <!-- Registro Manual -->
      <div class="bg-white rounded-xl shadow p-4 sm:p-6">
        <h2 class="text-lg font-semibold mb-4 sm:mb-6">Registro Manual de Produtos</h2>
        
        <form @submit.prevent="handleManualRegister" class="space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Nome do Produto
              </label>
              <input
                v-model="manualForm.name"
                type="text"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Categoria
              </label>
              <select
                v-model="manualForm.category"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              >
                <option value="">Selecione uma categoria</option>
                <option v-for="category in categories" :key="category" :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Descrição
            </label>
            <textarea
              v-model="manualForm.description"
              rows="3"
              class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
            ></textarea>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Quantidade Inicial
              </label>
              <input
                v-model="manualForm.initialQuantity"
                type="number"
                min="0"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Preço
              </label>
              <input
                v-model="manualForm.price"
                type="number"
                min="0"
                step="0.01"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Quantidade Mínima
              </label>
              <input
                v-model="manualForm.minQuantity"
                type="number"
                min="0"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Validade
              </label>
              <input
                v-model="manualForm.expiryDate"
                type="date"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Código da Nota Fiscal
              </label>
              <input
                v-model="manualForm.barcode"
                type="text"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Fornecedor
            </label>
            <input
              v-model="manualForm.supplier"
              type="text"
              class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
              required
            />
          </div>

          <div class="flex flex-col sm:flex-row justify-end gap-2 sm:gap-4 pt-4">
            <button
              type="button"
              @click="resetForm"
              class="w-full sm:w-auto px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 text-sm sm:text-base"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="w-full sm:w-auto px-4 py-2 text-white bg-purple-500 rounded-lg hover:bg-purple-600 text-sm sm:text-base"
            >
              Registrar Produto
            </button>
          </div>
        </form>
      </div>

      <!-- Registro Automatizado -->
      <div class="space-y-4 sm:space-y-6">
        <div class="bg-white rounded-xl shadow p-4 sm:p-6">
          <h2 class="text-lg font-semibold mb-4 sm:mb-6">Registro Automatizado de Produto</h2>
          
          <form @submit.prevent="handleAutomatedRegister" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Link da Nota Fiscal
              </label>
              <input
                v-model="automatedForm.invoiceLink"
                type="text"
                class="w-full p-2 border rounded-lg focus:ring-2 focus:ring-purple-300 focus:outline-none text-sm sm:text-base"
                required
              />
            </div>

            <div class="flex justify-end">
              <button
                type="submit"
                class="w-full sm:w-auto px-4 py-2 text-white bg-purple-500 rounded-lg hover:bg-purple-600 text-sm sm:text-base"
              >
                Registrar Produto
              </button>
            </div>
          </form>
        </div>

        <!-- "Como funciona" -->
        <div class="bg-blue-50 rounded-xl p-4 sm:p-6">
          <h3 class="font-semibold mb-4">Como funciona:</h3>
          <ul class="space-y-3 sm:space-y-4">
            <li class="flex items-start">
              <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mr-3">
                <span class="text-sm sm:text-base">1</span>
              </div>
              <p class="text-sm sm:text-base">Coloque o Link da Nota Fiscal e clique em Registrar Produto</p>
            </li>
            <li class="flex items-start">
              <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mr-3">
                <span class="text-sm sm:text-base">2</span>
              </div>
              <p class="text-sm sm:text-base">O sistema automaticamente extrai os produtos do Link da Nota Fiscal</p>
            </li>
            <li class="flex items-start">
              <div class="flex-shrink-0 w-6 h-6 sm:w-8 sm:h-8 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 mr-3">
                <span class="text-sm sm:text-base">3</span>
              </div>
              <p class="text-sm sm:text-base">Os produtos ficam marcados como "Entrega Pendente" até a confirmação da entrega</p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const categories = ["Alimentos", "Bebidas", "Laticínios"];

const manualForm = ref({
  name: '',
  category: '',
  description: '',
  initialQuantity: 0,
  price: 0,
  minQuantity: 1,
  expiryDate: '',
  barcode: '',
  supplier: ''
});

const automatedForm = ref({
  invoiceLink: ''
});

const handleManualRegister = async () => {
  try {
    // Verifique se todos os campos obrigatórios estão preenchidos
    if (!manualForm.value.name || !manualForm.value.category || manualForm.value.initialQuantity <= 0) {
      alert('Por favor, preencha todos os campos obrigatórios!');
      return;
    }

    const produto = {
      nome_produto: manualForm.value.name,
      preco_produto: manualForm.value.price,
      desc_produto: manualForm.value.description,
      numero_nf_produto: manualForm.value.barcode,
      validade_produto: manualForm.value.expiryDate ? new Date(manualForm.value.expiryDate).toISOString().split('T')[0] : null,
      fornecedor_produto: manualForm.value.supplier,
      qtd_minima_produto: manualForm.value.minQuantity,
    };

    const estoque = {
      categoria_estoque: manualForm.value.category,
      qtde_estoque: manualForm.value.initialQuantity,
    };

    console.log("Enviando:", { produto, estoque });

    const response = await api.post('/produto', {
      produto, 
      estoque
    });

    alert('Produto cadastrado com sucesso!');
    resetForm();
    router.push('/estoque'); // Redireciona para a página de estoque após cadastro
  } catch (error) {
    console.error(error);
    if (error.response && error.response.data && error.response.data.detail) {
      alert(error.response.data.detail);
    } else {
      alert('Erro ao cadastrar produto. Verifique o console para mais detalhes.');
    }
  }
};

const handleAutomatedRegister = () => {
  // Implementar lógica de registro automatizado
  //Aqui entra o backend
  console.log('Link da nota fiscal:', automatedForm.value.invoiceLink);
};

const resetForm = () => {
  if (confirm('Deseja apagar os dados diigtados?')) {
    manualForm.value = {
      name: '',
      category: '',
      description: '',
      initialQuantity: 0,
      price: 0,
      minQuantity: 1,
      expiryDate: '',
      barcode: '',
      supplier: ''
    };
  }
};
</script>