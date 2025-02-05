<template>
  <div class="borrow-summary">
    <div class="summary-header">
      <span class="alert-icon">⚠️</span>
      <h3 class="summary-title">Необходимо вернуть книги <br />Отметьте те, которые принесете</h3>
    </div>

    <div class="book-list">
      <div v-for="item in orderStore.borrowedBooks" :key="item.book.id" class="book-item card">
        <label class="book-content">
          <input
            type="checkbox"
            :value="item.id"
            v-model="orderStore.selectedBorrowedBooks"
            class="book-checkbox"
          />
          <div class="book-details">
            <div class="book-header">
              <h4 class="book-title">
                📖 {{ item.book.title[0] }}
                <span class="book-year">({{ item.book.year }})</span>
              </h4>
            </div>
            <div class="book-authors">
              <template v-if="item.book.author.length > 0">
                <span class="author-icon">✍️</span>
                {{ item.book.author.join(", ") }}
              </template>
              <template v-else-if="item.book.collective.length > 0">
                <span class="collective-icon">👥</span>
                {{ item.book.collective.join(", ") }}
              </template>
            </div>
          </div>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useOrderStore } from "@/stores/orderStore";

const orderStore = useOrderStore();
</script>

<style scoped lang="scss">
.borrow-summary {
  background: #fff8f8;
  border-radius: 12px;
  padding: 1.5rem;
  margin: 2rem 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #ffe5e5;
}

.alert-icon {
  font-size: 1.8rem;
}

.summary-title {
  margin: 0;
  color: #cc0000;
  font-size: 1.4rem;
}

.book-list {
  display: grid;
  gap: 1rem;
}

.book-item {
  background: white;
  border: 1px solid #ffebeb;
  border-radius: 8px;
  padding: 1rem;
  transition: all 0.2s ease;
}

.book-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.book-item.not-returned {
  border-left: 4px solid #ff4444;
}

.book-content {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  cursor: pointer;
}

.book-checkbox {
  width: 20px;
  height: 20px;
  margin-top: 0.3rem;
  accent-color: #42b983;
}

.book-details {
  flex-grow: 1;
}

.book-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 1rem;
}

.book-title {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.book-year {
  font-size: 0.9rem;
  color: #7f8c8d;
}

.return-status {
  font-size: 0.8rem;
  color: #ff4444;
  background: #ffecec;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
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
  opacity: 0.8;
}
</style>
