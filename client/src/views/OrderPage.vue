<script setup>
import { ref, computed } from "vue";
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification'; //хук для уведомлений


const router = useRouter();
const toast = useToast();

const selectedBooks = ref([
  { title: "Война и мир", author: "Лев Толстой", quantity: 1 },
  { title: "Гарри Поттер и философский камень", author: "Джоан Роулинг", quantity: 1 },
]);

// Поле для ввода email (опционально)
const email = ref("");

// Подсчитываем общее количество книг
const totalBooks = computed(() => {
  return selectedBooks.value.reduce((total, book) => total + book.quantity, 0);
});

// Функция для оформления заказа
const placeOrder = () => {
  toast.success('Заказ успешно отправлен!');
  toast.info('Ожидайте сообщения на почту о готовности');
  router.push({ name: "home" }); //возвращаем в начало пользовательского пути
};
</script>

<template>
  <div class="container">
    <div class="order-summary">
      <h2>Оформление заказа</h2>

      <!-- Список книг -->
      <div class="book-list">
        <h5>Список книг:</h5>
        <ul>
          <li v-for="book in selectedBooks" :key="book.title">
            <strong>{{ book.title }}</strong> — {{ book.author }} (x{{ book.quantity }})
          </li>
        </ul>
      </div>

      <!-- Информация о заказе -->
      <div class="order-info">
        <p><strong>Оформлено книг:</strong> {{ totalBooks }} шт</p>
        <p><strong>Срок готовности:</strong> 1-2 дня</p>
      </div>

      <!-- Поле для ввода email (опционально) -->
      <div class="email-input">
        <label for="email">Email (необязательно)</label>
        <input
          id="email"
          type="email"
          v-model="email"
          placeholder="Введите ваш email для получения уведомлений"
        />
      </div>

      <!-- Кнопка оформления заказа -->
      <div class="order-button">
        <button class="btn btn-success" @click="placeOrder">Оформить заказ</button>
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