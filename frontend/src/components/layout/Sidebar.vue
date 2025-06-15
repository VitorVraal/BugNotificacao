<template>
  <aside class="bg-purple-300 h-screen w-64 fixed left-0 top-0">
    <div class="p-6">
      <div class="flex items-center mb-12">
        <CubeIcon class="h-8 w-8 mr-2" />
        <h1 class="text-2xl font-bold">Mini Mercado Ideal</h1>
      </div>
      
      <nav class="space-y-6">
        <SidebarLink to="/dashboard" icon="ChartBarIcon" text="Dashboard" />
        <SidebarLink to="/produtos" icon="CubeIcon" text="Produtos" />
        <SidebarLink to="/estoque" icon="CollectionIcon" text="Estoque" />
        <SidebarLink to="/checkout" icon="ShoppingCartIcon" text="Checkout" />
        <SidebarLink to="/notificacoes" icon="BellIcon" text="Notificações" />
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { CubeIcon } from '@heroicons/vue/solid';
import SidebarLink from '@/components/layout/SidebarLink.vue';
</script>