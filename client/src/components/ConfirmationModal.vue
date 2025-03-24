<script setup lang="ts">
import StyledButton from '@/components/StyledButton.vue';
const props = defineProps<{
  title: string;
  text: string;
}>();

const emit = defineEmits<{
  (e: "confirm"): void;
}>();

const open = defineModel<boolean>({ required: true });

const confirmCancel = () => {
  emit("confirm");
  open.value = false;
};
</script>

<template>
  <div v-if="open" class="modal-overlay" @click="open = false">
    <div class="modal-content" @click.stop>
      <h5>
        <strong class="title">{{ props.title }}</strong>
      </h5>
      <p class="content">{{ props.text }}</p>
      <div class="buttons">
        <StyledButton theme="secondary" @click="confirmCancel">Да</StyledButton>
        <StyledButton theme="accent" @click="open = false">Нет</StyledButton>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  display: flex;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.info {
  margin-bottom: 2rem;
}

.info img:hover {
  cursor: help;
}

.title {
  color: var(--color-text-800);
}
.content {
  color: var(--color-text-700);
}
.modal-content {
  background: var(--color-background-200);
  padding: 50px;
  max-width: fit-content;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.buttons {
  margin-top: 15px;
  display: flex;
  display: flex;
  flex-direction: row;
  gap: 1rem;
}
</style>
