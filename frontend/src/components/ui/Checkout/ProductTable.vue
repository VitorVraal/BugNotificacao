<template>
  <div class="overflow-x-auto rounded-lg shadow">
    <table class="w-full border-collapse bg-white">
      <thead>
        <tr class="bg-gray-50">
          <th class="px-4 py-3 text-left text-xs sm:text-sm font-medium text-gray-600">
            Nome
          </th>
          <th class="px-4 py-3 text-right text-xs sm:text-sm font-medium text-gray-600">
            Preço (R$)
          </th>
          <th class="px-4 py-3 text-center text-xs sm:text-sm font-medium text-gray-600">
            Ação
          </th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200">
        <tr
          v-for="product in products"
          :key="product.id"
          class="hover:bg-gray-50"
        >
          <td class="px-4 py-3">
            <div class="flex flex-col">
              <span class="font-medium text-sm sm:text-base">{{ product.nome }}</span>
              <span class="text-xs text-gray-500 sm:hidden">{{ product.categoria }}</span>
            </div>
          </td>
          <td class="px-4 py-3 text-right text-sm sm:text-base">
            {{ formatPrice(product.preco) }}
          </td>
          <td class="px-4 py-3 text-center">
            <button
              class="w-full sm:w-auto px-3 py-1.5 text-sm text-white bg-blue-600 rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              @click="$emit('add-to-cart', product)"
              :disabled="product.estoque === 0"
              :title="product.estoque === 0 ? 'Produto sem estoque' : 'Adicionar ao carrinho'"
            >
              {{ product.estoque === 0 ? 'Indisponível' : 'Adicionar' }}
            </button>
          </td>
        </tr>
        <tr v-if="products.length === 0">
          <td colspan="5" class="px-4 py-8 text-center text-gray-500">
            <p class="text-sm sm:text-base">Nenhum produto encontrado.</p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  products: {
    type: Array,
    required: true
  }
})

function formatPrice(price) {
  if (typeof price !== 'number') return ''
  return price.toFixed(2)
}

</script>