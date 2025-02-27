<template>
  <form @submit.prevent="login">
    <div class="login-form">
      <h1 class="text-center">Вход</h1>
      <label for="username">Имя пользователя:</label>
      <TextField id="username" v-model="username" required class="field" />

      <label for="password">Пароль:</label>
      <PasswordTextField id="password" v-model="password" required class="field" />

      <StyledButton type="submit" class="btn">Войти</StyledButton>
      <a :href="`https://int.istu.edu/oauth/authorize?client_id=${OAUTH_CLIENT_ID}`" class="btn">
        <StyledButton type="button" theme="secondary" class="w-full">
          Войти через кампус
        </StyledButton>
      </a>
      <a href="https://library.istu.edu/for-students/zapis-v-biblioteku/" class="btn">
        <StyledButton type="button" theme="secondary" class="w-full">
          Запись в библиотеку
        </StyledButton>
      </a>
    </div>
  </form>
</template>

<script setup lang="ts">
import PasswordTextField from "@/components/PasswordTextField.vue";
import StyledButton from "@/components/StyledButton.vue";
import TextField from "@/components/TextField.vue";
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

<style scoped lang="scss">
@use "@/styles/breakpoints.scss" as *;

form {
  background-color: var(--color-background-100);
  color: var(--color-text-900);
  border-radius: 2rem;

  margin-top: 20px;
  padding: 1rem;
  width: 90vw;
  @include media-lg {
    padding: 4rem;
  }
}

.login-form {
  display: flex;
  flex-direction: column;

  margin: auto;
  width: 100%;
  @include media-md {
    width: 50%;
  }
  @include media-lg {
    width: 30%;
  }
}

.field {
  margin-bottom: 1rem;
}

label {
  font-weight: 600;
}

.btn {
  margin-bottom: 0.5rem;
  width: 100%;
}
</style>
