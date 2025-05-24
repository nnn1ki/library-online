import { createRouter, createWebHistory } from "vue-router";
import readerRoutes from "./routes.reader";
import { useAuthStore } from "@core/store/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...readerRoutes,
    {
      path: "/:pathMatch(.*)*",
      redirect: "/",
    },
  ],
});

router.beforeEach((to, from) => {
  const auth = useAuthStore();

  if (to.query.token) {
    auth.thirdPartyLogin(to.query.token.toString());
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { path: from.path };
  }
});

export default router;
