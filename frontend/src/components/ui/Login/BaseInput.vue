<template>
  <div class="relative">
    <div
      class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none"
      v-if="icon"
    >
      <component :is="icon" class="h-5 w-5 text-gray-400" />
    </div>

    <input
      :type="showPassword ? 'text' : type"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="w-full py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-300"
      :class="{
        'pl-10': icon,
        'pr-10': showPasswordToggle && type === 'password',
        'pl-3': !icon,
      }"
      :placeholder="placeholder"
      autocomplete="new-password"
    />

    <button
      v-if="showPasswordToggle && type === 'password'"
      type="button"
      @click="togglePassword"
      class="absolute inset-y-0 right-0 flex items-center pr-3 cursor-pointer"
    >
      <EyeIcon
        v-if="!showPassword"
        class="h-5 w-5 text-gray-400 hover:text-gray-600"
      />
      <EyeOffIcon v-else class="h-5 w-5 text-gray-400 hover:text-gray-600" />
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { EyeIcon, EyeOffIcon } from "@heroicons/vue/outline";

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: "",
  },
  placeholder: {
    type: String,
    default: "",
  },
  type: {
    type: String,
    default: "text",
  },
  icon: {
    type: [Object, Function],
    default: null,
  },
  showPasswordToggle: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["update:modelValue"]);

const showPassword = ref(false);

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};
</script>