<template>
  <div class="container mt-5">
    
    <form v-if="!isAuthenticated" @submit.prevent="login" class="w-50 mx-auto">
      <h1 class="text-center">Вход</h1>
      <div class="mb-3">
        <label for="username" class="form-label">Имя пользователя:</label>
        <input type="text" class="form-control" id="username" v-model="username" required />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Пароль:</label>
        <input type="password" class="form-control" id="password" v-model="password" required />
      </div>
      <button type="submit" class="btn btn-primary w-100" style="margin-bottom: 10px">
        Войти
      </button>
      <button type="button" enabled="false" class="btn btn-primary w-100" style="margin-bottom: 10px">
        Войти через кампус
      </button>
      <button type="button" enabled="false" class="btn btn-outline-primary w-100">
        Зарегистрироваться
      </button>
    </form>

    <form form v-else @submit.prevent="authStore.logout" class="w-50 mx-auto">
      <button type="submit" class="btn btn-danger w-100">Выйти</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { ref } from "vue";

const authStore = useAuthStore();
const { isAuthenticated } = storeToRefs(authStore);

const username = ref("");
const password = ref("");

async function login() {
  // TODO: предупреждать пользователя об ошибках
  await authStore.login(username.value, password.value);
}
</script>

<style lang="scss" scoped></style>