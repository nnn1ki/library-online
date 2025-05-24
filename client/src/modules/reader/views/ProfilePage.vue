<template>
  <div class="container">
    <LoginForm v-if="!isAuthenticated" />
    <div v-else class="profile">
      <h1 class="text-center">{{ currentUser?.first_name }} {{ currentUser?.last_name }}</h1>
      <h2 class="text-center">{{ currentUser?.username }}</h2>
      <h3 class="text-center">
        {{ currentUser?.groups.map((group) => groups[group]).join(", ") }}
      </h3>
      <StyledButton theme="accent" class="w-full" @click="authStore.logout">Выйти</StyledButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { groups } from "@api/types";
import StyledButton from "@components/StyledButton.vue";
import LoginForm from "@reader/components/LoginForm.vue";
import { useAuthStore } from "@core/store/auth";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { isAuthenticated, currentUser } = storeToRefs(authStore);
</script>

<style scoped lang="scss">
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile {
  width: 50%;
  margin: auto;
}
</style>
