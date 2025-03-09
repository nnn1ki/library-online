<template>
  <div v-if="visible" class="modal" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <h3>Подробнее о книге</h3>

        <div class="modal-body">
          <div v-if="book.cover !== null">
            <img :src="book.cover" />
          </div>
          <BookOpenIcon v-else class="book-icon" />

          <div>
            <h5 v-for="[index, title] in book.title.entries()" v-bind:key="index" class="title">
              {{ title }}
            </h5>
            <p class="text-muted">Год: {{ book.year }}</p>

            <p v-if="book.author.length > 0" class="text-muted">
              Авторы: {{ book.author.join(", ") }}
            </p>
            <p v-else-if="book.collective.length > 0" class="text-muted">
              Коллективы: {{ book.collective.join(", ") }}
            </p>

            <p>Количество: {{ book.copies }}</p>

            <StyledButton @click="basketStore.addBook(book)" :disabled="isInBasket">
              <ShoppingCartIcon class="cart-icon" />В корзину
            </StyledButton>
            <h6 class="text-muted">{{ book.keyword.join(", ") }}</h6>
          </div>
        </div>

        <div class="text-end">
          <StyledButton theme="accent" @click="visible = false">Закрыть</StyledButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
import { useBasketStore } from "@/stores/basket";
import { storeToRefs } from "pinia";
import { computed } from "vue";
import { BookOpenIcon, ShoppingCartIcon } from "@heroicons/vue/24/outline";
import StyledButton from "@/components/StyledButton.vue";

const { book } = defineProps<{
  book: Book;
}>();

const basketStore = useBasketStore();

const { books: basketBooks } = storeToRefs(basketStore);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.id));

const visible = defineModel<boolean>();
</script>

<style scoped lang="scss">
.modal {
  display: block;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1050;
}

.modal-dialog {
  position: relative;
  margin: 10% auto;
  max-width: 1000px;
}

.modal-content {
  background-color: var(--color-background-50);
  border-radius: 1rem;
  padding: 1rem;
}

.modal-body {
  display: flex;
  flex-direction: row;
  column-gap: 1rem;
}

.title {
  margin-top: 0rem;
  margin-bottom: 0rem;
}

.text-muted {
  color: var(--color-text-400);
}

.cart-icon {
  width: 1.2em;
  height: 1.2em;
  margin-right: 0.5em;
}

.book-icon {
  width: 32rem;
  height: 32rem;
}
</style>
