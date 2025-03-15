<template>
  <img v-if="book.cover !== null" :src="book.cover" />

  <div v-else class="book-fake-image">
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
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";

const { book } = defineProps<{
  book: Book;
}>();
</script>

<style scoped lang="scss">
@use "@/styles/colors.scss" as *;

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.book-fake-image {
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  flex-direction: column;

  text-align: center;
  align-items: center;
  padding: 0.25rem;

  background-color: var(--color-background-200);
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);

  @include light-theme {
    color: var(--color-text-50);
  }

  @include dark-theme {
    color: var(--color-text-950);
  }
}
</style>
