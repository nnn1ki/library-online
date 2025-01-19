import { createApp } from "vue"
import { createPinia } from "pinia"

import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.min.css"
import "bootstrap/dist/js/bootstrap"

import App from "@/App.vue"
import router from "@/router"

import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App)

app.use(Toast);

app.use(createPinia())
app.use(router)

app.mount("#app")
