<template>
  <div class="book-content">
    <span class="book-index">📖 {{ num + 1 }}</span>
    <div class="book-details">
      <h3 class="book-title">
        {{ props.book.title[0] }}
        <span class="book-year">{{ props.book.year }}</span>
      </h3>

      <div class="book-authors">
        <template v-if="props.book.author.length > 0">
          <span class="author-icon">✍️</span>
          {{ props.book.author.join(", ") }}
        </template>
        <template v-else-if="props.book.collective.length > 0">
          <span class="collective-icon">👥</span>
          {{ props.book.collective.join(", ") }}
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from "@/api/types";
const props = defineProps<{
  book: Book;
  num: number;
}>();
</script>

<style scoped>
.book-content {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.book-index {
  min-width: 32px;
  height: 32px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
}

.book-details {
  flex-grow: 1;
}

.book-title {
  margin: 0;
  font-size: 1.1rem;
  color: #34495e;
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.book-year {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.book-authors {
  margin-top: 0.5rem;
  font-size: 0.95rem;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author-icon,
.collective-icon {
  font-size: 0.9em;
}
</style>
