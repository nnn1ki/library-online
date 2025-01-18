<template>
  <div class="card shadow-sm border-0">
    <!-- Картинка -->
    <img :src="book.cover || 'https://via.placeholder.com/250x200'" class="card-img-top" :alt="book.description" />

    <div class="card-body">
      <!-- Заголовок книги и автор -->
      <h5 class="card-title">{{ book.description }}</h5>
      <h6 class="card-subtitle text-muted">{{ book.year }}</h6>

      <div class="d-flex justify-content-between align-items-center">
        <!-- Кнопка добавления в корзину -->
        <button class="btn btn-info btn-sm" type="button" @click="handleAddToBasket" :disabled="isInBasket">
          <i class="bi bi-cart3"></i> В Корзину
        </button>

        <!-- Кнопка для подробного описания -->
        <button class="btn btn-primary btn-sm mt-2" type="button" @click="isModalVisible = true">Подробнее</button>
      </div>
    </div>
  </div>

  <!-- модальное окно книги -->
  <div v-if="isModalVisible" class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Подробнее о книге</h5>
          <button type="button" class="btn-close" @click="isModalVisible = false"></button>
        </div>
        <div class="modal-body d-flex">
          <!-- Левая часть: картинка -->
          <div class="book-image">
            <img :src="book.cover || 'https://via.placeholder.com/250x200'" alt="Книга" />
          </div>
          <!-- Правая часть: информация -->
          <div class="book-details ms-3">
            <h5>{{ book.description }}</h5>
            <h6 class="text-muted">Год: {{ book.year }}</h6>
            <p>Количество: {{ book.copies }}</p>
            <button class="btn btn-info btn-sm" type="button" @click="handleAddToBasket" :disabled="isInBasket">
              <i class="bi bi-cart3"></i> В Корзину
            </button>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="isModalVisible = false">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToast } from 'vue-toastification'; //хук для уведомлений
import { computed, ref, toRefs } from 'vue';
import type { Book } from '@/api/types';
import { useBasketStore } from '@/stores/basket';

const toast = useToast();
const basketStore = useBasketStore();

const basketBooks = ref<Book[]>([]);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.value.id))

const props = defineProps<{
  book: Book
}>();
const { book } = toRefs(props);

const isModalVisible = ref(false);

function handleAddToBasket() {
  toast.success(book.value.description + ' добавлен(a) в корзину');
  basketStore.addBook(book.value)
}
</script>

<style scoped>
.modal {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  /* Полупрозрачный фон */
  z-index: 1050;
  /* Убедитесь, что модальное окно поверх всего */
}

.modal-dialog {
  position: relative;
  margin: 10% auto;
  max-width: 1000px;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
}

.modal-header .btn-close {
  background: none;
  border: none;
}

.modal-footer {
  text-align: right;
}


.card {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-body {
  padding: 16px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.card-subtitle {
  font-size: 1rem;
  color: #555;
  margin-bottom: 16px;
}

.card-text {
  font-size: 1rem;
  color: #888;
}
</style>
