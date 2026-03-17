<script setup lang="ts">
defineProps<{
  currentLogoLabel: string;
}>();
</script>

<template>
  <div class="logo-view">
    <span class="logo-label">Текущий статус</span>
    <strong>{{ currentLogoLabel }}</strong>
  </div>
</template>

<style scoped lang="scss">
.logo-view {
  display: grid;
  gap: 0.35rem;
  padding: 1rem;
  border-radius: 1rem;
  background: linear-gradient(180deg, var(--color-background-50), var(--color-background-100));
  border: 1px solid var(--color-text-200);
}

.logo-label {
  color: var(--color-text-600);
  font-size: var(--text-xs);
}
</style>
