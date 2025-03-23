<template>
  <div class="card shadow-sm border-0 d-flex flex-row">
    <div class="card-body col-10">
      <!-- Заголовок книги и автор -->
      <h5 class="card-title">{{ book.title[0] }} ({{ book.year }})</h5>
      <h6 v-if="book.author.length > 0" class="card-subtitle text-muted">
        {{ book.author.join(", ") }}
      </h6>
      <h6 v-else-if="book.collective.length > 0" class="card-subtitle text-muted">
        {{ book.collective.join(", ") }}
      </h6>

      <div>
        <!-- Кнопка добавления в корзину -->
        <button
          class="btn btn-info btn-sm me-2"
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
    <!-- Картинка -->
    <div class="col">
      <div v-if="book.cover !== null" class="book-image">
        <img :src="book.cover" />
      </div>
      <div v-else class="book-fake-image">
        <!-- <i class="book-image bi bi-image"></i> -->
        <div class="fake-image-content">
          <h6>{{ book.title[0] }}</h6>
          <div v-if="book.author.length > 0">
            <div v-if="book.author.length <= 2">
              <h6>{{ book.author.join(", ") }}</h6>
            </div>
            <div v-else>
              <h6>{{ book.author.slice(0, 2).join(", ") }} и другие</h6>
            </div>
          </div>
          <h6 v-else-if="book.collective.length > 0">{{ book.collective.join(", ") }}</h6>
        </div>
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
}

.card:hover {
  transform: scale(1.05);
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

.book-image {
  width: 200px;
  height: auto;
  text-align: center;
  overflow: hidden;
}

.book-image img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.book-image i {
  font-size: 50px;
  color: #888;
}

.book-fake-image {
  background: #c0c0c0;
  width: 200px;
  height: 290px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.fake-image-content {
  padding: 5px;
  color: #fff;
}
</style>
