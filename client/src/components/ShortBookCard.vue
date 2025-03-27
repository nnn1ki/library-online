<template>
  <div class="book-details grid">
    <h4 class="book-title grid-tr">
      <div class="book-icon grid-td">
        📖
      </div>
      <div class="book-title-conten grid-td">
        {{ book.title[0] }}
      </div>
      <span class="book-year">({{ book.year }})</span>
    </h4>
    <div class="book-authors grid-tr">
      <template v-if="book.author.length > 0">
        <span class="author-icon grid-td">✍️</span>
        {{ book.author.join(", ") }}
      </template>
      <template v-else-if="book.collective.length > 0">
        <span class="collective-icon grid-td">👥</span>
        {{ book.collective.join(", ") }}
      </template>
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
.book-content {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.book-index {
  min-width: 32px;
  height: 32px;
  background-color: none;
  color: var(--color-text-700);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.book-details {
  flex-grow: 1;
}

.grid {
  display: table;
  border-collapse: separate;
}

.grid-tr {
  display: table-row;
}

.grid-td {
  display: table-cell;
  vertical-align: top;
}

.book-title {
  margin: 0;
  font-size: 1.1rem;
  color: var(--color-text-700);
  display: flex;
  align-items: baseline;
}

.book-year {
  font-size: 0.9rem;
  color: var(--color-text-700);
}

.book-authors {
  margin-top: 0.5rem;
  font-size: 0.95rem;
  color: var(--color-text-700);
  display: flex;
  align-items: center;

}

.author-icon,
.collective-icon {
  font-size: 0.9em;
}
</style>
