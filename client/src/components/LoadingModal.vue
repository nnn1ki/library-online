<template>
  <div class="modal-content">
    <LoadingSpinner />
    <p>Загрузка данных...</p>
  </div>
</template>

<script setup lang="ts">
import LoadingSpinner from "@/components/LoadingSpinner.vue";
</script>

<style scoped lang="scss">
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: var(--color-background-100);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
