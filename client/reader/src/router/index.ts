import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/views/HomePage.vue";
import BasketPage from "@/views/BasketPage.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import OrderPage from "@/views/OrderPage.vue";
import NotePage from "@/views/NotePage.vue";
import OrdersPage from "@/views/OrdersPage.vue";
import OauthRedirectPage from "@/views/OauthRedirectPage.vue";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: HomePage,
    },
    {
      path: "/profile",
      name: "ProfilePage",
      component: ProfilePage,
    },
    {
      path: "/bitrix-auth",
      name: "OauthRedirectPage",
      component: OauthRedirectPage,
    },
    {
      path: "/basket",
      name: "BasketPage",
      component: BasketPage,
    },
    {
      path: "/order",
      name: "OrderPage",
      component: OrderPage,
      meta: { requiresAuth: true },
    },
    {
      path: "/note",
      name: "NotePage",
      component: NotePage,
    },
    {
      path: "/orders",
      name: "OrdersPage",
      component: OrdersPage,
    },
  ],
});

router.beforeEach((to, from) => {
  const auth = useAuthStore();

  if (to.query.token){
    auth.thirdPartyLogin(to.query.token.toString())
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return {
      path: from.path,
    };
  }
});

export default router;
