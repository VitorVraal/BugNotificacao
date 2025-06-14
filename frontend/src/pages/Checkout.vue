<template>
  <div class="p-4 sm:p-6">
    <div class="flex flex-col lg:flex-row gap-4 sm:gap-6">
      <div class="w-full lg:w-3/4 space-y-4 sm:space-y-6">
        <div class="bg-white rounded-lg shadow p-4">
          <ProductSearch 
            v-model="searchTerm"
            @search="buscarProdutos"
            class="w-full"
          />

          <ProductTable :products="filteredProducts" @add-to-cart="addToCart" />


        </div>
      </div>

      <div class="w-full lg:w-1/4">
        <div class="sticky top-6">
          <CheckoutSummary
            :cart="cart"
            @remove="removeFromCart"
            @finalize="finalizeCheckout"
            @clear="clearCart"
            @update-quantity="updateQuantity"
            class="w-full"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ProductSearch from '@/components/ui/Checkout/ProductSearch.vue'
import ProductTable from '@/components/ui/Checkout/ProductTable.vue'
import CheckoutSummary from '@/components/ui/Checkout/CheckoutSummary.vue'
import api from '@/services/api'
import { eventBus } from '@/services/eventBus'

const cart = ref([])
const searchTerm = ref('')
const produtosBuscados = ref([])

const mappedProducts = computed(() =>
  produtosBuscados.value.map(prod => ({
    id: prod.id_produto,
    nome: prod.nome_produto,
    preco: prod.preco_produto,
    descricao: prod.desc_produto,
    numero_nf: prod.numero_nf_produto,
    validade: prod.validade_produto,
    fornecedor: prod.fornecedor_produto,
    qtd_minima: prod.qtd_minima_produto,
    id_estoque: prod.id_estoque,
    categoria_estoque: prod.categoria_estoque,
    qtde_estoque: prod.qtde_estoque
  }))
)

const filteredProducts = computed(() => mappedProducts.value)

async function buscarProdutos(nome) {
  if (!nome) {
    produtosBuscados.value = []
    return
  }
  try {
    const response = await api.get('/produto/nome/' + nome)
    produtosBuscados.value = response.data.data || []
  } catch (error) {
    console.error('Erro ao buscar produtos:', error)
    produtosBuscados.value = []
  }
}

function addToCart(product) {
  const index = cart.value.findIndex(item => item.id === product.id)
  if (index !== -1) {
    cart.value[index].quantidade = (cart.value[index].quantidade || 1) + 1
  } else {
    cart.value.push({ ...product, quantidade: 1 })
  }
}

function removeFromCart(index) {
  cart.value.splice(index, 1)
}

function updateQuantity({ index, quantidade }) {
  if (quantidade < 1) return
  cart.value[index].quantidade = quantidade
}

function clearCart() {
  cart.value = []
}

async function finalizeCheckout() {
  if (cart.value.length === 0) {
    alert('Carrinho vazio!')
    return
  }

  try {
    // Atualiza o estoque para cada produto no carrinho
    for (const item of cart.value) {
      await api.post('/estoque/atualizar', {
        id_produto: item.id,
        qtde_estoque: item.quantidade
      })
    }

    alert('Compra finalizada com sucesso!')

    // Limpa o carrinho após atualizar o estoque
    clearCart()

    // Opcional: emitir evento para atualizar o estoque na UI, caso necessário
    eventBus.emit('estoque-atualizado')

  } catch (error) {
    console.error('Erro ao atualizar estoque no checkout:', error)
    alert('Erro ao finalizar compra. Tente novamente.')
  }
}
</script>

<style scoped>
@media (max-width: 1023px) {
  .sticky {
    position: relative;
    top: 0;
  }
}
</style>