import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/views/HomePage.vue";
import BasketPage from "@/views/BasketPage.vue";
import LoginPage from "@/views/LoginPage.vue";
import OrderPage from "@/views/OrderPage.vue";
import NotePage from "@/views/NotePage.vue";
import OrdersPage from "@/views/OrdersPage.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomePage,
    },
    {
      path: "/profile",
      name: "LoginPage",
      component: LoginPage,
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
    },
    {
      path: "/note",
      name: "NotePage",
      component: NotePage,
    },
    {
      path:"/orders",
      name: "OrdersPage",
      component: OrdersPage,
    }

  ],
});

export default router;
