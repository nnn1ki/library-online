<template>
  <div v-if="open" class="modal-overlay" @click="open = false">
    <div class="modal-content" @click.stop>
      <div title="Книги на руки выдаются только авторизованным читателям библиотеки">
        <InformationCircleIcon class="info" />
      </div>

      <h5><strong>Авторизуйтесь, чтобы сделать заказ</strong></h5>

      <div class="buttons">
        <StyledButton theme="primary" @click="goToProfile">Перейти к авторизации</StyledButton>
        <StyledButton theme="accent" @click="open = false">Закрыть</StyledButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import { InformationCircleIcon } from "@heroicons/vue/24/outline";
import StyledButton from "@/components/StyledButton.vue";

const router = useRouter();
const open = defineModel<boolean>();

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
  width: 8rem;
  height: 8rem;
  &:hover {
    cursor: help;
  }
}

.buttons {
  display: flex;
  flex-direction: column;
  row-gap: 0.25rem;
}

.modal-content {
  background: var(--color-background-50);
  padding: 50px;
  max-width: fit-content;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
</style>
