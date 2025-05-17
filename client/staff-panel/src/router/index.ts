import { createRouter, createWebHistory } from "vue-router";
import ManageOrdersPage from "@/views/ManageOrdersPage.vue";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "orders",
      component: ManageOrdersPage,
    },
  ],
});

// router.beforeEach((to, from) => {
//   const auth = useAuthStore();
//   if (to.meta.requiresAuth && !auth.isAuthenticated) {
//     return {
//       path: from.path,
//     };
//   }
// });

export default router;
