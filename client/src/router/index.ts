import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/views/HomePage.vue";
import BasketPage from "@/views/BasketPage.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import OrderPage from "@/views/OrderPage.vue";
import NotePage from "@/views/NotePage.vue";
import OauthRedirectPage from "@/views/OauthRedirectPage.vue";

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
      path: "/orders",
      name: "OrderPage",
      component: OrderPage,
    },
    {
      path: "/note",
      name: "NotePage",
      component: NotePage,
    },
  ],
});

export default router;
