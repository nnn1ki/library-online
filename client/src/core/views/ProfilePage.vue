<template>
  <div class="container">
    <LoginForm v-if="!isAuthenticated" />
    <div v-else class="profile">
      <h3 class="text-center">{{ currentUser?.first_name }} {{ currentUser?.last_name }}</h3>
      <h4 class="text-center">{{ currentUser?.username }}</h4>
      <h5 class="text-center">
        {{ groups[currentUserRole] }}
      </h5>
      <StyledButton theme="accent" class="w-full" @click="handleLogout">Выйти</StyledButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { groups } from "@api/types";
import StyledButton from "@components/StyledButton.vue";
import LoginForm from "@modules/reader/components/LoginForm.vue";
import { useAuthStore } from "@core/store/auth";
import { storeToRefs } from "pinia";
import router from "@core/router/index";
const authStore = useAuthStore();
const { isAuthenticated, currentUser, currentUserRole } = storeToRefs(authStore);

const handleLogout = () => {
  router.push("/");
  authStore.logout();
};
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
