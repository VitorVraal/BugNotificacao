<template>
  <div class="min-h-screen bg-purple-300">
    <div
      v-show="!showSplash"
      class="flex items-center justify-center min-h-screen px-4 sm:px-6"
    >
      <div class="bg-white p-6 sm:p-8 rounded-lg shadow-lg w-full max-w-md mx-auto">
        <div class="flex justify-center mb-6 sm:mb-8">
          <div class="flex items-center">
            <img
              src="@/assets/logo.svg"
              alt="Logo"
              class="h-16 w-16 sm:h-20 sm:w-20 mr-4 black-logo"
            />
            <h1 class="text-xl sm:text-2xl font-bold text-gray-800">
              Mini Mercado Ideal
            </h1>
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

    <SplashScreen
      v-if="showSplash"
      @transition-complete="handleTransitionComplete"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { MailIcon, LockClosedIcon } from "@heroicons/vue/outline";
import BaseInput from "@/components/ui/Login/BaseInput.vue";
import BaseButton from "@/components/ui/Login/BaseButton.vue";
import SplashScreen from "@/components/ui/Login/SplashScreen.vue";
import { useAuth } from "@/composables/useAuth";

const router = useRouter();
const email = ref("");
const password = ref("");
const isLoading = ref(false);
const error = ref("");
const showSplash = ref(false);
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
    
    showSplash.value = true;

    setTimeout(() => {
      router.push("/dashboard");
    }, 7500);
  } catch (err) {
    error.value = "Email ou senha inválidos";
    console.error("Erro ao fazer login:", err);
  } finally {
    isLoading.value = false;
  }
};

const handleTransitionComplete = () => {
  showSplash.value = false;
};
</script>

<style scoped>
.dashboard-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  transition: opacity 2s ease-in-out;
  z-index: 1;
}

.fade-in {
  opacity: 1;
}

.black-logo {
  filter: brightness(0) saturate(100%);
}
</style>