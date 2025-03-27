<template>
  <div class="container">
    <BorrowedBooks v-if="orderStore.borrowedBooks.length > 0" />

    <div class="order-summary">
      <h2 class="summary-title"><BookOpenIcon class="title-icon" /> Оформление заказа</h2>

      <div class="book-list">
        <h5 class="section-subtitle">Выбранные книги</h5>
        <TransitionGroup name="list" tag="div">
          <div v-for="(book, i) in orderStore.selectedBooks" :key="book.id" class="book-item card">
            <div class="book-activities">
              <ShortBookCard :book="book" :num="i" />
              <i class="remove-icon" @click="removeBook(book.id)"> ❌ </i>
            </div>
          </div>
        </TransitionGroup>
      </div>

      <div class="book-list" v-if="booksToreturn.length !== 0">
        <h5 class="section-subtitle">Книги которые вы принесете</h5>
        <TransitionGroup name="list" tag="div">
          <div v-for="(book, i) in booksToreturn" :key="book.id" class="book-item card">
            <div class="book-activities">
              <ShortBookCard :book="book.book" :num="i" />
            </div>
          </div>
        </TransitionGroup>
      </div>

      <div class="order-info card">
        <div class="info-item">
          <span class="info-label">Книг в заказе:</span>
          <span class="info-value">{{ orderStore.selectedBooks.length }} шт</span>
        </div>
        <div class="info-item">
          <span class="info-label">Срок готовности:</span>
          <span class="info-value">1-2 дня ⏳</span>
        </div>
      </div>

      <div class="email-input card">
        <label for="email" class="input-label">📧 Email (для уведомлений)</label>
        <input
          id="email"
          type="email"
          v-model="email"
          placeholder="example@mail.com"
          class="styled-input"
        />
        <div class="notifcation">
          <label for="email" class="input-label">📨 Уведомления в кампусе</label>
          <input type="checkbox" class="notifcation-checkbox" />
        </div>
      </div>

      <StyledButton
        class="order-button"
        @click="placeOrder"
        :disabled="loading"
        :class="{ processing: loading }"
      >
        <span v-if="!loading">Оформить заказ</span>
        <span v-else>
          <span class="button-spinner"></span>
          Обработка...
        </span>
      </StyledButton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from "vue";
import { BookOpenIcon, CheckCircleIcon } from "@heroicons/vue/24/outline";

import BorrowedBooks from "@/layouts/BorrowedBooks.vue";
import ShortBookCard from "@/components/ShortBookCard.vue";
import StyledButton from "@/components/StyledButton.vue";
import { useOrderStore } from "@/stores/orderStore";
import { borrowedList } from "@/api/order";

const orderStore = useOrderStore();

const email = ref("");

const booksToreturn = computed(() => {
  return orderStore.borrowedBooks.filter((book) =>
    orderStore.selectedBorrowedBooks.includes(book.id)
  );
});

const loading = ref(false);
const placeOrder = async () => {
  loading.value = true;
  await orderStore.handleCreateOrder();
  loading.value = false;
};

onBeforeMount(async () => {
  orderStore.borrowedBooks = await borrowedList();
});

const removeBook = (id: string) => {
  orderStore.selectedBooks = orderStore.selectedBooks.filter((book) => book.id !== id);
};
</script>

<style scoped lang="scss">
.notifcation {
  display: flex;
  justify-content: space-between;
  margin-top: 1rem;
}

.notifcation-checkbox {
  width: 20px;
  height: 20px;
  margin-top: 0.3rem;
  accent-color: var(--color-primary-500);
}

.book-activities {
  display: flex;
  justify-content: space-between;
}

.remove-icon {
  padding-top: 1rem;
  color: var(--color-text-400);
}

.remove-icon:hover {
  cursor: pointer;
}

.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.title-icon {
  width: 2rem;
  height: 2rem;
}

.summary-title {
  color: var(--color-text-600);
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 1rem;
}

.card {
  background: var(--color-background-100);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.book-item {
  margin-bottom: 1rem;
  border-left: 4px solid var(--color-primary-500);
}

.section-subtitle {
  color: var(--color-text-400);
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  font-weight: 500;
}

.order-info {
  display: grid;
  gap: 1rem;
  background: var(--color-background-200);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  color: var(--color-text-400);
  font-weight: 500;
}

.info-value {
  color: var(--color-text-600);
  font-weight: 600;
}

.input-label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-text-400);
  font-size: 0.9em;
}

.styled-input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid var(--color-background-300);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
  background: var(--color-background-100);
  color: var(--color-text-600);
}

.styled-input:focus {
  border-color: var(--color-primary-500);
  outline: none;
  box-shadow: 0 0 0 3px var(--color-primary-100);
}

.order-button {
  width: 100%;
  padding: 1rem;
  color: var(--color-text-800);
  cursor: pointer;
}

.button-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  vertical-align: middle;
  box-sizing: border-box;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.7s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-active {
  position: absolute;
  transition:
    opacity 0.3s ease,
    transform 0.5s ease;
}

.list-enter-active {
  transition-delay: 0.5s;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
