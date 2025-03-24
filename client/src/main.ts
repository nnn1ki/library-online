import { createApp } from "vue";
import { createPinia } from "pinia";

import "modern-normalize/modern-normalize.css";
import "@/style.scss";

import App from "@/App.vue";
import router from "@/router";

import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

axios.interceptors.request.use(async (config) => {
  const authStore = useAuthStore();

  if (await authStore.updateTokens()) {
    config.headers.Authorization = `Bearer ${authStore.access}`;
  }

  return config;
});

const app = createApp(App);

if (screen.width < 768) {
  app.use(Toast, { timeout: 3000 });
} else {
  app.use(Toast);
}

app.use(createPinia());
app.use(router);

app.mount("#app");
