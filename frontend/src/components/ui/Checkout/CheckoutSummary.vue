<template>
  <div class="bg-purple-300 text-white p-4 rounded shadow flex flex-col">
    <h2 class="text-lg font-semibold mb-2">
      Resumo Checkout
      <div class="text-sm font-normal text-white/70">
        {{ cart.length }} {{ cart.length === 1 ? 'item' : 'itens' }} no carrinho
      </div>
    </h2>

    <div class="flex-1 overflow-y-auto max-h-[50vh] lg:max-h-[60vh]">
      <div
        v-for="(item, index) in cart"
        :key="item.id"
        class="mb-2 bg-white text-black rounded p-2"
      >
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
          <div class="flex-1">
            <div class="font-semibold">{{ item.nome }}</div>
            <div class="text-sm text-gray-500">
              {{ formatarPreco(item.preco) }} cada
            </div>
          </div>
          <div class="flex flex-col items-end gap-1">
            <div class="flex items-center gap-2">
              <button 
                class="w-8 h-8 rounded-full bg-purple-100 hover:bg-purple-200 text-purple-700 text-lg"
                @click="decrementar(index)"
              >
                −
              </button>

              <span class="w-8 text-center">{{ item.quantidade || 1 }}</span>

              <button 
                class="w-8 h-8 rounded-full bg-purple-100 hover:bg-purple-200 text-purple-700 text-lg"
                @click="incrementar(index)"
              >
                +
              </button>
            </div>
            <div class="font-semibold">
              R$ {{ formatarPreco(item.preco * (item.quantidade || 1)) }}
            </div>
          </div>
        </div>
        <button
          @click="$emit('remove', index)"
          class="text-sm text-red-500 hover:text-red-700 mt-2"
        >
          Remover
        </button>
      </div>
    </div>

    <div class="mt-4 space-y-3">
      <hr class="border-white/40" />
      
      <div class="flex justify-between font-semibold text-lg">
        <span>Total:</span>
        <span>R$ {{ formatarPreco(total) }}</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <button
          class="w-full bg-white text-purple-700 font-bold py-3 px-4 rounded hover:bg-purple-50"
          @click="$emit('finalize')"
        >
          Finalizar
        </button>
        <button
          class="w-full bg-white text-purple-700 py-3 px-4 rounded hover:bg-purple-50"
          @click="$emit('clear')"
        >
          Limpar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  cart: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['remove', 'finalize', 'clear', 'update-quantity'])

const total = computed(() =>
  props.cart.reduce((sum, item) => {
    const preco = Number(item.preco)
    const quantidade = Number(item.quantidade) || 1
    return sum + (isNaN(preco) ? 0 : preco * quantidade)
  }, 0)
)

function formatarPreco(valor) {
  const preco = Number(valor)
  return isNaN(preco) ? '0,00' : preco.toFixed(2).replace('.', ',')
}

function incrementar(index) {
  const item = props.cart[index]
  const novaQuantidade = (item.quantidade || 1) + 1
  emit('update-quantity', { index, quantidade: novaQuantidade })
}

function decrementar(index) {
  const item = props.cart[index]
  const quantidadeAtual = item.quantidade || 1
  if (quantidadeAtual > 1) {
    emit('update-quantity', { index, quantidade: quantidadeAtual - 1 })
  }
}
</script>