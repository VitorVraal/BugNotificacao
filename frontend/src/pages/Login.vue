<template>
  <div class="flex items-center justify-center min-h-screen bg-purple-300 px-4 sm:px-6">
    <div class="bg-white p-6 sm:p-8 rounded-lg shadow-lg w-full max-w-md mx-auto">
      <div class="flex justify-center mb-6 sm:mb-8">
        <div class="flex items-center">
          <CubeIcon class="h-6 w-6 sm:h-8 sm:w-8 mr-2 sm:mr-3 text-purple-500" />
          <h1 class="text-xl sm:text-2xl font-bold text-gray-800">Mini Mercado Ideal</h1>
        </div>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4 sm:space-y-6">
        <BaseInput
          v-model="email"
          type="email"
          placeholder="Email"
          :icon="MailIcon"
        />

        <BaseInput
          v-model="password"
          type="password"
          placeholder="Senha"
          :icon="LockClosedIcon"
          :showPasswordToggle="true"
        />

        <div class="text-center">
          <router-link
            to="/cadastro"
            class="text-sm sm:text-base text-gray-600 hover:text-gray-800 transition-colors"
          >
            Cadastrar usuário
          </router-link>
        </div>

        <BaseButton
          type="submit"
          class="w-full bg-purple-400 hover:bg-purple-500 text-white font-medium py-2.5 sm:py-3 rounded-lg transition-colors"
          :loading="isLoading"
        >
          {{ isLoading ? 'Entrando...' : 'Entrar' }}
        </BaseButton>
      </form>

      <div v-if="error" class="mt-4 p-3 bg-red-50 text-red-600 text-sm rounded-lg">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { CubeIcon, MailIcon, LockClosedIcon } from "@heroicons/vue/outline";
import BaseInput from "@/components/ui/Login/BaseInput.vue";
import BaseButton from "@/components/ui/Login/BaseButton.vue";
import { useAuth } from "@/composables/useAuth";

const router = useRouter();
const email = ref("");
const password = ref("");
const isLoading = ref(false);
const error = ref("");
const { login } = useAuth();

const handleLogin = async () => {
  if (!email.value || !password.value) {
    error.value = "Por favor, preencha todos os campos";
    return;
  }

  try {
    error.value = "";
    isLoading.value = true;
    await login(email.value, password.value);
    router.push("/dashboard");
  } catch (err) {
    error.value = "Email ou senha inválidos";
    console.error("Erro ao fazer login:", err);
  } finally {
    isLoading.value = false;
  }
};
</script>