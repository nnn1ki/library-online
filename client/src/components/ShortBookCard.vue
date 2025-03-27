<template>
  <div class="book-details">
    <div class="book-row">
      <div class="icon-cell">📖</div>
      <div class="content-cell">
        <span class="book-title book"
          >{{ book.title[0] }} <span class="year"> ({{ book.year }}) </span></span
        >
      </div>
    </div>
    <div v-if="book.author.length > 0 || book.collective.length > 0" class="book-row">
      <div class="icon-cell">
        <span v-if="book.author.length > 0">✍️</span>
        <span v-else-if="book.collective.length > 0">👥</span>
      </div>
      <div class="content-cell author">
        {{
          book.author.length > 0
            ? book.author.join(", ")
            : book.collective.length > 0
              ? book.collective.join(", ")
              : "Автор не указан"
        }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
const { book } = defineProps<{
  book: Book;
}>();
</script>

<style scoped lang="scss">
.book-details {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.book-row {
  display: flex;
  line-height: 1.3;
  justify-content: baseline;
}

.icon-cell {
  min-width: 1.5rem;
  text-align: center;
  padding-right: 0.3rem;
}

.content-cell {
  flex: 1;
  display: flex;
  align-items: flex-end;
}

.book-title {
  font-size: 1.1rem;
}

.book {
  font-size: 1.1rem;
  color: var(--color-text-700);
}

.author {
  font-size: 0.95rem;
  color: var(--color-text-600);
}

.year {
  font-size: 0.9rem;
  color: var(--color-text-600);
}
</style>
