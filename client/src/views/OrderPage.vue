<script setup>
import { ref, computed, onBeforeMount } from "vue";
import { useOrderStore } from "@/stores/orderStore";

import { borrowedList } from '@/api/order'
import borrowedBooks  from "@/components/BorrowedBooks.vue"
import { storeToRefs } from "pinia";

const orderStore = useOrderStore();

// Поле для ввода email (опционально)
const email = ref("");

const totalBooks = computed(() => {
  return selectedBooks.value.reduce((total, book) => total + book.quantity, 0);
});

const { selectedBooks } = storeToRefs(orderStore);
const loading = ref(false);
const placeOrder = async () => {
  loading.value = true;
  console.log(orderStore.selectedBooks);
  await orderStore.handleCreateOrder();
  loading.value = false;
};

onBeforeMount(async () => {
  orderStore.borrowedBooks = await borrowedList();
});

</script>

<template>
  <div class="container">
    <borrowedBooks v-if="orderStore.borrowedBooks.length > 0"/>
    <div class="order-summary">
      <h2>Оформление заказа</h2>
      <!-- Список книг -->
      <div class="book-list">
        <h5>Список книг:</h5>
        <ul>
          <li v-for="(book, i) in orderStore.selectedBooks" :key="book.title">
            <strong> {{ i + 1 }}</strong> - {{ book.description }}
          </li>
        </ul>
      </div>

      <!-- Информация о заказе -->
      <div class="order-info">
        <p><strong>Оформлено книг:</strong> {{ orderStore.selectedBooks.length }} шт</p>
        <p><strong>Срок готовности:</strong> 1-2 дня</p>
      </div>

      <!-- Поле для ввода email (опционально) -->
      <div class="email-input">
        <label for="email">Email (необязательно)</label>
        <input id="email" type="email" v-model="email" placeholder="Введите ваш email для получения уведомлений" />
      </div>

      <!-- Кнопка оформления заказа -->
      <div class="order-button">
        <button class="btn btn-success" @click="placeOrder" :disabled="loading">Оформить заказ</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.order-summary {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.order-summary h2 {
  margin-bottom: 20px;
  font-size: 1.8rem;
}

.order-info p {
  margin: 10px 0;
  font-size: 1.1rem;
}

.email-input {
  margin: 20px 0;
}

.email-input input {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.book-list ul {
  list-style: none;
  padding-left: 0;
}

.book-list li {
  margin-bottom: 5px;
}

.order-button {
  margin-top: 20px;
}

.order-button button {
  width: 100%;
  padding: 12px;
  font-size: 1.1rem;
  border-radius: 8px;
}
</style>