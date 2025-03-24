<script setup lang="ts">
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
        <strong>{{ props.title }}</strong>
      </h5>
      <p>{{ props.text }}</p>
      <div class="buttons">
        <button @click="confirmCancel">Да</button>
        <button class="close" @click="open = false">Нет</button>
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

.modal-content {
  background: white;
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
  flex-direction: column;
}

button {
  padding: 8px 32px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
  margin-top: 1rem;
}

button:hover {
  cursor: pointer;
}

button:first-child {
  background-color: #1eb742;
  color: white;
}

button:first-child:hover {
  background-color: #165300;
}

button.close {
  background: rgb(215, 2, 31);
  color: white;
}

button.close:hover {
  background: rgb(102, 5, 5);
}
</style>
