<template>
  <div class="container">
    <BorrowedBooks v-if="orderStore.borrowedBooks.length > 0" />

    <div class="order-summary">
      <h2 class="summary-title">📚 Оформление заказа</h2>

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

      <!-- Информация о заказе -->
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

      <!-- Поле для email -->
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

      <!-- Кнопка оформления -->
      <button
        class="order-button"
        @click="placeOrder"
        :disabled="loading"
        :class="{ processing: loading }"
      >
        <span v-if="!loading">✅ Оформить заказ</span>
        <span v-else>
          <span class="button-spinner"></span>
          Обработка...
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, computed } from "vue";
import BorrowedBooks from "@/layouts/BorrowedBooks.vue";
import ShortBookCard from "@/components/ShortBookCard.vue";
import { useOrderStore } from "@/stores/orderStore";
import { borrowedList } from "@/api/order";

const orderStore = useOrderStore();

// Поле для ввода email (опционально)
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
  flex-direction: row;
  justify-content: space-between;
  margin-top: 1rem;
}

.notifcation-checkbox {
  width: 20px;
  height: 20px;
  margin-top: 0.3rem;
  accent-color: #42b983;
}

.book-activities {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.remove-icon {
  padding-top: 1rem;
}

.remove-icon:hover {
  cursor: pointer;
}

.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.summary-title {
  color: #2c3e50;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 600;
}

.card {
  background: white;
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
  border-left: 4px solid #42b983;
}

.section-subtitle {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  font-weight: 500;
}

.order-info {
  display: grid;
  gap: 1rem;
  background: linear-gradient(145deg, #f6f6f6, #ffffff);
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  color: #7f8c8d;
  font-weight: 500;
}

.info-value {
  color: #2c3e50;
  font-weight: 600;
}

.input-label {
  display: block;
  margin-bottom: 0.5rem;
  color: #7f8c8d;
  font-size: 0.9em;
}

.styled-input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.styled-input:focus {
  border-color: #42b983;
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.1);
}

.order-button {
  width: 100%;
  padding: 1rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.order-button:hover:not(:disabled) {
  background: #3aa076;
  box-shadow: 0 4px 6px rgba(66, 185, 131, 0.2);
}

.order-button:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  opacity: 0.8;
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
  /* Важно для правильного размера */
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
