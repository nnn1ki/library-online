<template>
  <div class="card">
    <div v-if="book.cover !== null" class="book-image">
      <img :src="book.cover" />
    </div>

    <div v-else class="book-fake-image">
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

    <div class="card-body">
      <h5 class="card-title">{{ book.title[0] }} ({{ book.year }})</h5>
      <h6 v-if="book.author.length > 0" class="card-subtitle">
        {{ book.author.join(", ") }}
      </h6>
      <h6 v-else-if="book.collective.length > 0" class="card-subtitle">
        {{ book.collective.join(", ") }}
      </h6>
      <h6 class="card-subtitle">
        {{ book.brief }}
      </h6>

      <div class="buttons">
        <StyledButton theme="primary" @click="addBook" :disabled="isAdding || isInBasket">
          В Корзину <ShoppingCartIcon class="button-icon" />
        </StyledButton>

        <StyledButton theme="secondary" type="button" @click="isModalVisible = true">
          Подробнее <Bars3Icon class="button-icon" />
        </StyledButton>

        <a v-if="bookLink !== undefined" :href="bookLink">
          <StyledButton theme="accent">
            Читать онлайн <BookOpenIcon class="button-icon" />
          </StyledButton>
        </a>
      </div>
    </div>
  </div>

  <AboutBookDialog :book="book" v-model="isModalVisible" />
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { Book } from "@/api/types";
import { ShoppingCartIcon, Bars3Icon, BookOpenIcon } from "@heroicons/vue/24/outline";
import { useBasketStore } from "@/stores/basket";
import { storeToRefs } from "pinia";
import AboutBookDialog from "@/components/AboutBookDialog.vue";
import StyledButton from "@/components/StyledButton.vue";

const { book } = defineProps<{
  book: Book;
}>();

const basketStore = useBasketStore();

const { books: basketBooks } = storeToRefs(basketStore);
const isInBasket = computed(() => basketBooks.value.some((item) => item.id == book.id));

const isModalVisible = ref(false);
const isAdding = ref(false);

async function addBook() {
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

const bookLink = computed(
  () => book.links.filter((link) => link.description === "Электронная библиотека ИРНИТУ")[0]?.url
);
</script>

<style scoped lang="scss">
@use "@/styles/colors.scss" as *;

.card {
  width: 100%;

  background-color: var(--color-background-50);
  border-style: solid;
  border-radius: 0.5rem;
  border-width: 1px;
  border-color: var(--color-text-300);
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);

  display: flex;
  flex-direction: row;
}

.card-body {
  padding: 1rem;
}

.card-title {
  font-size: var(--text-lg);
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.card-subtitle {
  color: var(--color-text-700);
  margin-bottom: 1rem;
}

.book-image {
  flex-shrink: 0;
  flex-grow: 0;
  flex-basis: 200px;
  height: auto;
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
  }
}

.book-fake-image {
  background-color: var(--color-background-200);
  flex-shrink: 0;
  flex-grow: 0;
  flex-basis: 200px;
  height: 290px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}

.fake-image-content {
  padding: 0.25rem;
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);

  @include light-theme {
    color: var(--color-text-50);
  }

  @include dark-theme {
    color: var(--color-text-950);
  }
}

.buttons {
  display: flex;
  flex-direction: row;
  column-gap: 1rem;
}

.button-icon {
  width: 1.2em;
  height: 1.2em;
  margin-left: 0.5em;
}
</style>
