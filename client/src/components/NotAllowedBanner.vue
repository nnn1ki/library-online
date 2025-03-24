<template>
  <div v-if="open" class="modal-overlay" @click="open = false">
    <div class="modal-content" @click.stop>
      <div class="info">
        <img src="@/assets/circle-info.svg" style="width: 100px" alt="" />
      </div>
      <h5><strong>Авторизуйтесь, чтобы сделать заказ</strong></h5>
      <div class="buttons">
        <button @click="goToProfile">Перейти к авторизации 🔑</button>
        <button class="close" @click="open = false">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();
const open = defineModel<boolean>({ required: true });

// Переход на страницу профиля
const goToProfile = () => {
  open.value = false;
  router.push("/profile");
};
</script>

<style scoped lang="scss">
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
  padding: 8px 16px;
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
