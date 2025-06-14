import { createRouter, createWebHistory } from "vue-router";
import { useAuth } from "@/composables/useAuth";
import DefaultLayout from "@/components/layout/DefaultLayout.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/pages/Login.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/cadastro",
    name: "cadastro",
    component: () => import("@/pages/Cadastro.vue"),
    meta: { requiresGuest: true },
  },
  {
    path: "/dashboard",
    component: DefaultLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: "",
        name: "dashboard",
        component: () => import("@/pages/Dashboard.vue"),
        meta: { title: "Dashboard" },
      },
      {
        path: "/produtos",
        name: "produtos",
        component: () => import("@/pages/Produtos.vue"),
        meta: { title: "Produtos" },
      },
      {
        path: "/estoque",
        name: "estoque",
        component: () => import("@/pages/Estoque.vue"),
        meta: { title: "Estoque" },
      },
      {
        path: "/checkout",
        name: "checkout",
        component: () => import("@/pages/Checkout.vue"),
        meta: { title: "Checkout" },
      },
      {
        path: "/entregas",
        name: "entregas",
        component: () => import("@/pages/Entregas.vue"),
        meta: { title: "Entregas" },
      },
      {
        path: "/notificacoes",
        name: "notificacoes",
        component: () => import("@/pages/Notificacoes.vue"),
        meta: { title: "Notificações" },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const { isAuthenticated } = useAuth();

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next("/login");
    return;
  }

  if (to.meta.requiresGuest && isAuthenticated.value) {
    next("/dashboard");
    return;
  }

  next();
});

export default router;