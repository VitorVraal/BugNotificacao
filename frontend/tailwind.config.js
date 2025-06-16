/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/components/**/*.{vue,js}",
    "./src/pages/**/*.{vue,js}",
    "./src/layouts/**/*.{vue,js}",
    "./src/App.vue",
    "./src/main.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
