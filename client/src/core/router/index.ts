import { createRouter, createWebHistory } from "vue-router";
import readerRoutes from "./routes.reader";
import staffRoutes from "./routes.staff";
import { useAuthStore } from "@core/store/auth";
import { storeToRefs } from "pinia";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...readerRoutes,
    ...staffRoutes,
    {
      path: "/:pathMatch(.*)*",
      redirect: "/",
    },
  ],
});

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const { currentUserRole } = storeToRefs(authStore);
  const requiredRole = to.meta.role;

  if (!requiredRole) {
    return next();
  }

  if (currentUserRole.value === requiredRole) {
    return next();
  }

  if (currentUserRole.value === "Reader") {
    return next("/");
  } else if (currentUserRole.value === "Librarian") {
    return next("/staff/orders");
  } else {
    return next("/");
  }
});

export default router;
