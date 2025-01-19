<template>
  <div class="card shadow-sm border-0">
    <!-- Картинка -->
    <img :src="book.cover ? 'https://library.istu.edu/opac/' + book.cover : 'https://via.placeholder.com/250x200'"
      class="card-img-top" :alt="book.description" />

    <div class="card-body">
      <!-- Заголовок книги и автор -->
      <h5 class="card-title">{{ book.description }}</h5>
      <h6 class="card-subtitle text-muted">{{ book.year }}</h6>

      <div class="d-flex justify-content-between align-items-center">
        <!-- Кнопка добавления в корзину -->
        <button class="btn btn-info btn-sm" type="button" @click="basketStore.addBook(book)" :disabled="isInBasket">
          <i class="bi bi-cart3"></i> В Корзину
        </button>

        <!-- Кнопка для подробного описания -->
        <button class="btn btn-primary btn-sm mt-2" type="button" @click="isModalVisible = true">Подробнее</button>
      </div>
    </div>
  </div>

  <AboutBookDialog :book="book" v-model="isModalVisible" />
</template>

<script setup lang="ts">
import { computed, onMounted, ref, toRefs } from "vue";
import type { Book } from "@/api/types";
import { useBasketStore } from "@/stores/basket";
import { storeToRefs } from "pinia";
import AboutBookDialog from "./AboutBookDialog.vue";

const props = defineProps<{
  book: Book
}>();
const { book } = toRefs(props);

const basketStore = useBasketStore();

const { books: basketBooks } = storeToRefs(basketStore);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.value.id));

const isModalVisible = ref(false);
</script>

<style scoped>
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
