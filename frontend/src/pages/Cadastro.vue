<template>
  <div class="flex items-center justify-center min-h-screen bg-purple-300 px-4 sm:px-6">
    <div class="bg-white p-6 sm:p-8 rounded-lg shadow-lg w-full max-w-md mx-auto">
      <div class="flex justify-center mb-6 sm:mb-8">
        <div class="flex items-center">
          <CubeIcon class="h-6 w-6 sm:h-8 sm:w-8 mr-2 sm:mr-3 text-purple-500" />
          <h1 class="text-xl sm:text-2xl font-bold text-gray-800">Mini Mercado Ideal</h1>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4 sm:space-y-6">
        <div>
          <BaseInput
            v-model="email"
            type="email"
            placeholder="Email"
            :icon="MailIcon"
            @blur="validateEmail"
            class="text-sm sm:text-base"
          />
          <p v-if="emailError" class="mt-1 text-xs sm:text-sm text-red-600">
            {{ emailError }}
          </p>
        </div>

        <div>
          <BaseInput
            v-model="password"
            type="password"
            placeholder="Senha"
            :icon="LockClosedIcon"
            :showPasswordToggle="true"
            @blur="validatePassword"
            class="text-sm sm:text-base"
          />
          <p v-if="passwordError" class="mt-1 text-xs sm:text-sm text-red-600">
            {{ passwordError }}
          </p>
        </div>

        <BaseButton
          type="submit"
          class="w-full bg-purple-400 hover:bg-purple-500 text-white font-medium py-2.5 sm:py-3 rounded-lg transition-colors"
          :loading="isLoading"
        >
          {{ isLoading ? 'Cadastrando...' : 'Cadastrar' }}
        </BaseButton>

        <div class="text-center">
          <router-link
            to="/login"
            class="text-sm sm:text-base text-gray-600 hover:text-gray-800 transition-colors"
          >
            Voltar para Login
          </router-link>
        </div>
      </form>
    </div>

    <!-- Pop-up -->
    <Transition
      enter-active-class="transform transition duration-300 ease-out"
      enter-from-class="translate-y-2 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transform transition duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="translate-y-2 opacity-0"
    >
      <div
        v-if="showSuccessMessage"
        class="fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-white rounded-full shadow-lg px-4 py-2 flex items-center text-sm sm:text-base"
      >
        <CheckCircleIcon class="h-5 w-5 sm:h-6 sm:w-6 text-green-500 mr-2" />
        <span>Cadastro realizado com sucesso!</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { CubeIcon, MailIcon, LockClosedIcon, CheckCircleIcon } from "@heroicons/vue/outline";
import BaseInput from "@/components/ui/Login/BaseInput.vue";
import BaseButton from "@/components/ui/Login/BaseButton.vue";
import { useAuth } from "@/composables/useAuth";

const router = useRouter();
const email = ref("");
const password = ref("");
const isLoading = ref(false);
const emailError = ref("");
const passwordError = ref("");
const showSuccessMessage = ref(false);
const nome = ref("");
const { register } = useAuth();

const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.value) {
    emailError.value = "Email é obrigatório";
  } else if (!emailRegex.test(email.value)) {
    emailError.value = "Email inválido";
  } else {
    emailError.value = "";
  }
};

const validatePassword = () => {
  if (!password.value) {
    passwordError.value = "Senha é obrigatória";
  } else if (password.value.length < 6) {
    passwordError.value = "A senha deve ter no mínimo 6 caracteres";
  } else {
    passwordError.value = "";
  }
};

const handleSubmit = async () => {
  validateEmail();
  validatePassword();

  if (emailError.value || passwordError.value) return;

  try {
    isLoading.value = true;

    await register(email.value, password.value);
    showSuccessMessage.value = true;

    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (error) {
    console.error("Erro ao cadastrar:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>