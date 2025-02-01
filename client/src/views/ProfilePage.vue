<template>
  <div class="container mt-5">
    <Login v-if="!isAuthenticated" />
    <div v-else class="w-50 mx-auto">
      <h1 class="text-center mb-2">{{ currentUser?.username }}</h1>
      <h2 class="text-center mb-2">{{ currentUser?.groups.map((group) => groups[group]).join(", ") }}</h2>
      <button class="btn btn-danger w-100" @click="authStore.logout">Выйти</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { groups } from "@/api/types";
import Login from "@/layouts/LoginForm.vue";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { isAuthenticated, currentUser } = storeToRefs(authStore);
</script>

<style lang="scss" scoped></style>