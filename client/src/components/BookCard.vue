<template>
  <div class="card" :class="{ announcement: announcement }" :title="bookHint">
    <div class="book-image" :class="{ announcement: announcement }">
      <BookImage
        :class="{ 'rounded-left': !announcement, 'rounded-top': announcement }"
        :book="book"
      />
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
        <StyledButton
          v-if="showCart"
          theme="primary"
          @click="addBook"
          :disabled="isAdding || isInBasket"
        >
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

        <StyledButton v-if="basketCart" theme="accent" @click="basketStore.removeBook(book)">
          Удалить <TrashIcon class="button-icon" />
        </StyledButton>
      </div>
    </div>
  </div>

  <AboutBookDialog :book="book" v-model="isModalVisible" />
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import type { Book } from "@/api/types";
import { ShoppingCartIcon, Bars3Icon, BookOpenIcon, TrashIcon } from "@heroicons/vue/24/outline";
import { useBasketStore } from "@/stores/basket";
import { storeToRefs } from "pinia";
import AboutBookDialog from "@/components/AboutBookDialog.vue";
import StyledButton from "@/components/StyledButton.vue";
import BookImage from "@/components/BookImage.vue";

const {
  book,
  announcement = false,
  showCart = true,
  basketCart = false,
} = defineProps<{
  book: Book;
  announcement?: boolean;
  showCart?: boolean;
  basketCart?: boolean;
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

const bookHint = computed(() => {
  if (book.can_be_ordered) {
    if (book.copies > 0) {
      return `Книга доступна для заказа \nКниг, доступных для заказа: ${book.copies}`;
    } else {
      return "Доступных книг для заказа пока нет, закажите позже или возьмите в читальном зале";
    }
  } else {
    if (book.links.length > 0) {
      return "Можете только прочитать книгу онлайн";
    } else {
      return "Книга доступна только в зале";
    }
  }
});
</script>

<style scoped lang="scss">
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

  &.announcement {
    flex-direction: column;
  }
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
  flex-basis: 190px;
  height: 290px;

  &.announcement {
    flex-basis: 490px;
    height: 490px;
  }

  .rounded-left {
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
  }

  .rounded-top {
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
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
