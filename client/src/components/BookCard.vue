<template>
  <div class="card shadow-sm border-0" v-b-tooltip.hover.focus.bottom :title="getBookHintInfo(book)">
    <!-- Картинка -->
    <div v-if="book.cover !== null" class="book-image">
      <img :src="book.cover" />
    </div>
    <i v-else class="book-image bi bi-image"></i>

    <div class="card-body">
      <!-- Заголовок книги и автор -->
      <h5 class="card-title">{{ book.title[0] }} ({{ book.year }})</h5>
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
        <button class="btn btn-primary btn-sm mt-2" type="button" @click="isModalVisible = true">
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
import BootstrapVue from "bootstrap-vue";
import { TooltipPlugin } from "bootstrap-vue";

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

function getBookHintInfo(book: Book): string{
  let hint: string;

  hint = "";

  if (book.can_be_ordered && book.copies > 0){
    hint = `Книга доступна для заказа \nКниг, доступных для заказа: ${book.copies}`;
  } else if (book.can_be_ordered && book.copies == 0) {
    hint = 'Доступных книг для заказа пока нет, закажите позже или возьмите в читальном зале';
  } else if (!book.can_be_ordered && book.links.length > 0) {
    hint = 'Можете только прочитать книгу онлайн';
  } else if (!book.can_be_ordered && book.links.length == 0) {
    hint = 'Книга доступна только в зале';
  }

  return hint;
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

.book-image {
  font-size: 50px;
  text-align: center;
}
</style>
