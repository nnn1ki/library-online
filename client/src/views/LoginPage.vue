<script setup>
import { ref, computed } from "vue";
import axios from "axios";
</script>

<template>
  <div class="container mt-5">
    <h1 class="text-center">Вход</h1>

    <form v-if="!isLoggedIn" @submit.prevent="login" class="w-50 mx-auto">
      <div class="mb-3">
        <label for="username" class="form-label">Имя пользователя:</label>
        <input
          type="text"
          class="form-control"
          id="username"
          v-model="username"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Пароль:</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="pass"
          required
        />
      </div>
        <button type="submit" class="btn btn-primary w-100" style="margin-bottom: 10px">Войти</button>
        <button type="button" class="btn btn-outline-primary w-100">
          Зарегистрироваться
        </button>
    </form>

    <form form v-else @submit.prevent="logout" class="w-50 mx-auto">
      <button type="submit" class="btn btn-danger w-100">Выйти</button>
    </form>
  </div>
</template>

<style lang="scss" scoped>
</style>