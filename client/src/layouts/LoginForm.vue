<template>
    <form @submit.prevent="login" class="w-50 mx-auto">
        <h1 class="text-center">Вход</h1>
        <div class="mb-3">
            <label for="username" class="form-label">Имя пользователя:</label>
            <input type="text" class="form-control" id="username" v-model="username" required />
        </div>
        <div class="mb-3">
            <label for="password" class="form-label">Пароль:</label>
            <input type="password" class="form-control" id="password" v-model="password" required />
        </div>
        <button type="submit" class="btn btn-primary w-100 mb-2">
            Войти
        </button>
        <a :href="`https://int.istu.edu/oauth/authorize?client_id=${OAUTH_CLIENT_ID}`"
            class="btn btn-primary w-100 mb-2">
            Войти через кампус
        </a>
        <a href="https://library.istu.edu/for-students/zapis-v-biblioteku/" class="btn btn-outline-primary w-100">
            Запись в библиотеку
        </a>
    </form>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { ref } from "vue";

const OAUTH_CLIENT_ID = import.meta.env.VITE_OAUTH_CLIENT_ID;

const authStore = useAuthStore();

const username = ref("");
const password = ref("");

async function login() {
    // TODO: предупреждать пользователя об ошибках
    await authStore.login(username.value, password.value);
}
</script>

<style lang="scss" scoped></style>
