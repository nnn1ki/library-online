import { createApp } from "vue";
import { createPinia } from "pinia";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-icons/font/bootstrap-icons.min.css";
import "bootstrap/dist/js/bootstrap";

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
  app.use(Toast, {timeout:2000});
} else {
  app.use(Toast);
}

app.use(createPinia());
app.use(router);

app.mount("#app");
