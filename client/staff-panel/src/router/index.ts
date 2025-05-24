import { createRouter, createWebHistory } from "vue-router";
import ManageOrdersPage from "@/views/ManageOrdersPage.vue";
import AuthPage from "@/views/AuthPage.vue";
import { useAuthStore } from "@core/store/auth";
import { useAuthentication } from "@/composables/auth";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "orders",
      component: ManageOrdersPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/auth",
      name: "auth",
      component: AuthPage,
      meta: { requiresAuth: false },
    },
  ],
});

router.beforeEach(async (to, from) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;

  if (!isAuthenticated && to.meta.requiresAuth) {
    return {
      name: "auth",
      query: { redirect: to.fullPath },
    };
  }
});

export default router;
