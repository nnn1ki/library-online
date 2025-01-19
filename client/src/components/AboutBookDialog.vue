<template>
  <div v-if="visible" class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Подробнее о книге</h5>
          <button type="button" class="btn-close" @click="visible = false"></button>
        </div>
        <div class="modal-body d-flex">
          <!-- Левая часть: картинка -->
          <div class="book-image">
            <img
              :src="book.cover ? 'https://library.istu.edu/opac/' + book.cover : 'https://via.placeholder.com/250x200'"
              alt="Книга" />
          </div>
          <!-- Правая часть: информация -->
          <div class="book-details ms-3">
            <h5>{{ book.description }}</h5>
            <h6 class="text-muted">Год: {{ book.year }}</h6>
            <p>Количество: {{ book.copies }}</p>
            <button class="btn btn-info btn-sm" type="button" @click="basketStore.addBook(book)" :disabled="isInBasket">
              <i class="bi bi-cart3"></i> В Корзину
            </button>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="visible = false">Закрыть</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
import { useBasketStore } from "@/stores/basket";
import { storeToRefs } from "pinia";
import { computed, ref, toRefs, useModel } from "vue";

const props = defineProps<{
  book: Book
}>();
const { book } = toRefs(props);

const basketStore = useBasketStore();

const { books: basketBooks } = storeToRefs(basketStore);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.value.id))

const visible = defineModel<boolean>();
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
</style>