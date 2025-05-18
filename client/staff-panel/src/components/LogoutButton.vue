<template>
  <button class="logout-button" @click="handleLogout">
    <ArrowRightEndOnRectangleIcon class="icon" />
  </button>
</template>

<script setup>
import router from "@/router";
import { useAuthStore } from "@/stores/auth";
import { ArrowRightEndOnRectangleIcon } from "@heroicons/vue/24/solid";
const authStore = useAuthStore();

const handleLogout = () => {
  authStore.logout();
  router.push("/auth");
};
</script>

<style scoped>
.logout-button {
  display: flex;
  align-items: center;
  color: var(--color-background-500);
  border: none;
  border-radius: 2em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: var(--color-background-600);
}

.icon {
  width: 30px;
  font-size: 18px;
}
</style>
