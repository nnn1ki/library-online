<template>
  <div class="card shadow-sm border-0">
    <!-- Картинка -->
    <div v-if="book.cover !== null" class="book-image">
      <img :src="book.cover" />
    </div>
    <i v-else class="book-image bi bi-image"></i>

    <div class="card-body">
      <!-- Заголовок книги и автор -->
      <h5 class="card-title">{{ book.title[0] }}</h5>
      <h5 class="card-year">{{ book.year }} г.</h5>
      <h6 v-if="book.author.length > 0" class="card-subtitle text-muted">
        {{ book.author.join(", ") }}
      </h6>
      <h6 v-else-if="book.collective.length > 0" class="card-subtitle text-muted">
        {{ book.collective.join(", ") }}
      </h6>

      <div class="d-flex justify-content-between align-items-center">
        <!-- Кнопка добавления в корзину -->
        <button
          class="btn btn-info btn-sm"
          type="button"
          @click="addBook(book)"
          :disabled="isAdding || isInBasket"
        >
          <i class="bi bi-cart3"></i> В Корзину
        </button>

        <!-- Кнопка для подробного описания -->
        <button class="btn btn-primary btn-sm" type="button" @click="isModalVisible = true">
          Подробнее
        </button>
      </div>
    </div>
  </div>

  <AboutBookDialog :book="book" v-model="isModalVisible" />
</template>

<script setup lang="ts">
import { computed, ref, toRefs } from "vue";
import type { Book } from "@/api/types";
import { useBasketStore } from "@/stores/basket";
import { storeToRefs } from "pinia";
import AboutBookDialog from "./AboutBookDialog.vue";

const props = defineProps<{
  book: Book;
}>();
const { book } = toRefs(props);

const basketStore = useBasketStore();

const { books: basketBooks } = storeToRefs(basketStore);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.value.id));

const isModalVisible = ref(false);

const isAdding = ref(false);

async function addBook(book: Book) {
  if (isInBasket.value || isAdding.value) return;
  isAdding.value = true;

  await basketStore
    .addBook(book)
    .catch((error) => {
      console.error("Ошибка при добавлении книги:", error);
    })
    .finally(() => {
      if (!isInBasket.value) isAdding.value = false;
    });
}
</script>

<style scoped lang="scss">
.card {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease;
  align-items: center;
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
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: bold;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  -webkit-box-pack: end;
}

.card-year {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 8px;
}

.card-subtitle {
  font-size: 1rem;
  color: #555;
  margin-bottom: 16px;
  overflow: hidden;
  text-overflow: ellipsis;
  overflow-wrap: normal;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-pack: end;
}

.card-text {
  font-size: 1rem;
  color: #888;
}

.book-image {
  font-size: 50px;
  text-align: center;
}

@media (min-width: 768px) {
  .card-title {
    height: 5.9rem;
  }

  .card-subtitle {
    height: 2.5rem;
  }
}

</style>
